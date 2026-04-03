# LightWave Command Port Syntax Reference


## Overview

The **LightWave Command Port** is a UDP-based inter-process communication system built into LightWave 3D that enables external applications to control LightWave programmatically. It exposes LightWave's internal command system to any external script or application capable of sending UDP network packets.

### What is UDP?

**UDP (User Datagram Protocol)** is a connectionless network protocol that allows data to be sent without establishing a dedicated connection first. Unlike TCP, UDP does not wait for acknowledgment that data was received - it simply sends and moves on. This makes UDP faster and more efficient for real-time communication where occasional packet loss is acceptable.

### How the Command Port Works

The Command Port operates on a request-response model over UDP:

1. **Discovery**: Your script sends a broadcast packet on ports 50155-50165 to discover running LightWave instances
2. **Connection**: Establish contact with a discovered instance via UDP
3. **Command**: Send commands as text strings (e.g., `AddRotation 0 0 0.5`)
4. **Execution**: LightWave processes the command and returns a response

### Automation Capabilities

The Command Port enables powerful automation possibilities:

- **Scene Management**: Load, save, and manipulate scenes programmatically
- **Object Manipulation**: Create, transform, and animate 3D objects
- **Camera & Lighting Control**: Adjust views, lighting, and render settings
- **Material Editing**: Modify surfaces and textures dynamically
- **Batch Processing**: Automate repetitive tasks like renaming, material assignment
- **Pipeline Integration**: Connect LightWave to external tools like After Effects, Unity, Unreal, or render farms
- **Custom Tools**: Build real-time control panels in Python, tkinter, or other UI frameworks

### Two Interfaces

| Component | Purpose |
|-----------|---------|
| **Layout** | Scene orchestration, animation, rendering - 857 commands |
| **Modeler** | 3D polygon modeling, mesh editing - 62 commands |

---

## Layout Commands

Scene orchestration, animation, rendering, and object manipulation.

### Create/Modify (63 commands)

| Command | Syntax |
|---------|--------|
| AddAreaLight | `AddAreaLight(name)` |
| AddBone | `AddBone(name)` |
| AddBoneRestLength | `AddBoneRestLength(length)` |
| AddButton | `AddButton(command, group)` |
| AddCamera | `AddCamera(name)` |
| AddChildBone | `AddChildBone(name)` |
| AddChildJoint | `AddChildJoint(name)` |
| AddCustomBuffer | `AddCustomBuffer(buffer_name)` |
| AddDistantLight | `AddDistantLight(name)` |
| AddEnvelope | `AddEnvelope(channel)` |
| AddJoint | `AddJoint(name)` |
| AddLight | `AddLight(type_name, name)` |
| AddLinearLight | `AddLinearLight(name)` |
| AddNull | `AddNull(name)` |
| AddPartigon | `AddPartigon()` |
| AddPlugins | `AddPlugins(filename)` |
| AddPointLight | `AddPointLight(name)` |
| AddPosition | `AddPosition(x, y, z)` |
| AddRotation | `AddRotation(h, p, b)` |
| AddScale | `AddScale(x, y, z)` |
| AddSpotlight | `AddSpotlight(name)` |
| CreateContentPath | `CreateContentPath(pathtype)` |
| CreateKey | `CreateKey(time, scope, channelmask)` |
| DeleteKey | `DeleteKey(time)` |
| FlipSideSpline | `FlipSideSpline()` |
| Layout_AddViewport | `Layout_AddViewport()` |
| Layout_RemoveViewport | `Layout_RemoveViewport(index)` |
| Layout_SetWindowPos | `Layout_SetWindowPos(x, y)` |
| Layout_SetWindowSize | `Layout_SetWindowSize(width, height)` |
| MakePreview | `MakePreview()` |
| OBJMergePoints | `OBJMergePoints()` |
| OBJRemoveHidden | `OBJRemoveHidden()` |
| PathAlignLookAhead | `PathAlignLookAhead(time)` |
| PathAlignMaxLookSteps | `PathAlignMaxLookSteps(steps)` |
| PathAlignReliableDist | `PathAlignReliableDist(distance)` |
| Presets | `Presets()` |
| RemoveCustomBuffer | `RemoveCustomBuffer(buffer_name)` |
| RemoveEnvelope | `RemoveEnvelope(channel)` |
| RemoveMaster | `RemoveMaster(name)` |
| RemoveServer | `RemoveServer(klass, index)` |
| Reset | `Reset()` |
| ResolutionPreset | `ResolutionPreset(resolution_preset)` |
| Scene_SetWindowPos | `Scene_SetWindowPos(x, y)` |
| Scene_SetWindowSize | `Scene_SetWindowSize(width, height)` |
| SetBackgroundImage | `SetBackgroundImage(name)` |
| SetFixedNearClipDistance | `SetFixedNearClipDistance(dist)` |
| SetFlareIntensity | `SetFlareIntensity(intensity)` |
| SetForegroundAlphaImage | `SetForegroundAlphaImage(name)` |
| SetForegroundDissolve | `SetForegroundDissolve(percentage)` |
| SetForegroundImage | `SetForegroundImage(name)` |
| SetHighClipColor | `SetHighClipColor(red, green, blue)` |
| SetLowClipColor | `SetLowClipColor(red, green, blue)` |
| SetPreferenceValue | `SetPreferenceValue(value_key, value)` |
| SetRenderDisplay | `SetRenderDisplay()` |
| SetTCB | `SetTCB(t, c, b)` |
| ShadowOffset | `ShadowOffset(offset)` |
| SyncBufferSet | `SyncBufferSet()` |
| ViewPositionReset | `ViewPositionReset(view)` |
| ViewPositionSet | `ViewPositionSet(view, x, y, z)` |
| ViewRotationReset | `ViewRotationReset(view)` |
| ViewRotationSet | `ViewRotationSet(view, h, p, b)` |
| ViewZoomReset | `ViewZoomReset(view)` |
| ViewZoomSet | `ViewZoomSet(view, zoom)` |

