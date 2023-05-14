import bpy

def RemoveZeroVertObjectsFromScene():
    scene = bpy.context.scene

    empty_meshobs = [o for o in scene.objects
                    if o.type == 'MESH'
                    and not o.data.vertices]
                 
    while empty_meshobs:
        bpy.data.objects.remove(empty_meshobs.pop()) 