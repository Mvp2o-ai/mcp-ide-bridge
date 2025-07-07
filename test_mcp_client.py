#!/usr/bin/env python3
"""
MCP Test Harness - A client for testing MCP tools

Usage:
    python test_mcp_client.py get_my_identity
    python test_mcp_client.py checkin_client --client_id "test-client" --name "Test Client" 
    python test_mcp_client.py send_message_and_wait --sender_id "test" --recipient_id "target" --message "Hello"
    python test_mcp_client.py get_messages --client_id "test-client"
    python test_mcp_client.py get_active_sessions
"""

import json
import argparse
import sys
import requests
from typing import Dict, Any, Optional


class MCPTestClient:
    def __init__(self, base_url: str = "http://localhost:8111"):
        self.base_url = base_url
        self.session = requests.Session()
        # Set required headers for MCP streamable HTTP
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        })
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool and return the parsed response."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        print(f"🔧 Calling tool: {tool_name}")
        print(f"📦 Arguments: {json.dumps(arguments, indent=2)}")
        print(f"🌐 URL: {self.base_url}/mcp/")
        print("=" * 50)
        
        try:
            response = self.session.post(f"{self.base_url}/mcp/", json=payload)
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📋 Headers: {dict(response.headers)}")
            print("=" * 50)
            
            if response.status_code == 200:
                # Handle streaming response
                response_text = response.text
                print(f"📄 Raw Response:\n{response_text}")
                print("=" * 50)
                
                # Parse the streaming response
                if "event: message" in response_text and "data: " in response_text:
                    # Extract JSON from SSE format - handle both \n and \r\n
                    lines = response_text.replace('\r\n', '\n').split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith("data: "):
                            json_data = line[6:].strip()  # Remove "data: " prefix
                            try:
                                parsed = json.loads(json_data)
                                return parsed
                            except json.JSONDecodeError as e:
                                print(f"❌ JSON parsing error: {e}")
                                return {"error": f"JSON parsing failed: {e}", "raw": response_text}
                else:
                    # Try parsing as direct JSON
                    try:
                        return response.json()
                    except json.JSONDecodeError:
                        return {"error": "Non-JSON response", "raw": response_text}
            else:
                try:
                    error_data = response.json()
                    return {"error": f"HTTP {response.status_code}", "details": error_data}
                except json.JSONDecodeError:
                    return {"error": f"HTTP {response.status_code}", "raw": response.text}
                    
        except requests.exceptions.ConnectionError:
            return {"error": "❌ Connection failed - is the MCP server running on port 8111?"}
        except requests.exceptions.Timeout:
            return {"error": "❌ Request timed out - server may be overloaded"}
        except requests.exceptions.RequestException as e:
            return {"error": f"❌ Request failed: {e}"}
    
    def format_result(self, result: Dict[str, Any]) -> str:
        """Format the MCP tool result for display."""
        if "error" in result:
            return f"❌ Error: {result['error']}\nDetails: {result.get('details', result.get('raw', 'No details'))}"
        
        if "result" in result:
            tool_result = result["result"]
            if isinstance(tool_result, dict) and "content" in tool_result:
                # Extract text content from MCP response
                content = tool_result["content"]
                if isinstance(content, list) and len(content) > 0:
                    if isinstance(content[0], dict) and "text" in content[0]:
                        return content[0]["text"]
                return str(content)
            return str(tool_result)
        
        return str(result)