### File Operations (95 commands)

| Command | Syntax |
|---------|--------|
| AboutOpenGL | `AboutOpenGL()` |
| AffectOpenGL | `AffectOpenGL()` |
| AlembicExport | `AlembicExport()` |
| AlembicImport | `AlembicImport()` |
| AutoSaveObj | `AutoSaveObj()` |
| AutoSaveScene | `AutoSaveScene()` |
| BoneWeightMapName | `BoneWeightMapName(name)` |
| BoneWeightMapOnly | `BoneWeightMapOnly()` |
| BoneWeightShade | `BoneWeightShade()` |
| ClosePCoreCommander | `ClosePCoreCommander()` |
| ClosePCoreConsole | `ClosePCoreConsole()` |
| ClosePreferences | `ClosePreferences()` |
| ClosedSpline | `ClosedSpline()` |
| ColorSpaceCorrectOpenGL | `ColorSpaceCorrectOpenGL(enable)` |
| ExportLWO2 | `ExportLWO2(filename)` |
| ExportSceneInfo | `ExportSceneInfo(filename)` |
| LightLoadNodes | `LightLoadNodes(itemid, filename)` |
| LightSaveNodes | `LightSaveNodes(itemid, filename)` |
| LoadAudio | `LoadAudio()` |
| LoadBufferSet | `LoadBufferSet()` |
| LoadClip | `LoadClip(filename)` |
| LoadConfig | `LoadConfig(quoted_filename)` |
| LoadElementsFromScene | `LoadElementsFromScene(elements, filename)` |
| LoadFromScene | `LoadFromScene(filename)` |
| LoadMotion | `LoadMotion(filename)` |
| LoadObject | `LoadObject(filename)` |
| LoadObjectLayer | `LoadObjectLayer(layer, filename)` |
| LoadPreferences | `LoadPreferences(file_path)` |
| LoadPreview | `LoadPreview()` |
| LoadRenderSettings | `LoadRenderSettings(filename)` |
| LoadScene | `LoadScene(filename)` |
| LoadServerDataByItemID | `LoadServerDataByItemID(itemid, klass, index, optional_format, filename)` |
| OBJExportScale | `OBJExportScale()` |
| OBJImportScale | `OBJImportScale()` |
| OBJWriteNormals | `OBJWriteNormals()` |
| OpenGLOptions | `OpenGLOptions()` |
| OpenGLPickingEnabled | `OpenGLPickingEnabled()` |
| OpenGLUseFrameBufferObject | `OpenGLUseFrameBufferObject()` |
| OpenPCoreCommander | `OpenPCoreCommander()` |
| OpenPCoreConsole | `OpenPCoreConsole()` |
| OpenPreferences | `OpenPreferences(branch_key, search_terms, flags)` |
| PreLoadScene | `PreLoadScene()` |
| PreSaveScene | `PreSaveScene()` |
| RenderThreads | `RenderThreads(threads)` |
| RevertScene | `RevertScene()` |
| SaveAllObjects | `SaveAllObjects()` |
| SaveAlpha | `SaveAlpha()` |
| SaveAlphaPrefix | `SaveAlphaPrefix()` |
| SaveAlphaServer | `SaveAlphaServer(server)` |
| SaveAnimation | `SaveAnimation()` |
| SaveAnimationName | `SaveAnimationName()` |
| SaveAnimationServer | `SaveAnimationServer(server)` |
| SaveBufferSet | `SaveBufferSet()` |
| SaveBufferSetPreset | `SaveBufferSetPreset()` |
| SaveCommandList | `SaveCommandList(optional_filename)` |
| SaveCommandMessages | `SaveCommandMessages()` |
| SaveConfig | `SaveConfig(type, quoted_filename)` |
| SaveEndomorph | `SaveEndomorph(name)` |
| SaveFrozenLwo | `SaveFrozenLwo(objectid, trippled, filename)` |
| SaveFrozenWavefrontObj | `SaveFrozenWavefrontObj(objectid, trippled, filename)` |
| SaveLWSC1 | `SaveLWSC1(filename)` |
| SaveLWSC3 | `SaveLWSC3(filename)` |
| SaveLWSC4 | `SaveLWSC4(filename)` |
| SaveLWSC_2024 | `SaveLWSC_2024(filename)` |
| SaveLWSC_4_0 | `SaveLWSC_4_0(filename)` |
| SaveLWSC_5_6 | `SaveLWSC_5_6(filename)` |
| SaveLWSC_6_0 | `SaveLWSC_6_0(filename)` |
| SaveLWSC_9_2 | `SaveLWSC_9_2(filename)` |
| SaveLWSC_9_5 | `SaveLWSC_9_5(filename)` |
| SaveLight | `SaveLight(filename)` |
| SaveMotion | `SaveMotion(filename)` |
| SaveObject | `SaveObject(filename)` |
| SaveObjectCopy | `SaveObjectCopy(name)` |
| SaveOptions | `SaveOptions()` |
| SaveOptionsEnabled | `SaveOptionsEnabled()` |
| SavePreferences | `SavePreferences(branch_key, file_path)` |
| SavePreview | `SavePreview()` |
| SaveRGB | `SaveRGB()` |
| SaveRGBPrefix | `SaveRGBPrefix()` |
| SaveRGBServer | `SaveRGBServer(server)` |
| SaveRenderPreset | `SaveRenderPreset(flags, name, comment)` |
| SaveRenderSettings | `SaveRenderSettings(filename, flags, name, comment)` |
| SaveScene | `SaveScene()` |
| SaveSceneAs | `SaveSceneAs(filename)` |
| SaveSceneCopy | `SaveSceneCopy(filename)` |
| SaveServerDataByItemID | `SaveServerDataByItemID(itemid, klass, index, optional_format, filename)` |
| SaveTransformed | `SaveTransformed(filename)` |
| SaveTransformedWavefrontObj | `SaveTransformedWavefrontObj(objectid, filename)` |
| SaveViewLayout | `SaveViewLayout()` |
| SaveViewportImage | `SaveViewportImage(filename, imagetype, viewportnumber, scale)` |
| SaveWavefrontObj | `SaveWavefrontObj(objectid, filename)` |
| SceneEditorOpen | `SceneEditorOpen()` |
| ShowOpenGLUI | `ShowOpenGLUI(viewportnumber, on_off)` |
| ShutterOpen | `ShutterOpen(open)` |
| StereoOpenGL | `StereoOpenGL(state)` |

