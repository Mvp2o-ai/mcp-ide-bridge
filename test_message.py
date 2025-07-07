#!/usr/bin/env python3
import requests
import json

# MCP call to send a test message
mcp_payload = {
    "jsonrpc": "2.0",
    "id": "test-1",
    "method": "tools/call",
    "params": {
        "name": "send_message_without_waiting",
        "arguments": {
            "sender_id": "test-client",
            "recipient_ids": ["test-recipient"],
            "messages": ["Hello! This is a test message to verify client activity tracking."],
            "recipients_config": {
                "my_id": "test-client",
                "name": "Test Client", 
                "description": "Testing client activity tracking",
                "clientType": "test agent",
                "recipients": {
                    "test-recipient": {
                        "name": "Test Recipient",
                        "description": "Test target"
                    }
                }
            }
        }
    }
}

# Send to MCP server
response = requests.post('http://localhost:8111/mcp/', 
                        json=mcp_payload,
                        headers={'Content-Type': 'application/json'})

print("Status:", response.status_code)
print("Response:", response.text)
