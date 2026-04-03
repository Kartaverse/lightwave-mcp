"""
LightWave Command Port Library (Python 3 compatible fork)

Forked from original lwcommandport for Python 3.11+ compatibility.
Original Copyright (C) 2015 LightWaveDigital

This fork maintains the original API while updating Python 2 specific
code to work with Python 3.11+.
"""

__author__     = "Bob Hood"
__copyright__  = "Copyright (C) 2015 LightWaveDigital"
__version__    = "1.1"  # Python 3 fork version
__maintainer__ = "Bob Hood"
__email__      = "bobhood@lightwave3d.com"
__status__     = "Production"

# make sure any of our sub-modules (e.g., "layout") can be found
import pkgutil
__path__ = pkgutil.extend_path(__path__, __name__)

import os
import sys
import ctypes
import socket
import hashlib
import fnmatch
import subprocess

if os.name != 'nt':
    try:
        from subprocess import DEVNULL      # Python 3.x
    except ImportError:
        DEVNULL = open(os.devnull, 'wb')

# Python 2/3 compatibility helpers
def _is_string(s):
    """Check if object is a string type (str in Py3, str/unicode in Py2)"""
    return isinstance(s, str)

# These values must match their source values in lwcomport.h

CP_DISCOVERY_START = 50155
CP_DISCOVERY_END = 50165

CP_COMMANDSET_LAYOUT = 1
CP_COMMANDSET_MODELER = 2

CP_REQ_MAGIC = (((ord('C'))<<24)|((ord('R'))<<16)|((ord('E'))<<8)|(ord('Q')))
CP_INFO_MAGIC = (((ord('C'))<<24)|((ord('N'))<<16)|((ord('F'))<<8)|(ord('O')))

COMMANDPORT_REQ_VERSION = 1
class CommandPortReq(ctypes.Structure):
    _fields_ = [("magic", ctypes.c_int),
                ("version", ctypes.c_int),
                ("port", ctypes.c_ushort),
                ("dummy", ctypes.c_ushort)]

COMMANDPORT_INFO_VERSION = 2
class CommandPortInfo(ctypes.Structure):
    _fields_ = [("magic", ctypes.c_int),
                ("version", ctypes.c_int),
                ("major", ctypes.c_ushort),
                ("minor", ctypes.c_ushort),
                ("build", ctypes.c_ushort),
                ("app", ctypes.c_ushort),
                ("port", ctypes.c_ushort),
                ("port_alias", ctypes.c_char * 128)]

