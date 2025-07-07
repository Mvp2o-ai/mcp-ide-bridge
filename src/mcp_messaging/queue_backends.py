"""Queue backend implementations for MCP messaging server."""

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .models import Message, format_relative_time

logger = logging.getLogger(__name__)

def format_message_log(action: str, sender_id: str, recipient_id: str, message: str) -> str:
    """Format a message log entry with complete details."""
    return f"""
MESSAGE {action.upper()}
FROM: {sender_id}
TO: {recipient_id}
CONTENT:
{message}
{"=" * 80}"""


class QueueBackend(ABC):
    """Abstract queue backend interface - designed for Redis compatibility."""
    
    @abstractmethod
    async def send_message(self, recipient_id: str, message: Message) -> None:
        """Add message to recipient's queue."""
        pass
    
    @abstractmethod 
    async def get_messages(self, client_id: str, pop: bool = True) -> List[Message]:
        """Get messages for client (and optionally remove them)."""
        pass
    
    @abstractmethod
    async def cleanup_expired_messages(self) -> None:
        """Remove expired messages from all queues."""
        pass
    
    @abstractmethod
    async def wait_for_new_message(self, client_id: str, timeout: float) -> bool:
        """Block until new message arrives (or timeout). Returns True if message available."""
        pass
    
    @abstractmethod
    async def notify_new_message(self, client_id: str) -> None:
        """Notify any blocked calls that new message arrived."""
        pass


class InMemoryQueueBackend(QueueBackend):
    """In-memory queue backend using asyncio.Event for wake-up notifications."""
    
    def __init__(self, message_expiration_seconds: float = float('inf')):  # Set to infinity by default
        self.queues: Dict[str, List[Message]] = {}
        self.notification_events: Dict[str, asyncio.Event] = {}
        self.message_expiration_seconds = message_expiration_seconds
        logger.info(f"Initialized InMemoryQueueBackend (message expiration: {message_expiration_seconds}s)")
    
    async def send_message(self, recipient_id: str, message: Message) -> None:
        """Add message to recipient's queue."""
        if recipient_id not in self.queues:
            self.queues[recipient_id] = []
            logger.info(f"Created new queue for {recipient_id}")
        
        self.queues[recipient_id].append(message)
        logger.info(format_message_log("queued", message.from_client_id, recipient_id, message.content))
    
    async def get_messages(self, client_id: str, pop: bool = True) -> List[Message]:
        """Get messages for client (and optionally remove them)."""
        if client_id not in self.queues or not self.queues[client_id]:
            return []
        
        messages = self.queues[client_id].copy()
        message_count = len(messages)
        
        if pop:
            # Remove the queue entirely (pop all messages)
            del self.queues[client_id]
            # Log each retrieved message
            for msg in messages:
                logger.info(format_message_log("retrieved", msg.from_client_id, client_id, msg.content))
            logger.info(f"Popped {message_count} messages for {client_id}")
        else:
            logger.debug(f"Peeked at {message_count} messages for {client_id}")
        
        return messages
    
    async def cleanup_expired_messages(self) -> None:
        """Remove expired messages from all queues."""
        # Skip cleanup if expiration is disabled (infinity)
        if self.message_expiration_seconds == float('inf'):
            return
            
        cutoff_time = datetime.now() - timedelta(seconds=self.message_expiration_seconds)
        
        for recipient_id in list(self.queues.keys()):
            original_count = len(self.queues[recipient_id])
            self.queues[recipient_id] = [
                msg for msg in self.queues[recipient_id] 
                if msg.timestamp > cutoff_time
            ]
            
            cleaned_count = original_count - len(self.queues[recipient_id])
            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} expired messages for {recipient_id}")
            
            # Remove empty queues
            if not self.queues[recipient_id]:
                del self.queues[recipient_id]
                logger.debug(f"Removed empty queue for {recipient_id}")
    
    async def wait_for_new_message(self, client_id: str, timeout: float) -> bool:
        """Block until new message arrives, but check existing messages first."""
        
        # 🔥 KEY FIX: Check if messages already exist
        if client_id in self.queues and self.queues[client_id]:
            logger.debug(f"Messages already available for {client_id}")
            return True  # Messages exist, no need to wait
        
        # Create event if it doesn't exist
        if client_id not in self.notification_events:
            self.notification_events[client_id] = asyncio.Event()
        
        logger.debug(f"Waiting for new message for {client_id} (timeout: {timeout}s)")
        
        try:
            await asyncio.wait_for(self.notification_events[client_id].wait(), timeout)
            # Clear the event for next wait
            self.notification_events[client_id].clear()
            logger.debug(f"Wake-up notification received for {client_id}")
            return True
        except asyncio.TimeoutError:
            logger.debug(f"Timeout waiting for message for {client_id}")
            return False
        finally:
            # Clean up the event if no messages are waiting
            if client_id in self.notification_events and client_id not in self.queues:
                del self.notification_events[client_id]
                logger.debug(f"Cleaned up notification event for {client_id}")
    
    async def notify_new_message(self, client_id: str) -> None:
        """Wake up any blocked send_message_and_wait calls."""
        if client_id in self.notification_events:
            self.notification_events[client_id].set()
            logger.debug(f"Notified blocked call for {client_id}")
        else:
            logger.debug(f"No blocked calls waiting for {client_id}")
    
    def get_queue_stats(self) -> Dict[str, int]:
        """Get statistics about current queues (for debugging)."""
        return {
            "total_queues": len(self.queues),
            "total_messages": sum(len(msgs) for msgs in self.queues.values()),
            "active_waiters": len(self.notification_events)
        } 