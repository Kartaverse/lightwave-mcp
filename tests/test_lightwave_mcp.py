#!/usr/bin/env python
"""
Unit tests for LightWave MCP Server

These tests validate the MCP server functionality. They are designed to work
without LightWave being installed - mocking is used where necessary.

Paths configured for:
    Server: lightwave-mcp/src/lightwave_mcp_server.py
    lwcommandport: lightwave-mcp/src/lwcommandport

Run with:
    cd "lightwave-mcp"
    python3 tests/test_lightwave_mcp.py -v
    python3 -m unittest tests/test_lightwave_mcp.py -v
"""

import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch, mock_open

# Paths from mcp.json configuration
LIGHTWAVE_MCP_SERVER_PATH = "src/lightwave_mcp/server.py"
LIGHTWAVE_LWCOMMANDPORT_PATH = "src"

# Add lwcommandport to path (same as PYTHONPATH in mcp.json)
sys.path.insert(0, LIGHTWAVE_LWCOMMANDPORT_PATH)

# Add src to path
sys.path.insert(0, os.path.dirname(LIGHTWAVE_MCP_SERVER_PATH))

# Import the MCP server module
import importlib.util
spec = importlib.util.spec_from_file_location(
    "lightwave_mcp_server",
    LIGHTWAVE_MCP_SERVER_PATH
)
lightwave_mcp_server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lightwave_mcp_server)


class TestLightWaveModuleLoading(unittest.TestCase):
    """Test that LightWave module loads correctly"""

    def test_lwcommandport_imports(self):
        """lwcommandport should be importable from configured path"""
        try:
            import lwcommandport
            lwcommandport_imported = True
        except ImportError:
            lwcommandport_imported = False

        self.assertTrue(
            lwcommandport_imported,
            f"lwcommandport not importable from {LIGHTWAVE_LWCOMMANDPORT_PATH}. "
            "Check that LightWave is installed at the expected path."
        )

    def test_lwcommandport_layout_imports(self):
        """lwcommandport.layout should be importable"""
        sys.path.insert(0, LIGHTWAVE_LWCOMMANDPORT_PATH)
        try:
            from lwcommandport.layout import Layout
            layout_imported = True
        except ImportError:
            layout_imported = False

        self.assertTrue(
            layout_imported,
            "lwcommandport.layout.Layout not importable. Check LightWave installation."
        )

    def test_lwcommandport_modeler_imports(self):
        """lwcommandport.modeler should be importable"""
        sys.path.insert(0, LIGHTWAVE_LWCOMMANDPORT_PATH)
        try:
            from lwcommandport.modeler import Modeler
            modeler_imported = True
        except ImportError:
            modeler_imported = False

        self.assertTrue(
            modeler_imported,
            "lwcommandport.modeler.Modeler not importable. Check LightWave installation."
        )


