import bpy

from ..generator import Generator


class MESHGEN_PT_Warning(bpy.types.Panel):
    bl_idname = "MESHGEN_PT_warning"
    bl_label = "Warning"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MeshGen"

    @classmethod
    def poll(cls, context):
        generator = Generator.instance()
        return not generator.has_dependencies()

    def draw(self, context):
        layout = self.layout
        layout.label(text="Complete setup in addon preferences.", icon="ERROR")