class CommandPort(object):
    """
    This is a base class for the Command Port system.  It is
    subclassed by the Layout and Modeler classes to provide
    common support.

    It is not intended for direct usage.
    """
    def __init__(self, address, port):
        super(CommandPort, self).__init__()

        self._address = address
        self._port = self._port_name_to_number(port)

        self._sock = None

    def _send_command(self, command, args=None):
        if (args is not None) and len(args):
            command = "{0} {1}".format(command, " ".join([str(t) for t in args]))
        if self._sock is None:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self._sock is not None:
            self._sock.sendto(command.encode("utf-8"), (self._address, self._port))

    def _port_name_to_number(self, port):
        if not _is_string(port):
            port = str(port)

        try:
            return int(port)
        except ValueError:
            pass

        m = hashlib.md5()
        m.update(port.encode("utf-8"))
        h = m.digest()
        hash_val = 0
        for i in range(len(h)):
            hash_val += (h[i] << i)

        return (hash_val + 1024) % 65534

    @staticmethod
    def _common_walker(path, version, pattern):
        """Walk directory tree to find matching files"""
        files = []

        for root, dirs, filenames in os.walk(path):
            for name in filenames:
                fullpath = os.path.join(root, name)
                if fnmatch.fnmatch(name, pattern) and (version in fullpath):
                    files.append(fullpath)

        return files

    def _launch(self, module, *args, **kwargs):
        if not _is_string(module) or (len(module) == 0):
            return (False, 'Invalid argument type provided!')

        if os.path.exists(module):
            # they are specifying the executable to launch, so just use it
            launch_args = []
            for arg in args:
                if isinstance(arg, (list, tuple)):
                    launch_args.extend(arg)
                else:
                    launch_args.append(arg)

            command = [module] + launch_args
            print(command)
            try:
                pid = subprocess.Popen(command).pid
            except Exception as e:
                return (False, 'Failed to launch process "{}"! {}'.format(module, str(e)))
        else:
            if (str(module.lower()) != 'layout') and (str(module.lower()) != 'modeler'):
                return (False, 'Invalid argument value ("{}") provided!'.format(module))

            version = kwargs.get("version", None)

            # see if we can figure out where the executable has been placed

            if os.name == 'nt':
                path = ""

                # one of these will succeed
                try:
                    import winreg as reg        # v3
                except ImportError:
                    try:
                        import _winreg as reg   # v2
                    except ImportError:
                        return (False, 'The winreg module must be available to auto-detect your install path!')

                if version is None:
                    try:
                        key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE,
                                          r"SOFTWARE\LightWaveDigital\LightWave", 0)
                    except OSError:
                        return (False, 'LightWave does not appear to be installed on your machine!')

                    # enumerate the key values here to process
                    # each potential installed version
                    index = 0
                    versions = []
                    while True:
                        try:
                            data = reg.EnumKey(key, index)
                        except OSError:
                            break
                        versions.append(data)
                        index += 1

                    reg.CloseKey(key)

                    # sort them lexically and then start checking from newest to oldest
                    versions.sort(reverse=True)
                    best_version = None
                    for ver in versions:
                        try:
                            key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE,
                                              r"SOFTWARE\LightWaveDigital\LightWave\{}\x64".format(ver),
                                              0)
                            path, type = reg.QueryValueEx(key, "ApplicationPath")
                            reg.CloseKey(key)

                            if os.path.exists(path):
                                best_version = path
                                break
                        except OSError:
                            pass

                    if best_version is None:
                        return (False, 'LightWave does not appear to be installed on your machine!')
                else:
                    try:
                        key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE,
                                          r"SOFTWARE\LightWaveDigital\LightWave\{}.0\x64".format(version),
                                          0)
                    except OSError:
                        return (False, 'LightWave does not appear to be installed on your machine!')

                    path, type = reg.QueryValueEx(key, "ApplicationPath")
                    reg.CloseKey(key)

                if not os.path.exists(path):
                    return (False, 'Cannot detect LightWave installation!')

                if str(module.lower()) == 'layout':
                    module = os.path.join(path, 'bin', 'Layout.exe')
                    if not os.path.exists(module):
                        module = os.path.join(path, 'bin', 'Layout_db.exe')
                    if not os.path.exists(module):
                        return (False, 'Cannot locate Layout executable!')
                elif str(module.lower()) == 'modeler':
                    module = os.path.join(path, 'bin', 'Modeler.exe')
                    if not os.path.exists(module):
                        module = os.path.join(path, 'bin', 'Modeler_db.exe')
                    if not os.path.exists(module):
                        return (False, 'Cannot locate Modeler executable!')
            elif sys.platform == 'darwin':
                files = []
                path = '/Applications/LightWaveDigital'
                if not os.path.exists(path):
                    return (False, 'LightWave does not appear to be installed on your machine!')

                if version is None:
                    # enumerate installed versions and use the most current
                    folders = os.listdir(path)
                    if len(folders) == 0:
                        return (False, 'LightWave does not appear to be installed on your machine!')
                    folders.sort(reverse=True)

                    app = ""
                    if str(module.lower()) == 'layout':
                        app = "Layout"
                    elif str(module.lower()) == 'modeler':
                        app = "Modeler"

                    for folder in folders:
                        module = os.path.join(path, folder, "{}.app".format(app), "Contents", "MacOS", app)
                        if os.path.exists(module):
                            break
                        module = None

                    if module is None:
                        return (False, 'Cannot locate {} app!'.format(app))
                else:
                    if str(module.lower()) == 'layout':
                        files = self._common_walker(path, version, "Layout*.app")
                        if len(files) == 0:
                            return (False, 'Cannot detect LightWave installation!')
                        module = os.path.join(files[0], 'Contents', 'MacOS', 'Layout')
                        if not os.path.exists(module):
                            return (False, 'Cannot locate Layout app!')
                    elif str(module.lower()) == 'modeler':
                        files = self._common_walker(path, version, "Modeler*.app")
                        if len(files) == 0:
                            return (False, 'Cannot detect LightWave installation!')
                        module = os.path.join(files[0], 'Contents', 'MacOS', 'Modeler')
                        if not os.path.exists(module):
                            return (False, 'Cannot locate Modeler app!')
            else:
                # Linux (not officially supported but kept for compatibility)
                files = []
                path = '/opt/LightWaveDigital'

                if str(module.lower()) == 'layout':
                    files = self._common_walker(path, version, "Layout*")
                    if len(files) == 0:
                        return (False, 'Cannot detect LightWave installation!')
                    module = os.path.join(path, files[0])
                    if not os.path.exists(module):
                        return (False, 'Cannot locate Layout executable!')
                elif str(module.lower()) == 'modeler':
                    files = self._common_walker(path, version, "Modeler*")
                    if len(files) == 0:
                        return (False, 'Cannot detect LightWave installation!')
                    module = os.path.join(path, files[0])
                    if not os.path.exists(module):
                        return (False, 'Cannot locate Modeler executable!')

            cmd = []
            for arg in args:
                if isinstance(arg, (list, tuple)):
                    cmd.extend(arg)
                else:
                    cmd.append(arg)
            cmd.insert(0, module)

            if os.name == 'nt':
                try:
                    pid = subprocess.Popen(cmd).pid
                except Exception as e:
                    return (False, 'Failed to launch process "{}"! {}'.format(module, str(e)))
            else:
                try:
                    pid = subprocess.Popen(cmd, stdin=DEVNULL, stdout=DEVNULL, stderr=subprocess.STDOUT).pid
                except Exception as e:
                    return (False, 'Failed to launch process "{}"! {}'.format(module, str(e)))

        return (True, '')

    def Ring(self, topic, command):
        """ Ring(topic, command) """
        command = "{{0}} {1}".format(topic, command)
        self._send_command(command, None)