class TestJSONRPCProtocol(unittest.TestCase):
    """Test JSON-RPC 2.0 protocol compliance"""

    def test_initialize_response_has_jsonrpc_field(self):
        """Initialize response must have jsonrpc: '2.0'"""
        request = {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {}}
        response = lightwave_mcp_server.handle_request(request)
        self.assertIn('jsonrpc', response)
        self.assertEqual(response['jsonrpc'], '2.0')

    def test_tools_list_response_has_jsonrpc_field(self):
        """Tools/list response must have jsonrpc: '2.0'"""
        request = {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list', 'params': {}}
        response = lightwave_mcp_server.handle_request(request)
        self.assertIn('jsonrpc', response)
        self.assertEqual(response['jsonrpc'], '2.0')

    def test_tools_call_response_has_jsonrpc_field(self):
        """Tools/call response must have jsonrpc: '2.0'"""
        request = {
            'jsonrpc': '2.0',
            'id': 3,
            'method': 'tools/call',
            'params': {'name': 'list_connections', 'arguments': {}}
        }
        response = lightwave_mcp_server.handle_request(request)
        self.assertIn('jsonrpc', response)
        self.assertEqual(response['jsonrpc'], '2.0')

    def test_shutdown_response_has_jsonrpc_field(self):
        """Shutdown response must have jsonrpc: '2.0'"""
        request = {'jsonrpc': '2.0', 'id': 4, 'method': 'shutdown', 'params': {}}
        response = lightwave_mcp_server.handle_request(request)
        self.assertIn('jsonrpc', response)
        self.assertEqual(response['jsonrpc'], '2.0')

    def test_unknown_method_returns_error_with_jsonrpc(self):
        """Unknown method should return error with jsonrpc: '2.0'"""
        request = {'jsonrpc': '2.0', 'id': 5, 'method': 'unknown/method', 'params': {}}
        response = lightwave_mcp_server.handle_request(request)
        self.assertIn('jsonrpc', response)
        self.assertEqual(response['jsonrpc'], '2.0')
        self.assertIn('error', response)

    def test_initialize_response_has_protocol_version(self):
        """Initialize response must have protocolVersion"""
        request = {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {}}
        response = lightwave_mcp_server.handle_request(request)
        self.assertIn('result', response)
        self.assertIn('protocolVersion', response['result'])

    def test_initialize_response_has_server_info(self):
        """Initialize response must have serverInfo"""
        request = {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {}}
        response = lightwave_mcp_server.handle_request(request)
        self.assertIn('result', response)
        self.assertIn('serverInfo', response['result'])
        self.assertIn('name', response['result']['serverInfo'])

    def test_initialize_response_has_capabilities(self):
        """Initialize response must have capabilities"""
        request = {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {}}
        response = lightwave_mcp_server.handle_request(request)
        self.assertIn('result', response)
        self.assertIn('capabilities', response['result'])


class TestConnectionManagement(unittest.TestCase):
    """Test connection management functionality"""

    def setUp(self):
        """Reset active connections before each test"""
        lightwave_mcp_server.ACTIVE_CONNECTIONS.clear()

    def test_connect_to_layout_without_lwcommandport(self):
        """connect_to_layout should handle missing lwcommandport gracefully"""
        # Test when lwcommandport is not available
        original_available = lightwave_mcp_server.LWCPC_AVAILABLE
        lightwave_mcp_server.LWCPC_AVAILABLE = False

        result = lightwave_mcp_server.connect_to_layout('localhost', 50000)

        lightwave_mcp_server.LWCPC_AVAILABLE = original_available

        # Should return error since lwcommandport not available
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_connect_to_modeler_without_lwcommandport(self):
        """connect_to_modeler should handle missing lwcommandport gracefully"""
        original_available = lightwave_mcp_server.LWCPC_AVAILABLE
        lightwave_mcp_server.LWCPC_AVAILABLE = False

        result = lightwave_mcp_server.connect_to_modeler('localhost', 50001)

        lightwave_mcp_server.LWCPC_AVAILABLE = original_available

        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_list_active_connections_empty(self):
        """list_active_connections should return empty when no connections"""
        result = lightwave_mcp_server.list_active_connections()
        self.assertTrue(result['success'])
        self.assertEqual(result['count'], 0)
        self.assertEqual(result['connections'], [])

    def test_close_invalid_connection_returns_error(self):
        """close_connection with invalid ID should return error"""
        result = lightwave_mcp_server.close_connection('invalid-id-12345')
        self.assertFalse(result['success'])
        self.assertIn('error', result)


class TestCommandSending(unittest.TestCase):
    """Test command sending functionality"""

    def setUp(self):
        """Reset active connections before each test"""
        lightwave_mcp_server.ACTIVE_CONNECTIONS.clear()

    def test_send_layout_command_unknown_connection(self):
        """send_layout_command with unknown connection should return error"""
        result = lightwave_mcp_server.send_layout_command('invalid-id', 'LoadScene')
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_send_modeler_command_unknown_connection(self):
        """send_modeler_command with unknown connection should return error"""
        result = lightwave_mcp_server.send_modeler_command('invalid-id', 'clone')
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_send_command_with_args(self):
        """send_command should pass arguments correctly"""
        mock_instance = MagicMock()
        mock_instance.LoadScene = MagicMock()

        conn = lightwave_mcp_server.LightWaveConnection(
            connection_id='test-123',
            instance_type='layout',
            address='localhost',
            port=50000
        )
        conn.instance = mock_instance

        lightwave_mcp_server.ACTIVE_CONNECTIONS['test-123'] = conn

        result = lightwave_mcp_server.send_layout_command('test-123', 'LoadScene', ['scene.lws'])
        self.assertTrue(result['success'])
        mock_instance.LoadScene.assert_called_once_with('scene.lws')

    def test_send_command_without_args(self):
        """send_command should work without arguments"""
        mock_instance = MagicMock()
        mock_instance.ClearScene = MagicMock()

        conn = lightwave_mcp_server.LightWaveConnection(
            connection_id='test-456',
            instance_type='layout',
            address='localhost',
            port=50000
        )
        conn.instance = mock_instance

        lightwave_mcp_server.ACTIVE_CONNECTIONS['test-456'] = conn

        result = lightwave_mcp_server.send_layout_command('test-456', 'ClearScene')
        self.assertTrue(result['success'])
        mock_instance.ClearScene.assert_called_once()


class TestCommandCache(unittest.TestCase):
    """Test command cache functionality"""

    def test_list_layout_commands_returns_structure(self):
        """list_layout_commands should return commands structure"""
        # Initialize with empty cache
        lightwave_mcp_server.COMMAND_CACHE['layout'] = {
            'commands': {
                'LoadScene': {'name': 'LoadScene', 'args': ['filename']}
            }
        }

        result = lightwave_mcp_server.list_layout_commands()
        self.assertTrue(result['success'])
        self.assertIn('commands', result)

    def test_list_modeler_commands_returns_structure(self):
        """list_modeler_commands should return commands structure"""
        lightwave_mcp_server.COMMAND_CACHE['modeler'] = {
            'commands': {
                'clone': {'name': 'clone', 'args': []}
            }
        }

        result = lightwave_mcp_server.list_modeler_commands()
        self.assertTrue(result['success'])
        self.assertIn('commands', result)


class TestToolHandlers(unittest.TestCase):
    """Test that all tools are registered"""

    def test_discover_lightwave_handler_exists(self):
        """discover_lightwave handler should exist"""
        self.assertIn('discover_lightwave', lightwave_mcp_server.TOOL_HANDLERS)

    def test_connect_layout_handler_exists(self):
        """connect_layout handler should exist"""
        self.assertIn('connect_layout', lightwave_mcp_server.TOOL_HANDLERS)

    def test_connect_modeler_handler_exists(self):
        """connect_modeler handler should exist"""
        self.assertIn('connect_modeler', lightwave_mcp_server.TOOL_HANDLERS)

    def test_send_layout_command_handler_exists(self):
        """send_layout_command handler should exist"""
        self.assertIn('send_layout_command', lightwave_mcp_server.TOOL_HANDLERS)

    def test_send_modeler_command_handler_exists(self):
        """send_modeler_command handler should exist"""
        self.assertIn('send_modeler_command', lightwave_mcp_server.TOOL_HANDLERS)

    def test_list_connections_handler_exists(self):
        """list_connections handler should exist"""
        self.assertIn('list_connections', lightwave_mcp_server.TOOL_HANDLERS)

    def test_close_connection_handler_exists(self):
        """close_connection handler should exist"""
        self.assertIn('close_connection', lightwave_mcp_server.TOOL_HANDLERS)

    def test_refresh_command_cache_handler_exists(self):
        """refresh_command_cache handler should exist"""
        self.assertIn('refresh_command_cache', lightwave_mcp_server.TOOL_HANDLERS)


class TestDiscoveryFunctionality(unittest.TestCase):
    """Test LightWave discovery (mocked)"""

    @patch('socket.socket')
    def test_discover_returns_structure(self, mock_socket):
        """discover_lightwave_instances should return proper structure"""
        # Mock the socket operations
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.recvfrom.return_value = (b'', ('localhost', 50000))

        # Mock lwcommandport availability
        with patch.object(lightwave_mcp_server, 'LWCPC_AVAILABLE', False):
            result = lightwave_mcp_server.discover_lightwave_instances()

        # Should return structure even when lwcommandport not available
        self.assertIn('success', result)
        self.assertIn('instances', result)


class TestToolDefinitions(unittest.TestCase):
    """Test that tool definitions are properly loaded"""

    def setUp(self):
        """Setup tool definitions"""
        lightwave_mcp_server.setup_tools()

    def test_tools_loaded(self):
        """Tool definitions should be loaded"""
        self.assertGreater(len(lightwave_mcp_server.TOOL_DEFINITIONS), 0)

    def test_tool_has_name(self):
        """Each tool should have a name"""
        for tool in lightwave_mcp_server.TOOL_DEFINITIONS:
            self.assertIn('name', tool)

    def test_tool_has_description(self):
        """Each tool should have a description"""
        for tool in lightwave_mcp_server.TOOL_DEFINITIONS:
            self.assertIn('description', tool)

    def test_tool_has_input_schema(self):
        """Each tool should have inputSchema (MCP standard)"""
        for tool in lightwave_mcp_server.TOOL_DEFINITIONS:
            self.assertIn('inputSchema', tool)


def run_tests():
    """Run all tests and print results"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestJSONRPCProtocol))
    suite.addTests(loader.loadTestsFromTestCase(TestConnectionManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestCommandSending))
    suite.addTests(loader.loadTestsFromTestCase(TestCommandCache))
    suite.addTests(loader.loadTestsFromTestCase(TestToolHandlers))
    suite.addTests(loader.loadTestsFromTestCase(TestDiscoveryFunctionality))
    suite.addTests(loader.loadTestsFromTestCase(TestToolDefinitions))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.wasSuccessful():
        print("\nALL TESTS PASSED!")
        return 0
    else:
        print("\nSOME TESTS FAILED!")
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}")
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}")
        return 1


if __name__ == '__main__':
    sys.exit(run_tests())
