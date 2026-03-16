## Roots

1. **Defining Roots**: In [main.py](./main.py) accepts an argument which passes the root (file path) and passes it to `MCPClient`.
2. **Creating Root Objects**: According to MCP specifications, all roots should have an URI that begins with `file://`. So, create a function that converts these paths into `Root` objects using `create_roots` function in the [mcp_client.py](./mcp_client.py).
3. **Roots Callback**: The client doesn't immediately provide the list of roots to the server. Instead, the server can request the client at any point in future. So, have callback function in [mcp_client.py](./mcp_client.py) that executes when the server requests for it, and return the list of roots inside `ListRootsResult` object, and pass this callback into `ClientSession`.
4. **Using the Roots**: The [mcp_server.py](./mcp_server.py) will use the roots in two cases:
    - *Case-1*: When the tool attempts to access a file/folder.
    - *Case-2*: When LLM needs to resolve a file/folder to a full path by itself. When user gives only the name of the file, the LLM needs to figure out where to look for it.
5. **Accessing the Roots**: Roots can be accessed by [mcp_server.py](./mcp_server.py) by calling `ctx.session.list_roots()`. This triggers the root-listing callback in the client.
4. **Authorizing access**: Consider implementing a function like `is_path_allowed` [mcp_server.py](./mcp_server.py) in to decide which path will be accessible based on the list of roots.
