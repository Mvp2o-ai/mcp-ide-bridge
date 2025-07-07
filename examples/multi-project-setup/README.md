# Multi-Project MCP IDE Bridge Setup

This guide shows how to set up MCP IDE Bridge across multiple projects to enable **IDE-to-IDE communication** for seamless collaboration between different development environments.

**Important**: Each project gets ONE `mcp_recipients.json` file with its own unique ID and recipient list. The example filenames below are just for reference - your actual file must be named `mcp_recipients.json` in each project root.

## 🏗️ Multi-Project IDE Communication

```
mybackendapi_cursor     ←→  MCP IDE Bridge  ←→  myfrontendweb_vscode
      ↑                        ↑                        ↑
  Cursor IDE               Message Relay           VS Code IDE
  Backend Project                                    Frontend Project
  mcp_recipients.json                              mcp_recipients.json

projectspecs_claudedesktop  ←→  MCP IDE Bridge  ←→  myragproject_windsurf
      ↑                           ↑                        ↑
  Claude Desktop              Message Relay           Windsurf IDE
  Project Specs                                        RAG Project
  mcp_recipients.json                              mcp_recipients.json

mydevops_jetbrains  ←→  MCP IDE Bridge  ←→  All Project IDEs
      ↑                    ↑
  JetBrains IDE         Message Relay
  DevOps Project
  mcp_recipients.json
```

## 📁 Project Examples

**Note**: Each project below gets its own `mcp_recipients.json` file. The filenames shown are just for reference - your actual file must be named `mcp_recipients.json` in each project root.

### Project: mybackendapi_cursor
**IDE**: Cursor IDE working on a Node.js/Express backend API

```json
{
  "my_id": "mybackendapi_cursor",
  "recipients": {
    "myfrontendweb_vscode": {
      "name": "Frontend Web App",
      "description": "React frontend project in VS Code"
    },
    "projectspecs_claudedesktop": {
      "name": "Project Specifications", 
      "description": "Project docs and specs in Claude Desktop"
    },
    "myragproject_windsurf": {
      "name": "RAG Project",
      "description": "RAG implementation project in Windsurf"
    },
    "mydevops_jetbrains": {
      "name": "DevOps Project",
      "description": "Infrastructure project in JetBrains"
    },
    "myaiagent_cursor": {
      "name": "AI Agent Project",
      "description": "AI agent development in another Cursor instance"
    }
  },
  "server_info": {
    "url": "http://localhost:8111/mcp/",
    "transport": "http_streamable"
  }
}
```

### Project: myfrontendweb_vscode
**IDE**: VS Code working on a React frontend web application

```json
{
  "my_id": "myfrontendweb_vscode",
  "recipients": {
    "mybackendapi_cursor": {
      "name": "Backend API",
      "description": "Node.js/Express backend in Cursor"
    },
    "projectspecs_claudedesktop": {
      "name": "Project Specifications",
      "description": "Project docs and specs in Claude Desktop"
    },
    "myragproject_windsurf": {
      "name": "RAG Project",
      "description": "RAG implementation project in Windsurf"
    },
    "mydevops_jetbrains": {
      "name": "DevOps Project",
      "description": "Infrastructure project in JetBrains"
    },
    "myaiagent_cursor": {
      "name": "AI Agent Project",
      "description": "AI agent development in Cursor"
    }
  },
  "server_info": {
    "url": "http://localhost:8111/mcp/",
    "transport": "http_streamable"
  }
}
```

### Project: projectspecs_claudedesktop
**IDE**: Claude Desktop working on project specifications and documentation

```json
{
  "my_id": "projectspecs_claudedesktop",
  "recipients": {
    "mybackendapi_cursor": {
      "name": "Backend API",
      "description": "Node.js/Express backend in Cursor"
    },
    "myfrontendweb_vscode": {
      "name": "Frontend Web App",
      "description": "React frontend project in VS Code"
    },
    "myragproject_windsurf": {
      "name": "RAG Project",
      "description": "RAG implementation project in Windsurf"
    },
    "mydevops_jetbrains": {
      "name": "DevOps Project",
      "description": "Infrastructure project in JetBrains"
    },
    "myaiagent_cursor": {
      "name": "AI Agent Project",
      "description": "AI agent development in Cursor"
    }
  },
  "server_info": {
    "url": "http://localhost:8111/mcp/",
    "transport": "http_streamable"
  }
}
```

### Project: myragproject_windsurf
**IDE**: Windsurf working on a RAG (Retrieval-Augmented Generation) project

```json
{
  "my_id": "myragproject_windsurf",
  "recipients": {
    "mybackendapi_cursor": {
      "name": "Backend API",
      "description": "Node.js/Express backend in Cursor"
    },
    "myfrontendweb_vscode": {
      "name": "Frontend Web App",
      "description": "React frontend project in VS Code"
    },
    "projectspecs_claudedesktop": {
      "name": "Project Specifications",
      "description": "Project docs and specs in Claude Desktop"
    },
    "mydevops_jetbrains": {
      "name": "DevOps Project",
      "description": "Infrastructure project in JetBrains"
    },
    "myaiagent_cursor": {
      "name": "AI Agent Project",
      "description": "AI agent development in Cursor"
    }
  },
  "server_info": {
    "url": "http://localhost:8111/mcp/",
    "transport": "http_streamable"
  }
}
```

### Project: mydevops_jetbrains
**IDE**: JetBrains IDE working on DevOps and infrastructure

