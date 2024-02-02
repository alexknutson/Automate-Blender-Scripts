import bpy
from bpy.types import Operator, Panel

bl_info = {
    "name": "LOD Generator",
    "blender": (2, 80, 0),
    "category": "Object",
    "author": "Alex Knutson",
    "version": (1, 0),
    "description": "Generate Level of Detail (LOD) objects for the selected mesh"
}

class LODProperties(bpy.types.PropertyGroup):
    lod0_ratio: bpy.props.FloatProperty(
        name="LOD0 Decimation Ratio",
        default=0.9,
        min=0.0,
        max=1.0,
    )
    lod1_ratio: bpy.props.FloatProperty(
        name="LOD1 Decimation Ratio",
        default=0.75,
        min=0.0,
        max=1.0,
    )
    lod2_ratio: bpy.props.FloatProperty(
        name="LOD2 Decimation Ratio",
        default=0.5,
        min=0.0,
        max=1.0,
    )
    lod3_ratio: bpy.props.FloatProperty(
        name="LOD3 Decimation Ratio",
        default=0.2,
        min=0.0,
        max=1.0,
    )

class OBJECT_OT_generate_lods(Operator):
    bl_idname = "object.generate_lods"
    bl_label = "Generate LODs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
         # Get the LODProperties
        lod_props = context.scene.lod_properties

        if obj is None:
            self.report({'WARNING'}, "No object selected")
            return {'CANCELLED'}

        # Get the collections that the original object belongs to
        original_collections = obj.users_collection

        # Use the ratios from LODProperties
        decimate_ratios = [lod_props.lod0_ratio, lod_props.lod1_ratio, lod_props.lod2_ratio, lod_props.lod3_ratio]
        lod_names = ["_LOD0", "_LOD1", "_LOD2", "_LOD3"]

        ##############################################
        # Optional - Create a new "LOD" collection in the root and make that the parent for the LOD objects.
        # if "LOD" not in bpy.data.collections:
        #     lod_collection = bpy.data.collections.new("LOD")
        #     bpy.context.scene.collection.children.link(lod_collection)
        # else:
        #     lod_collection = bpy.data.collections["LOD"]
        ##############################################

        original_position = obj.location.copy()

        # Calculate the width of the object's bounding box
        bounding_box = obj.bound_box
        width = max([co[0] for co in bounding_box]) - min([co[0] for co in bounding_box])

        # Calculate the separation distance as a percentage of the width
        separation_distance = 1.1 * width  # 10% of the width

        for i, ratio in enumerate(decimate_ratios):
            new_obj = obj.copy()
            new_obj.data = obj.data.copy()
            new_obj.animation_data_clear()

            # Remove any ".001", ".002" from the object name
            normalizedObjectName = new_obj.name.split(".")[0]
            new_obj.name = normalizedObjectName + lod_names[i]

            decimate_mod = new_obj.modifiers.new(new_obj.name + "_decimate", 'DECIMATE')
            decimate_mod.ratio = ratio

            # Link the new object to the same collections as the original object
            for collection in original_collections:
                collection.objects.link(new_obj)

            # Adjust the translation to be a percentage of the width of the object
            new_obj.location.x = original_position.x + (i + 1) * separation_distance  

        context.scene["lod_original_position"] = original_position

        return {'FINISHED'}



class OBJECT_OT_apply_lods(Operator):
    bl_idname = "object.apply_lods"
    bl_label = "Apply LODs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        lod_collection = context.view_layer.active_layer_collection.collection

        if lod_collection is None:
            self.report({'WARNING'}, "No LODs to apply")
            return {'CANCELLED'}

        original_position = context.scene.get("lod_original_position")

        if original_position is None:
            self.report({'WARNING'}, "Original position not found")
            return {'CANCELLED'}

        for obj in lod_collection.objects:
            context.view_layer.objects.active = obj  # Make the object active
            bpy.ops.object.mode_set(mode='OBJECT')  # Ensure we're in object mode
            modifiers_to_apply = [mod for mod in obj.modifiers if mod.type == 'DECIMATE' and mod.name.endswith("_decimate")]
            for mod in modifiers_to_apply:
                # Apply the modifier by name
                bpy.ops.object.modifier_apply(modifier=mod.name)

            obj.location = original_position

        return {'FINISHED'}

class VIEW3D_PT_lod_generator(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "LOD Generator"
    bl_category = "LOD Generator"

    def draw(self, context):
        layout = self.layout
        lod_props = context.scene.lod_properties

        layout.prop(lod_props, "lod0_ratio")
        layout.prop(lod_props, "lod1_ratio")
        layout.prop(lod_props, "lod2_ratio")
        layout.prop(lod_props, "lod3_ratio")

        layout.operator(OBJECT_OT_generate_lods.bl_idname)
        layout.operator(OBJECT_OT_apply_lods.bl_idname)

def register():
    bpy.utils.register_class(LODProperties)
    bpy.types.Scene.lod_properties = bpy.props.PointerProperty(type=LODProperties)
    bpy.utils.register_class(OBJECT_OT_generate_lods)
    bpy.utils.register_class(OBJECT_OT_apply_lods)
    bpy.utils.register_class(VIEW3D_PT_lod_generator)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_lod_generator)
    bpy.utils.unregister_class(OBJECT_OT_apply_lods)
    bpy.utils.unregister_class(OBJECT_OT_generate_lods)
    del bpy.types.Scene.lod_properties
    bpy.utils.unregister_class(LODProperties)

if __name__ == "__main__":
    register()
