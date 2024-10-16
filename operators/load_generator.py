import bpy
import sys

from ..generator.generator import Generator
from ..utils import open_console


class MESHGEN_OT_LoadGenerator(bpy.types.Operator):
    bl_idname = "meshgen.load_generator"
    bl_label = "Load Generator"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        if sys.platform == "win32":
            open_console()

        Generator.instance().load_generator()

        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()

        return {"FINISHED"}
