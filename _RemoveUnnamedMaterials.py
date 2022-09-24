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