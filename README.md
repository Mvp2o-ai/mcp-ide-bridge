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
docker run -d --name mcp-ide-bridge -p 8111:8111 mcp-messaging-server
```

**Default Configuration:**
- **Port**: 8111 (both external and internal)
- **Host**: 0.0.0.0 (accepts connections from any interface)
- **Transport**: HTTP Streamable (MCP latest)
- **Health Check**: Built-in endpoint monitoring

**Python (Development Setup):**
```bash
# First-time setup (see Local Development section for full instructions)
pip install -r requirements.txt && pip install -e .

# Run server
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

## 🔗 Non-IDE Clients (LangChain, mcp-use, Custom Apps)

### Overview

Non-IDE clients use the **exact same MCP protocol** as IDE clients. The only difference is how they provide their configuration:

- **IDE clients**: Read `mcp_recipients.json` from local file system
- **Non-IDE clients**: Provide `recipients_config` as parameter to MCP tools

**No registration, no REST endpoints, no special setup** - just parameter injection!

This enables seamless integration with frameworks like **LangChain**, **mcp-use**, **custom Python scripts**, and **web applications**.

### Architecture

```
Non-IDE Client (LangChain/mcp-use)
         ↓
    Client wrapper adds recipients_config parameter
         ↓  
    Standard MCP Tools (same as IDE clients)
         ↓
    MCP IDE Bridge ←→ IDE Clients
```

### Setup - Client Wrapper Approach

Create a wrapper that automatically injects your configuration:

**LangChain Integration:**
```python
from mcp import Client

class MCPClientWrapper:
    def __init__(self, mcp_url, recipients_config):
        self.client = Client(mcp_url)
        self.recipients_config = recipients_config
        self.my_id = recipients_config.get("my_id")
    
    def get_my_identity(self):
        # Inject recipients_config parameter
        return self.client.call_tool("get_my_identity", {
            "client_id": self.my_id,
            "recipients_config": self.recipients_config
        })
    
    def send_message(self, recipient_ids, messages):
        return self.client.call_tool("send_message_without_waiting", {
            "sender_id": self.my_id,
            "recipient_ids": recipient_ids if isinstance(recipient_ids, list) else [recipient_ids],
            "messages": messages if isinstance(messages, list) else [messages]
        })
    
    def get_messages(self):
        return self.client.call_tool("get_messages", {
            "client_id": self.my_id
        })

# Usage
recipients_config = {
    "my_id": "my-langchain-app",
    "recipients": {
        "frontend_cursor": {
            "name": "Frontend Team Cursor",
            "description": "Frontend development in Cursor IDE"
        },
        "backend_vscode": {
            "name": "Backend Team VS Code", 
            "description": "Backend API development in VS Code"
        }
    },
    "server_info": {
        "host": "localhost",
        "port": 8111
    }
}

# Initialize wrapper
mcp_client = MCPClientWrapper("http://localhost:8111/mcp/", recipients_config)

# Use exactly like IDE clients
identity = mcp_client.get_my_identity()
print(identity)

response = mcp_client.send_message(["frontend_cursor"], ["Please update the user authentication flow"])
messages = mcp_client.get_messages()
```

**mcp-use Integration:**
```python
import mcp_use

# Same wrapper pattern  
wrapper = MCPClientWrapper("http://localhost:8111/mcp/", recipients_config)
wrapper.send_message(["team_cursor"], ["Task completed!"])
```

### Real-World Implementation: Proxy Pattern

For **production web applications**, the recommended approach is a **proxy/interceptor pattern** that selectively handles messaging tools:

**Next.js API Route Example (dyson_frontend implementation):**

```typescript
// app/api/mcp-proxy/route.ts
import { NextRequest } from 'next/server'

// Hardcoded configuration (no file dependencies)
const MCP_RECIPIENTS_CONFIG = {
  my_id: 'dyson_frontend',
  recipients: {
    'miles_mcp_server': { name: 'Miles Primary MCP Server', description: 'Main backend API' },
    'mcpresearchserver': { name: 'MCP Research Server', description: 'Research tools' },  
    'mcp-ide-bridge': { name: 'IDE Bridge', description: 'Cross-IDE communication' }
  },
  server_info: { host: 'localhost', port: 8111 }
}

// Only intercept these 4 messaging tools (99% of traffic passes through)
const INTERCEPTED_TOOLS = ['send_message_without_waiting', 'get_messages', 'get_my_identity', 'checkin_client']

export async function POST(request: NextRequest) {
  const { tool_name, arguments: toolArgs, server_id } = await request.json()
  
  // Only intercept messaging tools for ide-bridge
  if (server_id === 'ide-bridge' && INTERCEPTED_TOOLS.includes(tool_name)) {
    return handleMessagingTool(tool_name, toolArgs)
  }
  
  // Forward everything else unchanged
  return forwardToMcp(server_id, tool_name, toolArgs)
}

async function handleMessagingTool(toolName: string, toolArgs: any) {
  switch (toolName) {
    case 'get_my_identity':
      // Override with our config as markdown
      return Response.json(formatConfigAsMarkdown(MCP_RECIPIENTS_CONFIG))
      
    case 'send_message_without_waiting':
      // Inject sender_id and validate recipients
      return forwardToMcp('ide-bridge', toolName, {
        ...toolArgs,
        sender_id: MCP_RECIPIENTS_CONFIG.my_id
      })
      
    case 'get_messages':
      // Inject client_id
      return forwardToMcp('ide-bridge', toolName, {
        ...toolArgs,
        client_id: MCP_RECIPIENTS_CONFIG.my_id
      })
      
    case 'checkin_client':
      // Inject client identity
      return forwardToMcp('ide-bridge', toolName, {
        client_id: MCP_RECIPIENTS_CONFIG.my_id,
        name: 'Dyson Frontend App',
        capabilities: 'Web application for AI agent coordination'
      })
  }
}

function formatConfigAsMarkdown(config: any): string {
  const recipientRows = Object.entries(config.recipients).map(([id, info]: [string, any]) => 
    `| ${id} | ${info.description} | No URL |`
  ).join('\n')
  
  return `# 🆔 MCP Client Identity & Recipients