### General (404 commands)

Contains: About, ActivateMaster, AdaptiveSampling, AlertLevel, AlphaBackdrop, AlphaValue, AlignDistribute, ApplyServer, AutoFeedback, BoneFeedback, BoneMapType, BoneScaling, Break, BridgePols, ChangeSegment, Channel, Circular, ClearAllSelected, ClearEnvelopes, CloseDatabase, CloseEffects, CloseMotionOptions, ClosePackage, CloseScene, CloseSurfaces, CommandInput, Comment, CompFile, ConcatenateMerge, Connect, ContactShadows, Contrast, Convert, CreateBone, CreateMotion, CurveDivisions, CustomBall, DataViewAdd, DataViewBegin, DataViewEnd, and many more.

### Geometry (34 commands)

| Command | Syntax |
|---------|--------|
| ClearAllObjects | `ClearAllObjects()` |
| CloneToObject | `CloneToObject()` |
| ConvergencePoint | `ConvergencePoint()` |
| EditObjects | `EditObjects()` |
| ExcludeObject | `ExcludeObject()` |
| IncludeObject | `IncludeObject()` |
| MTMeshEval | `MTMeshEval()` |
| MatteObject | `MatteObject()` |
| MorphMap | `MorphMap()` |
| MorphMix | `MorphMix()` |
| MorphOptions | `MorphOptions()` |
| MorphPols | `MorphPols()` |
| MorphSelect | `MorphSelect()` |
| MorphUMap | `MorphUMap()` |
| MorphUV | `MorphUV()` |
| ObjectMeshGroup | `ObjectMeshGroup()` |
| PolygonEdge | `PolygonEdge()` |
| PolygonEdgeAdd | `PolygonEdgeAdd()` |
| PolygonEdgeInsert | `PolygonEdgeInsert()` |
| PolygonEdgeRemove | `PolygonEdgeRemove()` |
| SubPatch | `SubPatch()` |
| SubPatchLevels | `SubPatchLevels()` |
| Subdivision | `Subdivision()` |
| SubdivisionBind | `SubdivisionBind()` |
| SubdivisionCalcPreview | `SubdivisionCalcPreview()` |
| SubdivisionDisplace | `SubdivisionDisplace()` |
| SubdivisionLevels | `SubdivisionLevels()` |
| SubdivisionRender | `SubdivisionRender()` |
| SurfaceEditor | `SurfaceEditor()` |
| Symmetry | `Symmetry()` |
| SymmetryMerge | `SymmetryMerge()` |
| SymmetryPalette | `SymmetryPalette()` |
| ToggleComp ObjGadgets | `ToggleComp ObjGadgets()` |
| ToggleDragState | `ToggleDragState()` |

