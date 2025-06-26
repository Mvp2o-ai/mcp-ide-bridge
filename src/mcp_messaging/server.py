"""MCP HTTP Streamable messaging server for client-to-client communication."""

import argparse
import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import httpx
import uvicorn
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from starlette.responses import JSONResponse

from .models import Message, format_relative_time
from .queue_backends import QueueBackend, InMemoryQueueBackend

# Load environment variables
load_dotenv()

# Configure logging with a more detailed format
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s\n%(message)s\n"  # Added newline for better readability
)
logger = logging.getLogger(__name__)

# Default configuration values
DEFAULT_CONFIG = {
    "max_tokens": 4096,
    "max_iterations": 10,
    "timeouts": {
        "send_message_and_wait": 180.0,  # 3 minutes
        "get_messages": 60.0,  # 1 minute
        "message_expiration": 300.0  # 5 minutes
    }
}

def load_client_config(client_id: str) -> Dict:
    """Load client configuration from mcp_recipients.json."""
    try:
        # Try to find mcp_recipients.json in current directory or parent directories
        current_dir = Path.cwd()
        while current_dir.parent != current_dir:
            config_path = current_dir / "mcp_recipients.json"
            if config_path.exists():
                with open(config_path) as f:
                    config = json.load(f)
                    if config.get("my_id") == client_id:
                        message_config = config.get("message_config", {})
                        return {
                            "max_tokens": message_config.get("max_tokens", DEFAULT_CONFIG["max_tokens"]),
                            "max_iterations": message_config.get("max_iterations", DEFAULT_CONFIG["max_iterations"]),
                            "timeouts": {
                                **DEFAULT_CONFIG["timeouts"],
                                **message_config.get("timeouts", {})
                            }
                        }
            current_dir = current_dir.parent
    except Exception as e:
        logger.warning(f"Error loading config for {client_id}: {e}")
    
    return DEFAULT_CONFIG


def load_callbacks_from_config() -> Dict[str, List[str]]:
    """Load callback URLs from all *_recipients.json files."""
    callbacks = {"connect": [], "disconnect": []}
    
    try:
        # Find all *_recipients.json files in current directory
        current_dir = Path.cwd()
        for config_file in current_dir.glob("*_recipients.json"):
            try:
                with open(config_file) as f:
                    config = json.load(f)
                    file_callbacks = config.get("callbacks", {})
                    
                    # Add connect callbacks
                    if "connect" in file_callbacks:
                        if isinstance(file_callbacks["connect"], list):
                            callbacks["connect"].extend(file_callbacks["connect"])
                        else:
                            callbacks["connect"].append(file_callbacks["connect"])
                    
                    # Add disconnect callbacks
                    if "disconnect" in file_callbacks:
                        if isinstance(file_callbacks["disconnect"], list):
                            callbacks["disconnect"].extend(file_callbacks["disconnect"])
                        else:
                            callbacks["disconnect"].append(file_callbacks["disconnect"])
                            
                    logger.debug(f"Loaded callbacks from {config_file.name}: {file_callbacks}")
                    
            except Exception as e:
                logger.warning(f"Error loading callbacks from {config_file}: {e}")
    
    except Exception as e:
        logger.warning(f"Error scanning for callback configs: {e}")
    
    # Remove duplicates while preserving order
    callbacks["connect"] = list(dict.fromkeys(callbacks["connect"]))
    callbacks["disconnect"] = list(dict.fromkeys(callbacks["disconnect"]))
    
    logger.info(f"Loaded callbacks - Connect: {len(callbacks['connect'])}, Disconnect: {len(callbacks['disconnect'])}")
    return callbacks


async def fire_callbacks(event_type: str, payload: Dict) -> None:
    """Fire HTTP callbacks for the given event type."""
    callbacks = load_callbacks_from_config()
    urls = callbacks.get(event_type, [])
    
    if not urls:
        logger.debug(f"No callbacks configured for event: {event_type}")
        return
    
    logger.info(f"Firing {len(urls)} callback(s) for event: {event_type}")
    
    # Fire callbacks concurrently with retries
    tasks = []
    for url in urls:
        task = asyncio.create_task(fire_single_callback(url, payload, event_type))
        tasks.append(task)
    
    # Wait for all callbacks to complete (don't block the main flow)
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)