## Your Client ID: \`${config.my_id}\`
## Available Recipients
| Client ID | Description | URL |
|-----------|-------------|-----|
${recipientRows}
## Usage: Use your client ID in messaging tools...`
}
```

**Setup Steps for Non-IDE Clients:**

1. **Create MCP proxy endpoint** (`/api/mcp-proxy` or equivalent)
2. **Hardcode your recipient configuration** (no `mcp_recipients.json` files needed)
3. **Intercept only messaging tools:** `send_message_without_waiting`, `get_messages`, `get_my_identity`, `checkin_client`
4. **Inject required parameters** where missing (sender_id, client_id, etc.)
5. **Override `get_my_identity`** to return your config as markdown
6. **Forward everything else unchanged** (conservative approach)

**Framework Examples:**

```python
# Express.js
app.post('/mcp-proxy', (req, res) => {
  const { tool_name, server_id } = req.body
  if (server_id === 'ide-bridge' && MESSAGING_TOOLS.includes(tool_name)) {
    return handleMessaging(tool_name, req.body.arguments)
  }
  return forwardToMcp(server_id, tool_name, req.body.arguments)
})

# Django
def mcp_proxy(request):
    data = json.loads(request.body)
    if data['server_id'] == 'ide-bridge' and data['tool_name'] in MESSAGING_TOOLS:
        return handle_messaging(data['tool_name'], data['arguments'])
    return forward_to_mcp(data['server_id'], data['tool_name'], data['arguments'])

# Flask
@app.route('/mcp-proxy', methods=['POST'])
def mcp_proxy():
    data = request.json
    if data['server_id'] == 'ide-bridge' and data['tool_name'] in MESSAGING_TOOLS:
        return handle_messaging(data['tool_name'], data['arguments'])
    return forward_to_mcp(data['server_id'], data['tool_name'], data['arguments'])
```

### Benefits

- **🔗 Simple Integration**: Same protocol as IDE clients  
- **📡 No Special Setup**: Just parameter injection
- **🚀 Client-Side Control**: Proxy manages configuration
- **🛠️ Framework Agnostic**: Works with any MCP client library
- **🏗️ Conservative Approach**: Only intercepts what's needed (99% traffic unchanged)
- **💾 No File Dependencies**: Runtime configuration, no mcp_recipients.json required
- **🔧 Production Ready**: Real-world pattern used by active projects

## 📋 Available Tools

### Core Messaging Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| `checkin_client` | Register your presence | Announce availability |
| `send_message_without_waiting` | Fire & forget messaging | **ONLY** messaging method |
| `get_messages` | **📬 ESSENTIAL** - Check for replies | **Required** after messaging |
| `get_my_identity` | Get configuration help | Setup assistance |
| `get_active_sessions` | View active connections | Monitor team activity |

### 🚀 Messaging Workflow

**MESSAGING PATTERN**: Fire-and-forget + get_messages for efficient communication:

**1. Send Messages (Fire & Forget):**
```bash
# Send to one or more recipients - INSTANT return, no blocking!
send_message_without_waiting(
  sender_id="alice_cursor",
  recipient_ids=["bob_vscode", "charlie_windsurf", "diana_jetbrains"],  
  messages=["Meeting in 5 minutes! Please confirm attendance."]
)
```

**2. Check for Replies:**
```bash
# Get replies from recipients
get_messages("alice_cursor")
# Returns responses from bob_vscode, charlie_windsurf, diana_jetbrains
```

**Message Patterns:**
```bash
# Different messages to different recipients
send_message_without_waiting(
  sender_id="alice_cursor", 
  recipient_ids=["bob_vscode", "charlie_windsurf"],
  messages=["Review auth module please", "Check UI components for responsiveness"]
)

