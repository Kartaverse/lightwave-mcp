#!/usr/bin/env python
"""
LightWave Command Port MCP Server

This module implements a Model Context Protocol (MCP) server that provides
access to LightWave 3D's Command Port functionality. It allows AI assistants
like Cursor to discover, connect to, and control LightWave instances.

Usage:
    python lightwave_mcp_server.py

The server uses stdio transport for communication with the MCP client.
"""

import json
import os
import re
import socket
import sys
import threading
import uuid
from datetime import datetime

try:
    import lwcommandport as lwcp
    from lwcommandport.layout import Layout
    from lwcommandport.modeler import Modeler
    LWCPC_AVAILABLE = True
except ImportError:
    LWCPC_AVAILABLE = False
    print("Warning: lwcommandport module not available. Some features will be limited.", file=sys.stderr)


PROTOCOL_VERSION = "1.0"

ACTIVE_CONNECTIONS = {}
COMMAND_CACHE = {
    'layout': None,
    'modeler': None
}

TOOL_DEFINITIONS = []


def load_command_cache():
    """Load command caches from JSON files."""
    cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'cache')
    
    for cache_type in ['layout', 'modeler']:
        cache_path = os.path.join(cache_dir, f'{cache_type}_commands.json')
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    COMMAND_CACHE[cache_type] = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load {cache_type} command cache: {e}", file=sys.stderr)


def setup_tools():
    """Initialize tool definitions based on available tools."""
    global TOOL_DEFINITIONS
    
    tools_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools')
    
    tool_files = [
        'discover_lightwave.json',
        'connect_layout.json',
        'connect_layout_auto.json',
        'connect_modeler.json',
        'connect_modeler_auto.json',
        'send_layout_command.json',
        'send_modeler_command.json',
        'list_connections.json',
        'close_connection.json',
        'list_layout_commands.json',
        'list_modeler_commands.json',
        'refresh_command_cache.json'
    ]
    
    for tool_file in tool_files:
        tool_path = os.path.join(tools_dir, tool_file)
        if os.path.exists(tool_path):
            try:
                with open(tool_path, 'r') as f:
                    tool_def = json.load(f)
                    TOOL_DEFINITIONS.append(tool_def)
            except Exception as e:
                print(f"Warning: Failed to load tool {tool_file}: {e}", file=sys.stderr)


class LightWaveConnection:
    """Represents an active connection to a LightWave instance."""
    
    def __init__(self, connection_id, instance_type, address, port, version=None):
        self.id = connection_id
        self.type = instance_type  # 'layout' or 'modeler'
        self.address = address
        self.port = port
        self.version = version
        self.instance = None
        self.created_at = datetime.now().isoformat()
    
    def connect(self):
        """Establish connection to the LightWave instance."""
        if not LWCPC_AVAILABLE:
            return False, "lwcommandport module not available"
        
        try:
            if self.type == 'layout':
                self.instance = Layout(address=self.address, port=self.port)
            else:
                self.instance = Modeler(address=self.address, port=self.port)
            return True, f"Connected to {self.type.capitalize()} at {self.address}:{self.port}"
        except Exception as e:
            return False, str(e)
    
    def send_command(self, command, args=None):
        """Send a command to the connected LightWave instance."""
        if self.instance is None:
            return False, "Not connected"
        
        try:
            if hasattr(self.instance, command):
                method = getattr(self.instance, command)
                if args:
                    method(*args)
                else:
                    method()
                return True, f"Command '{command}' executed successfully"
            else:
                return False, f"Unknown command: {command}"
        except Exception as e:
            return False, str(e)
    
    def close(self):
        """Close the connection."""
        if self.instance:
            self.instance = None
        return True, "Connection closed"
    
    def to_dict(self):
        """Convert to dictionary representation."""
        return {
            'id': self.id,
            'type': self.type,
            'address': self.address,
            'port': self.port,
            'version': self.version,
            'created_at': self.created_at
        }


