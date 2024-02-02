import bpy

# Set the Manual height here:
#BSH = 5.4
#Otherwise it usess the 3d cursor's Z Value
BSH = bpy.context.scene.cursor.location[2]



def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

if (len(bpy.context.selected_objects) <= 0):
    ShowMessageBox("You must select at least one object in the scene.", "Mesh Joining - Script", 'ERROR')
else:
    # Cache a reference to all selected objects.
    objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    # Switch to Object Mode, as this script will only work in that context.
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.context.object.name = "RoofREF"
    bpy.ops.object.duplicate(linked=False, mode='TRANSLATION' )
    bpy.context.object.name = "MainHullREF"
    bpy.ops.object.duplicate(linked=False, mode='TRANSLATION' )
    bpy.context.object.name = "BackupMainHullREF"
    bpy.ops.object.duplicate(linked=False, mode='TRANSLATION' )
    bpy.context.object.name = "leftoversdodelete"

    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.name.startswith('MainHullREF'):
            obj.select_set(True)

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(plane_co=(0, 0, BSH), plane_no=(0, 0, 1), use_fill=False, clear_inner=False, clear_outer=True, xstart=177, xend=639, ystart=266, yend=228, flip=False)
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.editmode_toggle()

    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.name.startswith('RoofREF'):
            obj.select_set(True)

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(plane_co=(0, 0, BSH), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, clear_outer=False, xstart=177, xend=639, ystart=266, yend=228, flip=False)
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.editmode_toggle()

    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.name.startswith('leftoversdodelete'):
            obj.select_set(True)
            bpy.ops.object.delete(use_global=False)
            
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.name.startswith('BackupMainHullREF'):
            obj.select_set(True)
            obj.hide_set(True)

