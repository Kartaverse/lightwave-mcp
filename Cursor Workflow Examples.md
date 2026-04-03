# Cursor + LightWave MCP Workflow Examples

Practical examples of prompts you can use in Cursor to control LightWave 3D via the `lightwave-mcp` server.

## Prerequisites

Before running these examples:
1. LightWave Layout or Modeler must be running with **Command Port enabled**
   - Open the `LightWave > Settings...` menu. In the Preferences window select the first sidebar item. At the bottom of the window is a checkbox `[x] Enable Command Port`.
2. The `lightwave-mcp` server must be running in Cursor

## Default Connection

After you connect to a LightWave instance, the server automatically uses that connection for all subsequent commands in the same session. You never need to pass `connection_id` yourself — the AI remembers it.

| Situation | What happens |
|-----------|--------------|
| One Layout connected | Commands auto-target it |
| One Modeler connected | Commands auto-target it |
| Many connections active | Specify which one (e.g. `send to Layout at 127.0.0.1:30513`) |
| None connected | Error prompts you to connect first |

## Quick Start Workflow

### 1. Connect to LightWave (Simplest Way)

The easiest approach is to let LightWave MCP automatically discover and connect:

**Connect to Layout:**
```
Connect to LightWave Layout
```
or

```
Connect to the LightWave Layout instance at 127.0.0.1 using the default port number
```

**Connect to Modeler:**
```
Connect to LightWave Modeler
```
or

```
Connect to the LightWave Modeler instance at 127.0.0.1 using the default port number
```

This automatically discovers running LightWave instances and connects to the first one found. All future commands in this session automatically target the connected instance.

### 2. Discover LightWave (Optional)

If you need to see all available instances or connect to a specific one:

```
Find all running LightWave instances on my network and show me their addresses and ports
```

This returns something like:
```json
{
  "instances": [
    { "type": "layout", "address": "127.0.0.1", "port": 42626, "version": "2025.0.3580" },
    { "type": "modeler", "address": "127.0.0.1", "port": 42627, "version": "2025.0.3580" }
  ]
}
```

### 3. Connect to a Specific Instance

```
Connect to the LightWave Layout instance at 127.0.0.1 port 42626
```

### 3. Run Commands

Now you can run commands without mentioning connection details:

```
Send the About command to LightWave Layout to display the about dialog
```

## Basic Information Commands

```
List all available Layout commands
```

### Show About Dialog

```
Send the About command to LightWave Layout to display the about dialog
```

### Get Scene Information

```
Show me the current scene statistics
```

## Object Manipulation

### Add Objects (WIP)

**Add a Null:**
```
Add a null to the scene at position 0, 0, 0
```

**Add a Camera:**
```
Add a camera to the scene at position 0, 0, 0
```

**Add a Light:**
```
Add an area light to the scene at position -1, -1, 0
```

### Select Objects

**Select by name:**
```
Select the object named "Camera" in the current scene
```

**Select all objects of a type:**
```
Select all null objects in the scene
```

### Transform Objects (WIP)

**Rotate selected object:**
```
Add a rotation of 45 degrees on the Y-axis to the currently selected object
```

**Move selected object:**
```
Translate the selected object by 5 units on X, 0 on Y, and 3 on Z
```

**Scale selected object:**
```
Scale the selected object by 2, 2, 2
```

### Rename Objects (WIP)

**Rename object by name:**
```
Rename the object currently named "Camera" to "RenderCamera"
```

**Rename selected object:**
```
Rename the currently selected object to "MyCube"
```

## Scene Operations (WIP)

### Save Scene

**Save the current scene:**
```
Save the current LightWave scene
```

**Save scene with filename:**
```
Save the current scene as "my_scene.lws" in the Documents folder
```

### Load Scene

**Load a scene:**
```
Load the scene "my_scene.lws" from the Documents folder
```

### Clear Scene

**Clear the current scene:**
```
Clear the LightWave scene (remove all objects)
```

## Viewport and Camera (WIP)

### Camera Operations

**Create a new camera:**

```
Create a new camera at position 0, 2, -10
```

```
Create a new camera at position 0, 2, -10 looking at the origin
```

**Switch to camera view:**
```
Select "Camera1". Set the viewport to this camera view 
```

### Viewport Operations (WIP)

**Frame all objects:**
```
Frame all objects in the current viewport
```

**Frame All:**
```
Fit all objects in the viewport
```

## Lighting (WIP)

### Light Operations

**Add a point light:**
```
Add a point light at position 0, 5, 0 with color white and intensity 100
```

**Add a distant light:**
```
Add a distant light rotated to 0, 45, 0 with intensity 80
```

