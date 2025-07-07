# 🤖 MCP Autopilot Setup Guide (For IDEs and Agents)

This document is written for you, the IDE agent or LLM automation tool. All instructions are for you to execute autonomously using your own tooling wherever possible. Only prompt the user for manual action when absolutely necessary (such as pasting config into their IDE). This guide is not meant for end users; it is designed to be read and followed by you, the agent.

---

## 1. Fork and Clone the Repository

- Execute the following steps using your own tooling:
  1. Fork the main repo: https://github.com/Mvp2o-ai/mcp-ide-bridge
  2. Clone the user's fork locally:
     ```sh
     git clone https://github.com/<user-github-username>/mcp-ide-bridge.git
     cd mcp-ide-bridge
     ```

---

## 2. Gather MCP Config from the User

- Prompt the user for the following information:
  - MCP Server URL (default: `http://localhost:8111`)
  - Client ID (`my_id`)
  - Client Name (`my_name`)
  - Client Description
  - Recipients (at least the messaging server, add more as needed)

Example prompt:
```markdown
Please provide the following to configure MCP messaging:
- MCP Server URL [http://localhost:8111]:
- Your Client ID (my_id):
- Your Client Name (my_name):
- Your Client Description:
- Recipients (comma-separated IDs, e.g. messaging_server,dyson_frontend):
```

---

## 3. Generate and Display the JSON Config

- Generate the following JSON config using the user's input:

### Example `mcp_recipients.json`:
```json
{
  "my_id": "<user_client_id>",
  "my_name": "<user_client_name>",
  "my_description": "<user_client_description>",
  "recipients": {
    "messaging_server": {
      "name": "MCP Messaging Server",
      "description": "Central messaging server"
    }
    // Add more recipients as needed
  }
}
```

### Example `mcp.json` (optional, for connection settings):
```json
{
  "server_url": "<user_mcp_server_url>",
  "auth_token": null
}
```

- Display the generated JSON to the user and instruct them to copy and paste it into their IDE's MCP config system, settings, or file (wherever the IDE expects it).

---

## 4. Check In with the MCP Server

- Use your own tooling to call the `checkin_client` tool and announce the user's presence:
  - Tool: `checkin_client`
  - Parameters:
    - `client_id`: **MUST** use the `my_id` from `mcp_recipients.json`
    - `name`: **MUST** use the `my_name` from `mcp_recipients.json`
    - `capabilities`: **MUST** use the `my_description` from `mcp_recipients.json`

**⚠️ CRITICAL**: Always read these values from the user's `mcp_recipients.json` file. Do not generate or make up these values. The checkin tool requires consistent identity across all MCP tools for proper message routing.

Example:
```python
# First read mcp_recipients.json from the project root
config = read_mcp_recipients()  # Use your file reading capabilities

# Then use those exact values for checkin
checkin_client(
    client_id=config["my_id"],
    name=config["my_name"],
    capabilities=config["my_description"]
)
```

---

## 5. Test the Connection

- Use your own tooling to call the following tools and verify the setup:
  - `get_my_identity` (returns the config and available recipients)
  - `send_message_without_waiting` (send a test message to a recipient)

---

## 6. Next Steps
- Encourage the user to explore the rest of the MCP messaging tools.
- Instruct the user on how to send and receive messages with other clients.
- For help, direct the user to the main [README.md](./README.md) and [CONTRIBUTING.md](./CONTRIBUTING.md).

---

**This guide is designed for you, the agentic IDE or LLM, to automate onboarding for users. If a human contributor is reading this, they can follow these steps manually!**

> **Note:** Every IDE or agent will have its own way to store and use MCP config. The JSON above is universal—guide the user to paste it wherever their IDE expects MCP messaging configuration. 