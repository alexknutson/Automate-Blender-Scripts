# Automate-Blender-Scripts
A collection of Python scripts to automate common blender tasks.

![Automation Gif](https://media2.giphy.com/media/1nR6fu93A17vWZbO9c/giphy.gif)

### Install
1) Clone the repo `git clone git@github.com:alexknutson/Automate-Blender-Scripts.git`
2) Switch to the `Scripting` tab in Blender
3) Click the folder button to open a new script
4) Navigate to the script you want to run and open it
5) Select any objects you want the script to work on
6) Click the "Play" button and let the magic happen

## Examples Included

#### Enable Backface Culling on All Materials
![Blender-Turn-On-Backface-Culling-On-All-Materials](https://user-images.githubusercontent.com/905228/192082577-e1804815-29ce-4a18-93b3-b3a66838890d.gif)
```python
import bpy

# Loop over all materials in the project.
for material in bpy.data.materials:
    material.use_backface_culling = True
```

----
<br>

#### Replace Material in Selected Objects with New Material By Name

[![Blender-Replace-Material-By-Name-gif](https://user-images.githubusercontent.com/905228/192082785-24d546a0-33f8-47fb-8617-bf3ec2a1c772.gif)](https://user-images.githubusercontent.com/905228/192082698-1abf586f-fb14-4408-946e-d7533702489e.mp4)


```python

import bpy

# Cache a reference to all selected objects.
objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

def replace_material(object,old_material,new_material):
    """
    replace a material in blender.
    params:
        object - object for which we are replacing the material
        old_material - The old material name as a string
        new_material - The new material name as a string
    """
    ob = object
    om = bpy.data.materials[old_material]
    nm = bpy.data.materials[new_material]
    # Iterate over the material slots and replace the material
    for s in ob.material_slots:
        if s.material.name == old_material:
            s.material = nm
            
# Loop through all selected objects.
for obj in objs:
    for slot in obj.material_slots:
        if (slot.name == "OLD-MATERIAL"):
            replace_material(obj, "OLD-MATERIAL", "NEW-MATERIAL")
```

----
<br>

#### Automatically Remove Materials from Selected Objects that aren't assigned to any faces
![Blender-Remove-Unused-Materials-Not-Assigned-To-Faces](https://user-images.githubusercontent.com/905228/192082924-1f154d50-796c-4e26-b213-06a4691dcf56.gif)
```python
import bpy

# Cache a reference to all selected objects.
objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

for obj in objs:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.material_slot_remove_unused()
```

----
<br>

#### Remove All Empty(unnamed) Material Slots from Selected Objects
![Blender-Remove-Empty-Material-Slots-All-Selected-Objects](https://user-images.githubusercontent.com/905228/192082974-8bd7af82-3fd8-4157-b01c-893621ac491e.gif)

> Unnamed material slots are removed from all selected objects and only the named materials remain.
```python
import bpy

# Cache a reference to all selected objects.
objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

for obj in objs:
    for x in obj.material_slots:
        if x.name == "":
            bpy.context.view_layer.objects.active = obj
            obj.active_material_index = x.slot_index
            bpy.ops.object.material_slot_remove()
            print("Removed empty material from... " + obj.name)
```

----
<br>

#### Assign original material to all instances of a duplicate material
> Any object with "Material.001" assigned would have it replaced with "Material"
```python
import bpy
mats = bpy.data.materials

for obj in bpy.data.objects:
    for slt in obj.material_slots:
        part = slt.name.rpartition('.')
        if part[2].isnumeric() and part[0] in mats:
            slt.material = mats.get(part[0])
```

----
<br>

#### Re-order Materials by Name to Alphabetical Order
> BEFORE: blue, white, red, green, black. AFTER: black, blue, green, red, white
```python
import bpy

context = bpy.context
ob = context.object

ob_mats = [mat.name for mat in ob.material_slots]
ob_mats.sort()

for i, mat_name in enumerate(ob_mats):
    # set active material slot to end slot
    ob.active_material_index = len(ob.material_slots)-1
    while ob.active_material.name != mat_name:
        ob.active_material_index -=1
    while ob.active_material_index > i:
        bpy.ops.object.material_slot_move(direction='UP')
```