async def fire_single_callback(url: str, payload: Dict, event_type: str) -> None:
    """Fire a single HTTP callback with retries."""
    max_retries = 3
    timeout_seconds = 5.0
    retry_delays = [1.0, 2.0, 4.0]  # Exponential backoff
    
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=timeout_seconds) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                
                logger.info(f"✅ Callback success: {event_type} -> {url} (attempt {attempt + 1})")
                return  # Success, exit retry loop
                
        except httpx.TimeoutException:
            logger.warning(f"⏰ Callback timeout: {event_type} -> {url} (attempt {attempt + 1}/{max_retries})")
        except httpx.HTTPStatusError as e:
            logger.warning(f"🔴 Callback HTTP error: {event_type} -> {url} - Status {e.response.status_code} (attempt {attempt + 1}/{max_retries})")
        except Exception as e:
            logger.warning(f"❌ Callback error: {event_type} -> {url} - {str(e)} (attempt {attempt + 1}/{max_retries})")
        
        # Wait before retry (except on last attempt)
        if attempt < max_retries - 1:
            await asyncio.sleep(retry_delays[attempt])
    
    # All retries failed
    logger.error(f"💥 Callback failed after {max_retries} attempts: {event_type} -> {url}")


def format_message_log(action: str, sender_id: str, recipient_id: str, message: str) -> str:
    """Format a message log entry with complete details."""
    return f"""
MESSAGE {action.upper()}
FROM: {sender_id}
TO: {recipient_id}
CONTENT:
{message}
{"=" * 80}"""

class MessagingServer:
    """Core stateless messaging server for client-to-client communication."""
    
    def __init__(self, queue_backend: Optional[QueueBackend] = None) -> None:
        self.queue_backend = queue_backend or InMemoryQueueBackend()
        logger.info(f"MessagingServer initialized with {type(self.queue_backend).__name__}")
        self.client_configs: Dict[str, Dict] = {}
    
    def get_client_config(self, client_id: str) -> Dict:
        """Get or load client configuration."""
        if client_id not in self.client_configs:
            self.client_configs[client_id] = load_client_config(client_id)
        return self.client_configs[client_id]
    
    async def send_message(self, sender_id: str, recipient_id: str, content: str) -> str:
        """Send a message from sender to recipient."""
        # Get sender's configuration
        config = self.get_client_config(sender_id)
        
        # Note: max_tokens and max_iterations checks will be implemented in the future
        
        # Cleanup expired messages before processing
        await self.queue_backend.cleanup_expired_messages()
        
        # Validate inputs
        if not sender_id.strip():
            return "❌ **Error**: Sender ID cannot be empty"
        
        if not recipient_id.strip():
            return "❌ **Error**: Recipient ID cannot be empty"
            
        if not content.strip():
            return "⚠️ **Warning**: Sending empty message"
        
        # Create message
        message = Message(
            from_client_id=sender_id,
            content=content,
            timestamp=datetime.now()
        )
        
        # Send message via queue backend
        await self.queue_backend.send_message(recipient_id, message)
        
        # Notify any blocked calls waiting for this recipient
        await self.queue_backend.notify_new_message(recipient_id)
        
        # Log complete message details
        logger.info(format_message_log("sent", sender_id, recipient_id, content))
        
        return f"✅ **Message sent successfully** to `{recipient_id}`"
    
    async def send_message_and_wait(self, sender_id: str, recipient_id: str, content: str) -> str:
        """Send a message and wait for a response (blocking call)."""
        # Get sender's configuration
        config = self.get_client_config(sender_id)
        timeout = config["timeouts"]["send_message_and_wait"]
        
        # First, send the message
        send_result = await self.send_message(sender_id, recipient_id, content)
        
        # If send failed, return the error
        if send_result.startswith("❌") or send_result.startswith("⚠️"):
            return send_result
        
        logger.info(f"Waiting for response to {sender_id} (timeout: {timeout}s)")
        
        # Wait for a response to arrive in sender's queue
        message_arrived = await self.queue_backend.wait_for_new_message(sender_id, timeout)
        
        if message_arrived:
            # Get the response messages
            messages = await self.queue_backend.get_messages(sender_id, pop=True)
            if messages:
                return self._format_messages_as_markdown(sender_id, messages)
            else:
                return "📭 **No response received** (queue was empty)"
        else:
            return f"⏰ **Timeout**: No response received within {timeout} seconds"
    
    async def get_messages(self, client_id: str) -> str:
        """Get and remove all messages for a client, formatted as markdown."""
        # Get client's configuration
        config = self.get_client_config(client_id)
        timeout = config["timeouts"]["get_messages"]
        
        # Cleanup expired messages before processing
        await self.queue_backend.cleanup_expired_messages()
        
        # Validate input
        if not client_id.strip():
            return "❌ **Error**: Client ID cannot be empty"
        
        # Get messages from queue backend
        messages = await self.queue_backend.get_messages(client_id, pop=True)
        
        if not messages:
            # No messages found - block for configured timeout
            logger.debug(f"No messages found for {client_id}, waiting {timeout} seconds...")
            
            message_arrived = await self.queue_backend.wait_for_new_message(client_id, timeout)
            
            if message_arrived:
                # Get the new messages that arrived
                messages = await self.queue_backend.get_messages(client_id, pop=True)
                if messages:
                    logger.info(f"Retrieved {len(messages)} messages for {client_id} after waiting")
                    return self._format_messages_as_markdown(client_id, messages)
                else:
                    return "📭 **No messages** for you right now."
            else:
                logger.debug(f"Timeout waiting for messages for {client_id}")
                return "📭 **No messages** for you right now."
        
        logger.info(f"Retrieved and popped {len(messages)} messages for {client_id}")
        
        return self._format_messages_as_markdown(client_id, messages)
    
    def _format_messages_as_markdown(self, client_id: str, messages: List[Message]) -> str:
        """Format messages as markdown."""
        message_count = len(messages)
        markdown_parts = [f"## 📨 Messages for `{client_id}` ({message_count} message{'s' if message_count != 1 else ''})", ""]
        
        for msg in messages:
            relative_time = format_relative_time(msg.timestamp)
            markdown_parts.extend([
                f"**From:** `{msg.from_client_id}`  ",
                f"**Time:** {relative_time}  ",
                f"**Message:** {msg.content}",
                "",
                "---",
                ""
            ])
        
        return "\n".join(markdown_parts)
    
    def checkin_client(self, client_id: str, name: str, capabilities: str) -> str:
        """Client checkin (for future features, currently just logs)."""
        if not client_id.strip():
            return "❌ **Error**: Client ID cannot be empty"
        
        logger.info(f"Client checkin - ID: {client_id}, Name: {name}, Capabilities: {capabilities}")
        
        return f"👋 **Checked in successfully** as `{client_id}`  \n**Name:** {name}  \n**Capabilities:** {capabilities}"


