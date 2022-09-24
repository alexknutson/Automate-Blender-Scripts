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