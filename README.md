# learn-mcp

A hands-on learning repository for the [Model Context Protocol (MCP)](https://modelcontextprotocol.io), built alongside the [Anthropic Academy](https://anthropic.skilljar.com) MCP courses.

## What is MCP?

Model Context Protocol (MCP) is a standard for connecting AI models to external tools and data. It defines how an AI client (like Claude) communicates with an MCP server that exposes capabilities the model can use.

MCP has three core primitives:

| Primitive | Controlled by | Purpose |
|-----------|--------------|---------|
| **Tool** | Model | Actions the AI can invoke (read, write, search, etc.) |
| **Resource** | Application | Data fetched into context (documents, records, etc.) |
| **Prompt** | User | Reusable prompt templates triggered by the user |

---

## Contents

### Basics

**`mcp_basics_anthropic/`** — Introduction to MCP primitives

Demonstrates tools, resources, and prompts using a document management scenario. A good starting point for understanding how MCP servers and clients work together.

---

### Advanced

**`mcp_advanced_anthropic/core/`** — Three advanced MCP capabilities:

| Topic | What you'll learn |
|-------|-------------------|
| **1. Sampling** | How a server can delegate LLM calls back to the client — useful for public servers that shouldn't hold API keys |
| **2. Notifications** | How servers emit real-time log messages and progress updates to the client during long-running tasks |
| **3. Roots** | How clients explicitly grant servers access to specific files or directories, for both security and convenience |

**`mcp_advanced_anthropic/transport/`** — MCP communication and transport methods

Covers how MCP messages work under the hood, the connection handshake, and the two transport types:

- **STDIO** — for local development; bidirectional communication via stdin/stdout
- **StreamableHTTP** — for remotely hosted servers; uses persistent SSE connections with session management, with options for stateless and non-streaming modes