# Initialize the messaging server and FastMCP
messaging_server = MessagingServer(
    queue_backend=InMemoryQueueBackend(
        message_expiration_seconds=DEFAULT_CONFIG["timeouts"]["message_expiration"]
    )
)

# Initialize FastMCP with HTTP Streamable transport
mcp = FastMCP(
    name="messaging-server",
    description="MCP server for client-to-client messaging using HTTP Streamable transport",
    stateless_http=True,  # Use stateless HTTP for Streamable HTTP transport
    json_response=False   # Use SSE streaming format for richer client experience
)


@mcp.tool()
async def checkin_client(client_id: str, name: str, capabilities: str = "Generic project description") -> str:
    """Check in as a client to announce your presence.
    
    Args:
        client_id: Your unique client ID (read from 'my_id' field in your local mcp_recipients.json file)
        name: Display name for this client instance
        capabilities: Description of client capabilities (default: Generic project description)
        
    Returns:
        Confirmation of successful checkin
    """
    return messaging_server.checkin_client(client_id, name, capabilities)


@mcp.tool()
async def send_message_and_wait(sender_id: str, recipient_id: str, message: str, expectation: str = "response_expected") -> str:
    """Send a message and wait for a response (blocking conversation mode).
    
    Args:
        sender_id: Your client ID (read from 'my_id' field in your local mcp_recipients.json file)
        recipient_id: The recipient's client ID (choose from 'recipients' section in your local mcp_recipients.json file)
        message: The message content to send
        expectation: Response expectation - one of:
            - "response_expected": I expect a response via send_message_and_wait
            - "no_response": I do not expect a response
            - "end_conversation": End of conversation
        
    Returns:
        The response message(s) in markdown format, or timeout message (3 minute timeout)
    """
    # Append expectation to message with emphasis
    expectation_text = {
        "response_expected": "**📬 I expect a response via send_message_and_wait**",
        "no_response": "**📭 I do not expect a response**", 
        "end_conversation": "**🔚 End of conversation**"
    }
    
    formatted_message = f"{message}\n\n---\n{expectation_text.get(expectation, expectation_text['response_expected'])}"
    
    # Fire and forget for no_response - don't block
    if expectation == "no_response":
        result = await messaging_server.send_message(sender_id, recipient_id, formatted_message)
        return f"📭 **Message sent** (no response expected)\n\n{result}"
    
    # Block and wait for response (original behavior)
    return await messaging_server.send_message_and_wait(sender_id, recipient_id, formatted_message)


