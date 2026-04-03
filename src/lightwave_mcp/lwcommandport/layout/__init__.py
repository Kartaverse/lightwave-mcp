__author__     = "Bob Hood"
__copyright__  = "Copyright (C) 2015 LightWaveDigital"
__version__    = "1.0"
__maintainer__ = "Bob Hood"
__email__      = "bobhood@lightwave3d.com"
__status__     = "Production"

import os
import uuid

from lwcommandport import CommandPort

class Layout(CommandPort):
    """
    The Command Port Layout class provides interaction with a LightWave
    Layout process.

    The Layout process can be running, in which case the class will accept
    arguments that specify how to contact the process, or the Layout process
    can be launched by this class instance, which will then auto-configure
    itself to communicate with the new process.

    Processes launched by the Command Port Layout class are not managed
    further after they have been launched.  Each process must be manually
    terminated, or, of its command system allows, terminated from a command
    issued by the Command Port Layout class (e.g., Quit()).

    Args:
        To interact with a running process, the 'address' and 'port' keywords
        will indicate the end point to which to send commands.  The 'address'
        value can specify a DNS host name, a raw IPv4 or IPv6 address, or
        'localhost' for interactions within the local domain.  The 'port' value
        can be a literal integer (in a valid port range), or it can be a symbolic
        port value, either of which should match the port value used when
        originally launching the Layout process.  For example:

            >>> Layout(address="localhost", port="Jenny")

        The Command Port Layout class also has the ability to launch a local
        LightWave Layout process.  This is the fallback mode when 'address'
        and 'port' are not provided.  In its simplest form, you can simply
        create an instance:

            >>> Layout()
            Launched Layout process with args "--command-port=LW_4FC54CAF"

        This will generate a unique symbolic port value for the new process,
        and will pursue platform-dependent means of automatically locating
        the installed LightWave product.  Under Windows, this will be an
        entry in the Registry; OS X will look for the installation under
        the /Applications/LightWaveDigital folder; Linux will search /opt/LightWaveDigital.

        Currently, the automatic location code will search for the most
        recent version of LightWave by default.  You may override this 
        by providing a 'version' keyword, specifying the version to filter:

            >>> Layout(version='2018')
            Launched Layout process with args "--command-port=LW_EC6D2B1B"

        If automatic location fails, you may specify an explicit path to
        an executable to launch by using the 'module' keyword:

            Layout(module='<path_to_executable>')

        This will cause a unique symbolic port value to be created for the
        new process.  If you want to provide an explicit port value, you
        can include the 'port' keyword:

            Layout(module='<path_to_executable>', port='<port_to_use>')

        You can pass additional command-line arguments to the new process
        by declaring them prior to any keywords:

            >>> Layout('-0', '--license-server')
            Launched Layout process with args "-0 --license-server --command-port=LW_09613799"

        This construction will trigger an automatic search for the Layout
        executable, with a symbolic port value automatically generated and
        added to the command-line options provided.

        The 'address' and 'module' keywords each trigger a different operation
        in the Command Port Layout class, and are therefore mutually exclusive.
        If you mistakenly provide both, the 'address' keyword will be ignored
        unless you also include 'port'; otherwise, the launch mode will be used
        and 'module' (if provided) will be processed.
    """
    def __init__(self, *args, **kwargs):
        address = kwargs.get("address", None)
        port = kwargs.get("port", None)
        if (address is not None) and (port is not None):
           super(Layout, self).__init__(address, port)
        else:
            module = kwargs.get("module", None)
            if (module is None) or (not os.path.exists(module)):
                module = 'Layout'.lower()
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
                print('Launched Layout process with args "{0}"'.format(' '.join(launch_args)))
                super(Layout, self).__init__("localhost", port)
            else:
                raise Exception(msg)

    def LoadScene(self, *args):
        """ LoadScene(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LoadScene(): expected (filename)" % len(args))
        self._send_command("LoadScene", args)
    def ClearScene(self):
        """ ClearScene() """
        self._send_command("ClearScene")
    def PreClearScene(self):
        """ PreClearScene() """
        self._send_command("PreClearScene")
    def PreLoadScene(self):
        """ PreLoadScene() """
        self._send_command("PreLoadScene")
    def RecentScenes(self):
        """ RecentScenes() """
        self._send_command("RecentScenes")
    def LoadFromScene(self, *args):
        """ LoadFromScene(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LoadFromScene(): expected (filename)" % len(args))
        self._send_command("LoadFromScene", args)
    def LoadElementsFromScene(self, *args):
        """ LoadElementsFromScene(elements, filename) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command LoadElementsFromScene(): expected (elements, filename)" % len(args))
        self._send_command("LoadElementsFromScene", args)
    def SaveScene(self):
        """ SaveScene() """
        self._send_command("SaveScene")
    def PreSaveScene(self):
        """ PreSaveScene() """
        self._send_command("PreSaveScene")
    def SaveSceneAs(self, *args):
        """ SaveSceneAs(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveSceneAs(): expected (filename)" % len(args))
        self._send_command("SaveSceneAs", args)
    def About(self):
        """ About() """
        self._send_command("About")
    def Quit(self):
        """ Quit() """
        self._send_command("Quit")
    def OnLine(self):
        """ OnLine() """
        self._send_command("OnLine")
    def OffLine(self):
        """ OffLine() """
        self._send_command("OffLine")
    def EnterUnlockCode(self):
        """ EnterUnlockCode() """
        self._send_command("EnterUnlockCode")
    def ReportABug(self):
        """ ReportABug() """
        self._send_command("ReportABug")
    def RequestAFeature(self):
        """ RequestAFeature() """
        self._send_command("RequestAFeature")
    def SaveLWSC_4_0(self, *args):
        """ SaveLWSC_4_0(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveLWSC_4_0(): expected (filename)" % len(args))
        self._send_command("SaveLWSC_4_0", args)
    def SaveLWSC_5_6(self, *args):
        """ SaveLWSC_5_6(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveLWSC_5_6(): expected (filename)" % len(args))
        self._send_command("SaveLWSC_5_6", args)
    def SaveLWSC_6_0(self, *args):
        """ SaveLWSC_6_0(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveLWSC_6_0(): expected (filename)" % len(args))
        self._send_command("SaveLWSC_6_0", args)
    def SaveLWSC_9_2(self, *args):
        """ SaveLWSC_9_2(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveLWSC_9_2(): expected (filename)" % len(args))
        self._send_command("SaveLWSC_9_2", args)
    def SaveLWSC_9_5(self, *args):
        """ SaveLWSC_9_5(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveLWSC_9_5(): expected (filename)" % len(args))
        self._send_command("SaveLWSC_9_5", args)
    def SaveLWSC_2024(self, *args):
        """ SaveLWSC_2024(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveLWSC_2024(): expected (filename)" % len(args))
        self._send_command("SaveLWSC_2024", args)
    def SaveLWSC1(self, *args):
        """ SaveLWSC1(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveLWSC1(): expected (filename)" % len(args))
        self._send_command("SaveLWSC1", args)
    def SaveLWSC3(self, *args):
        """ SaveLWSC3(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveLWSC3(): expected (filename)" % len(args))
        self._send_command("SaveLWSC3", args)
    def SaveLWSC4(self, *args):
        """ SaveLWSC4(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveLWSC4(): expected (filename)" % len(args))
        self._send_command("SaveLWSC4", args)
    def RevertScene(self):
        """ RevertScene() """
        self._send_command("RevertScene")
    def SaveSceneCopy(self, *args):
        """ SaveSceneCopy(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveSceneCopy(): expected (filename)" % len(args))
        self._send_command("SaveSceneCopy", args)
    def Model(self):
        """ Model() """
        self._send_command("Model")
    def Synchronize(self):
        """ Synchronize() """
        self._send_command("Synchronize")
    def SaveViewportImage(self, *args):
        """ SaveViewportImage(filename, imagetype, viewportnumber, scale) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command SaveViewportImage(): expected (filename, imagetype, viewportnumber, scale)" % len(args))
        self._send_command("SaveViewportImage", args)
    def Statistics(self):
        """ Statistics() """
        self._send_command("Statistics")
    def CommandInput(self, *args):
        """ CommandInput(command) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command CommandInput(): expected (command)" % len(args))
        self._send_command("CommandInput", args)
    def ClientCommandInput(self, *args):
        """ ClientCommandInput(client, command) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command ClientCommandInput(): expected (client, command)" % len(args))
        self._send_command("ClientCommandInput", args)
    def CommandHistory(self):
        """ CommandHistory() """
        self._send_command("CommandHistory")
    def Locale(self):
        """ Locale() """
        self._send_command("Locale")
    def vmapbrowser(self):
        """ vmapbrowser() """
        self._send_command("vmapbrowser")
    def Layout_SetWindowPos(self, *args):
        """ Layout_SetWindowPos(x, y) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command Layout_SetWindowPos(): expected (x, y)" % len(args))
        self._send_command("Layout_SetWindowPos", args)
    def Layout_WindowActivate(self):
        """ Layout_WindowActivate() """
        self._send_command("Layout_WindowActivate")
    def Layout_SetWindowSize(self, *args):
        """ Layout_SetWindowSize(width, height) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command Layout_SetWindowSize(): expected (width, height)" % len(args))
        self._send_command("Layout_SetWindowSize", args)
    def Scene_SetWindowPos(self, *args):
        """ Scene_SetWindowPos(x, y) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command Scene_SetWindowPos(): expected (x, y)" % len(args))
        self._send_command("Scene_SetWindowPos", args)
    def Scene_SetWindowSize(self, *args):
        """ Scene_SetWindowSize(width, height) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command Scene_SetWindowSize(): expected (width, height)" % len(args))
        self._send_command("Scene_SetWindowSize", args)
    def Item_SetWindowPos(self, *args):
        """ Item_SetWindowPos(x, y) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command Item_SetWindowPos(): expected (x, y)" % len(args))
        self._send_command("Item_SetWindowPos", args)
    def Modeler_Unsupported(self):
        """ Modeler_Unsupported() """
        self._send_command("Modeler_Unsupported")
    def ItemProperties(self):
        """ ItemProperties() """
        self._send_command("ItemProperties")
    def SelectItem(self, *args):
        """ SelectItem(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SelectItem(): expected (itemid)" % len(args))
        self._send_command("SelectItem", args)
    def SelectEditObject(self, *args):
        """ SelectEditObject(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SelectEditObject(): expected (itemid)" % len(args))
        self._send_command("SelectEditObject", args)
    def AddToSelection(self, *args):
        """ AddToSelection(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddToSelection(): expected (itemid)" % len(args))
        self._send_command("AddToSelection", args)
    def RemoveFromSelection(self, *args):
        """ RemoveFromSelection(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RemoveFromSelection(): expected (itemid)" % len(args))
        self._send_command("RemoveFromSelection", args)
    def EnableFromSelection(self, *args):
        """ EnableFromSelection(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command EnableFromSelection(): expected (itemid)" % len(args))
        self._send_command("EnableFromSelection", args)
    def DisableFromSelection(self, *args):
        """ DisableFromSelection(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DisableFromSelection(): expected (itemid)" % len(args))
        self._send_command("DisableFromSelection", args)
    def MeshElementSelect(self):
        """ MeshElementSelect() """
        self._send_command("MeshElementSelect")
    def EditObjects(self):
        """ EditObjects() """
        self._send_command("EditObjects")
    def EditBones(self):
        """ EditBones() """
        self._send_command("EditBones")
    def EditLights(self):
        """ EditLights() """
        self._send_command("EditLights")
    def EditCameras(self):
        """ EditCameras() """
        self._send_command("EditCameras")
    def SelectByName(self, *args):
        """ SelectByName(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SelectByName(): expected (name)" % len(args))
        self._send_command("SelectByName", args)
    def SelectByPartialName(self, *args):
        """ SelectByPartialName(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SelectByPartialName(): expected (name)" % len(args))
        self._send_command("SelectByPartialName", args)
    def PreviousItem(self):
        """ PreviousItem() """
        self._send_command("PreviousItem")
    def NextItem(self):
        """ NextItem() """
        self._send_command("NextItem")
    def FirstItem(self):
        """ FirstItem() """
        self._send_command("FirstItem")
    def LastItem(self):
        """ LastItem() """
        self._send_command("LastItem")
    def SelectParent(self):
        """ SelectParent() """
        self._send_command("SelectParent")
    def SelectChild(self):
        """ SelectChild() """
        self._send_command("SelectChild")
    def PreviousSibling(self):
        """ PreviousSibling() """
        self._send_command("PreviousSibling")
    def NextSibling(self):
        """ NextSibling() """
        self._send_command("NextSibling")
    def ClearSelected(self):
        """ ClearSelected() """
        self._send_command("ClearSelected")
    def Rename(self, *args):
        """ Rename(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command Rename(): expected (name)" % len(args))
        self._send_command("Rename", args)
    def RenameLayer(self, *args):
        """ RenameLayer(layer, name) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command RenameLayer(): expected (layer, name)" % len(args))
        self._send_command("RenameLayer", args)
    def RenameLayerID(self, *args):
        """ RenameLayerID(objectid, layer, name) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command RenameLayerID(): expected (objectid, layer, name)" % len(args))
        self._send_command("RenameLayerID", args)
    def ReplaceWithObject(self, *args):
        """ ReplaceWithObject(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ReplaceWithObject(): expected (filename)" % len(args))
        self._send_command("ReplaceWithObject", args)
    def ReplaceObjectLayer(self, *args):
        """ ReplaceObjectLayer(layer, filename) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command ReplaceObjectLayer(): expected (layer, filename)" % len(args))
        self._send_command("ReplaceObjectLayer", args)
    def ReplaceWithNull(self, *args):
        """ ReplaceWithNull(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ReplaceWithNull(): expected (name)" % len(args))
        self._send_command("ReplaceWithNull", args)
    def Clone(self, *args):
        """ Clone(clones) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command Clone(): expected (clones)" % len(args))
        self._send_command("Clone", args)
    def DuplicateProceduralGeometry(self, *args):
        """ DuplicateProceduralGeometry(copys) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DuplicateProceduralGeometry(): expected (copys)" % len(args))
        self._send_command("DuplicateProceduralGeometry", args)
    def CloneToObject(self, *args):
        """ CloneToObject(objectidto, objectidfrom) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command CloneToObject(): expected (objectidto, objectidfrom)" % len(args))
        self._send_command("CloneToObject", args)
    def Mirror(self):
        """ Mirror() """
        self._send_command("Mirror")
    def ItemActive(self, *args):
        """ ItemActive(active) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ItemActive(): expected (active)" % len(args))
        self._send_command("ItemActive", args)
    def ItemLock(self, *args):
        """ ItemLock(locked) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ItemLock(): expected (locked)" % len(args))
        self._send_command("ItemLock", args)
    def ItemVisibility(self, *args):
        """ ItemVisibility(visibility) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ItemVisibility(): expected (visibility)" % len(args))
        self._send_command("ItemVisibility", args)
    def ItemColor(self, *args):
        """ ItemColor(color) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ItemColor(): expected (color)" % len(args))
        self._send_command("ItemColor", args)
    def ItemShowChildren(self, *args):
        """ ItemShowChildren(itemid, show) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command ItemShowChildren(): expected (itemid, show)" % len(args))
        self._send_command("ItemShowChildren", args)
    def ItemShowChannels(self, *args):
        """ ItemShowChannels(itemid, show) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command ItemShowChannels(): expected (itemid, show)" % len(args))
        self._send_command("ItemShowChannels", args)
    def ObjectMeshGroup(self, *args):
        """ ObjectMeshGroup(groupid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ObjectMeshGroup(): expected (groupid)" % len(args))
        self._send_command("ObjectMeshGroup", args)
    def ItemUnlock(self, *args):
        """ ItemUnlock(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ItemUnlock(): expected (itemid)" % len(args))
        self._send_command("ItemUnlock", args)
    def ItemIconScale(self, *args):
        """ ItemIconScale(scale) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ItemIconScale(): expected (scale)" % len(args))
        self._send_command("ItemIconScale", args)
    def SelectAllBones(self):
        """ SelectAllBones() """
        self._send_command("SelectAllBones")
    def AddBone(self, *args):
        """ AddBone(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddBone(): expected (name)" % len(args))
        self._send_command("AddBone", args)
    def AddChildBone(self, *args):
        """ AddChildBone(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddChildBone(): expected (name)" % len(args))
        self._send_command("AddChildBone", args)
    def DrawBones(self):
        """ DrawBones() """
        self._send_command("DrawBones")
    def DrawChildBones(self):
        """ DrawChildBones() """
        self._send_command("DrawChildBones")
    def AddJoint(self, *args):
        """ AddJoint(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddJoint(): expected (name)" % len(args))
        self._send_command("AddJoint", args)
    def AddChildJoint(self, *args):
        """ AddChildJoint(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddChildJoint(): expected (name)" % len(args))
        self._send_command("AddChildJoint", args)
    def DrawJoints(self):
        """ DrawJoints() """
        self._send_command("DrawJoints")
    def DrawChildJoints(self):
        """ DrawChildJoints() """
        self._send_command("DrawChildJoints")
    def MoveTool(self):
        """ MoveTool() """
        self._send_command("MoveTool")
    def RotateTool(self):
        """ RotateTool() """
        self._send_command("RotateTool")
    def SizeTool(self):
        """ SizeTool() """
        self._send_command("SizeTool")
    def StretchTool(self):
        """ StretchTool() """
        self._send_command("StretchTool")
    def SquashTool(self):
        """ SquashTool() """
        self._send_command("SquashTool")
    def MovePivotTool(self):
        """ MovePivotTool() """
        self._send_command("MovePivotTool")
    def RotatePivotTool(self):
        """ RotatePivotTool() """
        self._send_command("RotatePivotTool")
    def MovePathTool(self):
        """ MovePathTool() """
        self._send_command("MovePathTool")
    def MorphAmountTool(self):
        """ MorphAmountTool() """
        self._send_command("MorphAmountTool")
    def MoveTCBTool(self):
        """ MoveTCBTool() """
        self._send_command("MoveTCBTool")
    def RestLengthTool(self):
        """ RestLengthTool() """
        self._send_command("RestLengthTool")
    def ConeAngleTool(self):
        """ ConeAngleTool() """
        self._send_command("ConeAngleTool")
    def CameraZoomTool(self):
        """ CameraZoomTool() """
        self._send_command("CameraZoomTool")
    def AdjustRegionTool(self):
        """ AdjustRegionTool() """
        self._send_command("AdjustRegionTool")
    def LightIntensityTool(self):
        """ LightIntensityTool() """
        self._send_command("LightIntensityTool")
    def ChangeTool(self):
        """ ChangeTool() """
        self._send_command("ChangeTool")
    def Reset(self):
        """ Reset() """
        self._send_command("Reset")
    def Undo(self):
        """ Undo() """
        self._send_command("Undo")
    def Redo(self):
        """ Redo() """
        self._send_command("Redo")
    def Numeric(self):
        """ Numeric() """
        self._send_command("Numeric")
    def DisplayOptions(self):
        """ DisplayOptions() """
        self._send_command("DisplayOptions")
    def OpenGLOptions(self):
        """ OpenGLOptions() """
        self._send_command("OpenGLOptions")
    def NavigationOptions(self):
        """ NavigationOptions() """
        self._send_command("NavigationOptions")
    def TopView(self):
        """ TopView() """
        self._send_command("TopView")
    def BottomView(self):
        """ BottomView() """
        self._send_command("BottomView")
    def ToggleTopBottomView(self):
        """ ToggleTopBottomView() """
        self._send_command("ToggleTopBottomView")
    def BackView(self):
        """ BackView() """
        self._send_command("BackView")
    def FrontView(self):
        """ FrontView() """
        self._send_command("FrontView")
    def ToggleBackFrontView(self):
        """ ToggleBackFrontView() """
        self._send_command("ToggleBackFrontView")
    def RightView(self):
        """ RightView() """
        self._send_command("RightView")
    def LeftView(self):
        """ LeftView() """
        self._send_command("LeftView")
    def ToggleRightLeftView(self):
        """ ToggleRightLeftView() """
        self._send_command("ToggleRightLeftView")
    def XYView(self):
        """ XYView() """
        self._send_command("XYView")
    def XZView(self):
        """ XZView() """
        self._send_command("XZView")
    def ZYView(self):
        """ ZYView() """
        self._send_command("ZYView")
    def PerspectiveView(self):
        """ PerspectiveView() """
        self._send_command("PerspectiveView")
    def LightView(self):
        """ LightView() """
        self._send_command("LightView")
    def CameraView(self):
        """ CameraView() """
        self._send_command("CameraView")
    def TogglePerspectiveCameraView(self):
        """ TogglePerspectiveCameraView() """
        self._send_command("TogglePerspectiveCameraView")
    def SchematicView(self):
        """ SchematicView() """
        self._send_command("SchematicView")
    def MotionBlurDOFPreview(self):
        """ MotionBlurDOFPreview() """
        self._send_command("MotionBlurDOFPreview")
    def BoneWeightShade(self):
        """ BoneWeightShade() """
        self._send_command("BoneWeightShade")
    def BoneXRay(self):
        """ BoneXRay() """
        self._send_command("BoneXRay")
    def ViewHeadlight(self):
        """ ViewHeadlight() """
        self._send_command("ViewHeadlight")
    def InteractiveMotionBlurDOFPreview(self):
        """ InteractiveMotionBlurDOFPreview() """
        self._send_command("InteractiveMotionBlurDOFPreview")
    def ViewLayout(self, *args):
        """ ViewLayout(layout) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ViewLayout(): expected (layout)" % len(args))
        self._send_command("ViewLayout", args)
    def UndockPreview(self, *args):
        """ UndockPreview(on_off) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command UndockPreview(): expected (on_off)" % len(args))
        self._send_command("UndockPreview", args)
    def UndockPreviewCameraResolution(self, *args):
        """ UndockPreviewCameraResolution(on_off) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command UndockPreviewCameraResolution(): expected (on_off)" % len(args))
        self._send_command("UndockPreviewCameraResolution", args)
    def UndockPreviewWidth(self, *args):
        """ UndockPreviewWidth(width) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command UndockPreviewWidth(): expected (width)" % len(args))
        self._send_command("UndockPreviewWidth", args)
    def UndockPreviewHeight(self, *args):
        """ UndockPreviewHeight(height) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command UndockPreviewHeight(): expected (height)" % len(args))
        self._send_command("UndockPreviewHeight", args)
    def PreviewScaleLevel(self, *args):
        """ PreviewScaleLevel(level) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PreviewScaleLevel(): expected (level)" % len(args))
        self._send_command("PreviewScaleLevel", args)
    def PreviousViewLayout(self):
        """ PreviousViewLayout() """
        self._send_command("PreviousViewLayout")
    def NextViewLayout(self):
        """ NextViewLayout() """
        self._send_command("NextViewLayout")
    def SingleView(self):
        """ SingleView() """
        self._send_command("SingleView")
    def SaveViewLayout(self):
        """ SaveViewLayout() """
        self._send_command("SaveViewLayout")
    def CenterMouse(self):
        """ CenterMouse() """
        self._send_command("CenterMouse")
    def CenterItem(self):
        """ CenterItem() """
        self._send_command("CenterItem")
    def ViewPositionSet(self, *args):
        """ ViewPositionSet(view, x, y, z) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command ViewPositionSet(): expected (view, x, y, z)" % len(args))
        self._send_command("ViewPositionSet", args)
    def ViewPositionReset(self, *args):
        """ ViewPositionReset(view) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ViewPositionReset(): expected (view)" % len(args))
        self._send_command("ViewPositionReset", args)
    def ViewRotationSet(self, *args):
        """ ViewRotationSet(view, h, p, b) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command ViewRotationSet(): expected (view, h, p, b)" % len(args))
        self._send_command("ViewRotationSet", args)
    def ViewRotationReset(self, *args):
        """ ViewRotationReset(view) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ViewRotationReset(): expected (view)" % len(args))
        self._send_command("ViewRotationReset", args)
    def ViewZoomSet(self, *args):
        """ ViewZoomSet(view, zoom) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command ViewZoomSet(): expected (view, zoom)" % len(args))
        self._send_command("ViewZoomSet", args)
    def ViewZoomReset(self, *args):
        """ ViewZoomReset(view) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ViewZoomReset(): expected (view)" % len(args))
        self._send_command("ViewZoomReset", args)
    def ViewStore(self, *args):
        """ ViewStore(view) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ViewStore(): expected (view)" % len(args))
        self._send_command("ViewStore", args)
    def ViewRecall(self, *args):
        """ ViewRecall(view) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ViewRecall(): expected (view)" % len(args))
        self._send_command("ViewRecall", args)
    def FitAll(self):
        """ FitAll() """
        self._send_command("FitAll")
    def FitSelected(self):
        """ FitSelected() """
        self._send_command("FitSelected")
    def FitAllViews(self):
        """ FitAllViews() """
        self._send_command("FitAllViews")
    def FitSelectedViews(self):
        """ FitSelectedViews() """
        self._send_command("FitSelectedViews")
    def ZoomIn(self):
        """ ZoomIn() """
        self._send_command("ZoomIn")
    def ZoomOut(self):
        """ ZoomOut() """
        self._send_command("ZoomOut")
    def ZoomInX2(self):
        """ ZoomInX2() """
        self._send_command("ZoomInX2")
    def ZoomOutX2(self):
        """ ZoomOutX2() """
        self._send_command("ZoomOutX2")
    def GridSize(self, *args):
        """ GridSize(size) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command GridSize(): expected (size)" % len(args))
        self._send_command("GridSize", args)
    def IncreaseGrid(self):
        """ IncreaseGrid() """
        self._send_command("IncreaseGrid")
    def DecreaseGrid(self):
        """ DecreaseGrid() """
        self._send_command("DecreaseGrid")
    def DynamicUpdate(self, *args):
        """ DynamicUpdate(level) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DynamicUpdate(): expected (level)" % len(args))
        self._send_command("DynamicUpdate", args)
    def ShowMotionPaths(self):
        """ ShowMotionPaths() """
        self._send_command("ShowMotionPaths")
    def ShowHandles(self):
        """ ShowHandles() """
        self._send_command("ShowHandles")
    def ShowIKChains(self):
        """ ShowIKChains() """
        self._send_command("ShowIKChains")
    def ShowCages(self):
        """ ShowCages() """
        self._send_command("ShowCages")
    def CopyToPerspective(self, *args):
        """ CopyToPerspective(on_off) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command CopyToPerspective(): expected (on_off)" % len(args))
        self._send_command("CopyToPerspective", args)
    def ShowSafeAreas(self):
        """ ShowSafeAreas() """
        self._send_command("ShowSafeAreas")
    def ShowFieldChart(self):
        """ ShowFieldChart() """
        self._send_command("ShowFieldChart")
    def ShowTargetLines(self):
        """ ShowTargetLines() """
        self._send_command("ShowTargetLines")
    def BoundingBoxThreshold(self, *args):
        """ BoundingBoxThreshold(threshold) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BoundingBoxThreshold(): expected (threshold)" % len(args))
        self._send_command("BoundingBoxThreshold", args)
    def HardwareShadingMethod(self, *args):
        """ HardwareShadingMethod(hw_shading_type_name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command HardwareShadingMethod(): expected (hw_shading_type_name)" % len(args))
        self._send_command("HardwareShadingMethod", args)
    def HardwareGeometryAccelerationMethod(self, *args):
        """ HardwareGeometryAccelerationMethod(hw_geometry_acceleration_type_name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command HardwareGeometryAccelerationMethod(): expected (hw_geometry_acceleration_type_name)" % len(args))
        self._send_command("HardwareGeometryAccelerationMethod", args)
    def AboutOpenGL(self):
        """ AboutOpenGL() """
        self._send_command("AboutOpenGL")
    def MatchViewport(self):
        """ MatchViewport() """
        self._send_command("MatchViewport")
    def NavigationActivateMKB(self):
        """ NavigationActivateMKB() """
        self._send_command("NavigationActivateMKB")
    def NavigationDeactivateMKB(self):
        """ NavigationDeactivateMKB() """
        self._send_command("NavigationDeactivateMKB")
    def UpdateMotion(self):
        """ UpdateMotion() """
        self._send_command("UpdateMotion")
    def DirtyMotion(self, *args):
        """ DirtyMotion(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DirtyMotion(): expected (itemid)" % len(args))
        self._send_command("DirtyMotion", args)
    def Redraw(self):
        """ Redraw() """
        self._send_command("Redraw")
    def RedrawNow(self):
        """ RedrawNow() """
        self._send_command("RedrawNow")
    def Refresh(self):
        """ Refresh() """
        self._send_command("Refresh")
    def RefreshNow(self):
        """ RefreshNow() """
        self._send_command("RefreshNow")
    def FlushUI(self):
        """ FlushUI() """
        self._send_command("FlushUI")
    def InteractiveMode(self, *args):
        """ InteractiveMode(on_off) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command InteractiveMode(): expected (on_off)" % len(args))
        self._send_command("InteractiveMode", args)
    def SchematicPosition(self, *args):
        """ SchematicPosition(x, y) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command SchematicPosition(): expected (x, y)" % len(args))
        self._send_command("SchematicPosition", args)
    def SceneEditorOpen(self):
        """ SceneEditorOpen() """
        self._send_command("SceneEditorOpen")
    def SceneEditorInstance(self):
        """ SceneEditorInstance() """
        self._send_command("SceneEditorInstance")
    def SceneEditor(self):
        """ SceneEditor() """
        self._send_command("SceneEditor")
    def ViewportObjectOption(self):
        """ ViewportObjectOption() """
        self._send_command("ViewportObjectOption")
    def VPRTab(self):
        """ VPRTab() """
        self._send_command("VPRTab")
    def PreviewWindow(self):
        """ PreviewWindow() """
        self._send_command("PreviewWindow")
    def GraphEditor(self):
        """ GraphEditor() """
        self._send_command("GraphEditor")
    def SaveOptions(self):
        """ SaveOptions() """
        self._send_command("SaveOptions")
    def SurfaceEditor(self):
        """ SurfaceEditor() """
        self._send_command("SurfaceEditor")
    def ImageEditor(self):
        """ ImageEditor() """
        self._send_command("ImageEditor")
    def VIPER(self):
        """ VIPER() """
        self._send_command("VIPER")
    def Presets(self):
        """ Presets() """
        self._send_command("Presets")
    def StudioPanel(self):
        """ StudioPanel() """
        self._send_command("StudioPanel")
    def DeviceManagerPanel(self):
        """ DeviceManagerPanel() """
        self._send_command("DeviceManagerPanel")
    def ControlBoothPanel(self):
        """ ControlBoothPanel() """
        self._send_command("ControlBoothPanel")
    def FlatMenuPopup(self):
        """ FlatMenuPopup() """
        self._send_command("FlatMenuPopup")
    def EnableXH(self):
        """ EnableXH() """
        self._send_command("EnableXH")
    def EnableYP(self):
        """ EnableYP() """
        self._send_command("EnableYP")
    def EnableZB(self):
        """ EnableZB() """
        self._send_command("EnableZB")
    def LockAxis(self, *args):
        """ LockAxis(axis, on_off) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command LockAxis(): expected (axis, on_off)" % len(args))
        self._send_command("LockAxis", args)
    def WorldCoordinateSystem(self):
        """ WorldCoordinateSystem() """
        self._send_command("WorldCoordinateSystem")
    def ParentCoordinateSystem(self):
        """ ParentCoordinateSystem() """
        self._send_command("ParentCoordinateSystem")
    def LocalCoordinateSystem(self):
        """ LocalCoordinateSystem() """
        self._send_command("LocalCoordinateSystem")
    def MotionOptions(self):
        """ MotionOptions() """
        self._send_command("MotionOptions")
    def ComponentPanel(self):
        """ ComponentPanel() """
        self._send_command("ComponentPanel")
    def GoToFrame(self, *args):
        """ GoToFrame(frame) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command GoToFrame(): expected (frame)" % len(args))
        self._send_command("GoToFrame", args)
    def GoToFirstFrame(self):
        """ GoToFirstFrame() """
        self._send_command("GoToFirstFrame")
    def GoToLastFrame(self):
        """ GoToLastFrame() """
        self._send_command("GoToLastFrame")
    def PreviousFrame(self):
        """ PreviousFrame() """
        self._send_command("PreviousFrame")
    def NextFrame(self):
        """ NextFrame() """
        self._send_command("NextFrame")
    def PreviousKey(self):
        """ PreviousKey() """
        self._send_command("PreviousKey")
    def NextKey(self):
        """ NextKey() """
        self._send_command("NextKey")
    def Pause(self):
        """ Pause() """
        self._send_command("Pause")
    def PlayBackward(self):
        """ PlayBackward() """
        self._send_command("PlayBackward")
    def PlayForward(self):
        """ PlayForward() """
        self._send_command("PlayForward")
    def FirstFrame(self, *args):
        """ FirstFrame(frame) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FirstFrame(): expected (frame)" % len(args))
        self._send_command("FirstFrame", args)
    def LastFrame(self, *args):
        """ LastFrame(frame) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LastFrame(): expected (frame)" % len(args))
        self._send_command("LastFrame", args)
    def FrameStep(self, *args):
        """ FrameStep(frames) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FrameStep(): expected (frames)" % len(args))
        self._send_command("FrameStep", args)
    def CreateKey(self, *args):
        """ CreateKey(time, scope, channelmask) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command CreateKey(): expected (time, scope, channelmask)" % len(args))
        self._send_command("CreateKey", args)
    def DeleteKey(self, *args):
        """ DeleteKey(time) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DeleteKey(): expected (time)" % len(args))
        self._send_command("DeleteKey", args)
    def AutoKey(self, *args):
        """ AutoKey(active) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AutoKey(): expected (active)" % len(args))
        self._send_command("AutoKey", args)
    def AutoKeyFixedFrame(self, *args):
        """ AutoKeyFixedFrame(autokey_fixed_frame) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AutoKeyFixedFrame(): expected (autokey_fixed_frame)" % len(args))
        self._send_command("AutoKeyFixedFrame", args)
    def Position(self, *args):
        """ Position(x, y, z) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command Position(): expected (x, y, z)" % len(args))
        self._send_command("Position", args)
    def Rotation(self, *args):
        """ Rotation(h, p, b) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command Rotation(): expected (h, p, b)" % len(args))
        self._send_command("Rotation", args)
    def Scale(self, *args):
        """ Scale(x, y, z) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command Scale(): expected (x, y, z)" % len(args))
        self._send_command("Scale", args)
    def AddPosition(self, *args):
        """ AddPosition(x, y, z) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command AddPosition(): expected (x, y, z)" % len(args))
        self._send_command("AddPosition", args)
    def AddRotation(self, *args):
        """ AddRotation(h, p, b) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command AddRotation(): expected (h, p, b)" % len(args))
        self._send_command("AddRotation", args)
    def AddScale(self, *args):
        """ AddScale(x, y, z) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command AddScale(): expected (x, y, z)" % len(args))
        self._send_command("AddScale", args)
    def PivotPosition(self, *args):
        """ PivotPosition(x, y, z) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command PivotPosition(): expected (x, y, z)" % len(args))
        self._send_command("PivotPosition", args)
    def PivotRotation(self, *args):
        """ PivotRotation(h, p, b) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command PivotRotation(): expected (h, p, b)" % len(args))
        self._send_command("PivotRotation", args)
    def RecordPivotRotation(self):
        """ RecordPivotRotation() """
        self._send_command("RecordPivotRotation")
    def SetTCB(self, *args):
        """ SetTCB(t, c, b) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command SetTCB(): expected (t, c, b)" % len(args))
        self._send_command("SetTCB", args)
    def PositionByItemID(self, *args):
        """ PositionByItemID(itemid, x, y, z) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command PositionByItemID(): expected (itemid, x, y, z)" % len(args))
        self._send_command("PositionByItemID", args)
    def RotationByItemID(self, *args):
        """ RotationByItemID(itemid, h, p, b) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command RotationByItemID(): expected (itemid, h, p, b)" % len(args))
        self._send_command("RotationByItemID", args)
    def ScaleByItemID(self, *args):
        """ ScaleByItemID(itemid, x, y, z) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command ScaleByItemID(): expected (itemid, x, y, z)" % len(args))
        self._send_command("ScaleByItemID", args)
    def AddPositionByItemID(self, *args):
        """ AddPositionByItemID(itemid, x, y, z) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command AddPositionByItemID(): expected (itemid, x, y, z)" % len(args))
        self._send_command("AddPositionByItemID", args)
    def AddRotationByItemID(self, *args):
        """ AddRotationByItemID(itemid, h, p, b) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command AddRotationByItemID(): expected (itemid, h, p, b)" % len(args))
        self._send_command("AddRotationByItemID", args)
    def AddScaleByItemID(self, *args):
        """ AddScaleByItemID(itemid, x, y, z) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command AddScaleByItemID(): expected (itemid, x, y, z)" % len(args))
        self._send_command("AddScaleByItemID", args)
    def AddEnvelope(self, *args):
        """ AddEnvelope(channel) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddEnvelope(): expected (channel)" % len(args))
        self._send_command("AddEnvelope", args)
    def RemoveEnvelope(self, *args):
        """ RemoveEnvelope(channel) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RemoveEnvelope(): expected (channel)" % len(args))
        self._send_command("RemoveEnvelope", args)
    def LoadMotion(self, *args):
        """ LoadMotion(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LoadMotion(): expected (filename)" % len(args))
        self._send_command("LoadMotion", args)
    def SaveMotion(self, *args):
        """ SaveMotion(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveMotion(): expected (filename)" % len(args))
        self._send_command("SaveMotion", args)
    def RotationOrder(self, *args):
        """ RotationOrder(order) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RotationOrder(): expected (order)" % len(args))
        self._send_command("RotationOrder", args)
    def ParentItem(self, *args):
        """ ParentItem(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ParentItem(): expected (itemid)" % len(args))
        self._send_command("ParentItem", args)
    def TargetItem(self, *args):
        """ TargetItem(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command TargetItem(): expected (itemid)" % len(args))
        self._send_command("TargetItem", args)
    def PoleItem(self, *args):
        """ PoleItem(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PoleItem(): expected (itemid)" % len(args))
        self._send_command("PoleItem", args)
    def SplineItem(self, *args):
        """ SplineItem(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SplineItem(): expected (itemid)" % len(args))
        self._send_command("SplineItem", args)
    def PositionItem(self, *args):
        """ PositionItem(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PositionItem(): expected (itemid)" % len(args))
        self._send_command("PositionItem", args)
    def PositionItemWorld(self, *args):
        """ PositionItemWorld(state) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PositionItemWorld(): expected (state)" % len(args))
        self._send_command("PositionItemWorld", args)
    def PositionItemBlendMethod(self, *args):
        """ PositionItemBlendMethod(method) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PositionItemBlendMethod(): expected (method)" % len(args))
        self._send_command("PositionItemBlendMethod", args)
    def PositionItemBlend(self, *args):
        """ PositionItemBlend(blend) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PositionItemBlend(): expected (blend)" % len(args))
        self._send_command("PositionItemBlend", args)
    def RotationItem(self, *args):
        """ RotationItem(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RotationItem(): expected (itemid)" % len(args))
        self._send_command("RotationItem", args)
    def RotationItemWorld(self, *args):
        """ RotationItemWorld(state) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RotationItemWorld(): expected (state)" % len(args))
        self._send_command("RotationItemWorld", args)
    def RotationItemBlendMethod(self, *args):
        """ RotationItemBlendMethod(method) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RotationItemBlendMethod(): expected (method)" % len(args))
        self._send_command("RotationItemBlendMethod", args)
    def RotationItemBlend(self, *args):
        """ RotationItemBlend(blend) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RotationItemBlend(): expected (blend)" % len(args))
        self._send_command("RotationItemBlend", args)
    def ScaleItem(self, *args):
        """ ScaleItem(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ScaleItem(): expected (itemid)" % len(args))
        self._send_command("ScaleItem", args)
    def ScaleItemWorld(self, *args):
        """ ScaleItemWorld(state) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ScaleItemWorld(): expected (state)" % len(args))
        self._send_command("ScaleItemWorld", args)
    def ScaleItemBlendMethod(self, *args):
        """ ScaleItemBlendMethod(method) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ScaleItemBlendMethod(): expected (method)" % len(args))
        self._send_command("ScaleItemBlendMethod", args)
    def ScaleItemBlend(self, *args):
        """ ScaleItemBlend(blend) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ScaleItemBlend(): expected (blend)" % len(args))
        self._send_command("ScaleItemBlend", args)
    def PathAlignLookAhead(self, *args):
        """ PathAlignLookAhead(time) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PathAlignLookAhead(): expected (time)" % len(args))
        self._send_command("PathAlignLookAhead", args)
    def PathAlignMaxLookSteps(self, *args):
        """ PathAlignMaxLookSteps(steps) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PathAlignMaxLookSteps(): expected (steps)" % len(args))
        self._send_command("PathAlignMaxLookSteps", args)
    def PathAlignReliableDist(self, *args):
        """ PathAlignReliableDist(distance) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PathAlignReliableDist(): expected (distance)" % len(args))
        self._send_command("PathAlignReliableDist", args)
    def ClosedSpline(self):
        """ ClosedSpline() """
        self._send_command("ClosedSpline")
    def FlipSideSpline(self):
        """ FlipSideSpline() """
        self._send_command("FlipSideSpline")
    def SplineFit(self, *args):
        """ SplineFit(fit) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SplineFit(): expected (fit)" % len(args))
        self._send_command("SplineFit", args)
    def UnaffectedByIK(self):
        """ UnaffectedByIK() """
        self._send_command("UnaffectedByIK")
    def EnableDeformations(self):
        """ EnableDeformations() """
        self._send_command("EnableDeformations")
    def EnableIK(self):
        """ EnableIK() """
        self._send_command("EnableIK")
    def EnableMC(self):
        """ EnableMC() """
        self._send_command("EnableMC")
    def GoalItem(self, *args):
        """ GoalItem(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command GoalItem(): expected (itemid)" % len(args))
        self._send_command("GoalItem", args)
    def FullTimeIK(self):
        """ FullTimeIK() """
        self._send_command("FullTimeIK")
    def GoalStrength(self, *args):
        """ GoalStrength(strength) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command GoalStrength(): expected (strength)" % len(args))
        self._send_command("GoalStrength", args)
    def GoalObjective(self, *args):
        """ GoalObjective(objective_type) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command GoalObjective(): expected (objective_type)" % len(args))
        self._send_command("GoalObjective", args)
    def SoftIK(self, *args):
        """ SoftIK(type) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SoftIK(): expected (type)" % len(args))
        self._send_command("SoftIK", args)
    def SoftIKDistanceType(self, *args):
        """ SoftIKDistanceType(type) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SoftIKDistanceType(): expected (type)" % len(args))
        self._send_command("SoftIKDistanceType", args)
    def SoftIKMin(self, *args):
        """ SoftIKMin(min_dist) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SoftIKMin(): expected (min_dist)" % len(args))
        self._send_command("SoftIKMin", args)
    def SoftIKMax(self, *args):
        """ SoftIKMax(max_dist) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SoftIKMax(): expected (max_dist)" % len(args))
        self._send_command("SoftIKMax", args)
    def IKInitialState(self, *args):
        """ IKInitialState(state) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command IKInitialState(): expected (state)" % len(args))
        self._send_command("IKInitialState", args)
    def IKInitialStateFrame(self, *args):
        """ IKInitialStateFrame(frame) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command IKInitialStateFrame(): expected (frame)" % len(args))
        self._send_command("IKInitialStateFrame", args)
    def IKFKBlending(self, *args):
        """ IKFKBlending(blend) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command IKFKBlending(): expected (blend)" % len(args))
        self._send_command("IKFKBlending", args)
    def UseIKChainVals(self, *args):
        """ UseIKChainVals(state) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command UseIKChainVals(): expected (state)" % len(args))
        self._send_command("UseIKChainVals", args)
    def MatchGoalOrientation(self):
        """ MatchGoalOrientation() """
        self._send_command("MatchGoalOrientation")
    def KeepGoalWithinReach(self):
        """ KeepGoalWithinReach() """
        self._send_command("KeepGoalWithinReach")
    def RecordMinPosition(self):
        """ RecordMinPosition() """
        self._send_command("RecordMinPosition")
    def RecordMaxPosition(self):
        """ RecordMaxPosition() """
        self._send_command("RecordMaxPosition")
    def RecordMinAngles(self):
        """ RecordMinAngles() """
        self._send_command("RecordMinAngles")
    def RecordMaxAngles(self):
        """ RecordMaxAngles() """
        self._send_command("RecordMaxAngles")
    def RecordMinScale(self):
        """ RecordMinScale() """
        self._send_command("RecordMinScale")
    def RecordMaxScale(self):
        """ RecordMaxScale() """
        self._send_command("RecordMaxScale")
    def XController(self, *args):
        """ XController(controller) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command XController(): expected (controller)" % len(args))
        self._send_command("XController", args)
    def YController(self, *args):
        """ YController(controller) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command YController(): expected (controller)" % len(args))
        self._send_command("YController", args)
    def ZController(self, *args):
        """ ZController(controller) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ZController(): expected (controller)" % len(args))
        self._send_command("ZController", args)
    def HController(self, *args):
        """ HController(controller) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command HController(): expected (controller)" % len(args))
        self._send_command("HController", args)
    def PController(self, *args):
        """ PController(controller) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PController(): expected (controller)" % len(args))
        self._send_command("PController", args)
    def BController(self, *args):
        """ BController(controller) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BController(): expected (controller)" % len(args))
        self._send_command("BController", args)
    def SXController(self, *args):
        """ SXController(controller) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SXController(): expected (controller)" % len(args))
        self._send_command("SXController", args)
    def SYController(self, *args):
        """ SYController(controller) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SYController(): expected (controller)" % len(args))
        self._send_command("SYController", args)
    def SZController(self, *args):
        """ SZController(controller) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SZController(): expected (controller)" % len(args))
        self._send_command("SZController", args)
    def XLimits(self, *args):
        """ XLimits(min, max) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command XLimits(): expected (min, max)" % len(args))
        self._send_command("XLimits", args)
    def YLimits(self, *args):
        """ YLimits(min, max) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command YLimits(): expected (min, max)" % len(args))
        self._send_command("YLimits", args)
    def ZLimits(self, *args):
        """ ZLimits(min, max) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command ZLimits(): expected (min, max)" % len(args))
        self._send_command("ZLimits", args)
    def HLimits(self, *args):
        """ HLimits(min, max) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command HLimits(): expected (min, max)" % len(args))
        self._send_command("HLimits", args)
    def PLimits(self, *args):
        """ PLimits(min, max) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command PLimits(): expected (min, max)" % len(args))
        self._send_command("PLimits", args)
    def BLimits(self, *args):
        """ BLimits(min, max) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command BLimits(): expected (min, max)" % len(args))
        self._send_command("BLimits", args)
    def SXLimits(self, *args):
        """ SXLimits(min, max) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command SXLimits(): expected (min, max)" % len(args))
        self._send_command("SXLimits", args)
    def SYLimits(self, *args):
        """ SYLimits(min, max) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command SYLimits(): expected (min, max)" % len(args))
        self._send_command("SYLimits", args)
    def SZLimits(self, *args):
        """ SZLimits(min, max) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command SZLimits(): expected (min, max)" % len(args))
        self._send_command("SZLimits", args)
    def LimitX(self):
        """ LimitX() """
        self._send_command("LimitX")
    def LimitY(self):
        """ LimitY() """
        self._send_command("LimitY")
    def LimitZ(self):
        """ LimitZ() """
        self._send_command("LimitZ")
    def LimitH(self):
        """ LimitH() """
        self._send_command("LimitH")
    def LimitP(self):
        """ LimitP() """
        self._send_command("LimitP")
    def LimitB(self):
        """ LimitB() """
        self._send_command("LimitB")
    def LimitSX(self):
        """ LimitSX() """
        self._send_command("LimitSX")
    def LimitSY(self):
        """ LimitSY() """
        self._send_command("LimitSY")
    def LimitSZ(self):
        """ LimitSZ() """
        self._send_command("LimitSZ")
    def XStiffness(self, *args):
        """ XStiffness(stiffness) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command XStiffness(): expected (stiffness)" % len(args))
        self._send_command("XStiffness", args)
    def YStiffness(self, *args):
        """ YStiffness(stiffness) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command YStiffness(): expected (stiffness)" % len(args))
        self._send_command("YStiffness", args)
    def ZStiffness(self, *args):
        """ ZStiffness(stiffness) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ZStiffness(): expected (stiffness)" % len(args))
        self._send_command("ZStiffness", args)
    def HStiffness(self, *args):
        """ HStiffness(stiffness) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command HStiffness(): expected (stiffness)" % len(args))
        self._send_command("HStiffness", args)
    def PStiffness(self, *args):
        """ PStiffness(stiffness) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PStiffness(): expected (stiffness)" % len(args))
        self._send_command("PStiffness", args)
    def BStiffness(self, *args):
        """ BStiffness(stiffness) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BStiffness(): expected (stiffness)" % len(args))
        self._send_command("BStiffness", args)
    def SXStiffness(self, *args):
        """ SXStiffness(stiffness) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SXStiffness(): expected (stiffness)" % len(args))
        self._send_command("SXStiffness", args)
    def SYStiffness(self, *args):
        """ SYStiffness(stiffness) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SYStiffness(): expected (stiffness)" % len(args))
        self._send_command("SYStiffness", args)
    def SZStiffness(self, *args):
        """ SZStiffness(stiffness) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SZStiffness(): expected (stiffness)" % len(args))
        self._send_command("SZStiffness", args)
    def XTransform(self, *args):
        """ XTransform(multiplier, offset) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command XTransform(): expected (multiplier, offset)" % len(args))
        self._send_command("XTransform", args)
    def YTransform(self, *args):
        """ YTransform(multiplier, offset) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command YTransform(): expected (multiplier, offset)" % len(args))
        self._send_command("YTransform", args)
    def ZTransform(self, *args):
        """ ZTransform(multiplier, offset) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command ZTransform(): expected (multiplier, offset)" % len(args))
        self._send_command("ZTransform", args)
    def HTransform(self, *args):
        """ HTransform(multiplier, offset) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command HTransform(): expected (multiplier, offset)" % len(args))
        self._send_command("HTransform", args)
    def PTransform(self, *args):
        """ PTransform(multiplier, offset) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command PTransform(): expected (multiplier, offset)" % len(args))
        self._send_command("PTransform", args)
    def BTransform(self, *args):
        """ BTransform(multiplier, offset) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command BTransform(): expected (multiplier, offset)" % len(args))
        self._send_command("BTransform", args)
    def SXTransform(self, *args):
        """ SXTransform(multiplier, offset) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command SXTransform(): expected (multiplier, offset)" % len(args))
        self._send_command("SXTransform", args)
    def SYTransform(self, *args):
        """ SYTransform(multiplier, offset) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command SYTransform(): expected (multiplier, offset)" % len(args))
        self._send_command("SYTransform", args)
    def SZTransform(self, *args):
        """ SZTransform(multiplier, offset) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command SZTransform(): expected (multiplier, offset)" % len(args))
        self._send_command("SZTransform", args)
    def XFollow(self, *args):
        """ XFollow(channel) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command XFollow(): expected (channel)" % len(args))
        self._send_command("XFollow", args)
    def YFollow(self, *args):
        """ YFollow(channel) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command YFollow(): expected (channel)" % len(args))
        self._send_command("YFollow", args)
    def ZFollow(self, *args):
        """ ZFollow(channel) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ZFollow(): expected (channel)" % len(args))
        self._send_command("ZFollow", args)
    def HFollow(self, *args):
        """ HFollow(channel) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command HFollow(): expected (channel)" % len(args))
        self._send_command("HFollow", args)
    def PFollow(self, *args):
        """ PFollow(channel) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PFollow(): expected (channel)" % len(args))
        self._send_command("PFollow", args)
    def BFollow(self, *args):
        """ BFollow(channel) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BFollow(): expected (channel)" % len(args))
        self._send_command("BFollow", args)
    def SXFollow(self, *args):
        """ SXFollow(channel) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SXFollow(): expected (channel)" % len(args))
        self._send_command("SXFollow", args)
    def SYFollow(self, *args):
        """ SYFollow(channel) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SYFollow(): expected (channel)" % len(args))
        self._send_command("SYFollow", args)
    def SZFollow(self, *args):
        """ SZFollow(channel) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SZFollow(): expected (channel)" % len(args))
        self._send_command("SZFollow", args)
    def MakePreview(self):
        """ MakePreview() """
        self._send_command("MakePreview")
    def PlayPreview(self):
        """ PlayPreview() """
        self._send_command("PlayPreview")
    def FreePreview(self):
        """ FreePreview() """
        self._send_command("FreePreview")
    def LoadPreview(self):
        """ LoadPreview() """
        self._send_command("LoadPreview")
    def SavePreview(self):
        """ SavePreview() """
        self._send_command("SavePreview")
    def PreviewOptions(self):
        """ PreviewOptions() """
        self._send_command("PreviewOptions")
    def PreviewFirstFrame(self, *args):
        """ PreviewFirstFrame(frame) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PreviewFirstFrame(): expected (frame)" % len(args))
        self._send_command("PreviewFirstFrame", args)
    def PreviewLastFrame(self, *args):
        """ PreviewLastFrame(frame) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PreviewLastFrame(): expected (frame)" % len(args))
        self._send_command("PreviewLastFrame", args)
    def PreviewFrameStep(self, *args):
        """ PreviewFrameStep(frames) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PreviewFrameStep(): expected (frames)" % len(args))
        self._send_command("PreviewFrameStep", args)
    def PreviewFrameRateScale(self, *args):
        """ PreviewFrameRateScale(scale) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PreviewFrameRateScale(): expected (scale)" % len(args))
        self._send_command("PreviewFrameRateScale", args)
    def AmbientOcclusionShadows(self, *args):
        """ AmbientOcclusionShadows(on_off) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AmbientOcclusionShadows(): expected (on_off)" % len(args))
        self._send_command("AmbientOcclusionShadows", args)
    def AmbientOcclusionRange(self, *args):
        """ AmbientOcclusionRange(range) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AmbientOcclusionRange(): expected (range)" % len(args))
        self._send_command("AmbientOcclusionRange", args)
    def SaveTransformed(self, *args):
        """ SaveTransformed(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveTransformed(): expected (filename)" % len(args))
        self._send_command("SaveTransformed", args)
    def LoadObject(self, *args):
        """ LoadObject(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LoadObject(): expected (filename)" % len(args))
        self._send_command("LoadObject", args)
    def ClearAudio(self):
        """ ClearAudio() """
        self._send_command("ClearAudio")
    def LoadAudio(self):
        """ LoadAudio() """
        self._send_command("LoadAudio")
    def PlayAudio(self):
        """ PlayAudio() """
        self._send_command("PlayAudio")
    def ToggleAudioScrubbing(self):
        """ ToggleAudioScrubbing() """
        self._send_command("ToggleAudioScrubbing")
    def RenderOptions(self):
        """ RenderOptions() """
        self._send_command("RenderOptions")
    def RenderProperties(self):
        """ RenderProperties() """
        self._send_command("RenderProperties")
    def GlobalIllumination(self):
        """ GlobalIllumination() """
        self._send_command("GlobalIllumination")
    def NetRender(self):
        """ NetRender() """
        self._send_command("NetRender")
    def AutoFrameAdvance(self, *args):
        """ AutoFrameAdvance(enable) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AutoFrameAdvance(): expected (enable)" % len(args))
        self._send_command("AutoFrameAdvance", args)
    def EnableVIPER(self):
        """ EnableVIPER() """
        self._send_command("EnableVIPER")
    def RayTraceShadows(self, *args):
        """ RayTraceShadows(enable) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RayTraceShadows(): expected (enable)" % len(args))
        self._send_command("RayTraceShadows", args)
    def RayTraceReflection(self, *args):
        """ RayTraceReflection(enable) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RayTraceReflection(): expected (enable)" % len(args))
        self._send_command("RayTraceReflection", args)
    def RayTraceRefraction(self, *args):
        """ RayTraceRefraction(enable) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RayTraceRefraction(): expected (enable)" % len(args))
        self._send_command("RayTraceRefraction", args)
    def RayTraceTransparency(self):
        """ RayTraceTransparency() """
        self._send_command("RayTraceTransparency")
    def RayTraceOcclusion(self):
        """ RayTraceOcclusion() """
        self._send_command("RayTraceOcclusion")
    def RayRecursionLimit(self, *args):
        """ RayRecursionLimit(limit) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RayRecursionLimit(): expected (limit)" % len(args))
        self._send_command("RayRecursionLimit", args)
    def TransparencyRecursionLimit(self, *args):
        """ TransparencyRecursionLimit(limit) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command TransparencyRecursionLimit(): expected (limit)" % len(args))
        self._send_command("TransparencyRecursionLimit", args)
    def ReflectionRecursionLimit(self, *args):
        """ ReflectionRecursionLimit(limit) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ReflectionRecursionLimit(): expected (limit)" % len(args))
        self._send_command("ReflectionRecursionLimit", args)
    def RefractionRecursionLimit(self, *args):
        """ RefractionRecursionLimit(limit) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RefractionRecursionLimit(): expected (limit)" % len(args))
        self._send_command("RefractionRecursionLimit", args)
    def RayPrecision(self, *args):
        """ RayPrecision(precision) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RayPrecision(): expected (precision)" % len(args))
        self._send_command("RayPrecision", args)
    def RayCutoff(self, *args):
        """ RayCutoff(cutoff) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RayCutoff(): expected (cutoff)" % len(args))
        self._send_command("RayCutoff", args)
    def ReflectionSamples(self, *args):
        """ ReflectionSamples(samples) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ReflectionSamples(): expected (samples)" % len(args))
        self._send_command("ReflectionSamples", args)
    def RefractionSamples(self, *args):
        """ RefractionSamples(samples) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RefractionSamples(): expected (samples)" % len(args))
        self._send_command("RefractionSamples", args)
    def SubsurfaceScatteringSamples(self, *args):
        """ SubsurfaceScatteringSamples(samples) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SubsurfaceScatteringSamples(): expected (samples)" % len(args))
        self._send_command("SubsurfaceScatteringSamples", args)
    def LightSamples(self, *args):
        """ LightSamples(samples) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LightSamples(): expected (samples)" % len(args))
        self._send_command("LightSamples", args)
    def GlobalMipmapMultiplier(self, *args):
        """ GlobalMipmapMultiplier(multiplier) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command GlobalMipmapMultiplier(): expected (multiplier)" % len(args))
        self._send_command("GlobalMipmapMultiplier", args)
    def GlobalEdgeMultiplier(self, *args):
        """ GlobalEdgeMultiplier(multiplier) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command GlobalEdgeMultiplier(): expected (multiplier)" % len(args))
        self._send_command("GlobalEdgeMultiplier", args)
    def EdgeVerticalPoints(self, *args):
        """ EdgeVerticalPoints(verticalpoints) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command EdgeVerticalPoints(): expected (verticalpoints)" % len(args))
        self._send_command("EdgeVerticalPoints", args)
    def DiffuseLimit(self, *args):
        """ DiffuseLimit(diffuse_limit) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DiffuseLimit(): expected (diffuse_limit)" % len(args))
        self._send_command("DiffuseLimit", args)
    def ReflectionLimit(self, *args):
        """ ReflectionLimit(reflection_limit) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ReflectionLimit(): expected (reflection_limit)" % len(args))
        self._send_command("ReflectionLimit", args)
    def RefractionLimit(self, *args):
        """ RefractionLimit(refraction_limit) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RefractionLimit(): expected (refraction_limit)" % len(args))
        self._send_command("RefractionLimit", args)
    def EnableDespike(self, *args):
        """ EnableDespike(enable) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command EnableDespike(): expected (enable)" % len(args))
        self._send_command("EnableDespike", args)
    def DespikeTolerance(self, *args):
        """ DespikeTolerance(tolerance) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DespikeTolerance(): expected (tolerance)" % len(args))
        self._send_command("DespikeTolerance", args)
    def RenderThreads(self, *args):
        """ RenderThreads(threads) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RenderThreads(): expected (threads)" % len(args))
        self._send_command("RenderThreads", args)
    def RenderTileSize(self, *args):
        """ RenderTileSize(tilesize) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RenderTileSize(): expected (tilesize)" % len(args))
        self._send_command("RenderTileSize", args)
    def RenderAlgorithm(self, *args):
        """ RenderAlgorithm(algorithm) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RenderAlgorithm(): expected (algorithm)" % len(args))
        self._send_command("RenderAlgorithm", args)
    def RenderMode(self, *args):
        """ RenderMode(renderintegrator) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RenderMode(): expected (renderintegrator)" % len(args))
        self._send_command("RenderMode", args)
    def HDRFilter(self, *args):
        """ HDRFilter(mode) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command HDRFilter(): expected (mode)" % len(args))
        self._send_command("HDRFilter", args)
    def NoiseFilter(self):
        """ NoiseFilter() """
        self._send_command("NoiseFilter")
    def NoiseFilterOptions(self):
        """ NoiseFilterOptions() """
        self._send_command("NoiseFilterOptions")
    def SaveAnimation(self):
        """ SaveAnimation() """
        self._send_command("SaveAnimation")
    def SaveAnimationName(self):
        """ SaveAnimationName() """
        self._send_command("SaveAnimationName")
    def SaveAnimationServer(self, *args):
        """ SaveAnimationServer(server) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveAnimationServer(): expected (server)" % len(args))
        self._send_command("SaveAnimationServer", args)
    def UnPreMultiplyAlpha(self):
        """ UnPreMultiplyAlpha() """
        self._send_command("UnPreMultiplyAlpha")
    def SaveRGB(self):
        """ SaveRGB() """
        self._send_command("SaveRGB")
    def SaveRGBPrefix(self):
        """ SaveRGBPrefix() """
        self._send_command("SaveRGBPrefix")
    def SaveRGBServer(self, *args):
        """ SaveRGBServer(server) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveRGBServer(): expected (server)" % len(args))
        self._send_command("SaveRGBServer", args)
    def SaveAlpha(self):
        """ SaveAlpha() """
        self._send_command("SaveAlpha")
    def SaveAlphaPrefix(self):
        """ SaveAlphaPrefix() """
        self._send_command("SaveAlphaPrefix")
    def SaveAlphaServer(self, *args):
        """ SaveAlphaServer(server) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveAlphaServer(): expected (server)" % len(args))
        self._send_command("SaveAlphaServer", args)
    def MultilayerEnabled(self, *args):
        """ MultilayerEnabled(on_off) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command MultilayerEnabled(): expected (on_off)" % len(args))
        self._send_command("MultilayerEnabled", args)
    def MultilayerUseOutputPath(self, *args):
        """ MultilayerUseOutputPath(on_off) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command MultilayerUseOutputPath(): expected (on_off)" % len(args))
        self._send_command("MultilayerUseOutputPath", args)
    def MultilayerPath(self, *args):
        """ MultilayerPath(path) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command MultilayerPath(): expected (path)" % len(args))
        self._send_command("MultilayerPath", args)
    def MultilayerFilename(self, *args):
        """ MultilayerFilename(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command MultilayerFilename(): expected (filename)" % len(args))
        self._send_command("MultilayerFilename", args)
    def AddCustomBuffer(self, *args):
        """ AddCustomBuffer(buffer_name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddCustomBuffer(): expected (buffer_name)" % len(args))
        self._send_command("AddCustomBuffer", args)
    def RemoveCustomBuffer(self, *args):
        """ RemoveCustomBuffer(buffer_name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RemoveCustomBuffer(): expected (buffer_name)" % len(args))
        self._send_command("RemoveCustomBuffer", args)
    def LoadRenderSettings(self, *args):
        """ LoadRenderSettings(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LoadRenderSettings(): expected (filename)" % len(args))
        self._send_command("LoadRenderSettings", args)
    def SaveRenderSettings(self, *args):
        """ SaveRenderSettings(filename, flags, name, comment) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command SaveRenderSettings(): expected (filename, flags, name, comment)" % len(args))
        self._send_command("SaveRenderSettings", args)
    def SaveRenderPreset(self, *args):
        """ SaveRenderPreset(flags, name, comment) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command SaveRenderPreset(): expected (flags, name, comment)" % len(args))
        self._send_command("SaveRenderPreset", args)
    def SaveBufferSet(self):
        """ SaveBufferSet() """
        self._send_command("SaveBufferSet")
    def SaveBufferSetPreset(self):
        """ SaveBufferSetPreset() """
        self._send_command("SaveBufferSetPreset")
    def LoadBufferSet(self):
        """ LoadBufferSet() """
        self._send_command("LoadBufferSet")
    def SyncBufferSet(self):
        """ SyncBufferSet() """
        self._send_command("SyncBufferSet")
    def RenderSelected(self):
        """ RenderSelected() """
        self._send_command("RenderSelected")
    def RenderFrame(self):
        """ RenderFrame() """
        self._send_command("RenderFrame")
    def RenderScene(self):
        """ RenderScene() """
        self._send_command("RenderScene")
    def AbortRender(self):
        """ AbortRender() """
        self._send_command("AbortRender")
    def TestViewportObject(self):
        """ TestViewportObject() """
        self._send_command("TestViewportObject")
    def SetRenderDisplay(self):
        """ SetRenderDisplay() """
        self._send_command("SetRenderDisplay")
    def RenderDisplayOptions(self):
        """ RenderDisplayOptions() """
        self._send_command("RenderDisplayOptions")
    def ExtRendererOptions(self):
        """ ExtRendererOptions() """
        self._send_command("ExtRendererOptions")
    def ExtRendererPick(self):
        """ ExtRendererPick() """
        self._send_command("ExtRendererPick")
    def UseZMinimumMaximum(self):
        """ UseZMinimumMaximum() """
        self._send_command("UseZMinimumMaximum")
    def ZBufferMinimum(self, *args):
        """ ZBufferMinimum(z_minimum) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ZBufferMinimum(): expected (z_minimum)" % len(args))
        self._send_command("ZBufferMinimum", args)
    def ZBufferMaximum(self, *args):
        """ ZBufferMaximum(z_maximum) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ZBufferMaximum(): expected (z_maximum)" % len(args))
        self._send_command("ZBufferMaximum", args)
    def CalculateAllNormals(self, *args):
        """ CalculateAllNormals(on_off) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command CalculateAllNormals(): expected (on_off)" % len(args))
        self._send_command("CalculateAllNormals", args)
    def SelectAllObjects(self):
        """ SelectAllObjects() """
        self._send_command("SelectAllObjects")
    def ClearAllObjects(self):
        """ ClearAllObjects() """
        self._send_command("ClearAllObjects")
    def LoadObjectLayer(self, *args):
        """ LoadObjectLayer(layer, filename) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command LoadObjectLayer(): expected (layer, filename)" % len(args))
        self._send_command("LoadObjectLayer", args)
    def AddNull(self, *args):
        """ AddNull(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddNull(): expected (name)" % len(args))
        self._send_command("AddNull", args)
    def SaveAllObjects(self):
        """ SaveAllObjects() """
        self._send_command("SaveAllObjects")
    def SaveObject(self, *args):
        """ SaveObject(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveObject(): expected (filename)" % len(args))
        self._send_command("SaveObject", args)
    def SaveEndomorph(self, *args):
        """ SaveEndomorph(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveEndomorph(): expected (name)" % len(args))
        self._send_command("SaveEndomorph", args)
    def SaveObjectCopy(self, *args):
        """ SaveObjectCopy(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveObjectCopy(): expected (name)" % len(args))
        self._send_command("SaveObjectCopy", args)
    def ExportLWO2(self, *args):
        """ ExportLWO2(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ExportLWO2(): expected (filename)" % len(args))
        self._send_command("ExportLWO2", args)
    def SubdivisionOrder(self, *args):
        """ SubdivisionOrder(order) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SubdivisionOrder(): expected (order)" % len(args))
        self._send_command("SubdivisionOrder", args)
    def SaveWavefrontObj(self, *args):
        """ SaveWavefrontObj(objectid, filename) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command SaveWavefrontObj(): expected (objectid, filename)" % len(args))
        self._send_command("SaveWavefrontObj", args)
    def SaveTransformedWavefrontObj(self, *args):
        """ SaveTransformedWavefrontObj(objectid, filename) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command SaveTransformedWavefrontObj(): expected (objectid, filename)" % len(args))
        self._send_command("SaveTransformedWavefrontObj", args)
    def SaveFrozenWavefrontObj(self, *args):
        """ SaveFrozenWavefrontObj(objectid, trippled, filename) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command SaveFrozenWavefrontObj(): expected (objectid, trippled, filename)" % len(args))
        self._send_command("SaveFrozenWavefrontObj", args)
    def SaveFrozenLwo(self, *args):
        """ SaveFrozenLwo(objectid, trippled, filename) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command SaveFrozenLwo(): expected (objectid, trippled, filename)" % len(args))
        self._send_command("SaveFrozenLwo", args)
    def SubPatchLevel(self, *args):
        """ SubPatchLevel(display, render) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command SubPatchLevel(): expected (display, render)" % len(args))
        self._send_command("SubPatchLevel", args)
    def SubPatchUV(self, *args):
        """ SubPatchUV(on) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SubPatchUV(): expected (on)" % len(args))
        self._send_command("SubPatchUV", args)
    def MetaballResolution(self, *args):
        """ MetaballResolution(display, render) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command MetaballResolution(): expected (display, render)" % len(args))
        self._send_command("MetaballResolution", args)
    def AddPartigon(self):
        """ AddPartigon() """
        self._send_command("AddPartigon")
    def MorphAmount(self, *args):
        """ MorphAmount(morph) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command MorphAmount(): expected (morph)" % len(args))
        self._send_command("MorphAmount", args)
    def AlphaValue(self, *args):
        """ AlphaValue(alpha) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AlphaValue(): expected (alpha)" % len(args))
        self._send_command("AlphaValue", args)
    def MorphTarget(self, *args):
        """ MorphTarget(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command MorphTarget(): expected (itemid)" % len(args))
        self._send_command("MorphTarget", args)
    def MorphMTSE(self):
        """ MorphMTSE() """
        self._send_command("MorphMTSE")
    def MorphSurfaces(self):
        """ MorphSurfaces() """
        self._send_command("MorphSurfaces")
    def DeformationBlur(self):
        """ DeformationBlur() """
        self._send_command("DeformationBlur")
    def MatteObject(self):
        """ MatteObject() """
        self._send_command("MatteObject")
    def MatteColor(self, *args):
        """ MatteColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command MatteColor(): expected (red, green, blue)" % len(args))
        self._send_command("MatteColor", args)
    def ObjectDissolve(self, *args):
        """ ObjectDissolve(dissolve) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ObjectDissolve(): expected (dissolve)" % len(args))
        self._send_command("ObjectDissolve", args)
    def DistanceDissolve(self):
        """ DistanceDissolve() """
        self._send_command("DistanceDissolve")
    def MaxDissolveDistance(self, *args):
        """ MaxDissolveDistance(distance) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command MaxDissolveDistance(): expected (distance)" % len(args))
        self._send_command("MaxDissolveDistance", args)
    def ShadowOffset(self, *args):
        """ ShadowOffset(offset) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ShadowOffset(): expected (offset)" % len(args))
        self._send_command("ShadowOffset", args)
    def DisplacementMapOrder(self, *args):
        """ DisplacementMapOrder(order) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DisplacementMapOrder(): expected (order)" % len(args))
        self._send_command("DisplacementMapOrder", args)
    def NodeDisplacement(self):
        """ NodeDisplacement() """
        self._send_command("NodeDisplacement")
    def NodeDisplacementOrder(self, *args):
        """ NodeDisplacementOrder(order) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command NodeDisplacementOrder(): expected (order)" % len(args))
        self._send_command("NodeDisplacementOrder", args)
    def BumpDisplacement(self):
        """ BumpDisplacement() """
        self._send_command("BumpDisplacement")
    def BumpDisplacementDistance(self, *args):
        """ BumpDisplacementDistance(distance) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BumpDisplacementDistance(): expected (distance)" % len(args))
        self._send_command("BumpDisplacementDistance", args)
    def BumpDisplacementOrder(self, *args):
        """ BumpDisplacementOrder(order) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BumpDisplacementOrder(): expected (order)" % len(args))
        self._send_command("BumpDisplacementOrder", args)
    def PolygonSize(self, *args):
        """ PolygonSize(size) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PolygonSize(): expected (size)" % len(args))
        self._send_command("PolygonSize", args)
    def ParticleThickness(self, *args):
        """ ParticleThickness(size) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ParticleThickness(): expected (size)" % len(args))
        self._send_command("ParticleThickness", args)
    def LineThickness(self, *args):
        """ LineThickness(size) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LineThickness(): expected (size)" % len(args))
        self._send_command("LineThickness", args)
    def NodeEdges(self):
        """ NodeEdges() """
        self._send_command("NodeEdges")
    def UnseenByRays(self):
        """ UnseenByRays() """
        self._send_command("UnseenByRays")
    def UnseenByCamera(self):
        """ UnseenByCamera() """
        self._send_command("UnseenByCamera")
    def UnseenByAlphaChannel(self):
        """ UnseenByAlphaChannel() """
        self._send_command("UnseenByAlphaChannel")
    def UnaffectedByFog(self):
        """ UnaffectedByFog() """
        self._send_command("UnaffectedByFog")
    def UnseenByRadiosity(self):
        """ UnseenByRadiosity() """
        self._send_command("UnseenByRadiosity")
    def FogLevel(self, *args):
        """ FogLevel(percent) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FogLevel(): expected (percent)" % len(args))
        self._send_command("FogLevel", args)
    def SelfShadow(self):
        """ SelfShadow() """
        self._send_command("SelfShadow")
    def CastShadow(self):
        """ CastShadow() """
        self._send_command("CastShadow")
    def ReceiveShadow(self):
        """ ReceiveShadow() """
        self._send_command("ReceiveShadow")
    def IncludeLight(self, *args):
        """ IncludeLight(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command IncludeLight(): expected (itemid)" % len(args))
        self._send_command("IncludeLight", args)
    def ExcludeLight(self, *args):
        """ ExcludeLight(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ExcludeLight(): expected (itemid)" % len(args))
        self._send_command("ExcludeLight", args)
    def PolygonEdgeFlags(self, *args):
        """ PolygonEdgeFlags(flags) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PolygonEdgeFlags(): expected (flags)" % len(args))
        self._send_command("PolygonEdgeFlags", args)
    def PolygonEdgeThickness(self, *args):
        """ PolygonEdgeThickness(silhouette, unshared, crease, surface, other, patch, intersection) """
        if len(args) != 7:
            raise Exception("Invalid argument count %d provided to command PolygonEdgeThickness(): expected (silhouette, unshared, crease, surface, other, patch, intersection)" % len(args))
        self._send_command("PolygonEdgeThickness", args)
    def PolygonEdgeColor(self, *args):
        """ PolygonEdgeColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command PolygonEdgeColor(): expected (red, green, blue)" % len(args))
        self._send_command("PolygonEdgeColor", args)
    def PolygonEdgeZScale(self, *args):
        """ PolygonEdgeZScale(scale) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PolygonEdgeZScale(): expected (scale)" % len(args))
        self._send_command("PolygonEdgeZScale", args)
    def ShadeEdges(self):
        """ ShadeEdges() """
        self._send_command("ShadeEdges")
    def ShrinkEdgesWithDistance(self):
        """ ShrinkEdgesWithDistance() """
        self._send_command("ShrinkEdgesWithDistance")
    def ShrinkEdgesNominalDistance(self, *args):
        """ ShrinkEdgesNominalDistance(length) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ShrinkEdgesNominalDistance(): expected (length)" % len(args))
        self._send_command("ShrinkEdgesNominalDistance", args)
    def ObjGIUseGlobal(self, *args):
        """ ObjGIUseGlobal(mode) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ObjGIUseGlobal(): expected (mode)" % len(args))
        self._send_command("ObjGIUseGlobal", args)
    def ObjGIBruteForceRays(self, *args):
        """ ObjGIBruteForceRays(count) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ObjGIBruteForceRays(): expected (count)" % len(args))
        self._send_command("ObjGIBruteForceRays", args)
    def ObjGIRaysPerEvaluation(self, *args):
        """ ObjGIRaysPerEvaluation(count) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ObjGIRaysPerEvaluation(): expected (count)" % len(args))
        self._send_command("ObjGIRaysPerEvaluation", args)
    def ObjGISecondaryBounceRays(self, *args):
        """ ObjGISecondaryBounceRays(count) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ObjGISecondaryBounceRays(): expected (count)" % len(args))
        self._send_command("ObjGISecondaryBounceRays", args)
    def ObjGIMissingSampleRays(self, *args):
        """ ObjGIMissingSampleRays(count) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ObjGIMissingSampleRays(): expected (count)" % len(args))
        self._send_command("ObjGIMissingSampleRays", args)
    def ObjGIRadiosityTolerance(self, *args):
        """ ObjGIRadiosityTolerance(degrees) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ObjGIRadiosityTolerance(): expected (degrees)" % len(args))
        self._send_command("ObjGIRadiosityTolerance", args)
    def ObjGIMinPixelSpacing(self, *args):
        """ ObjGIMinPixelSpacing(amount) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ObjGIMinPixelSpacing(): expected (amount)" % len(args))
        self._send_command("ObjGIMinPixelSpacing", args)
    def ObjGIMaxPixelSpacing(self, *args):
        """ ObjGIMaxPixelSpacing(amount) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ObjGIMaxPixelSpacing(): expected (amount)" % len(args))
        self._send_command("ObjGIMaxPixelSpacing", args)
    def ClearAllBones(self):
        """ ClearAllBones() """
        self._send_command("ClearAllBones")
    def SkelegonsToBones(self):
        """ SkelegonsToBones() """
        self._send_command("SkelegonsToBones")
    def BoneSource(self, *args):
        """ BoneSource(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BoneSource(): expected (itemid)" % len(args))
        self._send_command("BoneSource", args)
    def BoneFalloffType(self, *args):
        """ BoneFalloffType(type) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BoneFalloffType(): expected (type)" % len(args))
        self._send_command("BoneFalloffType", args)
    def UseMorphedPositions(self):
        """ UseMorphedPositions() """
        self._send_command("UseMorphedPositions")
    def FasterBones(self):
        """ FasterBones() """
        self._send_command("FasterBones")
    def BoneMode(self, *args):
        """ BoneMode(mode) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BoneMode(): expected (mode)" % len(args))
        self._send_command("BoneMode", args)
    def NumLimitedBones(self, *args):
        """ NumLimitedBones(number) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command NumLimitedBones(): expected (number)" % len(args))
        self._send_command("NumLimitedBones", args)
    def BoneType(self, *args):
        """ BoneType(type) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BoneType(): expected (type)" % len(args))
        self._send_command("BoneType", args)
    def BoneActive(self):
        """ BoneActive() """
        self._send_command("BoneActive")
    def BoneMayaStyleDraw(self):
        """ BoneMayaStyleDraw() """
        self._send_command("BoneMayaStyleDraw")
    def RecordRestPosition(self):
        """ RecordRestPosition() """
        self._send_command("RecordRestPosition")
    def BoneRestPosition(self, *args):
        """ BoneRestPosition(x, y, z) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command BoneRestPosition(): expected (x, y, z)" % len(args))
        self._send_command("BoneRestPosition", args)
    def BoneRestRotation(self, *args):
        """ BoneRestRotation(h, p, b) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command BoneRestRotation(): expected (h, p, b)" % len(args))
        self._send_command("BoneRestRotation", args)
    def BoneRestLength(self, *args):
        """ BoneRestLength(length) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BoneRestLength(): expected (length)" % len(args))
        self._send_command("BoneRestLength", args)
    def AddBoneRestLength(self, *args):
        """ AddBoneRestLength(length) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddBoneRestLength(): expected (length)" % len(args))
        self._send_command("AddBoneRestLength", args)
    def BoneStrength(self, *args):
        """ BoneStrength(strength) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BoneStrength(): expected (strength)" % len(args))
        self._send_command("BoneStrength", args)
    def BoneStrengthMultiply(self):
        """ BoneStrengthMultiply() """
        self._send_command("BoneStrengthMultiply")
    def BoneWeightMapName(self, *args):
        """ BoneWeightMapName(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BoneWeightMapName(): expected (name)" % len(args))
        self._send_command("BoneWeightMapName", args)
    def BoneWeightMapOnly(self):
        """ BoneWeightMapOnly() """
        self._send_command("BoneWeightMapOnly")
    def BoneNormalization(self):
        """ BoneNormalization() """
        self._send_command("BoneNormalization")
    def BoneLimitedRange(self):
        """ BoneLimitedRange() """
        self._send_command("BoneLimitedRange")
    def BoneMinRange(self, *args):
        """ BoneMinRange(distance) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BoneMinRange(): expected (distance)" % len(args))
        self._send_command("BoneMinRange", args)
    def BoneMaxRange(self, *args):
        """ BoneMaxRange(distance) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BoneMaxRange(): expected (distance)" % len(args))
        self._send_command("BoneMaxRange", args)
    def BoneJointComp(self):
        """ BoneJointComp() """
        self._send_command("BoneJointComp")
    def BoneJointCompParent(self):
        """ BoneJointCompParent() """
        self._send_command("BoneJointCompParent")
    def BoneJointCompAmounts(self, *args):
        """ BoneJointCompAmounts(self, parent) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command BoneJointCompAmounts(): expected (self, parent)" % len(args))
        self._send_command("BoneJointCompAmounts", args)
    def BoneMuscleFlex(self):
        """ BoneMuscleFlex() """
        self._send_command("BoneMuscleFlex")
    def BoneMuscleFlexParent(self):
        """ BoneMuscleFlexParent() """
        self._send_command("BoneMuscleFlexParent")
    def BoneMuscleFlexAmounts(self, *args):
        """ BoneMuscleFlexAmounts(self, parent) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command BoneMuscleFlexAmounts(): expected (self, parent)" % len(args))
        self._send_command("BoneMuscleFlexAmounts", args)
    def BoneTwist(self):
        """ BoneTwist() """
        self._send_command("BoneTwist")
    def BoneTwistAmount(self, *args):
        """ BoneTwistAmount(amount) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BoneTwistAmount(): expected (amount)" % len(args))
        self._send_command("BoneTwistAmount", args)
    def BoneBulge(self):
        """ BoneBulge() """
        self._send_command("BoneBulge")
    def BoneBulgeAmount(self, *args):
        """ BoneBulgeAmount(amount) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BoneBulgeAmount(): expected (amount)" % len(args))
        self._send_command("BoneBulgeAmount", args)
    def BoneBulgeParent(self):
        """ BoneBulgeParent() """
        self._send_command("BoneBulgeParent")
    def BoneBulgeParentAmount(self, *args):
        """ BoneBulgeParentAmount(amount) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BoneBulgeParentAmount(): expected (amount)" % len(args))
        self._send_command("BoneBulgeParentAmount", args)
    def SelectAllLights(self):
        """ SelectAllLights() """
        self._send_command("SelectAllLights")
    def ClearAllLights(self):
        """ ClearAllLights() """
        self._send_command("ClearAllLights")
    def AddLight(self, *args):
        """ AddLight(type_name, name) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command AddLight(): expected (type_name, name)" % len(args))
        self._send_command("AddLight", args)
    def AddDistantLight(self, *args):
        """ AddDistantLight(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddDistantLight(): expected (name)" % len(args))
        self._send_command("AddDistantLight", args)
    def AddPointLight(self, *args):
        """ AddPointLight(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddPointLight(): expected (name)" % len(args))
        self._send_command("AddPointLight", args)
    def AddSpotlight(self, *args):
        """ AddSpotlight(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddSpotlight(): expected (name)" % len(args))
        self._send_command("AddSpotlight", args)
    def AddLinearLight(self, *args):
        """ AddLinearLight(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddLinearLight(): expected (name)" % len(args))
        self._send_command("AddLinearLight", args)
    def AddAreaLight(self, *args):
        """ AddAreaLight(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddAreaLight(): expected (name)" % len(args))
        self._send_command("AddAreaLight", args)
    def SaveLight(self, *args):
        """ SaveLight(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveLight(): expected (filename)" % len(args))
        self._send_command("SaveLight", args)
    def DoubleSidedAreaLights(self):
        """ DoubleSidedAreaLights() """
        self._send_command("DoubleSidedAreaLights")
    def EnableLensFlares(self, *args):
        """ EnableLensFlares(enable) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command EnableLensFlares(): expected (enable)" % len(args))
        self._send_command("EnableLensFlares", args)
    def EnableVolumetricLights(self):
        """ EnableVolumetricLights() """
        self._send_command("EnableVolumetricLights")
    def ShadowExclusion(self):
        """ ShadowExclusion() """
        self._send_command("ShadowExclusion")
    def EnableRadiosity0(self):
        """ EnableRadiosity0() """
        self._send_command("EnableRadiosity0")
    def EnableRadiosity1(self):
        """ EnableRadiosity1() """
        self._send_command("EnableRadiosity1")
    def EnableMipMapping(self, *args):
        """ EnableMipMapping(enable) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command EnableMipMapping(): expected (enable)" % len(args))
        self._send_command("EnableMipMapping", args)
    def EnableVolumetrics(self):
        """ EnableVolumetrics() """
        self._send_command("EnableVolumetrics")
    def DiffuseBounces(self, *args):
        """ DiffuseBounces(bounces) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DiffuseBounces(): expected (bounces)" % len(args))
        self._send_command("DiffuseBounces", args)
    def CacheRadiosity(self):
        """ CacheRadiosity() """
        self._send_command("CacheRadiosity")
    def BakeRadiosityScene(self):
        """ BakeRadiosityScene() """
        self._send_command("BakeRadiosityScene")
    def RadiosityInterpolation(self, *args):
        """ RadiosityInterpolation(enabled) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RadiosityInterpolation(): expected (enabled)" % len(args))
        self._send_command("RadiosityInterpolation", args)
    def DistantLight(self):
        """ DistantLight() """
        self._send_command("DistantLight")
    def PointLight(self):
        """ PointLight() """
        self._send_command("PointLight")
    def Spotlight(self):
        """ Spotlight() """
        self._send_command("Spotlight")
    def LinearLight(self):
        """ LinearLight() """
        self._send_command("LinearLight")
    def AreaLight(self):
        """ AreaLight() """
        self._send_command("AreaLight")
    def CustomLight(self, *args):
        """ CustomLight(type_name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command CustomLight(): expected (type_name)" % len(args))
        self._send_command("CustomLight", args)
    def LightColor(self, *args):
        """ LightColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command LightColor(): expected (red, green, blue)" % len(args))
        self._send_command("LightColor", args)
    def LightIntensity(self, *args):
        """ LightIntensity(intensity) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LightIntensity(): expected (intensity)" % len(args))
        self._send_command("LightIntensity", args)
    def LightFalloffType(self, *args):
        """ LightFalloffType(type) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LightFalloffType(): expected (type)" % len(args))
        self._send_command("LightFalloffType", args)
    def LightFalloffType(self):
        """ LightFalloffType() """
        self._send_command("LightFalloffType")
    def AffectDiffuse(self):
        """ AffectDiffuse() """
        self._send_command("AffectDiffuse")
    def AffectSpecular(self):
        """ AffectSpecular() """
        self._send_command("AffectSpecular")
    def AffectOpenGL(self):
        """ AffectOpenGL() """
        self._send_command("AffectOpenGL")
    def LightConeAngle(self, *args):
        """ LightConeAngle(angle) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LightConeAngle(): expected (angle)" % len(args))
        self._send_command("LightConeAngle", args)
    def LightEdgeAngle(self, *args):
        """ LightEdgeAngle(angle) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LightEdgeAngle(): expected (angle)" % len(args))
        self._send_command("LightEdgeAngle", args)
    def LightBufferGroup(self, *args):
        """ LightBufferGroup(groupname) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LightBufferGroup(): expected (groupname)" % len(args))
        self._send_command("LightBufferGroup", args)
    def SelectLightBufferGroupMembers(self, *args):
        """ SelectLightBufferGroupMembers(groupname) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SelectLightBufferGroupMembers(): expected (groupname)" % len(args))
        self._send_command("SelectLightBufferGroupMembers", args)
    def ShadowColor(self, *args):
        """ ShadowColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command ShadowColor(): expected (red, green, blue)" % len(args))
        self._send_command("ShadowColor", args)
    def ShadowType(self, *args):
        """ ShadowType(type) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ShadowType(): expected (type)" % len(args))
        self._send_command("ShadowType", args)
    def GlobalLightIntensity(self, *args):
        """ GlobalLightIntensity(intensity) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command GlobalLightIntensity(): expected (intensity)" % len(args))
        self._send_command("GlobalLightIntensity", args)
    def GlobalLensFlareIntensity(self, *args):
        """ GlobalLensFlareIntensity(intensity) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command GlobalLensFlareIntensity(): expected (intensity)" % len(args))
        self._send_command("GlobalLensFlareIntensity", args)
    def ProjectionImage(self, *args):
        """ ProjectionImage(imageid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ProjectionImage(): expected (imageid)" % len(args))
        self._send_command("ProjectionImage", args)
    def CacheShadowMap(self):
        """ CacheShadowMap() """
        self._send_command("CacheShadowMap")
    def ShadowMapSize(self, *args):
        """ ShadowMapSize(size) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ShadowMapSize(): expected (size)" % len(args))
        self._send_command("ShadowMapSize", args)
    def ShadowMapFuzziness(self, *args):
        """ ShadowMapFuzziness(fuzziness) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ShadowMapFuzziness(): expected (fuzziness)" % len(args))
        self._send_command("ShadowMapFuzziness", args)
    def ShadowMapFitCone(self):
        """ ShadowMapFitCone() """
        self._send_command("ShadowMapFitCone")
    def ShadowMapAngle(self, *args):
        """ ShadowMapAngle(angle) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ShadowMapAngle(): expected (angle)" % len(args))
        self._send_command("ShadowMapAngle", args)
    def IncludeObject(self, *args):
        """ IncludeObject(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command IncludeObject(): expected (itemid)" % len(args))
        self._send_command("IncludeObject", args)
    def ExcludeObject(self, *args):
        """ ExcludeObject(itemid) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ExcludeObject(): expected (itemid)" % len(args))
        self._send_command("ExcludeObject", args)
    def LensFlare(self):
        """ LensFlare() """
        self._send_command("LensFlare")
    def FlareOptions(self):
        """ FlareOptions() """
        self._send_command("FlareOptions")
    def SetFlareIntensity(self, *args):
        """ SetFlareIntensity(intensity) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SetFlareIntensity(): expected (intensity)" % len(args))
        self._send_command("SetFlareIntensity", args)
    def FlareFadeOffScreen(self):
        """ FlareFadeOffScreen() """
        self._send_command("FlareFadeOffScreen")
    def FlareFadeBehindObjects(self):
        """ FlareFadeBehindObjects() """
        self._send_command("FlareFadeBehindObjects")
    def FlareFadeInFog(self):
        """ FlareFadeInFog() """
        self._send_command("FlareFadeInFog")
    def FlareFadeWithDistance(self):
        """ FlareFadeWithDistance() """
        self._send_command("FlareFadeWithDistance")
    def FlareFadeNominalDistance(self, *args):
        """ FlareFadeNominalDistance(distance) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FlareFadeNominalDistance(): expected (distance)" % len(args))
        self._send_command("FlareFadeNominalDistance", args)
    def FlareDissolve(self, *args):
        """ FlareDissolve(percent) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FlareDissolve(): expected (percent)" % len(args))
        self._send_command("FlareDissolve", args)
    def FlareCentralGlow(self):
        """ FlareCentralGlow() """
        self._send_command("FlareCentralGlow")
    def FlareGlowBehindObject(self):
        """ FlareGlowBehindObject() """
        self._send_command("FlareGlowBehindObject")
    def FlareCentralRing(self):
        """ FlareCentralRing() """
        self._send_command("FlareCentralRing")
    def FlareRedOuterGlow(self):
        """ FlareRedOuterGlow() """
        self._send_command("FlareRedOuterGlow")
    def FlareRingSize(self, *args):
        """ FlareRingSize(percent) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FlareRingSize(): expected (percent)" % len(args))
        self._send_command("FlareRingSize", args)
    def FlareRingColor(self, *args):
        """ FlareRingColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command FlareRingColor(): expected (red, green, blue)" % len(args))
        self._send_command("FlareRingColor", args)
    def FlareAnamorphicDistortion(self):
        """ FlareAnamorphicDistortion() """
        self._send_command("FlareAnamorphicDistortion")
    def FlareAnamorphicDistortionAmount(self, *args):
        """ FlareAnamorphicDistortionAmount(amount) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FlareAnamorphicDistortionAmount(): expected (amount)" % len(args))
        self._send_command("FlareAnamorphicDistortionAmount", args)
    def FlareStreaksStarFilter(self, *args):
        """ FlareStreaksStarFilter(list) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FlareStreaksStarFilter(): expected (list)" % len(args))
        self._send_command("FlareStreaksStarFilter", args)
    def FlareStreaksRotation(self, *args):
        """ FlareStreaksRotation(angle) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FlareStreaksRotation(): expected (angle)" % len(args))
        self._send_command("FlareStreaksRotation", args)
    def FlareStreaksOffScreen(self):
        """ FlareStreaksOffScreen() """
        self._send_command("FlareStreaksOffScreen")
    def FlareStreaksAnamorphic(self):
        """ FlareStreaksAnamorphic() """
        self._send_command("FlareStreaksAnamorphic")
    def FlareStreaksRandom(self):
        """ FlareStreaksRandom() """
        self._send_command("FlareStreaksRandom")
    def FlareStreaksIntensity(self, *args):
        """ FlareStreaksIntensity(intensity) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FlareStreaksIntensity(): expected (intensity)" % len(args))
        self._send_command("FlareStreaksIntensity", args)
    def FlareStreaksDensity(self, *args):
        """ FlareStreaksDensity(density) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FlareStreaksDensity(): expected (density)" % len(args))
        self._send_command("FlareStreaksDensity", args)
    def FlareStreaksSharpness(self, *args):
        """ FlareStreaksSharpness(sharpness) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FlareStreaksSharpness(): expected (sharpness)" % len(args))
        self._send_command("FlareStreaksSharpness", args)
    def FlareLensReflections(self):
        """ FlareLensReflections() """
        self._send_command("FlareLensReflections")
    def FlareLensElementShape(self, *args):
        """ FlareLensElementShape(shape) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FlareLensElementShape(): expected (shape)" % len(args))
        self._send_command("FlareLensElementShape", args)
    def FlareLensElementType(self, *args):
        """ FlareLensElementType(element, type) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command FlareLensElementType(): expected (element, type)" % len(args))
        self._send_command("FlareLensElementType", args)
    def FlareLensElementPosition(self, *args):
        """ FlareLensElementPosition(element, position) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command FlareLensElementPosition(): expected (element, position)" % len(args))
        self._send_command("FlareLensElementPosition", args)
    def FlareLensElementSize(self, *args):
        """ FlareLensElementSize(element, radius) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command FlareLensElementSize(): expected (element, radius)" % len(args))
        self._send_command("FlareLensElementSize", args)
    def FlareLensElementColor(self, *args):
        """ FlareLensElementColor(element, red, green, blue) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command FlareLensElementColor(): expected (element, red, green, blue)" % len(args))
        self._send_command("FlareLensElementColor", args)
    def VolumetricLighting(self):
        """ VolumetricLighting() """
        self._send_command("VolumetricLighting")
    def LightVolumetricSamples(self, *args):
        """ LightVolumetricSamples(samples) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LightVolumetricSamples(): expected (samples)" % len(args))
        self._send_command("LightVolumetricSamples", args)
    def LightVolumetricIntensity(self, *args):
        """ LightVolumetricIntensity(intensity) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LightVolumetricIntensity(): expected (intensity)" % len(args))
        self._send_command("LightVolumetricIntensity", args)
    def LightVisibleToCamera(self):
        """ LightVisibleToCamera() """
        self._send_command("LightVisibleToCamera")
    def LightCastsShadows(self):
        """ LightCastsShadows() """
        self._send_command("LightCastsShadows")
    def LightUseNodes(self):
        """ LightUseNodes() """
        self._send_command("LightUseNodes")
    def LightLoadNodes(self, *args):
        """ LightLoadNodes(itemid, filename) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command LightLoadNodes(): expected (itemid, filename)" % len(args))
        self._send_command("LightLoadNodes", args)
    def LightSaveNodes(self, *args):
        """ LightSaveNodes(itemid, filename) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command LightSaveNodes(): expected (itemid, filename)" % len(args))
        self._send_command("LightSaveNodes", args)
    def SelectAllCameras(self):
        """ SelectAllCameras() """
        self._send_command("SelectAllCameras")
    def ClearAllCameras(self):
        """ ClearAllCameras() """
        self._send_command("ClearAllCameras")
    def AddCamera(self, *args):
        """ AddCamera(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddCamera(): expected (name)" % len(args))
        self._send_command("AddCamera", args)
    def FieldRendering(self, *args):
        """ FieldRendering(fieldrend) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FieldRendering(): expected (fieldrend)" % len(args))
        self._send_command("FieldRendering", args)
    def ResolutionPreset(self, *args):
        """ ResolutionPreset(resolution_preset) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ResolutionPreset(): expected (resolution_preset)" % len(args))
        self._send_command("ResolutionPreset", args)
    def ResolutionMultiplier(self, *args):
        """ ResolutionMultiplier(multiplier) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ResolutionMultiplier(): expected (multiplier)" % len(args))
        self._send_command("ResolutionMultiplier", args)
    def FrameSize(self, *args):
        """ FrameSize(width, height) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command FrameSize(): expected (width, height)" % len(args))
        self._send_command("FrameSize", args)
    def OverscanMode(self, *args):
        """ OverscanMode(mode) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command OverscanMode(): expected (mode)" % len(args))
        self._send_command("OverscanMode", args)
    def OverscanSize(self, *args):
        """ OverscanSize(width, height) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command OverscanSize(): expected (width, height)" % len(args))
        self._send_command("OverscanSize", args)
    def PixelAspect(self, *args):
        """ PixelAspect(aspect) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PixelAspect(): expected (aspect)" % len(args))
        self._send_command("PixelAspect", args)
    def LimitedRegion(self, *args):
        """ LimitedRegion(region) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LimitedRegion(): expected (region)" % len(args))
        self._send_command("LimitedRegion", args)
    def RegionPosition(self, *args):
        """ RegionPosition(left, top, width, height) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command RegionPosition(): expected (left, top, width, height)" % len(args))
        self._send_command("RegionPosition", args)
    def ZoomFactor(self, *args):
        """ ZoomFactor(factor) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ZoomFactor(): expected (factor)" % len(args))
        self._send_command("ZoomFactor", args)
    def ApertureHeight(self, *args):
        """ ApertureHeight(height) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ApertureHeight(): expected (height)" % len(args))
        self._send_command("ApertureHeight", args)
    def FilmHeight(self, *args):
        """ FilmHeight(height) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FilmHeight(): expected (height)" % len(args))
        self._send_command("FilmHeight", args)
    def Antialiasing(self, *args):
        """ Antialiasing(level) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command Antialiasing(): expected (level)" % len(args))
        self._send_command("Antialiasing", args)
    def MinAntialiasing(self, *args):
        """ MinAntialiasing(level) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command MinAntialiasing(): expected (level)" % len(args))
        self._send_command("MinAntialiasing", args)
    def MaxAntialiasing(self, *args):
        """ MaxAntialiasing(level) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command MaxAntialiasing(): expected (level)" % len(args))
        self._send_command("MaxAntialiasing", args)
    def EnhancedAA(self):
        """ EnhancedAA() """
        self._send_command("EnhancedAA")
    def DrawAntialiasing(self, *args):
        """ DrawAntialiasing(level) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DrawAntialiasing(): expected (level)" % len(args))
        self._send_command("DrawAntialiasing", args)
    def ReconstructionFilter(self, *args):
        """ ReconstructionFilter(level) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ReconstructionFilter(): expected (level)" % len(args))
        self._send_command("ReconstructionFilter", args)
    def NoiseSampler(self, *args):
        """ NoiseSampler(sampler) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command NoiseSampler(): expected (sampler)" % len(args))
        self._send_command("NoiseSampler", args)
    def AdaptiveSampling(self):
        """ AdaptiveSampling() """
        self._send_command("AdaptiveSampling")
    def AdaptiveThreshold(self, *args):
        """ AdaptiveThreshold(threshold) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AdaptiveThreshold(): expected (threshold)" % len(args))
        self._send_command("AdaptiveThreshold", args)
    def Oversampling(self, *args):
        """ Oversampling(threshold) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command Oversampling(): expected (threshold)" % len(args))
        self._send_command("Oversampling", args)
    def MinimumSamples(self, *args):
        """ MinimumSamples(samples) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command MinimumSamples(): expected (samples)" % len(args))
        self._send_command("MinimumSamples", args)
    def MaximumSamples(self, *args):
        """ MaximumSamples(samples) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command MaximumSamples(): expected (samples)" % len(args))
        self._send_command("MaximumSamples", args)
    def PixelFiltersMT(self, *args):
        """ PixelFiltersMT(enable) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command PixelFiltersMT(): expected (enable)" % len(args))
        self._send_command("PixelFiltersMT", args)
    def ParticleBlur(self):
        """ ParticleBlur() """
        self._send_command("ParticleBlur")
    def MotionBlur(self):
        """ MotionBlur() """
        self._send_command("MotionBlur")
    def BlurLength(self, *args):
        """ BlurLength(length) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command BlurLength(): expected (length)" % len(args))
        self._send_command("BlurLength", args)
    def MotionBlurSubFrames(self, *args):
        """ MotionBlurSubFrames(subframes) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command MotionBlurSubFrames(): expected (subframes)" % len(args))
        self._send_command("MotionBlurSubFrames", args)
    def MotionBlurPasses(self):
        """ MotionBlurPasses() """
        self._send_command("MotionBlurPasses")
    def ShutterEfficiency(self, *args):
        """ ShutterEfficiency(efficiency) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ShutterEfficiency(): expected (efficiency)" % len(args))
        self._send_command("ShutterEfficiency", args)
    def RollingShutter(self, *args):
        """ RollingShutter(skew) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RollingShutter(): expected (skew)" % len(args))
        self._send_command("RollingShutter", args)
    def ShutterOpen(self, *args):
        """ ShutterOpen(open) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ShutterOpen(): expected (open)" % len(args))
        self._send_command("ShutterOpen", args)
    def Stereoscopic(self):
        """ Stereoscopic() """
        self._send_command("Stereoscopic")
    def UseConvergencePoint(self):
        """ UseConvergencePoint() """
        self._send_command("UseConvergencePoint")
    def EyeSeparation(self, *args):
        """ EyeSeparation(separation) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command EyeSeparation(): expected (separation)" % len(args))
        self._send_command("EyeSeparation", args)
    def ConvergencePoint(self, *args):
        """ ConvergencePoint(convergence_point) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ConvergencePoint(): expected (convergence_point)" % len(args))
        self._send_command("ConvergencePoint", args)
    def ConvergenceToeIn(self, *args):
        """ ConvergenceToeIn(amount) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ConvergenceToeIn(): expected (amount)" % len(args))
        self._send_command("ConvergenceToeIn", args)
    def StereoOpenGL(self, *args):
        """ StereoOpenGL(state) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command StereoOpenGL(): expected (state)" % len(args))
        self._send_command("StereoOpenGL", args)
    def StereoTrackedEye(self, *args):
        """ StereoTrackedEye(eye) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command StereoTrackedEye(): expected (eye)" % len(args))
        self._send_command("StereoTrackedEye", args)
    def DepthOfField(self):
        """ DepthOfField() """
        self._send_command("DepthOfField")
    def FocalDistance(self, *args):
        """ FocalDistance(distance) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FocalDistance(): expected (distance)" % len(args))
        self._send_command("FocalDistance", args)
    def LensFStop(self, *args):
        """ LensFStop(fstop) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LensFStop(): expected (fstop)" % len(args))
        self._send_command("LensFStop", args)
    def DiaphragmSides(self, *args):
        """ DiaphragmSides(sides) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DiaphragmSides(): expected (sides)" % len(args))
        self._send_command("DiaphragmSides", args)
    def DiaphragmRotation(self, *args):
        """ DiaphragmRotation(angle) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DiaphragmRotation(): expected (angle)" % len(args))
        self._send_command("DiaphragmRotation", args)
    def SoftFilter(self):
        """ SoftFilter() """
        self._send_command("SoftFilter")
    def Backdrop(self):
        """ Backdrop() """
        self._send_command("Backdrop")
    def GradientBackdrop(self):
        """ GradientBackdrop() """
        self._send_command("GradientBackdrop")
    def BackdropColor(self, *args):
        """ BackdropColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command BackdropColor(): expected (red, green, blue)" % len(args))
        self._send_command("BackdropColor", args)
    def ZenithColor(self, *args):
        """ ZenithColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command ZenithColor(): expected (red, green, blue)" % len(args))
        self._send_command("ZenithColor", args)
    def SkyColor(self, *args):
        """ SkyColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command SkyColor(): expected (red, green, blue)" % len(args))
        self._send_command("SkyColor", args)
    def GroundColor(self, *args):
        """ GroundColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command GroundColor(): expected (red, green, blue)" % len(args))
        self._send_command("GroundColor", args)
    def NadirColor(self, *args):
        """ NadirColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command NadirColor(): expected (red, green, blue)" % len(args))
        self._send_command("NadirColor", args)
    def SkySqueezeColor(self, *args):
        """ SkySqueezeColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command SkySqueezeColor(): expected (red, green, blue)" % len(args))
        self._send_command("SkySqueezeColor", args)
    def GroundSqueezeColor(self, *args):
        """ GroundSqueezeColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command GroundSqueezeColor(): expected (red, green, blue)" % len(args))
        self._send_command("GroundSqueezeColor", args)
    def Volumetrics(self):
        """ Volumetrics() """
        self._send_command("Volumetrics")
    def FogType(self, *args):
        """ FogType(type) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FogType(): expected (type)" % len(args))
        self._send_command("FogType", args)
    def FogMinDistance(self, *args):
        """ FogMinDistance(distance) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FogMinDistance(): expected (distance)" % len(args))
        self._send_command("FogMinDistance", args)
    def FogMaxDistance(self, *args):
        """ FogMaxDistance(distance) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FogMaxDistance(): expected (distance)" % len(args))
        self._send_command("FogMaxDistance", args)
    def FogMinAmount(self, *args):
        """ FogMinAmount(amount) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FogMinAmount(): expected (amount)" % len(args))
        self._send_command("FogMinAmount", args)
    def FogMaxAmount(self, *args):
        """ FogMaxAmount(amount) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FogMaxAmount(): expected (amount)" % len(args))
        self._send_command("FogMaxAmount", args)
    def FogColor(self, *args):
        """ FogColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command FogColor(): expected (red, green, blue)" % len(args))
        self._send_command("FogColor", args)
    def UseBackgroundColor(self, *args):
        """ UseBackgroundColor(enabled) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command UseBackgroundColor(): expected (enabled)" % len(args))
        self._send_command("UseBackgroundColor", args)
    def BackgroundColor(self, *args):
        """ BackgroundColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command BackgroundColor(): expected (red, green, blue)" % len(args))
        self._send_command("BackgroundColor", args)
    def Compositing(self):
        """ Compositing() """
        self._send_command("Compositing")
    def ImageProcessing(self):
        """ ImageProcessing() """
        self._send_command("ImageProcessing")
    def LimitDynamicRange(self):
        """ LimitDynamicRange() """
        self._send_command("LimitDynamicRange")
    def LimitDynamicRangeMin(self, *args):
        """ LimitDynamicRangeMin(minimum) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LimitDynamicRangeMin(): expected (minimum)" % len(args))
        self._send_command("LimitDynamicRangeMin", args)
    def LimitDynamicRangeMax(self, *args):
        """ LimitDynamicRangeMax(maximum) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LimitDynamicRangeMax(): expected (maximum)" % len(args))
        self._send_command("LimitDynamicRangeMax", args)
    def DefaultDitherIntensity(self, *args):
        """ DefaultDitherIntensity(default_dither_intensity) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DefaultDitherIntensity(): expected (default_dither_intensity)" % len(args))
        self._send_command("DefaultDitherIntensity", args)
    def DitherIntensity(self, *args):
        """ DitherIntensity(dither_intensity) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DitherIntensity(): expected (dither_intensity)" % len(args))
        self._send_command("DitherIntensity", args)
    def DepthBufferAA(self, *args):
        """ DepthBufferAA(type) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DepthBufferAA(): expected (type)" % len(args))
        self._send_command("DepthBufferAA", args)
    def RenderLines(self, *args):
        """ RenderLines(type) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RenderLines(): expected (type)" % len(args))
        self._send_command("RenderLines", args)
    def RenderInstances(self, *args):
        """ RenderInstances(type) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RenderInstances(): expected (type)" % len(args))
        self._send_command("RenderInstances", args)
    def SetPreferenceValue(self, *args):
        """ SetPreferenceValue(__value_key___value) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SetPreferenceValue(): expected (__value_key___value)" % len(args))
        self._send_command("SetPreferenceValue", args)
    def SavePreferences(self, *args):
        """ SavePreferences(__branch_key_____file_path__) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SavePreferences(): expected (__branch_key_____file_path__)" % len(args))
        self._send_command("SavePreferences", args)
    def LoadPreferences(self, *args):
        """ LoadPreferences(__file_path__) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LoadPreferences(): expected (__file_path__)" % len(args))
        self._send_command("LoadPreferences", args)
    def OpenPreferences(self, *args):
        """ OpenPreferences(__branch_key_____search_terms___flags) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command OpenPreferences(): expected (__branch_key_____search_terms___flags)" % len(args))
        self._send_command("OpenPreferences", args)
    def ClosePreferences(self):
        """ ClosePreferences() """
        self._send_command("ClosePreferences")
    def GeneralOptions(self):
        """ GeneralOptions() """
        self._send_command("GeneralOptions")
    def PathsOptions(self):
        """ PathsOptions() """
        self._send_command("PathsOptions")
    def ColorSpaceOptions(self):
        """ ColorSpaceOptions() """
        self._send_command("ColorSpaceOptions")
    def OBJOptions(self):
        """ OBJOptions() """
        self._send_command("OBJOptions")
    def SaveOptionsEnabled(self):
        """ SaveOptionsEnabled() """
        self._send_command("SaveOptionsEnabled")
    def OBJOneLayer(self):
        """ OBJOneLayer() """
        self._send_command("OBJOneLayer")
    def OBJOneVMap(self):
        """ OBJOneVMap() """
        self._send_command("OBJOneVMap")
    def OBJPivotInCenter(self):
        """ OBJPivotInCenter() """
        self._send_command("OBJPivotInCenter")
    def OBJWriteNormals(self):
        """ OBJWriteNormals() """
        self._send_command("OBJWriteNormals")
    def OBJMergePoints(self):
        """ OBJMergePoints() """
        self._send_command("OBJMergePoints")
    def OBJReverseKaKd(self):
        """ OBJReverseKaKd() """
        self._send_command("OBJReverseKaKd")
    def OBJParts(self):
        """ OBJParts() """
        self._send_command("OBJParts")
    def OBJSmGrps(self):
        """ OBJSmGrps() """
        self._send_command("OBJSmGrps")
    def OBJRemoveHidden(self):
        """ OBJRemoveHidden() """
        self._send_command("OBJRemoveHidden")
    def OBJForegound(self):
        """ OBJForegound() """
        self._send_command("OBJForegound")
    def OBJContinuousUV(self):
        """ OBJContinuousUV() """
        self._send_command("OBJContinuousUV")
    def OBJDoubleSided(self):
        """ OBJDoubleSided() """
        self._send_command("OBJDoubleSided")
    def OBJImportScale(self):
        """ OBJImportScale() """
        self._send_command("OBJImportScale")
    def OBJExportScale(self):
        """ OBJExportScale() """
        self._send_command("OBJExportScale")
    def OpenGLUseFrameBufferObject(self):
        """ OpenGLUseFrameBufferObject() """
        self._send_command("OpenGLUseFrameBufferObject")
    def GraphEditorAudioEnabled(self):
        """ GraphEditorAudioEnabled() """
        self._send_command("GraphEditorAudioEnabled")
    def ViewportMonitorEnabled(self):
        """ ViewportMonitorEnabled() """
        self._send_command("ViewportMonitorEnabled")
    def OpenGLPickingEnabled(self):
        """ OpenGLPickingEnabled() """
        self._send_command("OpenGLPickingEnabled")
    def ColorSpaceViewer(self):
        """ ColorSpaceViewer() """
        self._send_command("ColorSpaceViewer")
    def ColorSpaceSurfaceColor(self):
        """ ColorSpaceSurfaceColor() """
        self._send_command("ColorSpaceSurfaceColor")
    def ColorSpaceLightColor(self):
        """ ColorSpaceLightColor() """
        self._send_command("ColorSpaceLightColor")
    def ColorSpacePaletteFiles(self):
        """ ColorSpacePaletteFiles() """
        self._send_command("ColorSpacePaletteFiles")
    def ColorSpace8BitFiles(self):
        """ ColorSpace8BitFiles() """
        self._send_command("ColorSpace8BitFiles")
    def ColorSpaceFloatFiles(self):
        """ ColorSpaceFloatFiles() """
        self._send_command("ColorSpaceFloatFiles")
    def ColorSpaceAlpha(self):
        """ ColorSpaceAlpha() """
        self._send_command("ColorSpaceAlpha")
    def ColorSpaceOutput(self):
        """ ColorSpaceOutput() """
        self._send_command("ColorSpaceOutput")
    def ColorSpaceOutputAlpha(self):
        """ ColorSpaceOutputAlpha() """
        self._send_command("ColorSpaceOutputAlpha")
    def ColorSpaceOutputVPR(self):
        """ ColorSpaceOutputVPR() """
        self._send_command("ColorSpaceOutputVPR")
    def ColorSpaceOutputVPRAlpha(self):
        """ ColorSpaceOutputVPRAlpha() """
        self._send_command("ColorSpaceOutputVPRAlpha")
    def ColorSpaceOutputBuffer(self):
        """ ColorSpaceOutputBuffer() """
        self._send_command("ColorSpaceOutputBuffer")
    def ColorSpaceAutoSense(self, *args):
        """ ColorSpaceAutoSense(enable) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ColorSpaceAutoSense(): expected (enable)" % len(args))
        self._send_command("ColorSpaceAutoSense", args)
    def ColorSpaceCorrectOpenGL(self, *args):
        """ ColorSpaceCorrectOpenGL(enable) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ColorSpaceCorrectOpenGL(): expected (enable)" % len(args))
        self._send_command("ColorSpaceCorrectOpenGL", args)
    def ColorSpaceAffectPicker(self, *args):
        """ ColorSpaceAffectPicker(enable) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ColorSpaceAffectPicker(): expected (enable)" % len(args))
        self._send_command("ColorSpaceAffectPicker", args)
    def ColorSpace8BitToFloat(self, *args):
        """ ColorSpace8BitToFloat(enable) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ColorSpace8BitToFloat(): expected (enable)" % len(args))
        self._send_command("ColorSpace8BitToFloat", args)
    def ImageCacheDirectory(self, *args):
        """ ImageCacheDirectory(dirname) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ImageCacheDirectory(): expected (dirname)" % len(args))
        self._send_command("ImageCacheDirectory", args)
    def ImageCacheMaximum(self, *args):
        """ ImageCacheMaximum(size) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ImageCacheMaximum(): expected (size)" % len(args))
        self._send_command("ImageCacheMaximum", args)
    def ImageCacheEnable(self, *args):
        """ ImageCacheEnable(enable) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ImageCacheEnable(): expected (enable)" % len(args))
        self._send_command("ImageCacheEnable", args)
    def MTMeshEval(self):
        """ MTMeshEval() """
        self._send_command("MTMeshEval")
    def DefaultsOptions(self):
        """ DefaultsOptions() """
        self._send_command("DefaultsOptions")
    def ContentDirectory(self, *args):
        """ ContentDirectory(dirname) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ContentDirectory(): expected (dirname)" % len(args))
        self._send_command("ContentDirectory", args)
    def ContentTypeDirectory(self, *args):
        """ ContentTypeDirectory(type, dirname) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command ContentTypeDirectory(): expected (type, dirname)" % len(args))
        self._send_command("ContentTypeDirectory", args)
    def UseCustomPaths(self):
        """ UseCustomPaths() """
        self._send_command("UseCustomPaths")
    def CreateContentPath(self, *args):
        """ CreateContentPath(pathtype) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command CreateContentPath(): expected (pathtype)" % len(args))
        self._send_command("CreateContentPath", args)
    def RecentContentDirs(self):
        """ RecentContentDirs() """
        self._send_command("RecentContentDirs")
    def HideWindows(self):
        """ HideWindows() """
        self._send_command("HideWindows")
    def HideToolbar(self):
        """ HideToolbar() """
        self._send_command("HideToolbar")
    def CameraViewBackground(self, *args):
        """ CameraViewBackground(type) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command CameraViewBackground(): expected (type)" % len(args))
        self._send_command("CameraViewBackground", args)
    def ParentInPlace(self):
        """ ParentInPlace() """
        self._send_command("ParentInPlace")
    def FramesPerSecond(self, *args):
        """ FramesPerSecond(fps) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command FramesPerSecond(): expected (fps)" % len(args))
        self._send_command("FramesPerSecond", args)
    def FractionalFrames(self):
        """ FractionalFrames() """
        self._send_command("FractionalFrames")
    def AutoSaveObj(self):
        """ AutoSaveObj() """
        self._send_command("AutoSaveObj")
    def AutoSaveScene(self):
        """ AutoSaveScene() """
        self._send_command("AutoSaveScene")
    def ExportSceneInfo(self, *args):
        """ ExportSceneInfo(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ExportSceneInfo(): expected (filename)" % len(args))
        self._send_command("ExportSceneInfo", args)
    def ProtectLegacyScenes(self, *args):
        """ ProtectLegacyScenes(on_off) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ProtectLegacyScenes(): expected (on_off)" % len(args))
        self._send_command("ProtectLegacyScenes", args)
    def SaveConfig(self, *args):
        """ SaveConfig(type, quoted_filename) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command SaveConfig(): expected (type, quoted_filename)" % len(args))
        self._send_command("SaveConfig", args)
    def LoadConfig(self, *args):
        """ LoadConfig(quoted_filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LoadConfig(): expected (quoted_filename)" % len(args))
        self._send_command("LoadConfig", args)
    def AutoConfirm(self, *args):
        """ AutoConfirm(on_off) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AutoConfirm(): expected (on_off)" % len(args))
        self._send_command("AutoConfirm", args)
    def AlertLevel(self, *args):
        """ AlertLevel(level) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AlertLevel(): expected (level)" % len(args))
        self._send_command("AlertLevel", args)
    def EditMenus(self):
        """ EditMenus() """
        self._send_command("EditMenus")
    def EditKeys(self):
        """ EditKeys() """
        self._send_command("EditKeys")
    def edit_fonts(self):
        """ edit_fonts() """
        self._send_command("edit_fonts")
    def DefaultSceneLength(self, *args):
        """ DefaultSceneLength(threshold) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DefaultSceneLength(): expected (threshold)" % len(args))
        self._send_command("DefaultSceneLength", args)
    def DefaultStartFrame(self, *args):
        """ DefaultStartFrame(start) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DefaultStartFrame(): expected (start)" % len(args))
        self._send_command("DefaultStartFrame", args)
    def DefaultKeyframe(self, *args):
        """ DefaultKeyframe(keyframe) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command DefaultKeyframe(): expected (keyframe)" % len(args))
        self._send_command("DefaultKeyframe", args)
    def InitialKeyframePerScene(self):
        """ InitialKeyframePerScene() """
        self._send_command("InitialKeyframePerScene")
    def MasterPlugins(self):
        """ MasterPlugins() """
        self._send_command("MasterPlugins")
    def Simulations(self):
        """ Simulations() """
        self._send_command("Simulations")
    def AddPlugins(self, *args):
        """ AddPlugins(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command AddPlugins(): expected (filename)" % len(args))
        self._send_command("AddPlugins", args)
    def ActivateMaster(self, *args):
        """ ActivateMaster(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ActivateMaster(): expected (name)" % len(args))
        self._send_command("ActivateMaster", args)
    def ActivateMasterUnique(self, *args):
        """ ActivateMasterUnique(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command ActivateMasterUnique(): expected (name)" % len(args))
        self._send_command("ActivateMasterUnique", args)
    def RemoveMaster(self, *args):
        """ RemoveMaster(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command RemoveMaster(): expected (name)" % len(args))
        self._send_command("RemoveMaster", args)
    def ApplyServer(self, *args):
        """ ApplyServer(klass, server) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command ApplyServer(): expected (klass, server)" % len(args))
        self._send_command("ApplyServer", args)
    def ApplyServerByItemID(self, *args):
        """ ApplyServerByItemID(itemid, klass, server) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command ApplyServerByItemID(): expected (itemid, klass, server)" % len(args))
        self._send_command("ApplyServerByItemID", args)
    def RemoveServer(self, *args):
        """ RemoveServer(klass, index) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command RemoveServer(): expected (klass, index)" % len(args))
        self._send_command("RemoveServer", args)
    def RemoveServerByItemID(self, *args):
        """ RemoveServerByItemID(itemid, klass, index) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command RemoveServerByItemID(): expected (itemid, klass, index)" % len(args))
        self._send_command("RemoveServerByItemID", args)
    def EditServer(self, *args):
        """ EditServer(klass, index) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command EditServer(): expected (klass, index)" % len(args))
        self._send_command("EditServer", args)
    def EnableServer(self, *args):
        """ EnableServer(klass, index, enable) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command EnableServer(): expected (klass, index, enable)" % len(args))
        self._send_command("EnableServer", args)
    def EnableServerByItemID(self, *args):
        """ EnableServerByItemID(itemid, klass, index, enable) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command EnableServerByItemID(): expected (itemid, klass, index, enable)" % len(args))
        self._send_command("EnableServerByItemID", args)
    def PositionServerByItemID(self, *args):
        """ PositionServerByItemID(itemid, klass, name, pos) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command PositionServerByItemID(): expected (itemid, klass, name, pos)" % len(args))
        self._send_command("PositionServerByItemID", args)
    def ReorderServerByItemID(self, *args):
        """ ReorderServerByItemID(itemid, klass, index, pos) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command ReorderServerByItemID(): expected (itemid, klass, index, pos)" % len(args))
        self._send_command("ReorderServerByItemID", args)
    def SaveServerDataByItemID(self, *args):
        """ SaveServerDataByItemID(itemid, klass, index, optional_format, filename) """
        if len(args) != 5:
            raise Exception("Invalid argument count %d provided to command SaveServerDataByItemID(): expected (itemid, klass, index, optional_format, filename)" % len(args))
        self._send_command("SaveServerDataByItemID", args)
    def LoadServerDataByItemID(self, *args):
        """ LoadServerDataByItemID(itemid, klass, index, optional_format, filename) """
        if len(args) != 5:
            raise Exception("Invalid argument count %d provided to command LoadServerDataByItemID(): expected (itemid, klass, index, optional_format, filename)" % len(args))
        self._send_command("LoadServerDataByItemID", args)
    def SetServerDescriptionByItemID(self, *args):
        """ SetServerDescriptionByItemID(itemid, klass, index, description) """
        if len(args) != 4:
            raise Exception("Invalid argument count %d provided to command SetServerDescriptionByItemID(): expected (itemid, klass, index, description)" % len(args))
        self._send_command("SetServerDescriptionByItemID", args)
    def FlushUnusedPlugins(self):
        """ FlushUnusedPlugins() """
        self._send_command("FlushUnusedPlugins")
    def StatusMsg(self, *args):
        """ StatusMsg(message) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command StatusMsg(): expected (message)" % len(args))
        self._send_command("StatusMsg", args)
    def EditPlugins(self):
        """ EditPlugins() """
        self._send_command("EditPlugins")
    def LastPluginInterface(self):
        """ LastPluginInterface() """
        self._send_command("LastPluginInterface")
    def SaveCommandList(self, *args):
        """ SaveCommandList(optional_filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SaveCommandList(): expected (optional_filename)" % len(args))
        self._send_command("SaveCommandList", args)
    def SaveCommandMessages(self):
        """ SaveCommandMessages() """
        self._send_command("SaveCommandMessages")
    def AddButton(self, *args):
        """ AddButton(command, group) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command AddButton(): expected (command, group)" % len(args))
        self._send_command("AddButton", args)
    def Generics(self):
        """ Generics() """
        self._send_command("Generics")
    def Lights(self):
        """ Lights() """
        self._send_command("Lights")
    def SetBackgroundImage(self, *args):
        """ SetBackgroundImage(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SetBackgroundImage(): expected (name)" % len(args))
        self._send_command("SetBackgroundImage", args)
    def SetForegroundImage(self, *args):
        """ SetForegroundImage(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SetForegroundImage(): expected (name)" % len(args))
        self._send_command("SetForegroundImage", args)
    def SetForegroundAlphaImage(self, *args):
        """ SetForegroundAlphaImage(name) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SetForegroundAlphaImage(): expected (name)" % len(args))
        self._send_command("SetForegroundAlphaImage", args)
    def SyncImageToFrame(self, *args):
        """ SyncImageToFrame(frame) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SyncImageToFrame(): expected (frame)" % len(args))
        self._send_command("SyncImageToFrame", args)
    def EnableForegroundFaderAlpha(self, *args):
        """ EnableForegroundFaderAlpha(on_off) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command EnableForegroundFaderAlpha(): expected (on_off)" % len(args))
        self._send_command("EnableForegroundFaderAlpha", args)
    def SetForegroundDissolve(self, *args):
        """ SetForegroundDissolve(percentage) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SetForegroundDissolve(): expected (percentage)" % len(args))
        self._send_command("SetForegroundDissolve", args)
    def EnableForegroundKey(self, *args):
        """ EnableForegroundKey(on_off) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command EnableForegroundKey(): expected (on_off)" % len(args))
        self._send_command("EnableForegroundKey", args)
    def SetLowClipColor(self, *args):
        """ SetLowClipColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command SetLowClipColor(): expected (red, green, blue)" % len(args))
        self._send_command("SetLowClipColor", args)
    def SetHighClipColor(self, *args):
        """ SetHighClipColor(red, green, blue) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command SetHighClipColor(): expected (red, green, blue)" % len(args))
        self._send_command("SetHighClipColor", args)
    def ChangeClipType(self, *args):
        """ ChangeClipType(lwimageid, type) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command ChangeClipType(): expected (lwimageid, type)" % len(args))
        self._send_command("ChangeClipType", args)
    def LoadClip(self, *args):
        """ LoadClip(filename) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command LoadClip(): expected (filename)" % len(args))
        self._send_command("LoadClip", args)
    def Layout_AddViewport(self):
        """ Layout_AddViewport() """
        self._send_command("Layout_AddViewport")
    def Layout_PositionViewport(self, *args):
        """ Layout_PositionViewport(index, x, y) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command Layout_PositionViewport(): expected (index, x, y)" % len(args))
        self._send_command("Layout_PositionViewport", args)
    def Layout_RemoveViewport(self, *args):
        """ Layout_RemoveViewport(index) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command Layout_RemoveViewport(): expected (index)" % len(args))
        self._send_command("Layout_RemoveViewport", args)
    def Layout_RowViewports(self):
        """ Layout_RowViewports() """
        self._send_command("Layout_RowViewports")
    def Layout_ColViewports(self):
        """ Layout_ColViewports() """
        self._send_command("Layout_ColViewports")
    def Layout_TileViewports(self):
        """ Layout_TileViewports() """
        self._send_command("Layout_TileViewports")
    def ViewPortToggleVPR(self, *args):
        """ ViewPortToggleVPR(view_number, view_level) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command ViewPortToggleVPR(): expected (view_number, view_level)" % len(args))
        self._send_command("ViewPortToggleVPR", args)
    def ViewPortToggleShader(self, *args):
        """ ViewPortToggleShader(view_number, view_level) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command ViewPortToggleShader(): expected (view_number, view_level)" % len(args))
        self._send_command("ViewPortToggleShader", args)
    def OpenPCoreConsole(self):
        """ OpenPCoreConsole() """
        self._send_command("OpenPCoreConsole")
    def ClosePCoreConsole(self):
        """ ClosePCoreConsole() """
        self._send_command("ClosePCoreConsole")
    def OpenPCoreCommander(self):
        """ OpenPCoreCommander() """
        self._send_command("OpenPCoreCommander")
    def ClosePCoreCommander(self):
        """ ClosePCoreCommander() """
        self._send_command("ClosePCoreCommander")
    def AlembicImport(self):
        """ AlembicImport() """
        self._send_command("AlembicImport")
    def AlembicExport(self):
        """ AlembicExport() """
        self._send_command("AlembicExport")
    def StudioTraitCollectionToggle(self, *args):
        """ StudioTraitCollectionToggle(collection, option, toggle) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command StudioTraitCollectionToggle(): expected (collection, option, toggle)" % len(args))
        self._send_command("StudioTraitCollectionToggle", args)
    def StudioTraitToggle(self, *args):
        """ StudioTraitToggle(trait, option, toggle) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command StudioTraitToggle(): expected (trait, option, toggle)" % len(args))
        self._send_command("StudioTraitToggle", args)
    def StudioToggle(self, *args):
        """ StudioToggle(option, toggle) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command StudioToggle(): expected (option, toggle)" % len(args))
        self._send_command("StudioToggle", args)
    def StudioLIVE(self):
        """ StudioLIVE() """
        self._send_command("StudioLIVE")
    def StudioTraitCollectionStoreToTime(self, *args):
        """ StudioTraitCollectionStoreToTime(collection, time) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command StudioTraitCollectionStoreToTime(): expected (collection, time)" % len(args))
        self._send_command("StudioTraitCollectionStoreToTime", args)
    def StudioTraitStoreToTime(self, *args):
        """ StudioTraitStoreToTime(trait, time) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command StudioTraitStoreToTime(): expected (trait, time)" % len(args))
        self._send_command("StudioTraitStoreToTime", args)
    def EnableCommandPort(self, *args):
        """ EnableCommandPort(port) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command EnableCommandPort(): expected (port)" % len(args))
        self._send_command("EnableCommandPort", args)
    def DisableCommandPort(self):
        """ DisableCommandPort() """
        self._send_command("DisableCommandPort")
    def PCorePython(self):
        """ PCorePython() """
        self._send_command("PCorePython")
    def SendImageToIView(self, *args):
        """ SendImageToIView(filename, name, colorspace) """
        if len(args) != 3:
            raise Exception("Invalid argument count %d provided to command SendImageToIView(): expected (filename, name, colorspace)" % len(args))
        self._send_command("SendImageToIView", args)
    def EnableFixedNearClipDistance(self, *args):
        """ EnableFixedNearClipDistance(on_off) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command EnableFixedNearClipDistance(): expected (on_off)" % len(args))
        self._send_command("EnableFixedNearClipDistance", args)
    def SetFixedNearClipDistance(self, *args):
        """ SetFixedNearClipDistance(dist) """
        if len(args) != 1:
            raise Exception("Invalid argument count %d provided to command SetFixedNearClipDistance(): expected (dist)" % len(args))
        self._send_command("SetFixedNearClipDistance", args)
    def ShowOpenGLUI(self, *args):
        """ ShowOpenGLUI(viewportnumber, on_off) """
        if len(args) != 2:
            raise Exception("Invalid argument count %d provided to command ShowOpenGLUI(): expected (viewportnumber, on_off)" % len(args))
        self._send_command("ShowOpenGLUI", args)