def discover_lightwave_instances():
    """
    Discover running LightWave instances using UDP broadcast.
    
    Returns:
        List of discovered instances, each with address, port, type, and version
    """
    if not LWCPC_AVAILABLE:
        return {
            'success': False,
            'error': 'lwcommandport module not available',
            'instances': []
        }
    
    instances = []
    
    try:
        locator_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        locator_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        import random
        random.seed()
        
        while True:
            port = random.randrange(1025, 65534)
            try:
                locator_socket.bind(('', port))
                break
            except:
                pass
        
        locator_socket.setblocking(False)
        
        import ctypes
        req_packet = lwcp.CommandPortReq(lwcp.CP_REQ_MAGIC, lwcp.COMMANDPORT_REQ_VERSION, port, 0)
        
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        for discover_port in range(lwcp.CP_DISCOVERY_START, lwcp.CP_DISCOVERY_END + 1):
            try:
                broadcast_socket.sendto(req_packet, ('localhost', discover_port))
            except:
                pass
        
        import select
        loop_count = 50
        
        while loop_count != 0:
            ready_read, _, _ = select.select([locator_socket], [], [], 0.1)
            loop_count -= 1
            
            if locator_socket not in ready_read:
                continue
            
            try:
                data, address = locator_socket.recvfrom(65535)
                req_info = lwcp.CommandPortInfo()
                ctypes.memmove(ctypes.addressof(req_info), data, ctypes.sizeof(req_info))
                
                if req_info.magic == lwcp.CP_INFO_MAGIC:
                    instance_type = 'Layout' if req_info.app == lwcp.CP_COMMANDSET_LAYOUT else 'Modeler'
                    
                    version = f"{req_info.major}.{req_info.minor}"
                    if req_info.version > 1:
                        version += f".{req_info.build}"
                    
                    instances.append({
                        'type': instance_type.lower(),
                        'address': address[0],
                        'port': req_info.port,
                        'version': version
                    })
            except:
                pass
        
        broadcast_socket.close()
        locator_socket.close()
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'instances': []
        }
    
    return {
        'success': True,
        'instances': instances,
        'count': len(instances)
    }


def connect_to_layout(address, port):
    """Connect to a LightWave Layout instance."""
    connection_id = str(uuid.uuid4())
    
    try:
        port_int = int(port)
    except ValueError:
        port_int = port
    
    conn = LightWaveConnection(
        connection_id=connection_id,
        instance_type='layout',
        address=address,
        port=port_int
    )
    
    success, message = conn.connect()
    
    if success:
        ACTIVE_CONNECTIONS[connection_id] = conn
        return {
            'success': True,
            'connection_id': connection_id,
            'message': message,
            'connection': conn.to_dict()
        }
    else:
        return {
            'success': False,
            'error': message
        }


def connect_to_modeler(address, port):
    """Connect to a LightWave Modeler instance."""
    connection_id = str(uuid.uuid4())
    
    try:
        port_int = int(port)
    except ValueError:
        port_int = port
    
    conn = LightWaveConnection(
        connection_id=connection_id,
        instance_type='modeler',
        address=address,
        port=port_int
    )
    
    success, message = conn.connect()
    
    if success:
        ACTIVE_CONNECTIONS[connection_id] = conn
        return {
            'success': True,
            'connection_id': connection_id,
            'message': message,
            'connection': conn.to_dict()
        }
    else:
        return {
            'success': False,
            'error': message
        }


def connect_layout_auto(address=None, port=None):
    """
    Automatically discover LightWave Layout instances and connect to one.

    If address and/or port are not provided, discovers instances first and uses
    the first discovered Layout instance. Falls back to localhost:42626 if no
    instances are found and LWCPC is available.

    Args:
        address: Optional address to connect to. If None, uses discovered or default.
        port: Optional port to connect to. If None, uses discovered or default.

    Returns:
        Connection result with connection_id on success.
    """
    discovered_layout = None

    # Discover instances if we need to find address/port
    if address is None or port is None:
        discovery = discover_lightwave_instances()
        if discovery.get('success') and discovery.get('count', 0) > 0:
            for instance in discovery.get('instances', []):
                if instance.get('type') == 'layout':
                    discovered_layout = instance
                    break

    # Determine final address and port
    final_address = address or (discovered_layout['address'] if discovered_layout else 'localhost')
    final_port = port or (discovered_layout['port'] if discovered_layout else 42626)

    return connect_to_layout(final_address, int(final_port))


def connect_modeler_auto(address=None, port=None):
    """
    Automatically discover LightWave Modeler instances and connect to one.

    If address and/or port are not provided, discovers instances first and uses
    the first discovered Modeler instance. Falls back to localhost:42627 if no
    instances are found and LWCPC is available.

    Args:
        address: Optional address to connect to. If None, uses discovered or default.
        port: Optional port to connect to. If None, uses discovered or default.

    Returns:
        Connection result with connection_id on success.
    """
    discovered_modeler = None

    # Discover instances if we need to find address/port
    if address is None or port is None:
        discovery = discover_lightwave_instances()
        if discovery.get('success') and discovery.get('count', 0) > 0:
            for instance in discovery.get('instances', []):
                if instance.get('type') == 'modeler':
                    discovered_modeler = instance
                    break

    # Determine final address and port
    final_address = address or (discovered_modeler['address'] if discovered_modeler else 'localhost')
    final_port = port or (discovered_modeler['port'] if discovered_modeler else 42627)

    return connect_to_modeler(final_address, int(final_port))


