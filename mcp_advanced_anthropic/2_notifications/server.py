from mcp.server.fastmcp import FastMCP, Context
import asyncio

mcp = FastMCP(name="Demo Server")


@mcp.tool()
### STEP - 1:
# The tool functions reveive an additional argument `ctx` of type `Context`.
# This object allows you to send notifications and progress updates back to the client.
async def add(a: int, b: int, ctx: Context) -> int:

    ### STEP - 2:
    # Use `ctx.info()` to send informational messages to the client.
    # Use `ctx.report_progress()` to send progress updates. The first argument is the current progress, and the second argument is the total.
    await ctx.info("Preparing to add...")
    await ctx.report_progress(20, 100)

    await asyncio.sleep(2)

    await ctx.info("OK, adding...")
    await ctx.report_progress(80, 100)

    return a + b


if __name__ == "__main__":
    mcp.run(transport="stdio")
