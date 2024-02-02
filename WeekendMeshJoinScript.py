import bpy


def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    
def GameReadyMeshJoin():
    bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.join()    
    bpy.ops.object.modifier_add(type='TRIANGULATE')
    bpy.context.object.modifiers["Triangulate"].min_vertices = 5
    
def CleanUp():
    # Getting rid of stuff with no faces
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.delete_loose()
    bpy.ops.object.editmode_toggle()

def AllQuads():    
    # Getting all quads
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.tris_convert_to_quads(uvs=True, seam=True, sharp=True, materials=True)
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.modifier_add(type='TRIANGULATE')
    bpy.context.object.modifiers["Triangulate"].min_vertices = 5

def FixNormals():    
    # Fixing normals
    bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
    bpy.context.object.modifiers["WeightedNormal"].keep_sharp = True
    bpy.context.object.modifiers["WeightedNormal"].weight = 64
    bpy.ops.mesh.customdata_custom_splitnormals_clear()
    bpy.ops.object.shade_smooth(use_auto_smooth=True, auto_smooth_angle=1.0472) #This is for 60 degree
    

if (len(bpy.context.selected_objects) <= 0):
    ShowMessageBox("You must select at least one object in the scene.", "Mesh Joining - Script", 'ERROR')
else:
    # Cache a reference to all selected objects.
    objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    # Switch to Object Mode, as this script will only work in that context.
    bpy.ops.object.mode_set(mode='OBJECT')
    
    GameReadyMeshJoin()
    CleanUp()
    AllQuads() #This one is Heavy! comment it out  for +1M tris or more
    FixNormals()
    