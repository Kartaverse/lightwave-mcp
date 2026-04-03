#!/usr/bin/env python
"""
Integration tests for LightWave MCP Server - Live Testing

These tests connect to a REAL LightWave instance running with command port enabled.
Requires LightWave Layout or Modeler to be running with command port active.

CAUTION: These tests send actual commands to LightWave!

Prerequisites:
1. LightWave Layout or Modeler must be running
2. Command Port must be enabled in LightWave settings (General > Commands > Enable Command Port)
3. Note the command port number displayed in LightWave's title bar (e.g., "--command-port=45454")

Usage:
    python3 tests/test_integration_live.py

Run specific tests:
    python3 tests/test_integration_live.py TestLiveDiscovery
    python3 tests/test_integration_live.py TestLiveLayoutConnection
"""

import json
import os
import sys
import unittest
import importlib.util

# Paths from mcp.json configuration
LIGHTWAVE_MCP_SERVER_PATH = "src/lightwave_mcp/server.py"
LIGHTWAVE_LWCOMMANDPORT_PATH = "src"

# Add paths
sys.path.insert(0, LIGHTWAVE_LWCOMMANDPORT_PATH)
sys.path.insert(0, os.path.dirname(LIGHTWAVE_MCP_SERVER_PATH))

# Import the MCP server module
spec = importlib.util.spec_from_file_location(
    "lightwave_mcp_server",
    LIGHTWAVE_MCP_SERVER_PATH
)
lightwave_mcp_server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lightwave_mcp_server)


