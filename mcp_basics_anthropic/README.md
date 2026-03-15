# MCP Basics — Anthropic Academy

A hands-on project built while completing the [Introduction to MCP](https://anthropic.skilljar.com/introduction-to-model-context-protocol) course on Anthropic Academy. It demonstrates the three core MCP primitives using a document management use case.

## What is MCP?

Model Context Protocol (MCP) is a standard for connecting AI models to external tools and data. An MCP server exposes **primitives** that a client (and the AI) can interact with.

## The Three MCP Primitives

### `@mcp.tool` — Things Claude can *do*
- **Model-controlled**: Claude decides when to call them.
- Use when you want to give Claude new capabilities (read, edit, search, etc.).
- Example in this project: `read_doc_contents`, `edit_doc_contents`

### `@mcp.resource` — Data to *feed* into the AI
- **App-controlled**: your code decides when to fetch them.
- Requires a `uri=resource://<path>` — supports both direct and templated URIs.
- Use when you want to pull data into the app/AI for context (e.g., via `@filename` mentions).
- Can return strings, JSON, binary, etc.
- Example in this project:
  - `docs://documents` → lists all document IDs (direct URI)
  - `docs://documents/{doc_id}` → returns contents of a specific doc (templated URI)

### `@mcp.prompt` — Reusable prompt templates
- **User-controlled**: surfaces as `/command` suggestions (like `/compact`, `/skills`).
- Use to create predefined workflows that users can trigger.
- Example in this project: `format` (reformat a doc as Markdown), `summarize_doc`

## Project Structure

```
mcp_basics_anthropic/
├── mcp_server.py     # MCP server — defines tools, resources, and prompts
├── mcp_client.py     # MCP client — wraps the MCP SDK session
├── main.py           # Entry point — wires client, Claude, and CLI together
├── core/
│   ├── claude.py     # Anthropic API wrapper
│   ├── cli_chat.py   # Chat logic (tool calls, resource fetching, prompts)
│   ├── cli.py        # CLI app (input loop, Tab autocomplete)
│   ├── chat.py       # Base chat abstractions
│   └── tools.py      # Tool formatting helpers
└── .env              # API key and model config (not committed)
```

## Setup & Running

See [SETUP.md](SETUP.md) for full setup instructions (environment variables, `uv` vs plain Python, dependencies).

Quick start with `uv`:

```bash
uv run main.py
```

## Inspecting the MCP Server

Use the MCP Inspector to explore and test the server's tools, resources, and prompts interactively:

```bash
mcp dev mcp_server.py
```

## Usage

| Action | Example |
|---|---|
| Chat normally | `Tell me about the project plan` |
| Fetch a document as context | `@deposition.md what does Angela Smith say?` |
| Run a prompt command | `/summarize_doc plan.md` |
| Tab | Autocompletes available `/` commands |


# Reference:

- [Introduction to MCP](https://anthropic.skilljar.com/introduction-to-model-context-protocol)