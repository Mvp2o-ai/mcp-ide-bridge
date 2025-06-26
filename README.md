# MCP IDE Bridge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![MCP Protocol](https://img.shields.io/badge/MCP-HTTP%20Streamable-green.svg)](https://spec.modelcontextprotocol.io/)

## 🎬 Demo Video

<div align="center">

<table>
  <tr>
    <td align="center" width="50%"><b>FRONT END WEB APP<br/>CURSOR IDE</b></td>
    <td align="center" width="50%"><b>BACK END API<br/>CURSOR IDE</b></td>
  </tr>
  <tr>
    <td colspan="2">
      <a href="https://www.youtube.com/watch?v=TA97TGoOMJA" target="_blank">
        <img 
          src="https://img.youtube.com/vi/TA97TGoOMJA/maxresdefault.jpg" 
          alt="MCP IDE Bridge Demo"
          style="
            border: 7px solid #e5534b; 
            border-radius: 14px; 
            padding: 0; 
            box-shadow: 0 0 36px 8px #e5534b, 0 0 0 4px #fff inset;
            transition: box-shadow 0.3s;
          "
        >
      </a>
    </td>
  </tr>
</table>

</div>

<p align="center"><i>
Click the image above to watch the live demo of MCP IDE Bridge in action!<br>
<b>This shows two Cursor IDEs (front end and back end) collaborating in real time via the IDE Bridge.</b>
</i></p>

A stateless, open source MCP (Model Context Protocol) HTTP Streamable server that enables **client-to-client communication** between IDEs and development tools. This opens up a new dimension of collaboration beyond traditional MCP client-server interactions.

**🚀 Perfect for**: Cross-IDE collaboration, team development workflows, AI agent coordination, and seamless tool integration.

## 🌟 What Makes This Special?

### Traditional MCP vs MCP IDE Bridge

| Traditional MCP | MCP IDE Bridge |
|----------------|----------------|
| Client ↔ Server | Client ↔ Server ↔ Client |
| One-way communication | Bidirectional messaging |
| Tool execution only | Real-time collaboration |
| Single IDE focus | Multi-IDE coordination |

### Real-World Use Cases

**🎯 IDE Collaboration**
- **Cursor ↔ Cursor**: Share code snippets, debugging sessions, or pair programming
- **Cursor ↔ VS Code**: Cross-editor communication and file sharing
- **Windsurf ↔ Any IDE**: AI agent coordination across different development environments
- **Team Workflows**: Coordinate multiple developers working on the same project

**🤖 AI Agent Coordination**
- Agent-to-agent communication for complex workflows
- Distributed AI processing across multiple tools
- Human-in-the-loop collaboration with AI assistants

## 🏗️ Architecture

### Client-to-Client Communication

```
IDE A (Cursor)  ←→  MCP IDE Bridge  ←→  IDE B (VS Code)
     ↑                    ↑                    ↑
  MCP Client         Message Relay        MCP Client
```

### Key Components

- **Message Relay**: Stateless server that routes messages between clients
- **Client Registry**: Dynamic client discovery and registration
- **Message Queues**: Per-recipient queues with automatic expiration
- **HTTP Streamable**: Latest MCP transport for real-time communication

## 🚀 Quick Start

### 1. Start the Server

**Docker (Recommended):**
```bash
docker run -d --name mcp-ide-bridge -p 8111:8123 mcp-messaging-server
```

**Python:**
```bash
python -m mcp_messaging.server --port 8111
```

### 2. Configure Your IDE

Create `mcp_recipients.json` in your project root. **Each project gets ONE file with its own unique ID and list of recipients it can communicate with:**

```json
{
  "my_id": "myproject_cursor",
  "recipients": {
    "teammate_vscode": {
      "name": "Teammate's Project",
      "description": "My teammate's project in VS Code"
    },
    "aiagent_windsurf": {
      "name": "AI Agent Project", 
      "description": "AI agent development in Windsurf"
    }
  },
  "server_info": {
    "url": "http://localhost:8111/mcp/",
    "transport": "http_streamable"
  }
}
```

**🤖 AI Agent Generation**: Your IDE's AI agent can generate this file! Simply ask:
- **Cursor**: "Generate an mcp_recipients.json for my project"
- **VS Code**: "Create mcp_recipients.json configuration for my team"
- **Windsurf**: "Help me set up mcp_recipients.json for collaboration"

**📁 Multi-Project Examples**: See `examples/multi-project-setup/` for examples showing how different projects communicate. **Each project file must be named `mcp_recipients.json`** - the filename examples in that folder are just for reference.

### 3. Connect Your IDE

**Cursor IDE:**
1. Create `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "messaging-server": {
      "url": "http://localhost:8111/mcp/",
      "type": "streamable-http",
      "description": "MCP HTTP Streamable messaging server for client-to-client communication"
    }
  }
}
```
2. Open Command Palette (`Cmd/Ctrl + Shift + P`)
3. Search for "MCP: Connect to Server"
4. Enter: `http://localhost:8111/mcp/`

**VS Code:**
1. Install MCP extension from marketplace
2. Create `mcp_recipients.json` in project root
3. Configure MCP settings in VS Code preferences
4. Use MCP commands to connect and collaborate

**Windsurf:**
1. Create `mcp_recipients.json` in project root
2. Open Windsurf settings → MCP configuration
3. Add server URL: `http://localhost:8111/mcp/`
4. Start messaging with other IDEs