**Change light color:**
```
Set the color of the selected light to RGB values 255, 200, 150
```

## Materials and Surfaces (WIP)

### Surface Operations

**Apply a surface:**
```
Apply the surface named "Metal" to the selected object
```

**Change surface color:**
```
Change the color of surface "Plastic" to blue
```

### Create New Surface

```
Create a new surface named "CustomSurface" with diffuse color RGB 128, 64, 32
```

## Animation (WIP)

### Keyframe Operations

**Set position keyframe:**
```
Set a position keyframe for the selected object at time 0 seconds
```

**Set rotation keyframe:**
```
Set a rotation keyframe of 90 degrees on Y for the selected object at frame 24
```

**Set scale keyframe:**
```
Set a scale keyframe of 2, 2, 2 for the selected object at frame 48
```

### Playback Controls

**Set animation end frame:**
```
Set the animation end frame to 120
```

**Go to frame:**
```
Go to frame 60 in the timeline
```

## Modeler Commands (WIP)

### Enter Modeler

Note: Modeler must be running separately with Command Port enabled.

**Connect to Modeler (simplest):**
```
Connect to LightWave Modeler
```

**Connect with explicit address:**
```
Connect to LightWave Modeler at 127.0.0.1 using the default port number
```

**List Available Commands**

```
List all LightWave Modeler commands
```

### Modeler Selection

**Invert selection:**
```
Invert the current selection in Modeler
```

### Geometry Operations

**Copy and paste:**
```
Copy the selected geometry and paste it
```

**Reverse polygon normals:**
```
Reverse the normals of the selected polygons
```

### Tool Operations

## Multi-Step Workflows (WIP)

### Workflow: Setup a Simple Scene

```
I want to set up a simple product visualization scene:
1. Connect to LightWave Layout
2. Clear any existing scene
3. Add a distant light at intensity 80 pointing downward
4. Move the camera to position 0, 0, -3
5. Save the scene as "product_viz.lws"
```

### Workflow: Animate an Object

```
Create an animation of a bouncing null:
1. Connect to LightWave Layout
2. Clear the scene
3. Add a Null named "AnimationNull" at position 0, 5, 0
4. Set keyframes for the Null:
   - Frame 0: position 0, 5, 0
   - Frame 30: position 0, 0, 0
   - Frame 60: position 0, 5, 0
5. Set the end frame to 60
```

## Debugging and Diagnostics (WIP)

### Check Connection Status

```
List all active LightWave connections and show their status
```

### Refresh Command Cache

```
Refresh the command cache to ensure I have the latest LightWave commands available
```

### List Available Commands

```
Show me all available Layout commands
```

```
Show me all available Modeler commands
```

### Test Discovery

```
Run a discovery scan to find all LightWave instances on the network
```

## Error Handling Examples

### Handle Missing Connection

```
If the connection to LightWave fails, try reconnecting up to 3 times before giving up
```

### Handle Invalid Command

```
Send the command "InvalidCommandXYZ" to Layout and show me the error response
```

### Handle Missing Object

```
Try to select an object named "NonExistent" and gracefully handle the case where it doesn't exist
```

## Tips for Effective Prompts

1. **Be Specific**: Include exact positions, sizes, and names when possible
   - Good: `Add a Null at position 0, 2, 5 named "MyNull"`
   - Less Good: `Add a Null somewhere`

2. **Include Context**: Mention what you're trying to achieve
   - Good: `I want to set up a three-point lighting rig for product photography`
   - Less Good: `Add some lights`

3. **Chain Commands**: Use numbered lists for complex operations
   - Cursor can execute multiple MCP calls in sequence

4. **Check State**: When in doubt, ask for the current state first
   - `What's currently selected in LightWave?`
   - `Show me all objects in the current scene`

5. **Handle Errors**: Always have a backup plan
   - If the object doesn't exist, create it first
   - If the command fails, try the alternate syntax

## Quick Reference

| Task | Prompt Hint |
|------|------------|
| Connect to Layout | `Connect to LightWave Layout` |
| Connect to Modeler | `Connect to LightWave Modeler` |
| Connect (explicit) | `Connect to the LightWave Layout instance at 127.0.0.1 using the default port number` |
| Discover | `Find all running LightWave instances on my network` |
| About Dialog | `Send the About command to LightWave Layout to display the about dialog` |
| Save Scene | `Save the current LightWave scene` |
| List Commands | `Show me all available Layout commands` |
| Close | `Close the active LightWave connection` |

> **Note**: After connecting, `connection_id` is auto-resolved — you never need to specify it manually in prompts.

## Getting Help

```
Show me all available tools in the lightwave-mcp server
```

```
Explain how the send_layout_command tool works
```
