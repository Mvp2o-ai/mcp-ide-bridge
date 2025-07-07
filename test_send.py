import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    # Connect to server
    streams_context = streamablehttp_client(
        url="http://localhost:8111/mcp",
        headers={},
    )
    read_stream, write_stream, _ = await streams_context.__aenter__()
    
    # Create session
    session_context = ClientSession(read_stream, write_stream)
    session = await session_context.__aenter__()
    await session.initialize()
    
    try:
        # Send message
        response = await session.call_tool(
            "send_message_without_waiting",
            {
                "sender_id": "test_client",
                "recipients": [
                    {
                        "id": "milesdyson",
                        "message": "Test message from test_client - please acknowledge if you receive this!"
                    }
                ],
                "recipients_config": {
                    "my_sender_id": "test_client",
                    "my_name": "Test Client"
                }
            }
        )
        print("Message sent:", response)
        
    finally:
        # Cleanup
        await session_context.__aexit__(None, None, None)
        await streams_context.__aexit__(None, None, None)

if __name__ == "__main__":
    asyncio.run(main()) 