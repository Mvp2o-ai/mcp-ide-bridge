# MCP Reference Client

This is a reference implementation of an MCP client that demonstrates how to connect to the MCP IDE Bridge messaging server for **client-to-client communication**.

## 🌟 Purpose

This client serves as both a **testing tool** for the messaging server and a **reference implementation** for developers building their own MCP clients. It demonstrates:

- **HTTP Streamable Transport**: Connects to MCP servers using the latest HTTP Streamable transport
- **Client-to-Client Messaging**: Enables communication between different IDEs and tools
- **Tool Execution**: Automatically executes MCP tools based on natural language queries
- **Interactive Testing**: Provides a command-line interface for testing the messaging server

## 🎯 Use Cases

### IDE Collaboration Testing
- Test messaging between different IDE instances
- Verify cross-editor communication workflows
- Debug MCP connection issues
- Validate message routing and delivery

### Development Workflows
- **Cursor ↔ Cursor**: Test pair programming scenarios
- **Cursor ↔ VS Code**: Verify cross-editor file sharing
- **Windsurf ↔ Any IDE**: Test AI agent coordination
- **Team Coordination**: Simulate multi-developer workflows

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.12+
- MCP IDE Bridge server running on port 8111
- Optional: Anthropic API key for full functionality

### 2. Setup

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Set up environment (optional):**
Create a `.env` file with your Anthropic API key for full functionality:
```
ANTHROPIC_API_KEY=your_api_key_here
```

**Note**: The client works without an API key for basic connection testing.

### 3. Usage

**Start the messaging server first:**
```bash
# In the main project directory
python -m mcp_messaging.server --port 8111
```

**Test basic connection (no API key required):**
```bash
python test_connection.py --mcp-localhost-port 8111
```

**Run full client (requires API key):**
```bash
python client.py --mcp-localhost-port 8111
```

## 🧪 Testing Examples

### Connection Test
```bash
python test_connection.py --mcp-localhost-port 8111
```
This will:
- Connect to the MCP server
- List all available tools
- Verify the connection is working

### Interactive Testing
```bash
python client.py --mcp-localhost-port 8111
```

**Example interactions:**
```
Query: Check in as client_1 with name "Test Client"
Query: Send a message from client_1 to client_2 saying "Hello from client 1!"
Query: Get messages for client_2
Query: What are the active sessions?
```

## 🔧 How It Works

1. **Connection**: Establishes HTTP Streamable connection to the MCP server
2. **Tool Discovery**: Retrieves available tools from the server
3. **Query Processing**: Sends user queries to Claude with available tools (if API key provided)
4. **Tool Execution**: Executes MCP tools based on analysis
5. **Response Handling**: Processes tool results and continues conversation

## 🏗️ Architecture

- **MCPClient**: Main client class handling MCP protocol communication
- **Claude Integration**: Uses Anthropic's API for natural language processing (optional)
- **Tool Management**: Automatically handles tool discovery and execution
- **Session Management**: Proper cleanup of MCP sessions and streams

## 📋 Available Tools

The client can interact with all MCP IDE Bridge tools:

| Tool | Purpose | Example |
|------|---------|---------|
| `checkin_client` | Register presence | "Check in as alice_cursor" |
| `send_message_without_waiting` | Send message (fire & forget) | "Send message to bob_vscode" |
| `get_messages` | Retrieve messages | "Get messages for alice_cursor" |
| `get_my_identity` | Get configuration help | "What's my identity?" |
| `get_active_sessions` | View active connections | "Show active sessions" |

## 🔒 Security Note

This client is designed for **testing and development** purposes. For production use, consider:

- Using the enterprise solution at [MilesDyson.ai](https://milesdyson.ai)
- Implementing proper authentication
- Adding message encryption
- Setting up audit logging

## 🤝 Contributing

This reference client is part of the open source MCP IDE Bridge project. Contributions are welcome!

- Report issues in the main repository
- Submit pull requests for improvements
- Help improve documentation and examples 