def _resolve_connection_id(connection_id, instance_type):
    """Resolve a connection_id: use the provided one, or auto-select if only one exists.

    Args:
        connection_id: The connection_id passed by the caller (may be None).
        instance_type: 'layout' or 'modeler' to filter connections by type.

    Returns:
        The resolved connection_id string.

    Raises:
        ValueError: If no matching connection exists or multiple exist without explicit selection.
    """
    matching = {
        cid: conn for cid, conn in ACTIVE_CONNECTIONS.items()
        if conn.type == instance_type
    }

    if connection_id is not None:
        if connection_id not in matching:
            raise ValueError(f'No active connection with ID: {connection_id}')
        return connection_id

    if len(matching) == 0:
        raise ValueError(f'No active {instance_type} connection. Use connect_{instance_type} first.')
    if len(matching) == 1:
        return next(iter(matching.keys()))

    raise ValueError(
        f'Multiple {instance_type} connections exist. '
        f'Please specify connection_id: {list(matching.keys())}'
    )


def send_layout_command(connection_id, command, args=None):
    """Send a command to a connected Layout instance."""
    try:
        resolved_id = _resolve_connection_id(connection_id, 'layout')
    except ValueError as e:
        return {'success': False, 'error': str(e)}

    conn = ACTIVE_CONNECTIONS[resolved_id]

    if args is None:
        args = []
    elif not isinstance(args, list):
        args = [args]
    
    success, message = conn.send_command(command, args)
    
    return {
        'success': success,
        'message': message,
        'command': command,
        'args': args
    }


def send_modeler_command(connection_id, command, args=None):
    """Send a command to a connected Modeler instance."""
    try:
        resolved_id = _resolve_connection_id(connection_id, 'modeler')
    except ValueError as e:
        return {'success': False, 'error': str(e)}

    conn = ACTIVE_CONNECTIONS[resolved_id]
    
    if args is None:
        args = []
    elif not isinstance(args, list):
        args = [args]
    
    success, message = conn.send_command(command, args)
    
    return {
        'success': success,
        'message': message,
        'command': command,
        'args': args
    }


def list_active_connections():
    """List all active connections."""
    connections = [conn.to_dict() for conn in ACTIVE_CONNECTIONS.values()]
    
    return {
        'success': True,
        'connections': connections,
        'count': len(connections)
    }


def close_connection(connection_id):
    """Close an active connection."""
    if connection_id not in ACTIVE_CONNECTIONS:
        return {
            'success': False,
            'error': f'No active connection with ID: {connection_id}'
        }
    
    conn = ACTIVE_CONNECTIONS[connection_id]
    success, message = conn.close()
    
    if success:
        del ACTIVE_CONNECTIONS[connection_id]
    
    return {
        'success': success,
        'message': message
    }


def list_layout_commands():
    """List all available Layout commands from cache."""
    if COMMAND_CACHE['layout'] is None:
        return {
            'success': False,
            'error': 'Layout command cache not loaded'
        }
    
    return {
        'success': True,
        'commands': COMMAND_CACHE['layout']
    }


def list_modeler_commands():
    """List all available Modeler commands from cache."""
    if COMMAND_CACHE['modeler'] is None:
        return {
            'success': False,
            'error': 'Modeler command cache not loaded'
        }
    
    return {
        'success': True,
        'commands': COMMAND_CACHE['modeler']
    }


