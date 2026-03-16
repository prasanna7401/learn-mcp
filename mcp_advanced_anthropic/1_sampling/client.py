import asyncio
from anthropic import AsyncAnthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import RequestContext
from mcp.types import (
    CreateMessageRequestParams,
    CreateMessageResult,
    TextContent,
    SamplingMessage,
)

anthropic_client = AsyncAnthropic()
model = "claude-sonnet-4-0"

server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)

### STEP - 3:
# The messages sent from the server are formatted as a list of `SamplingMessage` objects accepted by MCP.
# We need to convert them into the format expected by the Anthropic (or any LLM) SDK, 
# which is a list of dictionaries with "role" and "content" keys.
# After we get the response from Claude, we extract the text content and return it back to the server in the expected format.
async def chat(input_messages: list[SamplingMessage], max_tokens=4000):
    messages = []
    for msg in input_messages:
        if msg.role == "user" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "user", "content": content})
        elif msg.role == "assistant" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "assistant", "content": content})

    response = await anthropic_client.messages.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
    )

    text = "".join([p.text for p in response.content if p.type == "text"])
    return text

### STEP - 2: 
# On the Client side, we implement a callback function that will be called when the server sends a message. 
# In this callback, we call the `chat` function to get a response from Claude and return it back to the server.
async def sampling_callback(
    context: RequestContext, params: CreateMessageRequestParams
):
    # Call Claude using the Anthropic SDK
    text = await chat(params.messages) # convert the message to a format accepted by the Anthropic SDK and get the response

    ### STEP - 4:
    # Finally, we return the response back to the server in the expected format using the `CreateMessageResult` class.
    return CreateMessageResult(
        role="assistant",
        model=model,
        content=TextContent(type="text", text=text),
    )


async def run():
    async with stdio_client(server_params) as (read, write):
        ### STEP - 5:
        # We create a `ClientSession` and pass the `sampling_callback` function as a
        # parameter. This will allow the client to call the callback function whenever it receives a message from the server.
        async with ClientSession(
            read, write, sampling_callback=sampling_callback
        ) as session:
            await session.initialize()

            result = await session.call_tool(
                name="summarize",
                arguments={"text_to_summarize": "lots of text"},
            )
            print(result.content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
