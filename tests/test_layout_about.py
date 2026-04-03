#!/usr/bin/env python3
"""
Test script to connect to LightWave Layout and show the About dialog.
"""
import sys
import os
import json
import importlib.util

# Paths from mcp.json configuration (relative paths for portability)
LIGHTWAVE_MCP_SERVER_PATH = "src/lightwave_mcp/server.py"
LIGHTWAVE_LWCOMMANDPORT_PATH = "src"

sys.path.insert(0, LIGHTWAVE_LWCOMMANDPORT_PATH)
sys.path.insert(0, os.path.dirname(LIGHTWAVE_MCP_SERVER_PATH))

# Import the MCP server module
spec = importlib.util.spec_from_file_location(
    "lightwave_mcp_server",
    LIGHTWAVE_MCP_SERVER_PATH
)
lightwave_mcp_server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lightwave_mcp_server)

def main():
    print("=" * 60)
    print("LightWave MCP - Layout About Test")
    print("=" * 60)

    # Discover instances
    print("\n1. Discovering LightWave instances...")
    discovery = lightwave_mcp_server.discover_lightwave_instances()

    if not discovery.get('success'):
        print(f"   Discovery failed: {discovery.get('error')}")
        return 1

    instances = discovery.get('instances', [])
    print(f"   Found {len(instances)} instance(s)")

    if not instances:
        print("   No instances found. Is LightWave running with Command Port enabled?")
        return 1

    # Show all discovered instances
    for i, inst in enumerate(instances):
        print(f"   [{i}] {inst.get('type', '?').capitalize()} at {inst.get('address')}:{inst.get('port')} (v{inst.get('version', '?')})")

    # Find Layout instance
    layout_inst = None
    for inst in instances:
        if inst.get('type', '').lower() == 'layout':
            layout_inst = inst
            break

    if layout_inst is None:
        print("\n   No Layout instance found.")
        print("   Available instances:")
        for inst in instances:
            print(f"   - {inst.get('type', '?').capitalize()} at {inst.get('address')}:{inst.get('port')}")
        return 1

    print(f"\n2. Connecting to Layout at {layout_inst.get('address')}:{layout_inst.get('port')}...")

    connect_result = lightwave_mcp_server.connect_to_layout(
        layout_inst['address'],
        layout_inst['port']
    )

    if not connect_result.get('success'):
        print(f"   Connection failed: {connect_result.get('error')}")
        return 1

    connection_id = connect_result.get('connection_id')
    print(f"   Connected! Connection ID: {connection_id}")

    # Send About command
    print("\n3. Sending 'About' command to Layout...")
    result = lightwave_mcp_server.send_layout_command(
        connection_id,
        "About",
        []
    )

    print(f"\n   Result: {json.dumps(result, indent=4)}")

    # Validate the result
    if result.get('success'):
        print("\n   About dialog command executed successfully!")
    else:
        print(f"\n   About dialog command failed: {result.get('message')}")

    # Cleanup
    print("\n4. Closing connection...")
    close_result = lightwave_mcp_server.close_connection(connection_id)
    print(f"   {close_result}")

    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())