```json
{
  "my_id": "mydevops_jetbrains",
  "recipients": {
    "mybackendapi_cursor": {
      "name": "Backend API",
      "description": "Node.js/Express backend in Cursor"
    },
    "myfrontendweb_vscode": {
      "name": "Frontend Web App",
      "description": "React frontend project in VS Code"
    },
    "projectspecs_claudedesktop": {
      "name": "Project Specifications",
      "description": "Project docs and specs in Claude Desktop"
    },
    "myragproject_windsurf": {
      "name": "RAG Project",
      "description": "RAG implementation project in Windsurf"
    },
    "myaiagent_cursor": {
      "name": "AI Agent Project",
      "description": "AI agent development in Cursor"
    }
  },
  "server_info": {
    "url": "http://localhost:8111/mcp/",
    "transport": "http_streamable"
  }
}
```

## 🎯 IDE Setup Instructions

**Each project gets ONE `mcp_recipients.json` file with its own unique ID and recipient list.**

### Cursor IDE Setup

1. **Create mcp_recipients.json** in your project root (see examples above)

2. **Configure .cursor/mcp.json**:
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

3. **Connect to Server**:
   - Open Command Palette (`Cmd/Ctrl + Shift + P`)
   - Search for "MCP: Connect to Server"
   - Enter: `http://localhost:8111/mcp/`

4. **Start Collaborating**:
   - Use MCP tools to send/receive messages
   - Coordinate with other IDEs working on different projects

### VS Code Setup

1. **Install MCP Extension**:
   - Search for "MCP" in VS Code extensions
   - Install the official MCP extension

2. **Create mcp_recipients.json** in your project root

3. **Configure MCP Settings**:
   - Open VS Code settings
   - Search for "MCP"
   - Add server configuration

4. **Connect and Collaborate**:
   - Use MCP commands to interact with other IDEs

### Claude Desktop Setup

1. **Create mcp_recipients.json** in your project root

2. **Configure Claude Desktop MCP**:
   - Open Claude Desktop settings
   - Navigate to MCP configuration
   - Add server URL: `http://localhost:8111/mcp/`

3. **Start Messaging**:
   - Use Claude's MCP integration to communicate with other IDEs

### Windsurf Setup

1. **Create mcp_recipients.json** in your project root

2. **Configure Windsurf MCP**:
   - Open Windsurf settings
   - Navigate to MCP configuration
   - Add server URL: `http://localhost:8111/mcp/`

3. **Start Messaging**:
   - Use Windsurf's MCP integration to communicate

### JetBrains IDEs Setup

1. **Install MCP Plugin**:
   - Go to Settings → Plugins
   - Search for "MCP" and install

2. **Create mcp_recipients.json** in your project root

3. **Configure MCP Server**:
   - Open MCP plugin settings
   - Add server: `http://localhost:8111/mcp/`

4. **Begin Collaboration**:
   - Use MCP tools from the IDE

## 🤖 AI Agent Generation

Your IDE's AI agent can help generate `mcp_recipients.json` files! Simply ask:

**In Cursor:**
```
"Generate an mcp_recipients.json file for my backend API project. I need to communicate with frontend, RAG, DevOps, and AI agent projects."
```

**In VS Code:**
```
"Create an mcp_recipients.json configuration for my frontend web app. Include recipients for backend, RAG, DevOps, and AI agent projects."
```

**In Claude Desktop:**
```
"Help me set up mcp_recipients.json for project specifications. I need to coordinate with backend, frontend, RAG, and DevOps projects."
```

**Important**: Place `mcp_recipients.json` in the **project root** for easy discovery by IDE agents and MCP tools. **Each project gets ONE file with its own unique ID and recipient list.**

## 🔄 Cross-Project Communication Examples

### Backend API → Frontend Web App
```bash
# Backend developer notifies frontend about API changes
send_message_without_waiting("mybackendapi_cursor", ["myfrontendweb_vscode"], ["I've updated the user authentication endpoint. New fields: user_id, email, role"])
```

### Frontend Web App → Project Specs
```bash
# Frontend developer requests specification clarification
send_message_without_waiting("myfrontendweb_vscode", ["projectspecs_claudedesktop"], ["Need clarification on the user dashboard layout requirements"])
```

### RAG Project → Backend API
```bash
# RAG developer requests API integration
send_message_without_waiting("myragproject_windsurf", ["mybackendapi_cursor"], ["Need to integrate RAG search with your API. Can you add a /search endpoint?"])
```

### DevOps → All Projects
```bash
# DevOps announces deployment
send_message_without_waiting("mydevops_jetbrains", ["mybackendapi_cursor", "myfrontendweb_vscode", "myragproject_windsurf"], ["Production deployment scheduled for 2 PM. Please ensure your components are ready."])
```

## 🚀 Benefits of Multi-Project IDE Communication

- **Cross-Project Coordination**: Communicate between different projects seamlessly
- **IDE Flexibility**: Use your preferred IDE for each project
- **Real-time Updates**: Instant communication about changes and requirements
- **Knowledge Sharing**: Share insights across different project contexts
- **Deployment Coordination**: Synchronize releases across multiple projects

## 🔧 Troubleshooting

**Common Issues:**
- **Connection Failed**: Ensure MCP IDE Bridge server is running on port 8111
- **No Recipients Found**: Check that all IDEs have registered with `checkin_client`
- **Messages Not Delivered**: Verify recipient IDs match exactly in all configurations

**Debug Commands:**
```bash
# Check server status
curl -X GET http://localhost:8111/api/sessions

# Test connection
python test_connection.py --mcp-localhost-port 8111

# List active sessions
get_active_sessions()
``` 