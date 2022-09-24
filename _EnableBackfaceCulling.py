import bpy

for material in bpy.data.materials:
    material.use_backface_culling = True