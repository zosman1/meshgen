import bpy

from .generator import Generator
from .operators.download_models import MESHGEN_OT_DownloadRequiredModels
from .operators.install_dependencies import (MESHGEN_OT_InstallDependencies,
                                             MESHGEN_OT_UninstallDependencies)


class MeshGenPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    @staticmethod
    def register():
        pass

    def draw(self, context):
        layout = self.layout

        generator = Generator.instance()

        has_dependencies = generator.has_dependencies()
        if not has_dependencies:
            layout.label(text="Dependencies not installed.", icon="ERROR")
            box = layout.box()
            box.operator(MESHGEN_OT_InstallDependencies.bl_idname, icon="IMPORT")
            return

        if not generator.has_required_models():
            layout.label(text="Required models not downloaded.", icon="ERROR")
            layout.operator(MESHGEN_OT_DownloadRequiredModels.bl_idname, icon="IMPORT")
            return
        
        layout.label(text="Ready to generate. Press 'N' -> MeshGen to get started.")
        layout.separator()

        layout.prop(context.scene.meshgen_props, "show_developer_options", text="Show Developer Options")

        if context.scene.meshgen_props.show_developer_options:
            box = layout.box()
            box.operator(MESHGEN_OT_UninstallDependencies.bl_idname, icon="IMPORT")