# Single recipient
send_message_without_waiting(
  sender_id="alice_cursor",
  recipient_ids=["bob_vscode"],
  messages=["Quick question about the API endpoint"]
)

# Then check for replies
get_messages("alice_cursor")
```

**Benefits:**
- ✅ **No Blocking**: Instant return, no waits
- ✅ **Scalable**: Works for one or more recipients efficiently  
- ✅ **Fast**: No timeouts or blocking calls
- ✅ **Better UX**: Smooth, responsive messaging experience

### Example Workflows

**Team Collaboration**
```bash
# Developer A checks in
checkin_client("alice_cursor", "Alice", "Working on auth module")

# Developer A messages recipients
send_message_without_waiting("alice_cursor", 
  ["bob_vscode", "charlie_windsurf", "diana_jetbrains"],
  ["Need code review on auth module - who's available?"])

# Developer A checks for replies
get_messages("alice_cursor")
# Returns: "I can help! - bob_vscode", "Busy until 3pm - charlie_windsurf"
```

**AI Agent Coordination**
```bash
# AI Agent 1 announces completion
send_message_without_waiting("ai_agent_1", 
  ["ai_agent_2", "ai_agent_3", "human_reviewer"],
  ["Code review complete - ready for next phase"])

# Check for coordination responses
get_messages("ai_agent_1")
# Returns responses from recipients
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

### MCP Test Harness (Recommended)

**NEW!** We've included a comprehensive MCP test harness (`test_mcp_client.py`) that makes testing all MCP tools easy and reliable:

```bash
# Test identity and configuration
python test_mcp_client.py get_my_identity

# Check in as a client
python test_mcp_client.py checkin_client --client_id "test-client" --name "Test Client" --capabilities "Testing tools"

# Send fire-and-forget messages
python test_mcp_client.py send_message_without_waiting \
  --sender_id "test-client" \
  --args '{"recipient_ids": ["target-client"], "messages": ["Hello from test harness!"]}'

# NEW! Broadcast messages (fire & forget)
# Same message to multiple recipients
python test_mcp_client.py send_message_without_waiting \
  --sender_id "test-client" \
  --args '{"recipient_ids": ["alice", "bob", "charlie"], "messages": ["Team meeting in 5 minutes!"]}'

# Different messages to different recipients  
python test_mcp_client.py send_message_without_waiting \
  --sender_id "test-client" \
  --args '{"recipient_ids": ["alice", "bob"], "messages": ["Review the auth code", "Check the UI components"]}'

# Get pending messages
python test_mcp_client.py get_messages --client_id "test-client"

# Check server status
python test_mcp_client.py get_active_sessions

# Use custom JSON arguments
python test_mcp_client.py checkin_client --args '{"client_id": "custom", "name": "Custom Client"}'
```

**Features:**
- ✅ **Proper MCP Headers**: Handles `text/event-stream` and streaming responses correctly
- ✅ **Beautiful Output**: Clean markdown display with raw JSON debugging
- ✅ **All Tools Supported**: Test every MCP tool with proper argument handling
- ✅ **Flexible Arguments**: Use individual flags or JSON for complex parameters
- ✅ **Error Handling**: Clear error messages and troubleshooting info

**Installation:**
```bash
# Install required dependency
pip install requests

# Run any test
python test_mcp_client.py <tool_name> [arguments]
```

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
pip install -r requirements.txt
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

test_mcp_client.py     # MCP test harness for command-line testing
mcp_recipients.json    # Example configuration (each project gets ONE file)
requirements.txt       # Python dependencies
Dockerfile            # Container support
```

**Note**: Each project gets ONE `mcp_recipients.json` file with its own unique ID and recipient list. The example filenames in `multi-project-setup/` are just for reference - your actual file must be named `mcp_recipients.json` in each project root.

### Local Development

```bash
# Clone and setup
git clone https://github.com/your-username/mcp-ide-bridge.git
cd mcp-ide-bridge

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in editable mode (REQUIRED for Python to find mcp_messaging module)
pip install -e .

# Run server
python -m mcp_messaging.server --port 8111
```

**⚠️ Important:** The `pip install -e .` step is **required** for Python to properly find the `mcp_messaging` module. Without this, you'll get `ModuleNotFoundError: No module named 'mcp_messaging'`.

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

## Contributing via Pull Requests

We welcome contributions! To submit changes:

1. Fork this repository and clone your fork.
2. Create a new feature branch from your fork's main branch:
   ```sh
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit them to your feature branch.
4. Push your branch to your fork:
   ```sh
   git push --set-upstream origin feature/your-feature-name
   ```
5. Open a pull request from your fork/branch to the `main` branch of the upstream repository (Mvp2o-ai/mcp-ide-bridge).
6. Wait for review and feedback from the maintainers.

See `CONTRIBUTING.md` for more details.