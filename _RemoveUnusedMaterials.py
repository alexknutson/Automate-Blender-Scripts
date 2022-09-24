import bpy

# Cache a reference to all selected objects.
objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

for obj in objs:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.material_slot_remove_unused()