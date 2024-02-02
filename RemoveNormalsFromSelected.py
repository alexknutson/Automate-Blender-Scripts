import bpy

context = bpy.context
scene = context.scene

selected_mesh_objects = [o for o in context.selected_objects if o.type == 'MESH']

ao = context.view_layer.objects.active

for o in selected_mesh_objects:
    context.view_layer.objects.active = o
    r = bpy.ops.mesh.customdata_custom_splitnormals_clear()
    print(o.name, r)

# change ao back to original   
context.view_layer.objects.active = ao