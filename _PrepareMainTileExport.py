"""
Automates the process of correcting and renaming objects in a scene
and then selecting all objects needed for the Main Tile Object.
 
The script first calculates the Levenshtein distance between strings to find the closest matching 
names for NavMesh objects, even when the "NavMesh" prefix is misspelled. The script then deselects 
all objects, iterates through the objects in the scene, corrects the misspelled NavMesh names, selects 
and renames LOD objects, selects all main tile objects, and selects lights in the scene.
"""
import bpy

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def fix_misspelled_navmesh_names(obj_name):
    navmesh_names = [
        "NavMeshFloor",
        "NavMeshCeiling",
        "NavMeshEastSouthWall",
        "NavMeshNorthEastWall",
        "NavMeshSouthWestWall",
        "NavMeshSouthEastWall",
        "NavMeshWestNorthWall",
        "NavMeshEastWall",
        "NavMeshWestWall",
        "NavMeshNorthWall",
        "NavMeshSouthWall",
        "NavMeshEastSouth",
        "NavMeshNorthEast",
        "NavMeshSouthWest",
        "NavMeshWestNorth",
    ]

    if not obj_name.startswith("NavMesh"):
        for prefix in ["NavMsh", "NvMesh", "NaMesh", "NavMes", "Navesh", "Navmesh"]:
            if obj_name.lower().startswith(prefix.lower()):
                obj_name = "NavMesh" + obj_name[len(prefix):]
                break

    closest_distance = float('inf')
    closest_name = obj_name
    for navmesh_name in navmesh_names:
        distance = levenshtein_distance(obj_name, navmesh_name)
        if distance < closest_distance:
            closest_distance = distance
            closest_name = navmesh_name

    return closest_name

# DESELECT ALL
bpy.ops.object.select_all(action='DESELECT')

for o in bpy.context.scene.objects:
    # Correct misspelled NavMesh names
    if o.name.startswith("NavMesh") or o.name.lower().startswith("navmesh"):
        o.name = fix_misspelled_navmesh_names(o.name)
    
    # SELECT LODs AND RENAME         
    if o.name in ("LOD-0", "LOD0"):
        o.select_set(True)
        o.name = "_LOD0"
    if o.name in ("LOD-1", "LOD1", "_LOD01"):
        o.select_set(True)
        o.name = "_LOD1"
    if o.name in ("LOD-2", "LOD2", "_LOD02"):
        o.select_set(True)
        o.name = "_LOD2"
    if o.name in ("LOD-3", "LOD3", "_LOD03"):
        o.select_set(True)
        o.name = "_LOD3"
    # SELECT ALL MAIN TILE OBJECTS    
    if o.name in ("MainHull","Main Hull","Main hull","main hull","Mainhull","Mainhul","roof","Roof","_LOD0","_LOD1","_LOD2","_LOD3","NavMeshFloor","NavMeshCelling","NavMeshCeiling","NavMesCelling","NavMeshEastSouthWall","NavMeshNorthEastWall","NavMeshSouthWestWall","NavMeshSouthEastWall","NavMeshWestNorthWall","NavMeshEast","NavMeshEastWall","NavMeshWest","NavMeshWestWall","NavMeshNorth","NavMeshNorthWall","NavMeshSouth","NavMeshSouthWall","NavMeshWest","NavMeshEastSouth","NavMeshNorthEast","NavMeshSouthWest","NavMeshWestNorth"):
        o.select_set(True)
    # SELECT LIGHTS
    if o.name in ("Area-Light-1", "Area-Light-2", "Area-Light-3", "Area-Light-4", "Area-Light-5",):
        o.select_set(True)
    if o.name in ("MainHull",):
        bpy.context.view_layer.objects.active = o
