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

class OBJECT_OT_generate_lods(Operator):
    bl_idname = "object.generate_lods"
    bl_label = "Generate LODs"
    bl_options = {'REGISTER', 'UNDO'}

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

    def execute(self, context):
        obj = context.active_object

        if obj is None:
            self.report({'WARNING'}, "No object selected")
            return {'CANCELLED'}

        decimate_ratios = [self.lod0_ratio, self.lod1_ratio, self.lod2_ratio, self.lod3_ratio]
        lod_names = ["_LOD0", "_LOD1", "_LOD2", "_LOD3"]

        if "LOD" not in bpy.data.collections:
            lod_collection = bpy.data.collections.new("LOD")
            bpy.context.scene.collection.children.link(lod_collection)
        else:
            lod_collection = bpy.data.collections["LOD"]

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

            new_obj.name = lod_names[i]

            decimate_mod = new_obj.modifiers.new(new_obj.name + "_decimate", 'DECIMATE')
            decimate_mod.ratio = ratio

            lod_collection.objects.link(new_obj)

            # Adjust the translation to be a percentage of the width of the object
            new_obj.location.x = original_position.x + (i + 1) * separation_distance  

        context.scene["lod_original_position"] = original_position

        return {'FINISHED'}



class OBJECT_OT_apply_lods(Operator):
    bl_idname = "object.apply_lods"
    bl_label = "Apply LODs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        lod_collection = bpy.data.collections.get("LOD")

        if lod_collection is None:
            self.report({'WARNING'}, "No LODs to apply")
            return {'CANCELLED'}

        original_position = context.scene.get("lod_original_position")

        if original_position is None:
            self.report({'WARNING'}, "Original position not found")
            return {'CANCELLED'}

        for obj in lod_collection.objects:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_apply({"object": obj}, modifier=obj.name + "_decimate")

            obj.location = original_position

        return {'FINISHED'}

class VIEW3D_PT_lod_generator(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "LOD Generator"
    bl_category = "LOD Generator"

    def draw(self, context):
        layout = self.layout
        operator_generate = layout.operator(OBJECT_OT_generate_lods.bl_idname)

        layout.prop(operator_generate, "lod0_ratio")
        layout.prop(operator_generate, "lod1_ratio")
        layout.prop(operator_generate, "lod2_ratio")
        layout.prop(operator_generate, "lod3_ratio")

        layout.operator(OBJECT_OT_apply_lods.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_generate_lods)
    bpy.utils.register_class(OBJECT_OT_apply_lods)
    bpy.utils.register_class(VIEW3D_PT_lod_generator)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_lod_generator)
    bpy.utils.unregister_class(OBJECT_OT_apply_lods)
    bpy.utils.unregister_class(OBJECT_OT_generate_lods)

if __name__ == "__main__":
    register()
