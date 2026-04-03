__author__     = "Bob Hood"
__copyright__  = "Copyright (C) 2015 LightWaveDigital"
__version__    = "1.0"
__maintainer__ = "Bob Hood"
__email__      = "bobhood@lightwave3d.com"
__status__     = "Production"

import os
import uuid

from lwcommandport import CommandPort

class Modeler(CommandPort):
    """
    The Command Port Modeler class provides interaction with a LightWave
    Modeler process.

    The Modeler process can be running, in which case the class will accept
    arguments that specify how to contact the process, or the Modeler process
    can be launched by this class instance, which will then auto-configure
    itself to communicate with the new process.

    Processes launched by the Command Port Modeler class are not managed
    further after they have been launched.  Each process must be manually
    terminated, or, of its command system allows, terminated from a command
    issued by the Command Port Modeler class (e.g., Quit()).

    Args:
        To interact with a running process, the 'address' and 'port' keywords
        will indicate the end point to which to send commands.  The 'address'
        value can specify a DNS host name, a raw IPv4 or IPv6 address, or
        'localhost' for interactions within the local domain.  The 'port' value
        can be a literal integer (in a valid port range), or it can be a symbolic
        port value, either of which should match the port value used when
        originally launching the Modeler process.  For example:

            >>> Modeler(address="localhost", port="Jenny")

        The Command Port Modeler class also has the ability to launch a local
        LightWave Modeler process.  This is the fallback mode when 'address'
        and 'port' are not provided.  In its simplest form, you can simply
        create an instance:

            >>> Modeler()
            Launched Modeler process with args "--command-port=LW_4FC54CAF"

        This will generate a unique symbolic port value for the new process,
        and will pursue platform-dependent means of automatically locating
        the installed LightWave product.  Under Windows, this will be an
        entry in the Registry; OS X will look for the installation under
        the /Applications/LightWaveDigital folder; Linux will search /opt/LightWaveDigital.

        Currently, the automatic location code will search for the most
        recent version of LightWave by default.  You may override this 
        by providing a 'version' keyword, specifying the version to filter:

            >>> Modeler(version='2018')
            Launched Modeler process with args "--command-port=LW_EC6D2B1B"

        If automatic location fails, you may specify an explicit path to
        an executable to launch by using the 'module' keyword:

            Modeler(module='<path_to_executable>')

        This will cause a unique symbolic port value to be created for the
        new process.  If you want to provide an explicit port value, you
        can include the 'port' keyword:

            Modeler(module='<path_to_executable>', port='<port_to_use>')

        You can pass additional command-line arguments to the new process
        by declaring them prior to any keywords:

            >>> Modeler('-0', '--license-server')
            Launched Modeler process with args "-0 --license-server --command-port=LW_09613799"

        This construction will trigger an automatic search for the Modeler
        executable, with a symbolic port value automatically generated and
        added to the command-line options provided.

        The 'address' and 'module' keywords each trigger a different operation
        in the Command Port Modeler class, and are therefore mutually exclusive.
        If you mistakenly provide both, the 'address' keyword will be ignored
        unless you also include 'port'; otherwise, the launch mode will be used
        and 'module' (if provided) will be processed.
    """
    def __init__(self, *args, **kwargs):
        address = kwargs.get("address", None)
        port = kwargs.get("port", None)
        if (address is not None) and (port is not None):
           super(Modeler, self).__init__(address, port)
        else:
            module = kwargs.get("module", None)
            if (module is None) or (not os.path.exists(module)):
                module = 'Modeler'.lower()
            if port is None:
                port = 'LW_%s' % (str(uuid.uuid4()).split('-')[0]).upper()
            if len(args) == 0:
                launch_args = kwargs.get("args", [])
            else:
                launch_args = []
                for arg in args:
                    if isinstance(arg, (list, tuple)):
                        launch_args.extend(arg)
                    else:
                        launch_args.append(arg)

            ver = kwargs.get("version", None)

            port_arg = None
            for i in range(len(launch_args)):
                if 'command-port' in launch_args[i]:
                    port_arg = launch_args[i]
            if port_arg is None:
                launch_args.append('--command-port=%s' % port)

            result, msg = self._launch(module, launch_args, version=ver)

            if result:
                print('Launched Modeler process with args "{0}"'.format(' '.join(launch_args)))
                super(Modeler, self).__init__("localhost", port)
            else:
                raise Exception(msg)

    def mergepoints(self):
        """
        Name: Merge Points
        Call: mergepoints()
        """
        self._send_command("mergepoints")
    def weldpoints(self):
        """
        Name: Weld Points
        Call: weldpoints()
        """
        self._send_command("weldpoints")
    def weldaverage(self):
        """
        Name: Weld Points to Average
        Call: weldaverage()
        """
        self._send_command("weldaverage")
    def unweld(self):
        """
        Name: Unweld Points
        Call: unweld()
        """
        self._send_command("unweld")
    def make4patch(self):
        """
        Name: Make Spline Patch
        Call: make4patch()
        """
        self._send_command("make4patch")
    def togglepatches(self):
        """
        Name: Toggle Faces / SubPatches
        Call: togglepatches()
        """
        self._send_command("togglepatches")
    def pathextrude(self):
        """
        Name: Motion Path Extrude
        Call: pathextrude()
        """
        self._send_command("pathextrude")
    def pathclone(self):
        """
        Name: Motion Path Clone
        Call: pathclone()
        """
        self._send_command("pathclone")
    def railextrude(self):
        """
        Name: Rail Extrude
        Call: railextrude()
        """
        self._send_command("railextrude")
    def railclone(self, *args):
        """
        Name: Rail Clone
        Call: railclone(filename, name, colorspace)
        """
        self._send_command("railclone", args)
    def flip(self):
        """
        Name: Flip Polygons
        Call: flip()
        """
        self._send_command("flip")
    def splitpols(self):
        """
        Name: Split Polygons
        Call: splitpols()
        """
        self._send_command("splitpols")
    def mergepols(self):
        """
        Name: Merge Polygons
        Call: mergepols()
        """
        self._send_command("mergepols")
    def removepols(self):
        """
        Name: Remove Polygons
        Call: removepols()
        """
        self._send_command("removepols")
    def unifypols(self):
        """
        Name: Unify Polygons
        Call: unifypols()
        """
        self._send_command("unifypols")
    def alignpols(self):
        """
        Name: Align Polygons
        Call: alignpols()
        """
        self._send_command("alignpols")
    def triple(self):
        """
        Name: Convert Polygons to Triangles
        Call: triple()
        """
        self._send_command("triple")
    def changesurface(self):
        """
        Name: Change Surface
        Call: changesurface()
        """
        self._send_command("changesurface")
    def changepart(self):
        """
        Name: Change Part Name
        Call: changepart()
        """
        self._send_command("changepart")
    def toggleccstart(self):
        """
        Name: Begin Control Point On/Off
        Call: toggleccstart()
        """
        self._send_command("toggleccstart")
    def toggleccend(self):
        """
        Name: End Control Point On/Off
        Call: toggleccend()
        """
        self._send_command("toggleccend")
    def axisdrill(self):
        """
        Name: Template Drill
        Call: axisdrill()
        """
        self._send_command("axisdrill")
    def soliddrill(self):
        """
        Name: Solid Drill
        Call: soliddrill()
        """
        self._send_command("soliddrill")
    def boolean(self):
        """
        Name: Boolean CSG
        Call: boolean()
        """
        self._send_command("boolean")
    def freezecurves(self):
        """
        Name: Freeze Curves & Patches
        Call: freezecurves()
        """
        self._send_command("freezecurves")
    def smoothcurves(self):
        """
        Name: Smooth Curves
        Call: smoothcurves()
        """
        self._send_command("smoothcurves")
    def subdivide(self):
        """
        Name: Subdivide Polygons
        Call: subdivide()
        """
        self._send_command("subdivide")
    def copy(self):
        """
        Name: Copy
        Call: copy()
        """
        self._send_command("copy")
    def cut(self):
        """
        Name: Cut
        Call: cut()
        """
        self._send_command("cut")
    def delete(self):
        """
        Name: Delete
        Call: delete()
        """
        self._send_command("delete")
    def paste(self):
        """
        Name: Paste
        Call: paste()
        """
        self._send_command("paste")
    def undo(self):
        """
        Name: Undo
        Call: undo()
        """
        self._send_command("undo")
    def redo(self):
        """
        Name: Redo
        Call: redo()
        """
        self._send_command("redo")
    def new(self):
        """
        Name: New Object
        Call: new()
        """
        self._send_command("new")
    def close(self):
        """
        Name: Close Object
        Call: close()
        """
        self._send_command("close")
    def close_all(self):
        """
        Name: Close All Objects
        Call: close_all()
        """
        self._send_command("close_all")
    def load(self, *args):
        """
        Name: Load Object
        Call: load(filename)
        """
        self._send_command("load", args)
    def revert(self):
        """
        Name: Revert Current Object
        Call: revert()
        """
        self._send_command("revert")
    def save(self):
        """
        Name: Save Object
        Call: save()
        """
        self._send_command("save")
    def sel_invert(self):
        """
        Name: Invert Selection
        Call: sel_invert()
        """
        self._send_command("sel_invert")
    def sel_hide(self):
        """
        Name: Hide Selected
        Call: sel_hide()
        """
        self._send_command("sel_hide")
    def sel_unhide(self):
        """
        Name: Unhide All (Make Visible)
        Call: sel_unhide()
        """
        self._send_command("sel_unhide")
    def invert_hide(self, *args):
        """
        Name: Invert Hidden
        Call: invert_hide(path)
        """
        self._send_command("invert_hide", args)
    def cmdseq(self, *args):
        """ cmdseq(server, argument) """
        self._send_command("cmdseq", args)
    def meshedit(self, *args):
        """ meshedit(server) """
        self._send_command("meshedit", args)
    def jitter(self):
        """
        Name: Jitter
        Call: jitter()
        """
        self._send_command("jitter")
    def smscale(self):
        """
        Name: Smooth Scale
        Call: smscale()
        """
        self._send_command("smscale")
    def quantize(self):
        """
        Name: Quantize
        Call: quantize()
        """
        self._send_command("quantize")
    def center(self):
        """
        Name: Center All
        Call: center()
        """
        self._send_command("center")
    def smooth(self):
        """
        Name: Smooth
        Call: smooth()
        """
        self._send_command("smooth")
    def setviewcenter(self):
        """
        Name: Smooth
        Call: setviewcenter()
        """
        self._send_command("setviewcenter")
    def setviewrotation(self):
        """
        Name: Smooth
        Call: setviewrotation()
        """
        self._send_command("setviewrotation")
    def setviewscale(self):
        """
        Name: Smooth
        Call: setviewscale()
        """
        self._send_command("setviewscale")
    def setviewzoffset(self):
        """
        Name: Smooth
        Call: setviewzoffset()
        """
        self._send_command("setviewzoffset")
    def setviewposlookat(self):
        """
        Name: Smooth
        Call: setviewposlookat()
        """
        self._send_command("setviewposlookat")
    def setviewdirection(self):
        """
        Name: Smooth
        Call: setviewdirection()
        """
        self._send_command("setviewdirection")
    def clone(self):
        """
        Name: Clone
        Call: clone()
        """
        self._send_command("clone")
    def array(self):
        """
        Name: Array
        Call: array()
        """
        self._send_command("array")
    def skinpols(self):
        """
        Name: Create Skin
        Call: skinpols()
        """
        self._send_command("skinpols")
    def morphpols(self):
        """
        Name: Morph Polygons
        Call: morphpols()
        """
        self._send_command("morphpols")
    def plugin(self):
        """
        Name: Add Plugins
        Call: plugin()
        """
        self._send_command("plugin")
    def exit(self):
        """
        Name: Quit
        Call: exit()
        """
        self._send_command("exit")