def main():
    parser = argparse.ArgumentParser(description="MCP Test Harness")
    parser.add_argument("tool_name", help="Name of the MCP tool to call")
    parser.add_argument("--url", default="http://localhost:8111", help="MCP server URL")
    
    # Tool-specific arguments
    parser.add_argument("--client_id", help="Client ID parameter")
    parser.add_argument("--sender_id", help="Sender ID parameter")
    parser.add_argument("--recipient_id", help="Recipient ID parameter") 
    parser.add_argument("--name", help="Name parameter")
    parser.add_argument("--capabilities", help="Capabilities parameter")
    parser.add_argument("--message", help="Message parameter")
    parser.add_argument("--expectation", help="Expectation parameter")
    parser.add_argument("--random_string", help="Random string parameter")
    
    # Generic argument support
    parser.add_argument("--args", help="JSON string of arguments")
    
    args = parser.parse_args()
    
    # Build arguments dict
    arguments = {}
    
    # Add non-None arguments
    if args.client_id:
        arguments["client_id"] = args.client_id
    if args.sender_id:
        arguments["sender_id"] = args.sender_id
    if args.recipient_id:
        arguments["recipient_id"] = args.recipient_id
    if args.name:
        arguments["name"] = args.name
    if args.capabilities:
        arguments["capabilities"] = args.capabilities
    if args.message:
        arguments["message"] = args.message
    if args.expectation:
        arguments["expectation"] = args.expectation
    if args.random_string:
        arguments["random_string"] = args.random_string
    
    # Override with JSON args if provided
    if args.args:
        try:
            json_args = json.loads(args.args)
            arguments.update(json_args)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in --args: {e}")
            sys.exit(1)
    
    # Some tools need default arguments
    if args.tool_name in ["get_my_identity", "get_active_sessions"] and not arguments:
        arguments["random_string"] = "test"
    
    # Validate required arguments for specific tools
    validation_errors = []
    
    if args.tool_name == "checkin_client":
        if not arguments.get("client_id"):
            validation_errors.append("--client_id is required for checkin_client")
        if not arguments.get("name"):
            validation_errors.append("--name is required for checkin_client")
    
    elif args.tool_name == "send_message_and_wait":
        if not arguments.get("sender_id"):
            validation_errors.append("--sender_id is required for send_message_and_wait")
        if not arguments.get("recipient_id"):
            validation_errors.append("--recipient_id is required for send_message_and_wait")
        if not arguments.get("message"):
            validation_errors.append("--message is required for send_message_and_wait")
    
    elif args.tool_name == "send_message_without_waiting":
        if not arguments.get("sender_id"):
            validation_errors.append("--sender_id is required for send_message_without_waiting")
        if not arguments.get("recipient_ids"):
            validation_errors.append("--args with recipient_ids array is required for send_message_without_waiting")
        if not arguments.get("messages"):
            validation_errors.append("--args with messages array is required for send_message_without_waiting")
    
    elif args.tool_name == "get_messages":
        if not arguments.get("client_id"):
            validation_errors.append("--client_id is required for get_messages")
    
    if validation_errors:
        print("❌ Validation Errors:")
        for error in validation_errors:
            print(f"   • {error}")
        print(f"\n💡 Example usage for {args.tool_name}:")
        if args.tool_name == "checkin_client":
            print("   python test_mcp_client.py checkin_client --client_id \"mcp-ide-bridge\" --name \"Test Client\"")
        elif args.tool_name == "send_message_and_wait":
            print("   python test_mcp_client.py send_message_and_wait --sender_id \"mcp-ide-bridge\" --recipient_id \"miles_mcp_server\" --message \"Hello\"")
        elif args.tool_name == "send_message_without_waiting":
            print("   # Broadcast same message:")
            print("   python test_mcp_client.py send_message_without_waiting --sender_id \"mcp-ide-bridge\" --args '{\"recipient_ids\": [\"miles_mcp_server\", \"dyson_frontend\"], \"messages\": [\"Hello everyone!\"]}'")
            print("   # Different messages:")
            print("   python test_mcp_client.py send_message_without_waiting --sender_id \"mcp-ide-bridge\" --args '{\"recipient_ids\": [\"miles_mcp_server\", \"dyson_frontend\"], \"messages\": [\"Hi Miles\", \"Hi Dyson\"]}'")
        elif args.tool_name == "get_messages":
            print("   python test_mcp_client.py get_messages --client_id \"mcp-ide-bridge\"")
        sys.exit(1)
    
    # Create client and call tool
    client = MCPTestClient(args.url)
    result = client.call_tool(args.tool_name, arguments)
    
    # Display formatted result
    print("🎯 RESULT:")
    print("=" * 50)
    formatted = client.format_result(result)
    print(formatted)
    
    # Also show raw JSON for debugging
    print("\n🔍 RAW JSON:")
    print("=" * 50)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main() 