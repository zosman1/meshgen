import bpy

from ..generator.generator import Generator
from ..operators import (
    MESHGEN_OT_GenerateMesh,
    MESHGEN_OT_CancelGeneration,
)


class MESHGEN_PT_Panel(bpy.types.Panel):
    bl_idname = "MESHGEN_PT_panel"
    bl_label = "Generate"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MeshGen"

    @classmethod
    def poll(cls, context):
        generator = Generator.instance()
        return generator.is_generator_loaded()

    def draw(self, context):
        layout = self.layout
        props = context.scene.meshgen_props

        layout.prop(props, "prompt")
        layout.separator()
        if props.is_running:
            layout.operator(MESHGEN_OT_CancelGeneration.bl_idname, text="Cancel Generation")
        else:
            layout.operator(MESHGEN_OT_GenerateMesh.bl_idname, text="Generate Mesh")

        if props.vertices_generated > 0 or props.faces_generated > 0:
            layout.separator()
            if props.vertices_generated > 0:
                layout.label(text=f"Generated {props.vertices_generated} vertices")
            if props.faces_generated > 0:
                layout.label(text=f"Generated {props.faces_generated} faces")
            if not props.is_running:
                if props.cancelled:
                    layout.label(text="Generation cancelled")
                else:
                    layout.label(text="Generation complete")
