# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Educational repository for learning the Model Context Protocol (MCP) with Anthropic's Python SDK. Organized into two main sections:

- **`mcp_basics_anthropic/`** — MCP fundamentals: tools, resources, and prompts
- **`mcp_advanced_anthropic/`** — Advanced features: sampling, notifications, roots, and transport

## Package Manager & Environment

This repo uses **`uv`** for dependency management. Each module has its own `pyproject.toml` and `uv.lock`.

```bash
# Install dependencies for a module
cd mcp_basics_anthropic
uv sync

# Run a script within a module
uv run python main.py

# Run a server directly
uv run python mcp_server.py

# Run with MCP dev inspector
uv run mcp dev mcp_server.py
```

## Environment Setup

Each module requiring an API key expects a `.env` file (see `.env.example` where present):

```
ANTHROPIC_API_KEY=""
CLAUDE_MODEL="claude-sonnet-4-0"
```

## Running the Modules

Each module has a `main.py` entry point that launches an interactive CLI:

```bash
# Basics module
cd mcp_basics_anthropic && uv run python main.py

# Advanced: sampling
cd mcp_advanced_anthropic/core/1_sampling && uv run python client.py

# Advanced: notifications
cd mcp_advanced_anthropic/core/2_notifications && uv run python client.py

# Advanced: roots (pass directory path as argument)
cd mcp_advanced_anthropic/core/3_roots && uv run python main.py /path/to/directory

# Transport: HTTP mode
cd mcp_advanced_anthropic/transport && uv run python main.py
```

On Windows, `asyncio.WindowsProactorEventLoopPolicy` is set automatically in `main.py`.

## Architecture

### MCP Server Pattern (`mcp_server.py`)

Uses `FastMCP` decorator-based API:

- `@mcp.tool` — Model-controlled actions (Claude decides when to call)
- `@mcp.resource("uri://template/{param}")` — App-controlled data (direct and templated URIs)
- `@mcp.prompt` — User-controlled reusable templates

Servers run via `mcp.run(transport="stdio")` or `transport="streamable-http"`.

### MCP Client Pattern (`mcp_client.py`)

`MCPClient` is a custom async wrapper around MCP's `ClientSession`. It manages:
- Subprocess lifecycle for STDIO transport
- Callbacks: `sampling_callback`, `logging_callback`, `list_roots_callback`
- Supports async context manager (`async with MCPClient(...) as client`)

Key methods: `connect()`, `list_tools()`, `call_tool()`, `list_prompts()`, `get_prompt()`, `read_resource()`, `cleanup()`

### Core Utilities (`core/`)

Shared across modules:

- `claude.py` — Thin `Anthropic` SDK wrapper (`Claude` class with `.chat()`)
- `tools.py` — `ToolManager`: aggregates tools from multiple `MCPClient` instances and routes `call_tool` to the correct client
- `cli_chat.py` — `CliChat`: agentic loop (Claude ↔ tool execution)
- `cli.py` — `CliApp`: `prompt-toolkit`-based interactive terminal UI
- `chat.py` — Message history management

### Advanced Feature Patterns

**Sampling** — Server delegates LLM calls back to the client (no API keys needed on server):
```python
ClientSession(read, write, sampling_callback=my_sampling_fn)
```

**Notifications** — Server emits progress/logs via `Context`:
```python
async def my_tool(arg: str, ctx: Context):
    await ctx.info("Starting...")
    await ctx.report_progress(1, 10)
```

**Roots** — Client grants server access to specific filesystem paths:
```python
# Client converts paths → Root(uri=FileUrl("file://..."))
# Server calls: ctx.session.list_roots()
```

**Transport** — `mcp_advanced_anthropic/transport/` demonstrates StreamableHTTP with stateless mode vs STDIO.

### Multi-Client Architecture

`main.py` can connect to multiple `MCPClient` instances simultaneously. `ToolManager.get_all_tools()` aggregates all tools, and `execute_tool_requests()` routes each tool call to the correct client.