def refresh_command_cache(module_path=None):
    """Refresh the command cache by re-introspecting the lwcommandport module."""
    global COMMAND_CACHE
    
    if module_path:
        if module_path not in sys.path:
            sys.path.insert(0, module_path)
    
    try:
        if module_path:
            sys.path.insert(0, module_path)
        
        import importlib
        if 'lwcommandport' in sys.modules:
            importlib.reload(sys.modules['lwcommandport'])
        if 'lwcommandport.layout' in sys.modules:
            importlib.reload(sys.modules['lwcommandport.layout'])
        if 'lwcommandport.modeler' in sys.modules:
            importlib.reload(sys.modules['lwcommandport.modeler'])
        
        from lwcommandport.layout import Layout
        from lwcommandport.modeler import Modeler
        
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'cache')
        
        layout_commands = {}
        for name in dir(Layout):
            if not name.startswith('_') and callable(getattr(Layout, name)):
                doc = getattr(Layout, name).__doc__ or ''
                layout_commands[name] = {
                    'name': name,
                    'command': name,
                    'description': doc.strip()
                }
        
        modeler_commands = {}
        for name in dir(Modeler):
            if not name.startswith('_') and callable(getattr(Modeler, name)):
                doc = getattr(Modeler, name).__doc__ or ''
                modeler_commands[name] = {
                    'name': name,
                    'command': name,
                    'description': doc.strip()
                }
        
        COMMAND_CACHE['layout'] = {
            'command_count': len(layout_commands),
            'commands': layout_commands
        }
        COMMAND_CACHE['modeler'] = {
            'command_count': len(modeler_commands),
            'commands': modeler_commands
        }
        
        return {
            'success': True,
            'message': f'Refreshed cache: {len(layout_commands)} Layout, {len(modeler_commands)} Modeler commands'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


TOOL_HANDLERS = {
    'discover_lightwave': lambda args: discover_lightwave_instances(),
    'connect_layout': lambda args: connect_to_layout(
        args.get('address'),
        args.get('port')
    ),
    'connect_layout_auto': lambda args: connect_layout_auto(
        args.get('address'),
        args.get('port')
    ),
    'connect_modeler': lambda args: connect_to_modeler(
        args.get('address'),
        args.get('port')
    ),
    'connect_modeler_auto': lambda args: connect_modeler_auto(
        args.get('address'),
        args.get('port')
    ),
    'send_layout_command': lambda args: send_layout_command(
        args.get('connection_id'),
        args.get('command'),
        args.get('args', [])
    ),
    'send_modeler_command': lambda args: send_modeler_command(
        args.get('connection_id'),
        args.get('command'),
        args.get('args', [])
    ),
    'list_connections': lambda args: list_active_connections(),
    'close_connection': lambda args: close_connection(args.get('connection_id')),
    'list_layout_commands': lambda args: list_layout_commands(),
    'list_modeler_commands': lambda args: list_modeler_commands(),
    'refresh_command_cache': lambda args: refresh_command_cache(args.get('module_path'))
}


def handle_request(request):
    """Handle an MCP request and return a response."""
    # #region agent log
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.cursor', 'debug-b485b2.log')
    import time
    try:
        with open(log_path, 'a') as f:
            f.write(json.dumps({
                'sessionId': 'b485b2',
                'id': f'req_{int(time.time()*1000)}',
                'timestamp': int(time.time()*1000),
                'location': 'lightwave_mcp_server.py:handle_request',
                'message': 'Received request',
                'data': {'request': request},
                'runId': 'debug',
                'hypothesisId': 'A'
            }) + '\n')
    except:
        pass
    # #endregion

    request_id = request.get('id', 'unknown')
    method = request.get('method')
    params = request.get('params', {})

    jsonrpc_response = {'jsonrpc': '2.0'}

    if method == 'initialize':
        resp = {
            'id': request_id,
            'result': {
                'protocolVersion': '2024-11-05',
                'serverInfo': {
                    'name': 'LightWave Command Port MCP Server',
                    'version': '1.0.0'
                },
                'capabilities': {
                    'tools': {}
                },
                'instructions': 'LightWave 3D Command Port MCP Server. Use discover_lightwave to find instances.'
            }
        }
        resp.update(jsonrpc_response)
        return resp

    elif method == 'tools/list':
        resp = {
            'id': request_id,
            'result': {
                'tools': TOOL_DEFINITIONS
            }
        }
        resp.update(jsonrpc_response)
        return resp

    elif method == 'tools/call':
        tool_name = params.get('name')
        tool_args = params.get('arguments', {})

        if tool_name in TOOL_HANDLERS:
            result = TOOL_HANDLERS[tool_name](tool_args)
            resp = {
                'id': request_id,
                'result': {
                    'content': [
                        {
                            'type': 'text',
                            'text': json.dumps(result, indent=2)
                        }
                    ],
                    'isError': False
                }
            }
            resp.update(jsonrpc_response)
            return resp
        else:
            resp = {
                'id': request_id,
                'error': {
                    'code': -32601,
                    'message': f'Unknown tool: {tool_name}'
                }
            }
            resp.update(jsonrpc_response)
            return resp

    elif method == 'shutdown':
        resp = {
            'id': request_id,
            'result': {'success': True}
        }
        resp.update(jsonrpc_response)
        return resp

    else:
        resp = {
            'id': request_id,
            'error': {
                'code': -32601,
                'message': f'Unknown method: {method}'
            }
        }
        resp.update(jsonrpc_response)
        return resp


def main():
    """Main entry point for the MCP server."""
    load_command_cache()
    setup_tools()
    
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
            except json.JSONDecodeError:
                continue
            
            response = handle_request(request)
            
            if response:
                print(json.dumps(response), flush=True)
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()