@mcp.tool()
async def get_messages(client_id: str) -> str:
    """Get your pending messages (messages are removed from queue after retrieval). Blocks for 60 seconds if no messages.
    
    Args:
        client_id: Your client ID (read from 'my_id' field in your local mcp_recipients.json file)
        
    Returns:
        Your messages formatted in markdown (blocks up to 60 seconds waiting for new messages)
    """
    return await messaging_server.get_messages(client_id)


@mcp.tool()
async def get_my_identity() -> str:
    """Get information about how to find your client identity and available recipients.
    
    Returns:
        Instructions on using mcp_recipients.json file or a similar tool to get your list of mcp recipients
    """
    # Add 30 second delay to test blocking behavior
    logger.info("get_my_identity called - starting 30 second wait...")
    await asyncio.sleep(30)
    logger.info("get_my_identity - 30 second wait completed, returning response")
    
    return """## 🆔 Client Identity Information

**Check your local `mcp_recipients.json` file** for:

- **Your Client ID**: Found in the `"my_id"` field
- **Available Recipients**: Listed in the `"recipients"` section
- **Server Information**: Connection details in `"server_info"`

This file should be in the root directory of your project and contains all the client IDs and recipient information needed for messaging."""


@mcp.tool()
async def get_active_sessions() -> str:
    """Get information about active MCP sessions and connections.
    
    Returns:
        Information about current active sessions, queue statistics, and server status
    """
    try:
        # Get session information from FastMCP (if available)
        session_info = []
        
        # Get queue statistics
        if hasattr(messaging_server.queue_backend, 'get_queue_stats'):
            queue_stats = messaging_server.queue_backend.get_queue_stats()
        else:
            queue_stats = {
                "total_queues": len(getattr(messaging_server.queue_backend, 'queues', {})),
                "total_messages": sum(len(msgs) for msgs in getattr(messaging_server.queue_backend, 'queues', {}).values()),
                "active_waiters": len(getattr(messaging_server.queue_backend, 'notification_events', {}))
            }
        
        # Get active client IDs from queues
        active_clients = list(getattr(messaging_server.queue_backend, 'queues', {}).keys())
        waiting_clients = list(getattr(messaging_server.queue_backend, 'notification_events', {}).keys())
        
        # Format response
        response_parts = [
            "## 🌐 MCP Server Session Status",
            "",
            f"**Server Name:** {mcp.name}",
            f"**Transport:** HTTP Streamable (stateless)",
            "",
            "### 📊 Queue Statistics",
            f"- **Active Queues:** {queue_stats['total_queues']}",
            f"- **Total Messages:** {queue_stats['total_messages']}",
            f"- **Waiting Clients:** {queue_stats.get('active_waiters', 0)}",
            "",
        ]
        
        if active_clients:
            response_parts.extend([
                "### 📝 Active Client Queues",
                ""
            ])
            for client_id in active_clients:
                queue_size = len(messaging_server.queue_backend.queues.get(client_id, []))
                response_parts.append(f"- **{client_id}**: {queue_size} message(s)")
            response_parts.append("")
        
        if waiting_clients:
            response_parts.extend([
                "### ⏳ Clients Waiting for Messages",
                ""
            ])
            for client_id in waiting_clients:
                response_parts.append(f"- **{client_id}**: Blocking for new messages")
            response_parts.append("")
        
        if not active_clients and not waiting_clients:
            response_parts.extend([
                "### 💤 No Active Sessions",
                "",
                "No clients currently have active message queues or are waiting for messages.",
                ""
            ])
        
        response_parts.extend([
            "### ℹ️ Session Notes",
            "",
            "- **HTTP Streamable**: Sessions are managed by FastMCP automatically",
            "- **Stateless Design**: Session IDs are handled transparently", 
            "- **Queue Cleanup**: Expired messages are cleaned up automatically",
            "- **Message Expiration**: 5 minutes (300 seconds)"
        ])
        
        return "\n".join(response_parts)
        
    except Exception as e:
        logger.error(f"Error getting session info: {e}")
        return f"❌ **Error**: Could not retrieve session information: {str(e)}"