### Lighting/Camera (71 commands)

| Command | Syntax |
|---------|--------|
| AreaLightSize | `AreaLightSize()` |
| AreaLightSpot | `AreaLightSpot()` |
| CameraView | `CameraView()` |
| ChangeCamera | `ChangeCamera()` |
| DistantLight | `DistantLight()` |
| EditLights | `EditLights()` |
| EnableCamera | `EnableCamera()` |
| FitAllViews | `FitAllViews()` |
| FitSelectedViews | `FitSelectedViews()` |
| FitView | `FitView()` |
| FlareColor | `FlareColor()` |
| FlareIntensity | `FlareIntensity()` |
| FlareOptions | `FlareOptions()` |
| FlareRenderFlags | `FlareRenderFlags()` |
| FlipCamera | `FlipCamera()` |
| GlobalIllumination | `GlobalIllumination()` |
| InterpolateCamera | `InterpolateCamera()` |
| LightColor | `LightColor()` |
| LightConeAngle | `LightConeAngle()` |
| LightFalloffType | `LightFalloffType()` |
| LightIntensity | `LightIntensity()` |
| LightLensFlare | `LightLensFlare()` |
| LightLinghtDirectional | `LightLinghtDirectional()` |
| LightParent | `LightParent()` |
| LightReflection | `LightReflection()` |
| LightSamples | `LightSamples()` |
| LightShadowType | `LightShadowType()` |
| LightView | `LightView()` |
| LockCamera | `LockCamera()` |
| LookAt | `LookAt()` |
| PanView | `PanView()` |
| PointLight | `PointLight()` |
| PositionView | `PositionView()` |
| SetCamera | `SetCamera()` |
| Spotlight | `Spotlight()` |
| StereoAnaglyph | `StereoAnaglyph()` |
| StereoConvergence | `StereoConvergence()` |
| StereoSeparation | `StereoSeparation()` |
| TurnTable | `TurnTable()` |
| ViewAzimuth | `ViewAzimuth()` |
| ViewElevation | `ViewElevation()` |
| ViewLook | `ViewLook()` |
| ViewMode | `ViewMode()` |
| ViewNum | `ViewNum()` |
| ViewPerspective | `ViewPerspective()` |
| ViewPitch | `ViewPitch()` |
| ViewRoll | `ViewRoll()` |
| ViewSizing | `ViewSizing()` |
| ViewZoom | `ViewZoom()` |

