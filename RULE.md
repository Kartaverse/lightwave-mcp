If LightWave is referenced in a question assume I want you to use the MCP lightwave-mcp server.

When connecting to the lightwave-mcp server to start a new LightWave session check if the user asked for LightWave Modeler or LightWave Layout. If Modeler is requested use the tool "connect_modeler_auto". If Layout is requested use the tool "connect_layout_auto".

If you want to find the available commands that can be used in Layout use the tool "list_layout_commands". If you want to find the available commands that can be used in Modeler use the tool "list_modeler_commands".

Use the "send_modeler_command" tool to understand how to send commands to Modeler. Use the "send_layout_command" tool to understand how to send commands to Layout.

If you want to scan for active instances of LightWave on the current host system, or the local network use the tool "discover_lightwave".

If you want to close the active MCP lightwave-mcp server session connection to the LightWave instance use the tool "close-connection".

If the user has installed a new LightWave version, or upgraded their Lightwave version the tool "referesh_command_cache" is used to rebuild the internal list of available commands provided by LightWave.
