# Transport Methods & MCP Communication

MCP uses **JSON** to communicate between client and server. Messages are classified by who sends them.

## Message Types

| Type | Description | Example |
|------|-------------|---------|
| **Request / Result** | Always come in pairs | Tool call, List Prompts, Read Resource, Initialize |
| **Notification** | One-way, no response expected | Logging, Progress, Tool list changed, Resource updated |

> Reference: [MCP Schema](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema)

---

## Connection Handshake

Every MCP connection begins with a mandatory three-way handshake before any tool calls or other operations can occur.

```
Client                          Server
  │                               │
  │── Initialize Request ────────>│
  │<─ Initialize Response ────────│
  │── Initialized Notification ──>│
  │                               │
  │   (normal operations begin)   │
```

---

## Transport Types

### STDIO

Used when both client and server run on the **same machine**.

- Client sends to server via `stdin`; server responds via `stdout`
- Both sides can send messages at any time — true bidirectional communication
- Best for **development and testing**

```
Client ──stdin──> Server
Client <──stdout── Server
```

---

### StreamableHTTP

Used when the MCP server is **remotely hosted** at a known URL. Best for **production environments**.

The fundamental asymmetry of HTTP creates a challenge:
- ✅ Client → Server requests work naturally
- ❌ Server → Client requests are difficult (client has no known URL)

#### SSE (Server-Sent Events)

To allow server-initiated messages, StreamableHTTP establishes a **persistent SSE connection** using a `mcp-session-id` header on all messages after the Initialize handshake.

However, client-initiated requests (e.g., tool calls) can close the active SSE session when their response arrives. To prevent this, StreamableHTTP uses **two separate SSE channels**:

```
Client                              Server
  │                                   │
  │── GET /mcp (Primary SSE) ────────>│  ← stays open indefinitely
  │<═══════════════════════════════════│  (server-initiated messages)
  │                                   │
  │── POST /mcp (Tool call) ─────────>│  ← tool-specific SSE, per request
  │<─ Tool result / Logs ─────────────│  (closed after response)
  │                                   │
```

#### Dual SSE Connections

| Channel | Method | Lifetime | Purpose |
|---------|--------|----------|---------|
| **Primary SSE** | `GET` | Open indefinitely | Server-initiated requests; session-wide messages |
| **Tool-specific SSE** | `POST` | Closed after response | Per-tool-call results and logs |

> Both channels share the **same `mcp-session-id`** — it's one session with two communication channels, not two sessions.

#### Message Routing

Messages are routed based on whether they are session-wide or tied to a specific tool call:

| Message | Channel | Reason |
|---------|---------|--------|
| Progress notifications | Primary SSE | Self-correlating via `progressToken`; session-wide |
| Logging messages | Tool-specific SSE | Only meaningful in the context of a specific tool call |
| Tool results | Tool-specific SSE | Direct response to the triggering tool call |

---

## StreamableHTTP Configuration

Two key settings control how StreamableHTTP behaves:

### `stateless_http`

When `true`, disables session state management (`mcp-session-id` is not used). The default value is `false`

**Use case:** Horizontal scaling with a load balancer. With session IDs, a client may be tied to one specific server instance, making load balancing difficult.

**Trade-offs of enabling:**
- ❌ No sampling, logging, or progress notifications
- ❌ No server-initiated requests or resource subscriptions
- ✅ Simpler client — no Initialize handshake required
- ✅ Any server instance can handle any request

### `json_response`

When `true`, disables streaming for `POST` responses. A single plain JSON object is returned as the final result instead of a streaming SSE response. The default value is `false`

**Trade-offs of enabling:**
- ❌ No live progress updates or logs during tool execution
- ✅ Simpler response handling — one JSON result per tool call