### Materials/Textures (34 commands)

| Command | Syntax |
|---------|--------|
| BackdropColor | `BackdropColor()` |
| BackgroundColor | `BackgroundColor()` |
| BumpDisplacement | `BumpDisplacement()` |
| BumpDistance | `BumpDistance()` |
| BumpFringe | `BumpFringe()` |
| BumpSharp | `BumpSharp()` |
| BumpSharpness | `BumpSharpness()` |
| ColorSpace | `ColorSpace()` |
| ColorSpaceBkg | `ColorSpaceBkg()` |
| ColorSpaceOpenGL | `ColorSpaceOpenGL()` |
| FlareLensElement | `FlareLensElement()` |
| FogColor | `FogColor()` |
| FogDistance | `FogDistance()` |
| GroundColor | `GroundColor()` |
| MatteColor | `MatteColor()` |
| RayTrace | `RayTrace()` |
| RayTraceEffects | `RayTraceEffects()` |
| RayTraceOcclusion | `RayTraceOcclusion()` |
| RayTraceRefraction | `RayTraceRefraction()` |
| ReflectionColor | `ReflectionColor()` |
| ReflectionTrace | `ReflectionTrace()` |
| ShadowColor | `ShadowColor()` |
| SkyColor | `SkyColor()` |
| SkyRadiosity | `SkyRadiosity()` |
| SkyReflection | `SkyReflection()` |
| SubsurfaceColor | `SubsurfaceColor()` |
| TranslucencyColor | `TranslucencyColor()` |
| ZenithColor | `ZenithColor()` |

### Plugins/Servers (7 commands)

| Command | Syntax |
|---------|--------|
| ApplyServer | `ApplyServer(klass, name)` |
| EditPlugins | `EditPlugins()` |
| EditServer | `EditServer(klass, index)` |
| EnableServer | `EnableServer(klass, index, enable)` |
| FlushUnusedPlugins | `FlushUnusedPlugins()` |
| LastPluginInterface | `LastPluginInterface()` |
| MasterPlugins | `MasterPlugins()` |

### Rendering (28 commands)

| Command | Syntax |
|---------|--------|
| AbortRender | `AbortRender()` |
| DisplayOptions | `DisplayOptions()` |
| ExtRendererOptions | `ExtRendererOptions()` |
| FieldRendering | `FieldRendering()` |
| FreePreview | `FreePreview()` |
| MotionBlur | `MotionBlur()` |
| MotionBlurControls | `MotionBlurControls()` |
| MotionBlurEngine | `MotionBlurEngine()` |
| MotionBlurGlobal | `MotionBlurGlobal()` |
| MotionBlurTransparency | `MotionBlurTransparency()` |
| NetRender | `NetRender()` |
| PlayPreview | `PlayPreview()` |
| PreviewCustom | `PreviewCustom()` |
| PreviewDraw | `PreviewDraw()` |
| PreviewFirst | `PreviewFirst()` |
| PreviewLast | `PreviewLast()` |
| PreviewRayTrace | `PreviewRayTrace()` |
| Render | `Render()` |
| RenderCamera | `RenderCamera()` |
| RenderFrame | `RenderFrame()` |
| RenderFrames | `RenderFrames(first, last)` |
| RenderOptions | `RenderOptions()` |
| RenderScene | `RenderScene()` |
| SetBoudningBox | `SetBoudningBox()` |
| StereoRender | `StereoRender()` |
| UndockPreview | `UndockPreview()` |
| UseCompile | `UseCompile()` |
| UseTransport | `UseTransport()` |