**Claude Desktop:**
1. Create `mcp_recipients.json` in project root
2. Open Claude Desktop settings → MCP configuration
3. Add server URL: `http://localhost:8111/mcp/`
4. Use Claude's MCP integration to communicate

**JetBrains IDEs (IntelliJ, PyCharm, etc.):**
1. Install MCP plugin from plugin marketplace
2. Create `mcp_recipients.json` in project root
3. Configure MCP server in plugin settings
4. Use MCP tools from the IDE

**Note**: Each IDE requires both `mcp_recipients.json` (for messaging) and IDE-specific MCP configuration (for connection). **Each project gets ONE `mcp_recipients.json` file with its own unique ID and recipient list.** The file must be named exactly `mcp_recipients.json` and placed in the **project root** for easy discovery by IDE agents. See `examples/multi-project-setup/README.md` for detailed setup instructions.

## 📋 Available Tools

### Core Messaging Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| `checkin_client` | Register your presence | Announce availability |
| `send_message_and_wait` | Send message & wait for response | Real-time conversations |
| `get_messages` | Retrieve pending messages | Check for updates |
| `get_my_identity` | Get configuration help | Setup assistance |
| `get_active_sessions` | View active connections | Monitor team activity |

### Example Workflows

**Pair Programming:**
```bash
# Developer A checks in
checkin_client("alice_cursor", "Alice", "Working on auth module")

# Developer B sends a question
send_message_and_wait("bob_vscode", "alice_cursor", "Can you review this auth code?")

# Developer A gets the message
get_messages("alice_cursor")
```

**AI Agent Coordination:**
```bash
# AI Agent 1 announces task completion
checkin_client("ai_agent_1", "Code Review Bot", "Ready for review tasks")

# AI Agent 2 requests collaboration
send_message_and_wait("ai_agent_2", "ai_agent_1", "Need help with security review")
```

## 🔒 Security Considerations

### Current State (Desktop Use)

**✅ Suitable for:**
- Local development teams
- Personal projects
- Desktop-only workflows
- Trusted network environments

**⚠️ Limitations:**
- No authentication beyond client IDs
- No encryption of messages
- No access control
- No audit logging

**🔐 Security Model:**
- Client IDs act as simple credentials
- Messages stored in memory only
- 5-minute automatic expiration
- No persistent storage

### Enterprise Solution

For production use, security, and team collaboration, we offer **MilesDyson.ai** - an enterprise-grade Agentic Platform as a Service (aPaaS) that addresses all security concerns:

- **🔐 Enterprise Authentication**: SSO, RBAC, and audit trails
- **🛡️ End-to-End Encryption**: All messages encrypted in transit and at rest
- **🌐 Global Infrastructure**: Multi-region deployment with 99.9% uptime
- **👥 Team Management**: User management, permissions, and collaboration tools
- **📊 Analytics**: Usage insights and performance monitoring
- **🔧 Enterprise Support**: Dedicated support and custom integrations

**[Learn More → MilesDyson.ai](https://milesdyson.ai)**

## 🧪 Testing

### Quick Connection Test

```bash
# Test server connectivity
curl -X GET http://localhost:8111/api/sessions

# Test MCP client connection
cd examples/client
python test_connection.py --mcp-localhost-port 8111
```

### Reference Client

The project includes a reference MCP client for testing:

```bash
cd examples/client
pip install -e .
python client.py --mcp-localhost-port 8111
```

## 🏗️ Development

### Project Structure

```
src/mcp_messaging/
├── server.py          # Main server implementation
├── models.py          # Data models
└── queue_backends.py  # Queue implementations

examples/
├── client/            # Reference MCP client
├── configs/           # Project-specific configurations
├── multi-project-setup/  # Multi-project IDE communication examples
│   ├── README.md      # Comprehensive setup guide
│   ├── frontend-cursor.json
│   ├── backend-vscode.json
│   ├── rag-windsurf.json
│   ├── devops-jetbrains.json
│   └── ...            # More project examples (filenames for reference only)
└── reference/         # Additional examples

mcp_recipients.json    # Example configuration (each project gets ONE file)
Dockerfile            # Container support
```

**Note**: Each project gets ONE `mcp_recipients.json` file with its own unique ID and recipient list. The example filenames in `multi-project-setup/` are just for reference - your actual file must be named `mcp_recipients.json` in each project root.

### Local Development

```bash
# Clone and setup
git clone https://github.com/your-username/mcp-ide-bridge.git
cd mcp-ide-bridge

# Install dependencies
python -m venv venv
source venv/bin/activate
pip install -e .

# Run server
python -m mcp_messaging.server --port 8111
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development setup
- Code style guidelines
- Testing procedures
- Pull request process

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🚀 Enterprise Solution

**Ready for production use?** 

**[MilesDyson.ai](https://milesdyson.ai)** provides enterprise-grade MCP IDE Bridge with:

- 🔐 **Enterprise Security**: SSO, encryption, audit trails
- 🌐 **Global Infrastructure**: Multi-region, high availability  
- 👥 **Team Management**: User management and collaboration tools
- 📊 **Analytics & Monitoring**: Usage insights and performance tracking
- 🔧 **Enterprise Support**: Dedicated support and custom integrations

**Perfect for:**
- Development teams
- Enterprise environments
- Production deployments
- Multi-organization collaboration

---

**Built with MCP HTTP Streamable transport** • **Powered by FastMCP** • **Made with ❤️ by MVP2o.ai**