import bpy
from datetime import date
from os import system
cls = lambda: system('cls')

# Cache a reference to all selected objects.
objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

# Switch to Object Mode, as this script will only work in that context.
bpy.ops.object.mode_set(mode='OBJECT')

# GLOBALS
finalReport = ""
totalVertsRemoved = 0

#region Helpers

#########################
# Utility to give us the option of showing a popup around the user's cursor for warnings/errors.
#########################
def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#########################
# Outputs the prefix to the blender terminal before we begin optimizing.
#########################
def OutputReportPrefixToTerminal():
    # Add some space between terminal outputs.
    for x in range(6):
        print("")
    for x in range(4):
        print("###########################################")
    print("")
    print("'Quality is never an accident. It is always the result of intelligent effort' \n- John Ruskin")
    print("")
    print("###########################################")
    print("")
    print("Begin Optimizing {}....".format(bpy.path.basename(bpy.context.blend_data.filepath)))
    print("")  
    for x in range(1):
        print("###########################################")
    print("")   

#########################
# Outputs the final report to the blender terminal after we have optimized the selected objects.
#########################
def PrintFinalReport():
    global finalReport
    global totalVertsRemoved
    
    today = date.today()
    
    print("")
    for x in range(2):
        print("###########################################")
    print("")    
    print("FINAL REPORT")
    print("")  
    print("Report Date: {}".format(today))
    print("")
    for x in range(1):
        print("###########################################")
    print("")
    print(finalReport)
    print("TOTAL VERTICES REMOVED: {}".format(totalVertsRemoved))
    print("")
    for x in range(4):
        print("###########################################")

#########################
# Clears out the blender terminal of all previous text output.
#########################    
def ClearTerminal():
    cls()

#########################
# Cleans up any orphan material data that still exists in the blend file after the 
# selected objects have been optimized. ie. Yellow.001 material.
#########################    
def PurgeOrphanMaterialData():
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block) 

#endregion

#region Tasks
#########################
# Assign original material to all instances of a duplicate material
# Example: Any object with "Material.001" assigned would have it replaced with "Material"
#########################            
def RemoveDuplicateMaterials():
    global finalReport
    
    mats = bpy.data.materials

    # Loop through all selected objects.
    for obj in objs:
        # For each material slot on the selected object.
        for slt in obj.material_slots:
            # split the material name into different parts.
            part = slt.name.rpartition('.')
            # if part 2 is numeric (001, 002, etc) and part 0 (Yellow) exists in our materials list...
            if part[2].isnumeric() and part[0] in mats:
                # search for any faces using the duplicate material. ie. Yellow.001
                faces = [x for x in obj.data.polygons if x.material_index == obj.material_slots.find(slt.name)]
                # if we found any faces... 
                if (len(faces) > 0):
                    for f in faces:
                        finalReport += "Re-assigned duplicated material faces to original material in {} \n".format(obj.name)
                        # reassign to the original mat (Yellow)
                        f.material_index = obj.material_slots.find(part[0])
       
#########################
# Automatically remove materials from selected objects that aren't assigned to any faces
#########################
def RemoveUnusedMaterials(obj):
    global finalReport
    
    count = len(obj.material_slots)
    #print("Old Material Slot Count: {}".format(count))
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.material_slot_remove_unused()
    newCount = len(obj.material_slots)
    #print("New Material Slot Count: {}".format(newCount))
    if (count != newCount):
        finalReport += "Removed unused materials in {} \n".format(obj.name)

#########################
# Remove ALL Empty(unnamed) Material Slots from Selected Objects
# Example: Unnamed material slots are removed from all selected objects and only the named materials remain. 
#########################
def RemoveEmptyMaterialSlots(obj):
    global finalReport
    
    for x in obj.material_slots:
        if x.name == "":
            bpy.context.view_layer.objects.active = obj
            obj.active_material_index = x.slot_index
            bpy.ops.object.material_slot_remove()
            finalReport += "Removed empty materials in {} \n".format(obj.name)

#########################
# Re-order Materials by Name to Alphabetical Order
# Example: BEFORE: blue, white, red, green, black. AFTER: black, blue, green, red, white
#########################                 
def ApplyAlphabeticalOrderToMaterials(obj):
    mats = [mat.name for mat in obj.material_slots]
    mats.sort()

    for i, mat_name in enumerate(mats):
        # set active material slot to end slot
        obj.active_material_index = len(obj.material_slots)-1
        while obj.active_material.name != mat_name:
            obj.active_material_index -=1
        while obj.active_material_index > i:
            bpy.ops.object.material_slot_move(direction='UP')

#########################
# Merge vertices based on their proximity to optimize total vert count.
#########################                
def MergeByDistance(obj):
    global finalReport
    global totalVertsRemoved
    
    # Cache a quick reference to the current vert count so we can compare later.
    oldVertCount = len(obj.data.vertices);
    
    # Remove Doubles (Merge By Distance)
    bpy.ops.object.select_all(action='DESELECT') # deselect all object
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.editmode_toggle()
    
    newVertCount = len(obj.data.vertices);
    vertCountDifference = oldVertCount - newVertCount;
    totalVertsRemoved += vertCountDifference;
    if (oldVertCount != newVertCount):
        finalReport += "Merge by Distance removed {difference} vertices in {name} \n".format(name=obj.name, difference=vertCountDifference)

#endregion

#region Init
#########################
# Runs a series of methods to optimize the blend file and selected objects.
#########################       
def RunOptimizations():
    # Run through any pre-processors first.
    OutputReportPrefixToTerminal()   
    RemoveDuplicateMaterials()

    # Run the main loop through all selected objects and do work.
    for obj in objs:
            RemoveUnusedMaterials(obj)
            RemoveEmptyMaterialSlots(obj)
            ApplyAlphabeticalOrderToMaterials(obj)
            MergeByDistance(obj)
            
    # Finalize by purging any orphan material data.
    PurgeOrphanMaterialData()

# If the user has not selected any objects, throw an error.
if (len(bpy.context.selected_objects) <= 0):
    ShowMessageBox("You must select at least one object in the scene.", "Automate Blender Scripts - Optimization Script", 'ERROR')
else:
    ClearTerminal()
    # GO GO TILE OPTIMIZATIONS!     
    RunOptimizations()
    PrintFinalReport()

#endregion
