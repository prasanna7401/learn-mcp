## Sampling Process

1. **Initiate Sampling**: On the [server](./server.py), during a tool call, run the `create_message()` method, passing in some messages that you wish to send to a language model.
2. **Sampling Callbacks**: On the [client](./client.py), you must implement a sampling callback. It will receive a list of messages provided by the server.
3. **Message Format**: The list of messages provided by the server are formatted for communication in MCP. They need to be converted into a format acceptable by the LLM SDK you are using.
4. **Returning generated text**: After generating text with the LLM, you'll return a `CreateMessageResult`, which contains the generated text.
5. **Connecting the callback**: The callback on the client needs to be passed into the ClientSession call.
6. **Getting result**: After the client has generated and returned some text, it will be sent to the server. You can do anything with this text: Use it as part of a workflow in your tool, Decide to make another sampling call, Return the generated text, etc.