def safe_json_dumps(obj, indent=2):
    """JSON serialization that handles non-serializable objects."""
    def sanitize_for_json(obj):
        if isinstance(obj, dict):
            return {k: sanitize_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [sanitize_for_json(item) for item in obj]
        else:
            try:
                json.dumps(obj)
                return obj
            except (TypeError, ValueError):
                return str(obj)
    return json.dumps(sanitize_for_json(obj), indent=indent)


class TestLiveDiscovery(unittest.TestCase):
    """Test LightWave instance discovery on localhost"""

    @classmethod
    def setUpClass(cls):
        """Run discovery once before all tests in this class"""
        cls.discovery_result = lightwave_mcp_server.discover_lightwave_instances()
        print(f"\nDiscovery result: {safe_json_dumps(cls.discovery_result)}")

    def test_discovery_succeeds(self):
        """Discovery should succeed"""
        self.assertTrue(self.discovery_result.get('success', False),
                       f"Discovery failed: {self.discovery_result.get('error', 'Unknown error')}")

    def test_discovery_finds_instances(self):
        """Discovery should find at least one instance"""
        instances = self.discovery_result.get('instances', [])
        self.assertGreater(len(instances), 0,
                         "No LightWave instances found. Is LightWave running with Command Port enabled?")

    def test_discovery_returns_layout_instance(self):
        """Discovery should find at least one Layout or Modeler instance"""
        instances = self.discovery_result.get('instances', [])
        types = [inst.get('type', '').lower() for inst in instances]
        self.assertTrue(
            'layout' in types or 'modeler' in types,
            f"No Layout or Modeler found. Found types: {types}"
        )

    def test_discovery_returns_valid_address(self):
        """Instance should have valid address"""
        instances = self.discovery_result.get('instances', [])
        for inst in instances:
            self.assertIn('address', inst)
            self.assertIn('port', inst)
            self.assertIsInstance(inst['port'], int)


class TestLiveLayoutConnection(unittest.TestCase):
    """Test connecting to a real Layout instance"""

    connection_id = None
    instance_info = None
    skipReason = None

    @classmethod
    def setUpClass(cls):
        """Discover and connect to Layout once before tests"""
        cls.connection_id = None
        cls.skipReason = None

        # Discover instances
        discovery = lightwave_mcp_server.discover_lightwave_instances()
        instances = discovery.get('instances', [])

        # Find a Layout instance
        layout_inst = None
        for inst in instances:
            if inst.get('type', '').lower() == 'layout':
                layout_inst = inst
                break

        if layout_inst is None:
            cls.skipReason = "No Layout instance found"
            return

        # Connect to Layout
        try:
            connect_result = lightwave_mcp_server.connect_to_layout(
                layout_inst['address'],
                layout_inst['port']
            )
        except Exception as e:
            cls.skipReason = f"Failed to connect: {str(e)}"
            return

        if connect_result.get('success'):
            cls.connection_id = connect_result['connection_id']
            cls.instance_info = layout_inst
            print(f"\nConnected to Layout: {safe_json_dumps(connect_result)}")
        else:
            cls.skipReason = f"Failed to connect: {connect_result.get('error')}"

    @classmethod
    def tearDownClass(cls):
        """Close connection after tests"""
        if cls.connection_id:
            lightwave_mcp_server.close_connection(cls.connection_id)

    def test_connection_established(self):
        """Should have a valid connection ID"""
        if self.skipReason:
            self.skipTest(self.skipReason)
        self.assertIsNotNone(self.connection_id)

    def test_connection_in_active_list(self):
        """Connection should appear in active connections"""
        if self.skipReason:
            self.skipTest(self.skipReason)

        connections = lightwave_mcp_server.list_active_connections()
        conn_ids = [c['id'] for c in connections.get('connections', [])]
        self.assertIn(self.connection_id, conn_ids)


class TestLiveCommandExecution(unittest.TestCase):
    """Test sending actual commands to LightWave"""

    connection_id = None
    skipReason = None

    @classmethod
    def setUpClass(cls):
        """Connect to Layout once before tests"""
        cls.connection_id = None
        cls.skipReason = None

        # Discover and connect
        discovery = lightwave_mcp_server.discover_lightwave_instances()
        instances = discovery.get('instances', [])

        layout_inst = None
        for inst in instances:
            if inst.get('type', '').lower() == 'layout':
                layout_inst = inst
                break

        if layout_inst is None:
            cls.skipReason = "No Layout instance found"
            return

        try:
            connect_result = lightwave_mcp_server.connect_to_layout(
                layout_inst['address'],
                layout_inst['port']
            )
        except Exception as e:
            cls.skipReason = f"Failed to connect: {str(e)}"
            return

        if connect_result.get('success'):
            cls.connection_id = connect_result['connection_id']
        else:
            cls.skipReason = f"Failed to connect: {connect_result.get('error')}"

    @classmethod
    def tearDownClass(cls):
        """Close connection after tests"""
        if cls.connection_id:
            lightwave_mcp_server.close_connection(cls.connection_id)

    def test_send_about_command(self):
        """Send About command - should succeed"""
        if self.skipReason:
            self.skipTest(self.skipReason)

        result = lightwave_mcp_server.send_layout_command(
            self.connection_id,
            'About',
            []
        )
        print(f"\nAbout command result: {safe_json_dumps(result)}")
        self.assertTrue(result.get('success', False))

    def test_send_loadscene_command_no_args(self):
        """Send LoadScene with no args - should handle gracefully"""
        if self.skipReason:
            self.skipTest(self.skipReason)

        # LoadScene requires a filename, so this should fail gracefully
        result = lightwave_mcp_server.send_layout_command(
            self.connection_id,
            'LoadScene',
            []
        )
        print(f"\nLoadScene (no args) result: {safe_json_dumps(result)}")
        # Should return success=False since no filename provided
        self.assertFalse(result.get('success', True))

    def test_send_unknown_command(self):
        """Send unknown command - should return error"""
        if self.skipReason:
            self.skipTest(self.skipReason)

        result = lightwave_mcp_server.send_layout_command(
            self.connection_id,
            'NonexistentCommandXYZ',
            []
        )
        print(f"\nUnknown command result: {safe_json_dumps(result)}")
        self.assertFalse(result.get('success', True))
        # Server returns 'message' with error description
        self.assertIn('message', result)


class TestLiveModelerConnection(unittest.TestCase):
    """Test connecting to a real Modeler instance (if available)"""

    connection_id = None
    instance_info = None
    skipReason = None

    @classmethod
    def setUpClass(cls):
        """Discover and connect to Modeler once before tests"""
        cls.connection_id = None
        cls.skipReason = None

        # Discover instances
        discovery = lightwave_mcp_server.discover_lightwave_instances()
        instances = discovery.get('instances', [])

        # Find a Modeler instance
        modeler_inst = None
        for inst in instances:
            if inst.get('type', '').lower() == 'modeler':
                modeler_inst = inst
                break

        if modeler_inst is None:
            cls.skipReason = "No Modeler instance found (Modeler not running with Command Port)"
            return

        # Connect to Modeler
        try:
            connect_result = lightwave_mcp_server.connect_to_modeler(
                modeler_inst['address'],
                modeler_inst['port']
            )
        except Exception as e:
            cls.skipReason = f"Failed to connect: {str(e)}"
            return

        if connect_result.get('success'):
            cls.connection_id = connect_result['connection_id']
            cls.instance_info = modeler_inst
            print(f"\nConnected to Modeler: {safe_json_dumps(connect_result)}")
        else:
            cls.skipReason = f"Failed to connect: {connect_result.get('error')}"

    @classmethod
    def tearDownClass(cls):
        """Close connection after tests"""
        if cls.connection_id:
            lightwave_mcp_server.close_connection(cls.connection_id)

    def test_modeler_connection_established(self):
        """Should have a valid connection ID to Modeler"""
        if self.skipReason:
            self.skipTest(self.skipReason)
        self.assertIsNotNone(self.connection_id)

    def test_send_modeler_command(self):
        """Send a Modeler command"""
        if self.skipReason:
            self.skipTest(self.skipReason)

        # sel_invert doesn't require args
        result = lightwave_mcp_server.send_modeler_command(
            self.connection_id,
            'sel_invert',
            []
        )
        print(f"\nsel_invert command result: {safe_json_dumps(result)}")
        # Modeler commands return success even if nothing selected
        self.assertIn('success', result)


def check_prerequisites():
    """Check if prerequisites are met"""
    errors = []

    # Check paths exist
    if not os.path.exists(LIGHTWAVE_MCP_SERVER_PATH):
        errors.append(f"Server path not found: {LIGHTWAVE_MCP_SERVER_PATH}")
    if not os.path.exists(LIGHTWAVE_LWCOMMANDPORT_PATH):
        errors.append(f"lwcommandport path not found: {LIGHTWAVE_LWCOMMANDPORT_PATH}")

    return errors


def main():
    """Run integration tests with prerequisite checking"""
    print("=" * 70)
    print("LIGHTWAVE MCP LIVE INTEGRATION TESTS")
    print("=" * 70)
    print("\nPrerequisites:")
    print("1. LightWave Layout or Modeler must be running")
    print("2. Command Port must be enabled in LightWave settings")
    print("   (Settings > General > Commands > Enable Command Port)")
    print("-" * 70)

    # Check prerequisites
    errors = check_prerequisites()
    if errors:
        print("\nERRORS FOUND:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease fix the paths in this test file to match your installation.")
        return 1

    print("\nPaths OK:")
    print(f"  Server: {LIGHTWAVE_MCP_SERVER_PATH}")
    print(f"  lwcommandport: {LIGHTWAVE_LWCOMMANDPORT_PATH}")
    print("-" * 70)

    # Run discovery first to show what's available
    print("\nRunning discovery to find LightWave instances...")
    result = lightwave_mcp_server.discover_lightwave_instances()
    print(safe_json_dumps(result))

    if not result.get('success'):
        print(f"\nDiscovery failed: {result.get('error')}")
        return 1

    instances = result.get('instances', [])
    if len(instances) == 0:
        print("\nNo LightWave instances found!")
        print("Please start LightWave with Command Port enabled and try again.")
        return 1

    print(f"\nFound {len(instances)} instance(s):")
    for inst in instances:
        print(f"  - {inst.get('type')} @ {inst.get('address')}:{inst.get('port')} (v{inst.get('version')})")

    print("-" * 70)
    print("\nStarting integration tests...\n")

    # Run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes in order
    suite.addTests(loader.loadTestsFromTestCase(TestLiveDiscovery))
    suite.addTests(loader.loadTestsFromTestCase(TestLiveLayoutConnection))
    suite.addTests(loader.loadTestsFromTestCase(TestLiveCommandExecution))
    suite.addTests(loader.loadTestsFromTestCase(TestLiveModelerConnection))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.wasSuccessful():
        print("\nALL LIVE TESTS PASSED!")
        return 0
    else:
        print("\nSOME TESTS FAILED!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
