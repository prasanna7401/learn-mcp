from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import LoggingMessageNotificationParams

server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)

### STEP - 3.1:
# Define a callback function to handle logging messages from the server. The `params` argument will
# contain the data sent by the server using `ctx.info()`.
async def logging_callback(params: LoggingMessageNotificationParams):
    print(params.data)

### STEP - 3.2:
# Define a callback function to handle progress updates from the server.
# The `progress` and `total` arguments will contain the values sent by the server using `ctx.report_progress()`.
# The `message` argument will contain any informational message sent by the server using `ctx.info()` in the same step as the progress update.
async def print_progress_callback(
    progress: float, total: float | None, message: str | None
):
    if total is not None:
        percentage = (progress / total) * 100
        print(f"Progress: {progress}/{total} ({percentage:.1f}%)")
    else:
        print(f"Progress: {progress}")

### STEP - 4.1:
# In the `ClientSession` constructor, pass the `logging_callback` function as the `logging_callback` argument.
# This will ensure that any messages sent by the server using `ctx.info()` are handled by the `logging_callback` function.
async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, logging_callback=logging_callback
        ) as session:
            await session.initialize()

            ### STEP - 4.2:
            # When calling the tool, pass the `print_progress_callback` function as the `progress_callback` argument.
            # This will ensure that any progress updates sent by the server using `ctx.report_progress()` are handled by the `print_progress_callback` function.

            await session.call_tool(
                name="add",
                arguments={"a": 1, "b": 3},
                progress_callback=print_progress_callback,
            )


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