### Scene (15 commands)

| Command | Syntax |
|---------|--------|
| BakeRadiosityScene | `BakeRadiosityScene()` |
| ClearScene | `ClearScene()` |
| DefaultSceneLength | `DefaultSceneLength()` |
| InitialKeyframePerScene | `InitialKeyframePerScene()` |
| Multilayer | `Multilayer()` |
| OBJOneLayer | `OBJOneLayer()` |
| PreClearScene | `PreClearScene()` |
| ProtectLegacyScenes | `ProtectLegacyScenes()` |
| RecentScenes | `RecentScenes()` |
| RenameLayer | `RenameLayer()` |
| RenameLayerB | `RenameLayerB()` |
| SceneEditor | `SceneEditor()` |
| SceneEditorOpen | `SceneEditorOpen()` |
| UnseenByAlphaChannel | `UnseenByAlphaChannel()` |

### Selection (66 commands)

| Command | Syntax |
|---------|--------|
| AddToSelection | `AddToSelection()` |
| ClearSelected | `ClearSelected()` |
| DisableFromSelection | `DisableFromSelection()` |
| EnableFromSelection | `EnableFromSelection()` |
| FirstItem | `FirstItem()` |
| FitSelected | `FitSelected()` |
| ItemColor | `ItemColor()` |
| ItemInfo | `ItemInfo()` |
| ItemName | `ItemName()` |
| ItemParent | `ItemParent()` |
| ItemPivot | `ItemPivot()` |
| ItemRotation | `ItemRotation()` |
| ItemScale | `ItemScale()` |
| ItemSkeleton | `ItemSkeleton()` |
| ItemTranslation | `ItemTranslation()` |
| ItemType | `ItemType()` |
| ItemsSelect | `ItemsSelect()` |
| NextItem | `NextItem()` |
| ParentItem | `ParentItem()` |
| PositionItem | `PositionItem()` |
| PreviousItem | `PreviousItem()` |
| RemoveFromSelection | `RemoveFromSelection()` |
| RenderSelected | `RenderSelected()` |
| RotationItem | `RotationItem()` |
| ScaleItem | `ScaleItem()` |
| SelectAll | `SelectAll()` |
| SelectByChannel | `SelectByChannel()` |
| SelectFromRest | `SelectFromRest()` |
| SelectItem | `SelectItem()` |
| SelectItemByID | `SelectItemByID()` |
| SelectItemB | `SelectItemB()` |
| SelectItemBegin | `SelectItemBegin()` |
| SelectItemEnd | `SelectItemEnd()` |
| SelectItemMode | `SelectItemMode()` |
| SelectNone | `SelectNone()` |
| SelectedItemCount | `SelectedItemCount()` |
| SelectionOrder | `SelectionOrder()` |

### Transform (40 commands)

