#!/usr/bin/env python
"""
Introspection utility for LightWave Command Port.

This script extracts command information from the LightWave Command Port Python library
by parsing the docstrings and method signatures from the Layout and Modeler classes.

Usage:
    python introspect_commands.py [--output-dir PATH] [--module-path PATH]

The script will generate JSON cache files for Layout and Modeler commands that can be
used by the MCP server for command discovery and validation.
"""

import argparse
import inspect
import json
import os
import re
import sys


def get_command_signature(method):
    """Extract command signature from a method's docstring."""
    sig = inspect.signature(method) if hasattr(inspect, 'signature') else None
    
    if sig:
        params = []
        has_args = False
        for name, param in sig.parameters.items():
            if name == 'self':
                continue
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                has_args = True
            elif param.kind == inspect.Parameter.VAR_KEYWORD:
                continue
            else:
                params.append(name)
        
        if has_args:
            return "{}({})".format(method.__name__, ", ".join(params) + ", *args")
        return "{}({})".format(method.__name__, ", ".join(params))
    
    return method.__name__


def extract_call_signature(docstring, method_name=None):
    r"""Extract the Call: signature from a docstring.
    
    Handles two formats:
    1. Layout format: \""" LoadScene(filename) \"""
    2. Modeler format: 
       Name: Load Scene
       Call: LoadScene(filename)
    """
    if not docstring:
        return None
    
    docstring = docstring.strip()
    
    # Try the multi-line format with "Call:" prefix (Modeler style)
    call_match = re.search(r'Call:\s*(.+)', docstring)
    if call_match:
        return call_match.group(1).strip()
    
    # Try the simple format (Layout style): """ CommandName(args) """
    # Match pattern like """ LoadScene(filename) """ or """ CommandName() """
    simple_match = re.search(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*(\(.*\))?\s*$', docstring)
    if simple_match:
        cmd_name = simple_match.group(1)
        args_part = simple_match.group(2) or '()'
        # Only accept if it matches the method name or is a reasonable command format
        if method_name and cmd_name.lower() == method_name.lower():
            return f"{cmd_name}{args_part}"
        elif re.match(r'^[A-Z][a-zA-Z0-9]+$', cmd_name):
            return f"{cmd_name}{args_part}"
    
    return None


def extract_name(docstring, method_name=None):
    """Extract the Name: from a docstring, or derive from method name."""
    if not docstring:
        return None
    
    # Try the multi-line format with "Name:" prefix (Modeler style)
    name_match = re.search(r'Name:\s*(.+)', docstring)
    if name_match:
        return name_match.group(1).strip()
    
    # For Layout style, derive name from method name
    if method_name:
        # Convert CamelCase to Title Case
        name = re.sub(r'([A-Z])', r' \1', method_name)
        name = re.sub(r'^ ', '', name)
        return name.strip()
    
    return None


def get_command_category(method_name):
    """Determine the category of a command based on its name."""
    categories = {
        'Create/Modify': [
            'add', 'create', 'new', 'delete', 'remove', 'set', 'clear',
            'clone', 'merge', 'split', 'flip', 'align', 'make', 'build'
        ],
        'File Operations': [
            'load', 'save', 'open', 'close', 'export', 'import', 'write',
            'read', 'export', 'preload', 'presave', 'autosave'
        ],
        'Selection': [
            'select', 'deselect', 'clear', 'invert', 'hide', 'unhide',
            'enable', 'disable', 'item'
        ],
        'Transform': [
            'move', 'rotate', 'scale', 'position', 'transform', 'pivot',
            'translate', 'turn', 'pan', 'zoom', 'view'
        ],
        'Geometry': [
            'polygon', 'point', 'mesh', 'vertex', 'face', 'surface',
            'subdivision', 'patch', 'bone', 'morph'
        ],
        'Lighting/Camera': [
            'light', 'camera', 'spotlight', 'shadow', 'flare', 'view',
            'perspective', 'azimuth', 'elevation'
        ],
        'Materials/Textures': [
            'material', 'texture', 'color', 'bump', 'reflection', 'refraction',
            'surface', 'shade', 'fog', 'sky', 'backdrop'
        ],
        'Rendering': [
            'render', 'preview', 'ray', 'trace', 'motion', 'blur', 'field',
            'frame', 'abort'
        ],
        'Scene': [
            'scene', 'object', 'layer', 'loadscene', 'savescene', 'clear'
        ],
        'Plugins/Servers': [
            'plugin', 'server', 'apply', 'edit', 'enable', 'flush', 'master'
        ],
        'General': []  # Default category
    }
    
    method_lower = method_name.lower()
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in method_lower:
                if category != 'General' or keywords == []:
                    return category
    
    return 'General'


def introspect_class(cls, module_path=None):
    """
    Introspect a CommandPort subclass to extract all commands.
    
    Args:
        cls: The class to introspect (Layout or Modeler)
        module_path: Optional path to prepend to sys.path for imports
    
    Returns:
        Dictionary mapping command names to their metadata
    """
    commands = {}
    
    if module_path and module_path not in sys.path:
        sys.path.insert(0, module_path)
    
    for name in dir(cls):
        if name.startswith('_'):
            continue
        
        attr = getattr(cls, name)
        if not callable(attr):
            continue
        
        docstring = attr.__doc__ or ''
        
        call_sig = extract_call_signature(docstring, name)
        display_name = extract_name(docstring, name)
        signature = get_command_signature(attr)
        
        if call_sig and call_sig.startswith(name):
            category = get_command_category(name)
            
            commands[name] = {
                'name': display_name or name,
                'command': name,
                'signature': signature,
                'call': call_sig,
                'category': category,
                'description': docstring.strip() if docstring else ''
            }
    
    return commands


def categorize_commands(commands):
    """Organize commands by category."""
    categorized = {}
    for name, info in commands.items():
        category = info.get('category', 'General')
        if category not in categorized:
            categorized[category] = []
        categorized[category].append({
            'command': info['command'],
            'name': info['name'],
            'signature': info['signature'],
            'call': info['call'],
            'description': info['description']
        })
    
    for category in categorized:
        categorized[category].sort(key=lambda x: x['command'])
    
    return categorized


def main():
    parser = argparse.ArgumentParser(
        description='Introspect LightWave Command Port commands'
    )
    parser.add_argument(
        '--output-dir', '-o',
        default='.',
        help='Directory to write JSON cache files (default: current directory)'
    )
    parser.add_argument(
        '--module-path', '-m',
        default=None,
        help='Path to the lwcommandport module (for auto-detection)'
    )
    parser.add_argument(
        '--layout-only',
        action='store_true',
        help='Only process Layout commands'
    )
    parser.add_argument(
        '--modeler-only',
        action='store_true',
        help='Only process Modeler commands'
    )
    
    args = parser.parse_args()
    
    output_dir = args.output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        from lwcommandport.layout import Layout
        layout_commands = introspect_class(Layout, args.module_path)
        categorized_layout = categorize_commands(layout_commands)
        
        layout_output = {
            'source': 'lwcommandport.layout.Layout',
            'command_count': len(layout_commands),
            'categories': {}
        }
        
        for category, cmds in categorized_layout.items():
            layout_output['categories'][category] = cmds
        
        layout_path = os.path.join(output_dir, 'layout_commands.json')
        with open(layout_path, 'w') as f:
            json.dump(layout_output, f, indent=2)
        
        print("Generated {} Layout commands in {}".format(len(layout_commands), layout_path))
        
    except ImportError as e:
        print("Warning: Could not import Layout: {}".format(e))
    
    try:
        from lwcommandport.modeler import Modeler
        modeler_commands = introspect_class(Modeler, args.module_path)
        categorized_modeler = categorize_commands(modeler_commands)
        
        modeler_output = {
            'source': 'lwcommandport.modeler.Modeler',
            'command_count': len(modeler_commands),
            'categories': {}
        }
        
        for category, cmds in categorized_modeler.items():
            modeler_output['categories'][category] = cmds
        
        modeler_path = os.path.join(output_dir, 'modeler_commands.json')
        with open(modeler_path, 'w') as f:
            json.dump(modeler_output, f, indent=2)
        
        print("Generated {} Modeler commands in {}".format(len(modeler_commands), modeler_path))
        
    except ImportError as e:
        print("Warning: Could not import Modeler: {}".format(e))
    
    print("\nDone! Command caches generated successfully.")


if __name__ == '__main__':
    main()