@mcp.custom_route("/api/sessions", methods=["GET"])
async def get_sessions_json(request):
    """REST endpoint for session statistics - returns pure JSON for normal REST clients."""
    try:
        # Get queue statistics (same logic as MCP tool but return JSON)
        if hasattr(messaging_server.queue_backend, 'get_queue_stats'):
            queue_stats = messaging_server.queue_backend.get_queue_stats()
        else:
            queue_stats = {
                "total_queues": len(getattr(messaging_server.queue_backend, 'queues', {})),
                "total_messages": sum(len(msgs) for msgs in getattr(messaging_server.queue_backend, 'queues', {}).values()),
                "active_waiters": len(getattr(messaging_server.queue_backend, 'notification_events', {}))
            }
        
        # Get active client IDs from queues
        active_clients = list(getattr(messaging_server.queue_backend, 'queues', {}).keys())
        waiting_clients = list(getattr(messaging_server.queue_backend, 'notification_events', {}).keys())
        
        # Build client details
        client_details = {}
        for client_id in active_clients:
            queue_size = len(messaging_server.queue_backend.queues.get(client_id, []))
            client_details[client_id] = {
                "queue_size": queue_size,
                "status": "has_messages"
            }
        
        for client_id in waiting_clients:
            if client_id not in client_details:
                client_details[client_id] = {
                    "queue_size": 0,
                    "status": "waiting_for_messages"
                }
        
        # Return clean JSON structure using JSONResponse
        data = {
            "server_name": mcp.name,
            "transport": "HTTP Streamable (stateless)",
            "timestamp": datetime.now().isoformat(),
            "stats": {
                "active_queues": queue_stats['total_queues'],
                "total_messages": queue_stats['total_messages'],
                "waiting_clients": queue_stats.get('active_waiters', 0)
            },
            "clients": client_details,
            "session_notes": {
                "session_management": "FastMCP automatic",
                "design": "stateless",
                "cleanup": "automatic",
                "message_expiration_seconds": 300
            }
        }
        
        return JSONResponse(content=data)
        
    except Exception as e:
        logger.error(f"Error getting session JSON: {e}")
        error_data = {"error": f"Could not retrieve session information: {str(e)}"}
        return JSONResponse(content=error_data, status_code=500)


def main() -> None:
    """Main entry point for the messaging server."""
    parser = argparse.ArgumentParser(description="MCP HTTP Streamable messaging server")
    parser.add_argument(
        "--port", 
        type=int, 
        default=int(os.getenv("MCP_SERVER_PORT", "8123")),
        help="Port to listen on"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("MCP_SERVER_HOST", "localhost"),
        help="Host to bind to"
    )
    parser.add_argument(
        "--queue-backend",
        type=str,
        default=os.getenv("QUEUE_BACKEND", "memory"),
        choices=["memory"],  # Future: add "redis"
        help="Queue backend to use"
    )
    args = parser.parse_args()
    
    logger.info(f"Starting MCP messaging server on {args.host}:{args.port}")
    logger.info(f"Queue backend: {type(messaging_server.queue_backend).__name__}")
    logger.info("Tools available: checkin_client, send_message, send_message_and_wait, get_messages, get_my_identity, get_active_sessions")
    
    # Start the server with HTTP Streamable transport
    # Configure host and port via FastMCP settings
    mcp.settings.host = args.host
    mcp.settings.port = args.port
    
    print(f"🚀 Starting MCP messaging server at http://{args.host}:{args.port}")
    logger.info("MCP messaging server starting", extra={"host": args.host, "port": args.port})
    
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()