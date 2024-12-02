import bpy

from ..generator import Generator
from ..operators import MESHGEN_OT_LoadGenerator


class MESHGEN_PT_Setup(bpy.types.Panel):
    bl_idname = "MESHGEN_PT_setup"
    bl_label = "Setup"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MeshGen"

    @classmethod
    def poll(cls, context):
        generator = Generator.instance()
        return generator.has_dependencies() and not generator.is_generator_loaded()

    def draw(self, context):
        layout = self.layout
        layout.operator(MESHGEN_OT_LoadGenerator.bl_idname, text="Load Generator")
