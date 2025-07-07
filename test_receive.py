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
        # Get messages
        response = await session.call_tool(
            "get_messages",
            {
                "sender_id": "milesdyson",
                "recipients_config": {
                    "my_sender_id": "milesdyson",
                    "my_name": "MilesDyson"
                }
            }
        )
        print("Messages received:", response)
        
    finally:
        # Cleanup
        await session_context.__aexit__(None, None, None)
        await streams_context.__aexit__(None, None, None)

if __name__ == "__main__":
    asyncio.run(main()) 