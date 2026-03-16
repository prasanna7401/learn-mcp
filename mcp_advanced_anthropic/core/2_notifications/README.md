## Logging & Progress Notifications

1. **Tool receives context arguments**: The tool functions receive `Context` as an additional argument. This object allows the server to send the logging & progress updates to the client
2. **Create logs & progress with context**: Through the tool function, from the server, call the `info()`, `warning()`, `debug()`, `error()` methods to log different type of messages, and also `report_progress()` to estimate remaining amount of work to the client.
3. **Define callbacks on client**: The client will have a logging & progress callback functions which will be called whenever the server emits a log or progress updates. These callbacks should try to display the logging & progress data to the user in a desired manner.
4. **Pass callbacks to appropriate functions**: Pass the `logging_callback` to the `ClientSession` and the `progress_callback` to the `call_tool()` function.
   
> [!NOTE]
> - Logs can be sent anytime the server wants to send (even after a particular tool call session is over) and can also be associated with the entire session.
> - But progress is associated with a particular tool invocation status, not the entire session.