| Command | Syntax |
|---------|--------|
| BTransform | `BTransform()` |
| BoneRestPosition | `BoneRestPosition()` |
| HTransform | `HTransform()` |
| Move | `Move()` |
| MoveItems | `MoveItems()` |
| MoveLight | `MoveLight()` |
| MoveSelected | `MoveSelected()` |
| MoveTo | `MoveTo()` |
| MoveUser | `MoveUser()` |
| MoveView | `MoveView()` |
| PTransform | `PTransform()` |
| Pivot | `Pivot()` |
| PivotPosition | `PivotPosition()` |
| Position | `Position()` |
| RecordPivot | `RecordPivot()` |
| RecordPosition | `RecordPosition()` |
| RecordRotation | `RecordRotation()` |
| RecordScale | `RecordScale()` |
| Rotate | `Rotate()` |
| RotateItems | `RotateItems()` |
| RotateLight | `RotateLight()` |
| RotateSelected | `RotateSelected()` |
| RotateUser | `RotateUser()` |
| RotateView | `RotateView()` |
| Scale | `Scale()` |
| ScaleItems | `ScaleItems()` |
| ScaleLight | `ScaleLight()` |
| ScaleSelected | `ScaleSelected()` |
| ScaleUser | `ScaleUser()` |
| ScaleView | `ScaleView()` |
| Transform | `Transform()` |
| TransformItem | `TransformItem()` |
| XTransform | `XTransform()` |
| YTransform | `YTransform()` |
| ZTransform | `ZTransform()` |

---

## Modeler Commands

3D polygon modeling and mesh editing.

### Create/Modify (16 commands)

| Command | Syntax |
|---------|--------|
| alignpols | `alignpols()` |
| delete | `delete()` |
| flip | `flip()` |
| make4patch | `make4patch()` |
| mergepoints | `mergepoints()` |
| mergepols | `mergepols()` |
| removepols | `removepols()` |
| setviewcenter | `setviewcenter()` |
| setviewdirection | `setviewdirection()` |
| setviewposlookat | `setviewposlookat()` |
| setviewrotation | `setviewrotation()` |
| setviewscale | `setviewscale()` |
| setviewzoffset | `setviewzoffset()` |
| splitpols | `splitpols()` |
| triple | `triple()` |
| unifypols | `unifypols()` |

### File Operations (6 commands)

| Command | Syntax |
|---------|--------|
| close | `close()` |
| close_all | `close_all()` |
| load | `load()` |
| new | `new()` |
| revert | `revert()` |
| save | `save()` |

### General (17 commands)

| Command | Syntax |
|---------|--------|
| array | `array()` |
| center | `center()` |
| changepart | `changepart()` |
| clone | `clone()` |
| copy | `copy()` |
| cut | `cut()` |
| exit | `exit()` |
| invert_hide | `invert_hide()` |
| jitter | `jitter()` |
| paste | `paste()` |
| quantize | `quantize()` |
| railclone | `railclone()` |
| redo | `redo()` |
| smooth | `smooth()` |
| toggleccend | `toggleccend()` |
| toggleccstart | `toggleccstart()` |
| undo | `undo()` |

### Geometry (12 commands)

| Command | Syntax |
|---------|--------|
| axisdrill | `axisdrill()` |
| boolean | `boolean()` |
| changesurface | `changesurface()` |
| freezecurves | `freezecurves()` |
| meshedit | `meshedit()` |
| morphpols | `morphpols()` |
| railextrude | `railextrude()` |
| skinpols | `skinpols()` |
| smoothcurves | `smoothcurves()` |
| soliddrill | `soliddrill()` |
| subdivide | `subdivide()` |
| togglepatches | `togglepatches()` |

### Plugins/Servers (2 commands)

| Command | Syntax |
|---------|--------|
| cmdseq | `cmdseq()` |
| plugin | `plugin()` |

### Selection (3 commands)

| Command | Syntax |
|---------|--------|
| sel_hide | `sel_hide()` |
| sel_invert | `sel_invert()` |
| sel_unhide | `sel_unhide()` |

### Transform (6 commands)

| Command | Syntax |
|---------|--------|
| pathclone | `pathclone()` |
| pathextrude | `pathextrude()` |
| smscale | `smscale()` |
| unweld | `unweld()` |
| weldaverage | `weldaverage()` |
| weldpoints | `weldpoints()` |

---

## Usage via MCP

These commands are available through the LightWave MCP Server:

```
discover_lightwave()              # Find running LightWave instances
connect_layout(address, port)     # Connect to Layout
connect_modeler(address, port)    # Connect to Modeler
send_layout_command(cmd, args)     # Send command to Layout
send_modeler_command(cmd, args)    # Send command to Modeler
list_layout_commands()             # List all Layout commands
list_modeler_commands()            # List all Modeler commands
```
