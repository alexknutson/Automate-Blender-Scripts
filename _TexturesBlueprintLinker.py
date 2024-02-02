import bpy
import os

# Set the full path to the textures-blueprint.blend file
textures_blueprint_file = r"G:\My Drive\WeMightDie\We Might Die - 3D Artist\textures-blueprint.blend"

# Load the materials from the textures-blueprint.blend file
with bpy.data.libraries.load(textures_blueprint_file, link=True) as (data_from, data_to):
    for mat in data_from.materials:
        data_to.materials.append(mat)

# Replace the materials in the current blend file with the linked versions
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material:
                mat_name = slot.material.name
                linked_material = bpy.data.materials.get(mat_name)

                if linked_material and not linked_material.library:
                    # Check for the linked version of the material
                    for lib_material in bpy.data.materials:
                        if lib_material.library and lib_material.name == mat_name:
                            slot.material = lib_material
                            break

# Remove unused materials
for mat in bpy.data.materials:
    if not mat.users and not mat.library:
        bpy.data.materials.remove(mat)

print("Materials replaced successfully!")