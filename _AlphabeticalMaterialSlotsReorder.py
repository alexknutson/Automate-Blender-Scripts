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