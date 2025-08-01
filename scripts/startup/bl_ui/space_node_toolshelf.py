# SPDX-License-Identifier: GPL-2.0-or-later

# <pep8 compliant>
import bpy
from bpy import context

#Add tab, Node Group panel
from nodeitems_builtins import node_tree_group_type
from .node_add_menu import draw_node_groups, add_empty_group


# Icon or text buttons in shader editor and compositor in the ADD panel
class NODES_PT_shader_comp_textoricon_shader_add(bpy.types.Panel):
    """The prop to turn on or off text or icon buttons in the node editor tool shelf."""
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Display"
    bl_category = "Add"
    #bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type in {'ShaderNodeTree'})

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene
        row = layout.row()
        row.prop(addon_prefs,"Node_text_or_icon", text = "Icon Buttons")
        row.prop(addon_prefs,"Node_shader_add_common", text = "Common")


# Icon or text buttons in compositor in the ADD panel
class NODES_PT_shader_comp_textoricon_compositor_add(bpy.types.Panel):
    """The prop to turn on or off text or icon buttons in the node editor tool shelf."""
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Display"
    bl_category = "Add"
    #bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type in {'CompositorNodeTree'})

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene
        row = layout.row()
        row.prop(addon_prefs,"Node_text_or_icon", text = "Icon Buttons")


# Icon or text buttons in shader editor and compositor in the RELATIONS panel
class NODES_PT_shader_comp_textoricon_relations(bpy.types.Panel):
    """The prop to turn on or off text or icon buttons in the node editor tool shelf."""
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Display"
    bl_category = "Relations"
    #bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type in {'ShaderNodeTree', 'CompositorNodeTree'})

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene
        layout.prop(addon_prefs,"Node_text_or_icon", text = "Icon Buttons")


# Icon or text buttons in geometry node editor in the ADD panel
class NODES_PT_geom_textoricon_add(bpy.types.Panel):
    """The prop to turn on or off text or icon buttons in the node editor tool shelf."""
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Display"
    bl_category = "Add"
    #bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type in 'GeometryNodeTree')

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene
        layout.prop(addon_prefs,"Node_text_or_icon", text = "Icon Buttons")


# Icon or text buttons in geometry node editor in the RELATIONS panel
class NODES_PT_geom_textoricon_relations(bpy.types.Panel):
    """The prop to turn on or off text or icon buttons in the node editor tool shelf."""
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Display"
    bl_category = "Relations"
    #bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type in 'GeometryNodeTree')

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene
        layout.prop(addon_prefs,"Node_text_or_icon", text = "Icon Buttons")


# Shader editor, Input panel
class NODES_PT_shader_add_input(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Input"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"

    @classmethod
    def poll(cls, context):

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        return addon_prefs.Node_shader_add_common == False and context.space_data.tree_type == 'ShaderNodeTree' # Just in shader mode

    @staticmethod
    def draw(self, context):
        layout = self.layout#### Textbuttons
        default_context = bpy.app.translations.contexts.default

        scene = context.scene

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        ##### Textbuttons

        if not addon_prefs.Node_text_or_icon:

        ##### --------------------------------- Textures common ------------------------------------------- ####

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Ambient Occlusion  ", icon = "NODE_AMBIENT_OCCLUSION")
            props.use_transform = True
            props.type = "ShaderNodeAmbientOcclusion"

            props = col.operator("node.add_node", text=" Attribute          ", icon = "NODE_ATTRIBUTE")
            props.use_transform = True
            props.type = "ShaderNodeAttribute"

            props = col.operator("node.add_node", text=" Bevel               ", icon = "BEVEL")
            props.use_transform = True
            props.type = "ShaderNodeBevel"

            props = col.operator("node.add_node", text=" Camera Data   ", icon = "CAMERA_DATA")
            props.use_transform = True
            props.type = "ShaderNodeCameraData"

            props = col.operator("node.add_node", text=" Color Attribute ", icon = "NODE_VERTEX_COLOR")
            props.use_transform = True
            props.type = "ShaderNodeVertexColor"

            props = col.operator("node.add_node", text=" Fresnel              ", icon = "NODE_FRESNEL")
            props.use_transform = True
            props.type = "ShaderNodeFresnel"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Geometry        ", icon = "NODE_GEOMETRY")
            props.use_transform = True
            props.type = "ShaderNodeNewGeometry"

            props = col.operator("node.add_node", text=" Curves Info       ", icon = "NODE_HAIRINFO")
            props.use_transform = True
            props.type = "ShaderNodeHairInfo"

            props = col.operator("node.add_node", text=" Layer Weight   ", icon = "NODE_LAYERWEIGHT")
            props.use_transform = True
            props.type = "ShaderNodeLayerWeight"

            props = col.operator("node.add_node", text=" Light Path        ", icon = "NODE_LIGHTPATH")
            props.use_transform = True
            props.type = "ShaderNodeLightPath"

            props = col.operator("node.add_node", text=" Object Info       ", icon = "NODE_OBJECTINFO")
            props.use_transform = True
            props.type = "ShaderNodeObjectInfo"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Particle Info     ", icon = "NODE_PARTICLEINFO")
            props.use_transform = True
            props.type = "ShaderNodeParticleInfo"

            props = col.operator("node.add_node", text=" Point Info         ", icon = "POINT_INFO")
            props.use_transform = True
            props.type = "ShaderNodePointInfo"

            props = col.operator("node.add_node", text=" RGB                 ", icon = "NODE_RGB")
            props.use_transform = True
            props.type = "ShaderNodeRGB"

            props = col.operator("node.add_node", text=" Tangent             ", icon = "NODE_TANGENT")
            props.use_transform = True
            props.type = "ShaderNodeTangent"

            props = col.operator("node.add_node", text=" Texture Coordinate", icon = "NODE_TEXCOORDINATE")
            props.use_transform = True
            props.type = "ShaderNodeTexCoord"

            if context.space_data.shader_type == 'LINESTYLE':

                props = col.operator("node.add_node", text=" UV along stroke", icon = "NODE_UVALONGSTROKE")
                props.use_transform = True
                props.type = "ShaderNodeUVALongStroke"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" UV Map            ", icon = "GROUP_UVS")
            props.use_transform = True
            props.type = "ShaderNodeUVMap"

            props = col.operator("node.add_node", text=" Value                ", icon = "NODE_VALUE")
            props.use_transform = True
            props.type = "ShaderNodeValue"

            props = col.operator("node.add_node", text=" Volume Info    ", icon = "NODE_VOLUME_INFO")
            props.use_transform = True
            props.type = "ShaderNodeVolumeInfo"

            props = col.operator("node.add_node", text=" Wireframe        ", icon = "NODE_WIREFRAME")
            props.use_transform = True
            props.type = "ShaderNodeWireframe"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_AMBIENT_OCCLUSION")
            props.use_transform = True
            props.type = "ShaderNodeAmbientOcclusion"

            props = flow.operator("node.add_node", text = "", icon = "NODE_ATTRIBUTE")
            props.use_transform = True
            props.type = "ShaderNodeAttribute"

            props = flow.operator("node.add_node", text="", icon = "BEVEL")
            props.use_transform = True
            props.type = "ShaderNodeBevel"

            props = flow.operator("node.add_node", text="", icon = "CAMERA_DATA")
            props.use_transform = True
            props.type = "ShaderNodeCameraData"

            props = flow.operator("node.add_node", text="", icon = "NODE_VERTEX_COLOR")
            props.use_transform = True
            props.type = "ShaderNodeVertexColor"

            props = flow.operator("node.add_node", text = "", icon = "NODE_FRESNEL")
            props.use_transform = True
            props.type = "ShaderNodeFresnel"

            props = flow.operator("node.add_node", text = "", icon = "NODE_GEOMETRY")
            props.use_transform = True
            props.type = "ShaderNodeNewGeometry"

            props = flow.operator("node.add_node", text = "", icon = "NODE_HAIRINFO")
            props.use_transform = True
            props.type = "ShaderNodeHairInfo"

            props = flow.operator("node.add_node", text = "", icon = "NODE_LAYERWEIGHT")
            props.use_transform = True
            props.type = "ShaderNodeLayerWeight"

            props = flow.operator("node.add_node", text = "", icon = "NODE_LIGHTPATH")
            props.use_transform = True
            props.type = "ShaderNodeLightPath"

            props = flow.operator("node.add_node", text = "", icon = "NODE_OBJECTINFO")
            props.use_transform = True
            props.type = "ShaderNodeObjectInfo"

            props = flow.operator("node.add_node", text = "", icon = "NODE_PARTICLEINFO")
            props.use_transform = True
            props.type = "ShaderNodeParticleInfo"

            props = flow.operator("node.add_node", text = "", icon = "POINT_INFO")
            props.use_transform = True
            props.type = "ShaderNodePointInfo"

            props = flow.operator("node.add_node", text = "", icon = "NODE_RGB")
            props.use_transform = True
            props.type = "ShaderNodeRGB"

            props = flow.operator("node.add_node", text = "", icon = "NODE_TANGENT")
            props.use_transform = True
            props.type = "ShaderNodeTangent"

            props = flow.operator("node.add_node", text = "", icon = "NODE_TEXCOORDINATE")
            props.use_transform = True
            props.type = "ShaderNodeTexCoord"

            if context.space_data.shader_type == 'LINESTYLE':

                props = flow.operator("node.add_node", text = "", icon = "NODE_UVALONGSTROKE")
                props.use_transform = True
                props.type = "ShaderNodeUVALongStroke"

            props = flow.operator("node.add_node", text = "", icon = "GROUP_UVS")
            props.use_transform = True
            props.type = "ShaderNodeUVMap"

            props = flow.operator("node.add_node", text = "", icon = "NODE_VALUE")
            props.use_transform = True
            props.type = "ShaderNodeValue"

            props = flow.operator("node.add_node", text="", icon = "NODE_VOLUME_INFO")
            props.use_transform = True
            props.type = "ShaderNodeVolumeInfo"

            props = flow.operator("node.add_node", text = "", icon = "NODE_WIREFRAME")
            props.use_transform = True
            props.type = "ShaderNodeWireframe"


#Shader editor , Output panel
class NODES_PT_shader_add_output(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Output"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        return addon_prefs.Node_shader_add_common == False and context.space_data.tree_type == 'ShaderNodeTree' # Just in shader mode

    @staticmethod
    def draw(self, context):
        layout = self.layout#### Textbuttons
        default_context = bpy.app.translations.contexts.default

        scene = context.scene

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        engine = context.engine

        ##### Textbuttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" AOV Output    ", icon = "NODE_VALUE")
            props.use_transform = True
            props.type = "ShaderNodeOutputAOV"

            if context.space_data.shader_type == 'OBJECT':

                if engine == 'CYCLES':

                    props = col.operator("node.add_node", text=" Light Output    ", icon = "LIGHT")
                    props.use_transform = True
                    props.type = "ShaderNodeOutputLight"

                props = col.operator("node.add_node", text=" Material Output", icon = "NODE_MATERIAL")
                props.use_transform = True
                props.type = "ShaderNodeOutputMaterial"

            elif context.space_data.shader_type == 'WORLD':

                props = col.operator("node.add_node", text=" World Output    ", icon = "WORLD")
                props.use_transform = True
                props.type = "ShaderNodeOutputWorld"

            elif context.space_data.shader_type == 'LINESTYLE':

                props = col.operator("node.add_node", text=" Line Style Output", icon = "NODE_LINESTYLE_OUTPUT")
                props.use_transform = True
                props.type = "ShaderNodeOutputLineStyle"

        #### Image Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text="", icon = "NODE_VALUE")
            props.use_transform = True
            props.type = "ShaderNodeOutputAOV"

            if context.space_data.shader_type == 'OBJECT':

                if engine == 'CYCLES':

                    props = flow.operator("node.add_node", text="", icon = "LIGHT")
                    props.use_transform = True
                    props.type = "ShaderNodeOutputLight"

                props = flow.operator("node.add_node", text="", icon = "NODE_MATERIAL")
                props.use_transform = True
                props.type = "ShaderNodeOutputMaterial"

            elif context.space_data.shader_type == 'WORLD':

                props = flow.operator("node.add_node", text="", icon = "WORLD")
                props.use_transform = True
                props.type = "ShaderNodeOutputWorld"

            elif context.space_data.shader_type == 'LINESTYLE':

                props = flow.operator("node.add_node", text="", icon = "NODE_LINESTYLE_OUTPUT")
                props.use_transform = True
                props.type = "ShaderNodeOutputLineStyle"


#Compositor, Add tab, input panel
class NODES_PT_comp_add_input(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Input"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'CompositorNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout

        default_context = bpy.app.translations.contexts.default

        scene = context.scene

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

       #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Bokeh Image   ", icon = "NODE_BOKEH_IMAGE")
            props.use_transform = True
            props.type = "CompositorNodeBokehImage"

            props = col.operator("node.add_node", text=" Image              ", icon = "FILE_IMAGE")
            props.use_transform = True
            props.type = "CompositorNodeImage"

            props = col.operator("node.add_node", text=" Image Info       ", icon = "IMAGE_INFO")
            props.use_transform = True
            props.type = "CompositorNodeImageInfo"

            props = col.operator("node.add_node", text=" Image Coordinates ", icon = "IMAGE_COORDINATES")
            props.use_transform = True
            props.type = "CompositorNodeImageCoordinates"

            props = col.operator("node.add_node", text = "Mask               ", icon = "MOD_MASK")
            props.use_transform = True
            props.type = "CompositorNodeMask"

            props = col.operator("node.add_node", text=" Movie Clip        ", icon = "FILE_MOVIE")
            props.use_transform = True
            props.type = "CompositorNodeMovieClip"


        #### Image Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_BOKEH_IMAGE")
            props.use_transform = True
            props.type = "CompositorNodeBokehImage"

            props = flow.operator("node.add_node", text = "", icon = "FILE_IMAGE")
            props.use_transform = True
            props.type = "CompositorNodeImage"

            props = flow.operator("node.add_node", text = "", icon = "IMAGE_INFO")
            props.use_transform = True
            props.type = "CompositorNodeImageInfo"

            props = flow.operator("node.add_node", text = "", icon = "IMAGE_COORDINATES")
            props.use_transform = True
            props.type = "CompositorNodeImageCoordinates"

            props = flow.operator("node.add_node", text = "", icon = "MOD_MASK")
            props.use_transform = True
            props.type = "CompositorNodeMask"

            props = flow.operator("node.add_node", text = "", icon = "FILE_MOVIE")
            props.use_transform = True
            props.type = "CompositorNodeMovieClip"

            props = flow.operator("node.add_node", text = "", icon = "NODE_RGB")
            props.use_transform = True
            props.type = "CompositorNodeRGB"


#Compositor, Add tab, Constant supbanel
class NODES_PT_comp_add_input_constant(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Constant"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    #bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_comp_add_input"

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text = " RGB                ", icon = "NODE_RGB")
            props.use_transform = True
            props.type = "CompositorNodeRGB"

            props = col.operator("node.add_node", text=" Value               ", icon = "NODE_VALUE")
            props.use_transform = True
            props.type = "ShaderNodeValue"

            props = col.operator("node.add_node", text=" Normal               ", icon = "RECALC_NORMALS")
            props.use_transform = True
            props.type = "CompositorNodeNormal"


        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_RGB")
            props.use_transform = True
            props.type = "CompositorNodeRGB"

            props = flow.operator("node.add_node", text="", icon = "NODE_VALUE")
            props.use_transform = True
            props.type = "ShaderNodeValue"

            props = flow.operator("node.add_node", text="", icon = "RECALC_NORMALS")
            props.use_transform = True
            props.type = "CompositorNodeNormal"


#Compositor, Add tab, Scene supbanel
class NODES_PT_comp_add_input_scene(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Scene"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    #bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_comp_add_input"

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text = "  Render Layers              ", icon = "RENDERLAYERS")
            props.use_transform = True
            props.type = "CompositorNodeRLayers"

            props = col.operator("node.add_node", text = "  Scene Time              ", icon = "TIME")
            props.use_transform = True
            props.type = "CompositorNodeSceneTime"

            props = col.operator("node.add_node", text = "  Time Curve              ", icon = "NODE_CURVE_TIME")
            props.use_transform = True
            props.type = "CompositorNodeTime"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "RENDERLAYERS")
            props.use_transform = True
            props.type = "CompositorNodeRLayers"

            props = flow.operator("node.add_node", text = "", icon = "TIME")
            props.use_transform = True
            props.type = "CompositorNodeSceneTime"

            props = flow.operator("node.add_node", text = "", icon = "NODE_CURVE_TIME")
            props.use_transform = True
            props.type = "CompositorNodeTime"


#Compositor, Add tab, Output Panel
class NODES_PT_comp_add_output(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Output"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'CompositorNodeTree') # Just in compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout#### Textbuttons
        default_context = bpy.app.translations.contexts.default

        scene = context.scene

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Composite      ", icon = "NODE_COMPOSITING")
            props.use_transform = True
            props.type = "CompositorNodeComposite"

            props = col.operator("node.add_node", text=" Viewer            ", icon = "NODE_VIEWER")
            props.use_transform = True
            props.type = "CompositorNodeViewer"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" File Output     ", icon = "NODE_FILEOUTPUT")
            props.use_transform = True
            props.type = "CompositorNodeOutputFile"


        #### Image Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_COMPOSITING")
            props.use_transform = True
            props.type = "CompositorNodeComposite"

            props = flow.operator("node.add_node", text = "", icon = "NODE_FILEOUTPUT")
            props.use_transform = True
            props.type = "CompositorNodeOutputFile"

            props = flow.operator("node.add_node", text = "", icon = "NODE_VIEWER")
            props.use_transform = True
            props.type = "CompositorNodeViewer"

#Compositor, Add tab, Color Panel
class NODES_PT_comp_add_color(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Color"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'CompositorNodeTree') # Just in texture and compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout#### Textbuttons
        default_context = bpy.app.translations.contexts.default

        scene = context.scene

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Alpha Convert   ", icon = "NODE_ALPHACONVERT")
            props.use_transform = True
            props.type = "CompositorNodePremulKey"

            props = col.operator("node.add_node", text=" Color Ramp      ", icon = "NODE_COLORRAMP")
            props.use_transform = True
            props.type = "CompositorNodeValToRGB"

            props = col.operator("node.add_node", text=" Convert Colorspace      ", icon = "COLOR_SPACE")
            props.use_transform = True
            props.type = "CompositorNodeConvertColorSpace"

            props = col.operator("node.add_node", text=" Set Alpha          ", icon = "IMAGE_ALPHA")
            props.use_transform = True
            props.type = "CompositorNodeSetAlpha"


            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Invert Color       ", icon = "NODE_INVERT")
            props.use_transform = True
            props.type = "CompositorNodeInvert"

            props = col.operator("node.add_node", text=" RGB to BW       ", icon = "NODE_RGBTOBW")
            props.use_transform = True
            props.type = "CompositorNodeRGBToBW"


        #### Image Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5


            props = flow.operator("node.add_node", text = "", icon = "NODE_ALPHACONVERT")
            props.use_transform = True
            props.type = "CompositorNodePremulKey"

            props = flow.operator("node.add_node", text = "", icon = "NODE_COLORRAMP")
            props.use_transform = True
            props.type = "CompositorNodeValToRGB"

            props = flow.operator("node.add_node", text = "", icon = "COLOR_SPACE")
            props.use_transform = True
            props.type = "CompositorNodeConvertColorSpace"

            props = flow.operator("node.add_node", text = "", icon = "IMAGE_ALPHA")
            props.use_transform = True
            props.type = "CompositorNodeSetAlpha"

            props = flow.operator("node.add_node", text = "", icon = "NODE_INVERT")
            props.use_transform = True
            props.type = "CompositorNodeInvert"

            props = flow.operator("node.add_node", text = "", icon = "NODE_RGBTOBW")
            props.use_transform = True
            props.type = "CompositorNodeRGBToBW"


#Compositor, Add tab, Color, Adjust supbanel
class NODES_PT_comp_add_color_adjust(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Adjust"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_comp_add_color"

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Bright / Contrast", icon = "BRIGHTNESS_CONTRAST")
            props.use_transform = True
            props.type = "CompositorNodeBrightContrast"

            props = col.operator("node.add_node", text=" Color Balance", icon = "NODE_COLORBALANCE")
            props.use_transform = True
            props.type = "CompositorNodeColorBalance"

            props = col.operator("node.add_node", text=" Color Correction", icon = "NODE_COLORCORRECTION")
            props.use_transform = True
            props.type = "CompositorNodeColorCorrection"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Exposure", icon = "EXPOSURE")
            props.use_transform = True
            props.type = "CompositorNodeExposure"

            props = col.operator("node.add_node", text=" Gamma", icon = "NODE_GAMMA")
            props.use_transform = True
            props.type = "CompositorNodeGamma"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Hue Correct", icon = "NODE_HUESATURATION")
            props.use_transform = True
            props.type = "CompositorNodeHueCorrect"

            props = col.operator("node.add_node", text=" Hue/Saturation/Value", icon = "NODE_HUESATURATION")
            props.use_transform = True
            props.type = "CompositorNodeHueSat"

            props = col.operator("node.add_node", text=" RGB Curves", icon = "NODE_RGBCURVE")
            props.use_transform = True
            props.type = "CompositorNodeCurveRGB"

            props = col.operator("node.add_node", text=" Tonemap", icon = "NODE_TONEMAP")
            props.use_transform = True
            props.type = "CompositorNodeTonemap"



        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "BRIGHTNESS_CONTRAST")
            props.use_transform = True
            props.type = "CompositorNodeBrightContrast"

            props = flow.operator("node.add_node", text = "", icon = "NODE_COLORBALANCE")
            props.use_transform = True
            props.type = "CompositorNodeColorBalance"

            props = flow.operator("node.add_node", text = "", icon = "NODE_COLORCORRECTION")
            props.use_transform = True
            props.type = "CompositorNodeColorCorrection"

            props = flow.operator("node.add_node", text = "", icon = "EXPOSURE")
            props.use_transform = True
            props.type = "CompositorNodeExposure"

            props = flow.operator("node.add_node", text = "", icon = "NODE_GAMMA")
            props.use_transform = True
            props.type = "CompositorNodeGamma"

            props = flow.operator("node.add_node", text = "", icon = "NODE_HUESATURATION")
            props.use_transform = True
            props.type = "CompositorNodeHueCorrect"

            props = flow.operator("node.add_node", text = "", icon = "NODE_HUESATURATION")
            props.use_transform = True
            props.type = "CompositorNodeHueSat"

            props = flow.operator("node.add_node", text = "", icon = "NODE_RGBCURVE")
            props.use_transform = True
            props.type = "CompositorNodeCurveRGB"

            props = flow.operator("node.add_node", text = "", icon = "NODE_TONEMAP")
            props.use_transform = True
            props.type = "CompositorNodeTonemap"


#Compositor, Add tab, Color, Mix supbanel
class NODES_PT_comp_add_color_mix(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Mix"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    #bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_comp_add_color"

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Alpha Over", icon = "IMAGE_ALPHA")
            props.use_transform = True
            props.type = "CompositorNodeAlphaOver"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Combine Color", icon = "COMBINE_COLOR")
            props.use_transform = True
            props.type = "CompositorNodeCombineColor"

            props = col.operator("node.add_node", text=" Separate Color", icon = "SEPARATE_COLOR")
            props.use_transform = True
            props.type = "CompositorNodeSeparateColor"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Mix Color", icon = "NODE_MIXRGB")
            props.use_transform = True
            props.type = "CompositorNodeMixRGB"

            props = col.operator("node.add_node", text=" Z Combine", icon = "NODE_ZCOMBINE")
            props.use_transform = True
            props.type = "CompositorNodeZcombine"


        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "IMAGE_ALPHA")
            props.use_transform = True
            props.type = "CompositorNodeAlphaOver"

            props = flow.operator("node.add_node", text = "", icon = "COMBINE_COLOR")
            props.use_transform = True
            props.type = "CompositorNodeCombineColor"

            props = flow.operator("node.add_node", text = "", icon = "SEPARATE_COLOR")
            props.use_transform = True
            props.type = "CompositorNodeSeparateColor"

            props = flow.operator("node.add_node", text = "", icon = "NODE_MIXRGB")
            props.use_transform = True
            props.type = "CompositorNodeMixRGB"

            props = flow.operator("node.add_node", text = "", icon = "NODE_ZCOMBINE")
            props.use_transform = True
            props.type = "CompositorNodeZcombine"


#Compositor, Add tab, Filter Panel
class NODES_PT_comp_add_filter(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Filter"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'CompositorNodeTree') # Just in compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Anti Aliasing     ", icon = "ANTIALIASED")
            props.use_transform = True
            props.type = "CompositorNodeAntiAliasing"

            props = col.operator("node.add_node", text=" Denoise           ", icon = "NODE_DENOISE")
            props.use_transform = True
            props.type = "CompositorNodeDenoise"

            props = col.operator("node.add_node", text=" Despeckle         ", icon = "NODE_DESPECKLE")
            props.use_transform = True
            props.type = "CompositorNodeDespeckle"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Dilate / Erode    ", icon = "NODE_ERODE")
            props.use_transform = True
            props.type = "CompositorNodeDilateErode"

            props = col.operator("node.add_node", text=" Inpaint              ", icon = "NODE_IMPAINT")
            props.use_transform = True
            props.type = "CompositorNodeInpaint"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Filter                ", icon = "FILTER")
            props.use_transform = True
            props.type = "CompositorNodeFilter"

            props = col.operator("node.add_node", text=" Glare                ", icon = "NODE_GLARE")
            props.use_transform = True
            props.type = "CompositorNodeGlare"

            props = col.operator("node.add_node", text=" Kuwahara         ", icon = "KUWAHARA")
            props.use_transform = True
            props.type = "CompositorNodeKuwahara"

            props = col.operator("node.add_node", text=" Pixelate            ", icon = "NODE_PIXELATED")
            props.use_transform = True
            props.type = "CompositorNodePixelate"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Posterize          ", icon = "POSTERIZE")
            props.use_transform = True
            props.type = "CompositorNodePosterize"

            props = col.operator("node.add_node", text=" Sunbeams        ", icon = "NODE_SUNBEAMS")
            props.use_transform = True
            props.type = "CompositorNodeSunBeams"



        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "ANTIALIASED")
            props.use_transform = True
            props.type = "CompositorNodeAntiAliasing"

            props = flow.operator("node.add_node", text = "", icon = "NODE_DENOISE")
            props.use_transform = True
            props.type = "CompositorNodeDenoise"

            props = flow.operator("node.add_node", text = "", icon = "NODE_DESPECKLE")
            props.use_transform = True
            props.type = "CompositorNodeDespeckle"

            props = flow.operator("node.add_node", text = "", icon = "NODE_ERODE")
            props.use_transform = True
            props.type = "CompositorNodeDilateErode"

            props = flow.operator("node.add_node", text = "", icon = "NODE_IMPAINT")
            props.use_transform = True
            props.type = "CompositorNodeInpaint"

            props = flow.operator("node.add_node", text = "", icon = "FILTER")
            props.use_transform = True
            props.type = "CompositorNodeFilter"

            props = flow.operator("node.add_node", text = "", icon = "NODE_GLARE")
            props.use_transform = True
            props.type = "CompositorNodeGlare"

            props = flow.operator("node.add_node", text = "", icon = "KUWAHARA")
            props.use_transform = True
            props.type = "CompositorNodeKuwahara"

            props = flow.operator("node.add_node", text = "", icon = "NODE_PIXELATED")
            props.use_transform = True
            props.type = "CompositorNodePixelate"

            props = flow.operator("node.add_node", text = "", icon = "POSTERIZE")
            props.use_transform = True
            props.type = "CompositorNodePosterize"

            props = flow.operator("node.add_node", text = "", icon = "NODE_SUNBEAMS")
            props.use_transform = True
            props.type = "CompositorNodeSunBeams"


#Compositor, Add tab, Filter, Blur supbanel
class NODES_PT_comp_add_filter_blur(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Blur"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_comp_add_filter"

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Bilateral Blur    ", icon = "NODE_BILATERAL_BLUR")
            props.use_transform = True
            props.type = "CompositorNodeBilateralblur"

            props = col.operator("node.add_node", text=" Blur                   ", icon = "NODE_BLUR")
            props.use_transform = True
            props.type = "CompositorNodeBlur"

            props = col.operator("node.add_node", text=" Bokeh Blur       ", icon = "NODE_BOKEH_BLUR")
            props.use_transform = True
            props.type = "CompositorNodeBokehBlur"

            props = col.operator("node.add_node", text=" Defocus           ", icon = "NODE_DEFOCUS")
            props.use_transform = True
            props.type = "CompositorNodeDefocus"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Directional Blur ", icon = "NODE_DIRECITONALBLUR")
            props.use_transform = True
            props.type = "CompositorNodeDBlur"

            props = col.operator("node.add_node", text=" Vector Blur       ", icon = "NODE_VECTOR_BLUR")
            props.use_transform = True
            props.type = "CompositorNodeVecBlur"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_BILATERAL_BLUR")
            props.use_transform = True
            props.type = "CompositorNodeBilateralblur"

            props = flow.operator("node.add_node", text = "", icon = "NODE_BLUR")
            props.use_transform = True
            props.type = "CompositorNodeBlur"

            props = flow.operator("node.add_node", text = "", icon = "NODE_BOKEH_BLUR")
            props.use_transform = True
            props.type = "CompositorNodeBokehBlur"

            props = flow.operator("node.add_node", text = "", icon = "NODE_DEFOCUS")
            props.use_transform = True
            props.type = "CompositorNodeDefocus"

            props = flow.operator("node.add_node", text = "", icon = "NODE_DIRECITONALBLUR")
            props.use_transform = True
            props.type = "CompositorNodeDBlur"

            props = flow.operator("node.add_node", text = "", icon = "NODE_VECTOR_BLUR")
            props.use_transform = True
            props.type = "CompositorNodeVecBlur"


#Compositor, Add tab, Keying Panel
class NODES_PT_comp_add_keying(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Keying"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'CompositorNodeTree') # Just in compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

            #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Channel Key     ", icon = "NODE_CHANNEL")
            props.use_transform = True
            props.type = "CompositorNodeChannelMatte"

            props = col.operator("node.add_node", text=" Chroma Key     ", icon = "NODE_CHROMA")
            props.use_transform = True
            props.type = "CompositorNodeChromaMatte"

            props = col.operator("node.add_node", text=" Color Key         ", icon = "COLOR")
            props.use_transform = True
            props.type = "CompositorNodeColorMatte"

            props = col.operator("node.add_node", text=" Color Spill        ", icon = "NODE_SPILL")
            props.use_transform = True
            props.type = "CompositorNodeColorSpill"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Difference Key ", icon = "SELECT_DIFFERENCE")
            props.use_transform = True
            props.type = "CompositorNodeDiffMatte"

            props = col.operator("node.add_node", text=" Distance Key   ", icon = "DRIVER_DISTANCE")
            props.use_transform = True
            props.type = "CompositorNodeDistanceMatte"

            props = col.operator("node.add_node", text=" Keying              ", icon = "NODE_KEYING")
            props.use_transform = True
            props.type = "CompositorNodeKeying"

            props = col.operator("node.add_node", text=" Keying Screen  ", icon = "NODE_KEYINGSCREEN")
            props.use_transform = True
            props.type = "CompositorNodeKeyingScreen"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Luminance Key ", icon = "NODE_LUMINANCE")
            props.use_transform = True
            props.type = "CompositorNodeLumaMatte"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_CHANNEL")
            props.use_transform = True
            props.type = "CompositorNodeChannelMatte"

            props = flow.operator("node.add_node", text = "", icon = "NODE_CHROMA")
            props.use_transform = True
            props.type = "CompositorNodeChromaMatte"

            props = flow.operator("node.add_node", text = "", icon = "COLOR")
            props.use_transform = True
            props.type = "CompositorNodeColorMatte"

            props = flow.operator("node.add_node", text="", icon = "NODE_SPILL")
            props.use_transform = True
            props.type = "CompositorNodeColorSpill"

            props = flow.operator("node.add_node", text = "", icon = "SELECT_DIFFERENCE")
            props.use_transform = True
            props.type = "CompositorNodeDiffMatte"

            props = flow.operator("node.add_node", text = "", icon = "DRIVER_DISTANCE")
            props.use_transform = True
            props.type = "CompositorNodeDistanceMatte"

            props = flow.operator("node.add_node", text = "", icon = "NODE_KEYING")
            props.use_transform = True
            props.type = "CompositorNodeKeying"

            props = flow.operator("node.add_node", text = "", icon = "NODE_KEYINGSCREEN")
            props.use_transform = True
            props.type = "CompositorNodeKeyingScreen"

            props = flow.operator("node.add_node", text = "", icon = "NODE_LUMINANCE")
            props.use_transform = True
            props.type = "CompositorNodeLumaMatte"


#Compositor, Add tab, Mask Panel
class NODES_PT_comp_add_mask(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Mask"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'CompositorNodeTree') # Just in compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

            #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Cryptomatte    ", icon = "CRYPTOMATTE")
            props.use_transform = True
            props.type = "CompositorNodeCryptomatteV2"

            props = col.operator("node.add_node", text=" Cryptomatte (Legacy)", icon = "CRYPTOMATTE")
            props.use_transform = True
            props.type = "CompositorNodeCryptomatte"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Box Mask         ", icon = "NODE_BOXMASK")
            props.use_transform = True
            props.type = "CompositorNodeBoxMask"

            props = col.operator("node.add_node", text=" Ellipse Mask     ", icon = "NODE_ELLIPSEMASK")
            props.use_transform = True
            props.type = "CompositorNodeEllipseMask"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Double Edge Mask ", icon = "NODE_DOUBLEEDGEMASK")
            props.use_transform = True
            props.type = "CompositorNodeDoubleEdgeMask"

            props = col.operator("node.add_node", text=" ID Mask           ", icon = "MOD_MASK")
            props.use_transform = True
            props.type = "CompositorNodeIDMask"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text="", icon = "CRYPTOMATTE")
            props.use_transform = True
            props.type = "CompositorNodeCryptomatte"

            props = flow.operator("node.add_node", text="", icon = "CRYPTOMATTE")
            props.use_transform = True
            props.type = "CompositorNodeCryptomatteV2"

            props = flow.operator("node.add_node", text = "", icon = "NODE_BOXMASK")
            props.use_transform = True
            props.type = "CompositorNodeBoxMask"

            props = flow.operator("node.add_node", text = "", icon = "NODE_ELLIPSEMASK")
            props.use_transform = True
            props.type = "CompositorNodeEllipseMask"

            props = flow.operator("node.add_node", text="", icon = "NODE_DOUBLEEDGEMASK")
            props.use_transform = True
            props.type = "CompositorNodeDoubleEdgeMask"

            props = flow.operator("node.add_node", text = "", icon = "MOD_MASK")
            props.use_transform = True
            props.type = "CompositorNodeIDMask"


#Compositor, Add tab, Texture Panel
class NODES_PT_comp_add_texture(bpy.types.Panel):
    bl_label = "Texture"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'CompositorNodeTree') # Just in compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

            #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Brick Texture            ", icon = "NODE_BRICK")
            props.use_transform = True
            props.type = "ShaderNodeTexBrick"

            props = col.operator("node.add_node", text=" Checker Texture       ", icon = "NODE_CHECKER")
            props.use_transform = True
            props.type = "ShaderNodeTexChecker"

            props = col.operator("node.add_node", text=" Gabor Texture        ", icon = "GABOR_NOISE")
            props.use_transform = True
            props.type = "ShaderNodeTexGabor"

            props = col.operator("node.add_node", text=" Gradient Texture      ", icon = "NODE_GRADIENT")
            props.use_transform = True
            props.type = "ShaderNodeTexGradient"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Magic Texture         ", icon = "MAGIC_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexMagic"

            props = col.operator("node.add_node", text=" Noise Texture         ", icon = "NOISE_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexNoise"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Voronoi Texture       ", icon = "VORONI_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexVoronoi"

            props = col.operator("node.add_node", text=" Wave Texture          ", icon = "NODE_WAVES")
            props.use_transform = True
            props.type = "ShaderNodeTexWave"

            props = col.operator("node.add_node", text = " White Noise             ", icon = "NODE_WHITE_NOISE")
            props.use_transform = True
            props.type = "ShaderNodeTexWhiteNoise"


        #### Icon Buttons
        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_BRICK")
            props.use_transform = True
            props.type = "ShaderNodeTexBrick"

            props = flow.operator("node.add_node", text = "", icon = "NODE_CHECKER")
            props.use_transform = True
            props.type = "ShaderNodeTexChecker"

            props = flow.operator("node.add_node", text="", icon = "GABOR_NOISE")
            props.use_transform = True
            props.type = "ShaderNodeTexGabor"

            props = flow.operator("node.add_node", text = "", icon = "NODE_GRADIENT")
            props.use_transform = True
            props.type = "ShaderNodeTexGradient"

            props = flow.operator("node.add_node", text = "", icon = "MAGIC_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexMagic"

            props = flow.operator("node.add_node", text = "", icon = "NOISE_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexNoise"

            props = flow.operator("node.add_node", text = "", icon = "VORONI_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexVoronoi"

            props = flow.operator("node.add_node", text = "", icon = "NODE_WAVES")
            props.use_transform = True
            props.type = "ShaderNodeTexWave"

            props = flow.operator("node.add_node", text = "", icon = "NODE_WHITE_NOISE")
            props.use_transform = True
            props.type = "ShaderNodeTexWhiteNoise"


#Compositor, Add tab, Tracking Panel
class NODES_PT_comp_add_tracking(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Tracking"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'CompositorNodeTree') # Just in compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

            #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Plane Track Deform ", icon = "NODE_PLANETRACKDEFORM")
            props.use_transform = True
            props.type = "CompositorNodePlaneTrackDeform"

            props = col.operator("node.add_node", text=" Stabilize 2D     ", icon = "NODE_STABILIZE2D")
            props.use_transform = True
            props.type = "CompositorNodeStabilize"

            props = col.operator("node.add_node", text=" Track Position  ", icon = "NODE_TRACKPOSITION")
            props.use_transform = True
            props.type = "CompositorNodeTrackPos"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_PLANETRACKDEFORM")
            props.use_transform = True
            props.type = "CompositorNodePlaneTrackDeform"

            props = flow.operator("node.add_node", text = "", icon = "NODE_STABILIZE2D")
            props.use_transform = True
            props.type = "CompositorNodeStabilize"

            props = flow.operator("node.add_node", text = "", icon = "NODE_TRACKPOSITION")
            props.use_transform = True
            props.type = "CompositorNodeTrackPos"


#Compositor, Add tab, Transform Panel
class NODES_PT_comp_add_transform(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Transform"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'CompositorNodeTree') # Just in compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Rotate", icon = "TRANSFORM_ROTATE")
            props.use_transform = True
            props.type = "CompositorNodeRotate"

            props = col.operator("node.add_node", text=" Scale", icon = "TRANSFORM_SCALE")
            props.use_transform = True
            props.type = "CompositorNodeScale"

            props = col.operator("node.add_node", text=" Transform", icon = "NODE_TRANSFORM")
            props.use_transform = True
            props.type = "CompositorNodeTransform"

            props = col.operator("node.add_node", text=" Translate", icon = "TRANSFORM_MOVE")
            props.use_transform = True
            props.type = "CompositorNodeTranslate"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Corner Pin", icon = "NODE_CORNERPIN")
            props.use_transform = True
            props.type = "CompositorNodeCornerPin"

            props = col.operator("node.add_node", text=" Crop", icon = "NODE_CROP")
            props.use_transform = True
            props.type = "CompositorNodeCrop"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Displace", icon = "MOD_DISPLACE")
            props.use_transform = True
            props.type = "CompositorNodeDisplace"

            props = col.operator("node.add_node", text=" Flip", icon = "FLIP")
            props.use_transform = True
            props.type = "CompositorNodeFlip"

            props = col.operator("node.add_node", text=" Map UV", icon = "GROUP_UVS")
            props.use_transform = True
            props.type = "CompositorNodeMapUV"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Lens Distortion ", icon = "NODE_LENSDISTORT")
            props.use_transform = True
            props.type = "CompositorNodeLensdist"

            props = col.operator("node.add_node", text=" Movie Distortion ", icon = "NODE_MOVIEDISTORT")
            props.use_transform = True
            props.type = "CompositorNodeMovieDistortion"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "TRANSFORM_ROTATE")
            props.use_transform = True
            props.type = "CompositorNodeRotate"

            props = flow.operator("node.add_node", text = "", icon = "TRANSFORM_SCALE")
            props.use_transform = True
            props.type = "CompositorNodeScale"

            props = flow.operator("node.add_node", text = "", icon = "NODE_TRANSFORM")
            props.use_transform = True
            props.type = "CompositorNodeTransform"

            props = flow.operator("node.add_node", text = "", icon = "TRANSFORM_MOVE")
            props.use_transform = True
            props.type = "CompositorNodeTranslate"

            props = flow.operator("node.add_node", text = "", icon = "NODE_CORNERPIN")
            props.use_transform = True
            props.type = "CompositorNodeCornerPin"

            props = flow.operator("node.add_node", text = "", icon = "NODE_CROP")
            props.use_transform = True
            props.type = "CompositorNodeCrop"

            props = flow.operator("node.add_node", text = "", icon = "MOD_DISPLACE")
            props.use_transform = True
            props.type = "CompositorNodeDisplace"

            props = flow.operator("node.add_node", text = "", icon = "FLIP")
            props.use_transform = True
            props.type = "CompositorNodeFlip"

            props = flow.operator("node.add_node", text = "", icon = "GROUP_UVS")
            props.use_transform = True
            props.type = "CompositorNodeMapUV"

            props = flow.operator("node.add_node", text = "", icon = "NODE_LENSDISTORT")
            props.use_transform = True
            props.type = "CompositorNodeLensdist"

            props = flow.operator("node.add_node", text = "", icon = "NODE_MOVIEDISTORT")
            props.use_transform = True
            props.type = "CompositorNodeMovieDistortion"


#Compositor, Add tab, Utility Panel
class NODES_PT_comp_add_utility(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Utilities"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'CompositorNodeTree') # Just in compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Map Range       ", icon="NODE_MAP_RANGE")
            props.use_transform = True
            props.type = "ShaderNodeMapRange"

            props = col.operator("node.add_node", text=" Math                 ", icon = "NODE_MATH")
            props.use_transform = True
            props.type = "ShaderNodeMath"

            props = col.operator("node.add_node", text = "Mix              ", icon = "NODE_MIX")
            props.use_transform = True
            props.type = "ShaderNodeMix"

            props = col.operator("node.add_node", text=" Clamp              ", icon = "NODE_CLAMP")
            props.use_transform = True
            props.type = "ShaderNodeClamp"

            props = col.operator("node.add_node", text=" Float Curve      ", icon = "FLOAT_CURVE")
            props.use_transform = True
            props.type = "ShaderNodeFloatCurve"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Levels             ", icon = "LEVELS")
            props.use_transform = True
            props.type = "CompositorNodeLevels"

            props = col.operator("node.add_node", text=" Normalize        ", icon = "NODE_NORMALIZE")
            props.use_transform = True
            props.type = "CompositorNodeNormalize"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Split                 ", icon = "NODE_VIWERSPLIT")
            props.use_transform = True
            props.type = "CompositorNodeSplit"

            props = col.operator("node.add_node", text=" Switch              ", icon = "SWITCH_DIRECTION")
            props.use_transform = True
            props.type = "CompositorNodeSwitch"

            props = col.operator("node.add_node", text=" Switch View    ", icon = "VIEW_SWITCHACTIVECAM")
            props.use_transform = True
            props.type = "CompositorNodeSwitchView"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Relative to Pixel    ", icon = "NODE_RELATIVE_TO_PIXEL")
            props.use_transform = True
            props.type = "CompositorNodeRelativeToPixel"


        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_MAP_RANGE")
            props.use_transform = True
            props.type = "CompositorNodeMapRange"

            props = flow.operator("node.add_node", text = "", icon = "NODE_MATH")
            props.use_transform = True
            props.type = "ShaderNodeMath"

            props = flow.operator("node.add_node", text = "", icon = "NODE_CLAMP")
            props.use_transform = True
            props.type = "ShaderNodeClamp"

            props = flow.operator("node.add_node", text = "", icon = "NODE_MIX")
            props.use_transform = True
            props.type = "ShaderNodeMix"

            props = flow.operator("node.add_node", text = "", icon = "FLOAT_CURVE")
            props.use_transform = True
            props.type = "ShaderNodeFloatCurve"

            props = flow.operator("node.add_node", text = "", icon = "LEVELS")
            props.use_transform = True
            props.type = "CompositorNodeLevels"

            props = flow.operator("node.add_node", text = "", icon = "NODE_NORMALIZE")
            props.use_transform = True
            props.type = "CompositorNodeNormalize"

            props = flow.operator("node.add_node", text = "", icon = "NODE_VIWERSPLIT")
            props.use_transform = True
            props.type = "CompositorNodeSplit"

            props = flow.operator("node.add_node", text="", icon = "SWITCH_DIRECTION")
            props.use_transform = True
            props.type = "CompositorNodeSwitch"

            props = flow.operator("node.add_node", text = "", icon = "VIEW_SWITCHACTIVECAM")
            props.use_transform = True
            props.type = "CompositorNodeSwitchView"

            props = flow.operator("node.add_node", text = "", icon = "NODE_RELATIVE_TO_PIXEL")
            props.use_transform = True
            props.type = "CompositorNodeRelativeToPixel"


#Compositor, Add tab, Vector Panel
class NODES_PT_comp_add_vector(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Vector"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'CompositorNodeTree') # Just in compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

            #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Combine XYZ  ", icon = "NODE_COMBINEXYZ")
            props.use_transform = True
            props.type = "ShaderNodeCombineXYZ"

            props = col.operator("node.add_node", text=" Separate XYZ  ", icon = "NODE_SEPARATEXYZ")
            props.use_transform = True
            props.type = "ShaderNodeSeparateXYZ"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Mix Vector       ", icon = "NODE_MIX")
            props.use_transform = True
            props.type = "ShaderNodeMix"
            ops = props.settings.add()
            ops.name = "data_type"
            ops.value = "'VECTOR'"

            props = col.operator("node.add_node", text=" Vector Curves  ", icon = "NODE_VECTOR")
            props.use_transform = True
            props.type = "ShaderNodeVectorCurve"


            props = col.operator("node.add_node", text=" Vector Math     ", icon = "NODE_VECTORMATH")
            props.use_transform = True
            props.type = "ShaderNodeVectorMath"

            props = col.operator("node.add_node", text=" Vector Rotate   ", icon = "TRANSFORM_ROTATE")
            props.use_transform = True
            props.type = "ShaderNodeVectorRotate"


        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text="", icon = "NODE_COMBINEXYZ")
            props.use_transform = True
            props.type = "ShaderNodeCombineXYZ"

            props = flow.operator("node.add_node", text="", icon = "NODE_SEPARATEXYZ")
            props.use_transform = True
            props.type = "ShaderNodeSeparateXYZ"

            props = flow.operator("node.add_node", text="", icon = "NODE_MIX")
            props.use_transform = True
            props.type = "ShaderNodeMix"
            ops = props.settings.add()
            ops.name = "data_type"
            ops.value = "'VECTOR'"

            props = flow.operator("node.add_node", text = "", icon = "NODE_VECTOR")
            props.use_transform = True
            props.type = "ShaderNodeVectorCurve"

            props = flow.operator("node.add_node", text="", icon = "NODE_VECTORMATH")
            props.use_transform = True
            props.type = "ShaderNodeVectorMath"

            props = flow.operator("node.add_node", text="", icon = "TRANSFORM_ROTATE")
            props.use_transform = True
            props.type = "ShaderNodeVectorRotate"


#Input nodes tab, textures common panel. Texture mode
class NODES_PT_Input_input_tex(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Input"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Input"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'TextureNodeTree') # Just in texture mode

    @staticmethod
    def draw(self, context):
        layout = self.layout#### Textbuttons
        default_context = bpy.app.translations.contexts.default

        scene = context.scene

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)

            props = col.operator("node.add_node", text=" Image               ", icon = "FILE_IMAGE")
            props.use_transform = True
            props.type = "TextureNodeImage"

            props = col.operator("node.add_node", text=" Texture             ", icon = "TEXTURE")
            props.use_transform = True
            props.type = "TextureNodeTexture"

        #### Icon Buttons

        else:

            row = layout.row()
            row.alignment = 'LEFT'

            props = row.operator("node.add_node", text="", icon = "FILE_IMAGE")
            props.use_transform = True
            props.type = "TextureNodeImage"

            props = row.operator("node.add_node", text="", icon = "TEXTURE")
            props.use_transform = True
            props.type = "TextureNodeTexture"


#Input nodes tab, textures advanced panel. Just in Texture mode
class NODES_PT_Input_textures_tex(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Textures"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Input"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'TextureNodeTree') # Just in shader and texture mode

    @staticmethod
    def draw(self, context):
        layout = self.layout#### Textbuttons
        default_context = bpy.app.translations.contexts.default

        scene = context.scene

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)

            props = col.operator("node.add_node", text=" Blend                 ", icon = "BLEND_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexBlend"

            props = col.operator("node.add_node", text=" Clouds               ", icon = "CLOUD_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexClouds"

            props = col.operator("node.add_node", text=" Distorted Noise ", icon = "NOISE_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexDistNoise"

            props = col.operator("node.add_node", text=" Magic               ", icon = "MAGIC_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexMagic"

            col = layout.column(align=True)

            props = col.operator("node.add_node", text=" Marble              ", icon = "MARBLE_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexMarble"

            props = col.operator("node.add_node", text=" Noise                 ", icon = "NOISE_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexNoise"

            props = col.operator("node.add_node", text=" Stucci                ", icon = "STUCCI_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexStucci"

            props = col.operator("node.add_node", text=" Voronoi             ", icon = "VORONI_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexVoronoi"

            col = layout.column(align=True)

            props = col.operator("node.add_node", text=" Wood                ", icon = "WOOD_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexWood"

        #### Icon Buttons

        else:

            row = layout.row()
            row.alignment = 'LEFT'

            props = row.operator("node.add_node", text="", icon = "BLEND_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexBlend"

            props = row.operator("node.add_node", text="", icon = "CLOUD_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexClouds"

            props = row.operator("node.add_node", text="", icon = "NOISE_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexDistNoise"

            props = row.operator("node.add_node", text="", icon = "MAGIC_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexMagic"

            row = layout.row()
            row.alignment = 'LEFT'

            props = row.operator("node.add_node", text="", icon = "MARBLE_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexMarble"

            props = row.operator("node.add_node", text="", icon = "NOISE_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexNoise"

            props = row.operator("node.add_node", text="", icon = "STUCCI_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexStucci"

            props = row.operator("node.add_node", text="", icon = "VORONI_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexVoronoi"

            row = layout.row()
            row.alignment = 'LEFT'

            props = row.operator("node.add_node", text="", icon = "WOOD_TEX")
            props.use_transform = True
            props.type = "TextureNodeTexWood"


#Shader Editor - Shader panel
class NODES_PT_shader_add_shader(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Shader"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        return addon_prefs.Node_shader_add_common == False and (context.space_data.tree_type == 'ShaderNodeTree' and context.space_data.shader_type in ( 'OBJECT', 'WORLD')) # Just in shader mode, Just in Object and World

    @staticmethod
    def draw(self, context):
        layout = self.layout#### Textbuttons
        default_context = bpy.app.translations.contexts.default

        scene = context.scene
        engine = context.engine

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Add                   ", icon = "NODE_ADD_SHADER")
            props.use_transform = True
            props.type = "ShaderNodeAddShader"

            props = col.operator("node.add_node", text=" Metallic             ", icon = "METALLIC")
            props.use_transform = True
            props.type = "ShaderNodeBsdfMetallic"

            if context.space_data.shader_type == 'OBJECT':

                if engine == 'CYCLES':

                    props = col.operator("node.add_node", text=" Anisotopic BSDF", icon = "NODE_ANISOTOPIC")
                    props.use_transform = True
                    props.type = "ShaderNodeBsdfAnisotropic"

                props = col.operator("node.add_node", text=" Diffuse BSDF    ", icon = "NODE_DIFFUSESHADER")
                props.use_transform = True
                props.type = "ShaderNodeBsdfDiffuse"

                props = col.operator("node.add_node", text=" Emission           ", icon = "NODE_EMISSION")
                props.use_transform = True
                props.type = "ShaderNodeEmission"

                props = col.operator("node.add_node", text=" Glass BSDF       ", icon = "NODE_GLASSHADER")
                props.use_transform = True
                props.type = "ShaderNodeBsdfGlass"

                col = layout.column(align=True)
                col.scale_y = 1.5

                props = col.operator("node.add_node", text=" Glossy BSDF        ", icon = "NODE_GLOSSYSHADER")
                props.use_transform = True
                props.type = "ShaderNodeBsdfGlossy"

                props = col.operator("node.add_node", text=" Holdout              ", icon = "NODE_HOLDOUTSHADER")
                props.use_transform = True
                props.type = "ShaderNodeHoldout"

                props = col.operator("node.add_node", text=" Mix Shader        ", icon = "NODE_MIXSHADER")
                props.use_transform = True
                props.type = "ShaderNodeMixShader"

                props = col.operator("node.add_node", text=" Principled BSDF", icon = "NODE_PRINCIPLED")
                props.use_transform = True
                props.type = "ShaderNodeBsdfPrincipled"

                col = layout.column(align=True)
                col.scale_y = 1.5

                if engine == 'CYCLES':

                    props = col.operator("node.add_node", text=" Principled Hair BSDF  ", icon = "CURVES")
                    props.use_transform = True
                    props.type = "ShaderNodeBsdfHairPrincipled"

                props = col.operator("node.add_node", text=" Principled Volume", icon = "NODE_VOLUMEPRINCIPLED")
                props.use_transform = True
                props.type = "ShaderNodeVolumePrincipled"

                if engine == 'CYCLES':
                    props = col.operator("node.add_node", text=" Ray Portal            ", icon = "NODE_RAY_PORTAL")
                    props.use_transform = True
                    props.type = "ShaderNodeRayPortal"

                props = col.operator("node.add_node", text=" Refraction BSDF   ", icon = "NODE_REFRACTIONSHADER")
                props.use_transform = True
                props.type = "ShaderNodeBsdfRefraction"

                if engine == 'BLENDER_EEVEE':

                    props = col.operator("node.add_node", text=" Specular BSDF     ", icon = "NODE_GLOSSYSHADER")
                    props.use_transform = True
                    props.type = "ShaderNodeEeveeSpecular"

                props = col.operator("node.add_node", text=" Subsurface Scattering", icon = "NODE_SSS")
                props.use_transform = True
                props.type = "ShaderNodeSubsurfaceScattering"

                if engine == 'CYCLES':

                    props = col.operator("node.add_node", text=" Toon BSDF           ", icon = "NODE_TOONSHADER")
                    props.use_transform = True
                    props.type = "ShaderNodeBsdfToon"

                col = layout.column(align=True)
                col.scale_y = 1.5

                props = col.operator("node.add_node", text=" Translucent BSDF  ", icon = "NODE_TRANSLUCENT")
                props.use_transform = True
                props.type = "ShaderNodeBsdfTranslucent"

                props = col.operator("node.add_node", text=" Transparent BSDF  ", icon = "NODE_TRANSPARENT")
                props.use_transform = True
                props.type = "ShaderNodeBsdfTransparent"

                if engine == 'CYCLES':

                    props = col.operator("node.add_node", text=" Sheen BSDF            ", icon = "NODE_VELVET")
                    props.use_transform = True
                    props.type = "ShaderNodeBsdfSheen"

                props = col.operator("node.add_node", text=" Volume Absorption ", icon = "NODE_VOLUMEABSORPTION")
                props.use_transform = True
                props.type = "ShaderNodeVolumeAbsorption"

                props = col.operator("node.add_node", text=" Volume Scatter       ", icon = "NODE_VOLUMESCATTER")
                props.use_transform = True
                props.type = "ShaderNodeVolumeScatter"

                props = col.operator("node.add_node", text=" Volume Coefficients   ", icon = "NODE_VOLUME_COEFFICIENTS")
                props.use_transform = True
                props.type = "ShaderNodeVolumeCoefficients"


            if context.space_data.shader_type == 'WORLD':
                col = layout.column(align=True)
                col.scale_y = 1.5

                props = col.operator("node.add_node", text=" Background    ", icon = "NODE_BACKGROUNDSHADER")
                props.use_transform = True
                props.type = "ShaderNodeBackground"

                props = col.operator("node.add_node", text=" Emission           ", icon = "NODE_EMISSION")
                props.use_transform = True
                props.type = "ShaderNodeEmission"

                props = col.operator("node.add_node", text=" Principled Volume       ", icon = "NODE_VOLUMEPRINCIPLED")
                props.use_transform = True
                props.type = "ShaderNodeVolumePrincipled"

                props = col.operator("node.add_node", text=" Mix                   ", icon = "NODE_MIXSHADER")
                props.use_transform = True
                props.type = "ShaderNodeMixShader"


        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5


            props = flow.operator("node.add_node", text="", icon = "NODE_ADD_SHADER")
            props.use_transform = True
            props.type = "ShaderNodeAddShader"

            props = flow.operator("node.add_node", text="", icon = "METALLIC")
            props.use_transform = True
            props.type = "ShaderNodeBsdfMetallic"

            if context.space_data.shader_type == 'OBJECT':

                if engine == 'CYCLES':

                    props = flow.operator("node.add_node", text = "", icon = "NODE_ANISOTOPIC")
                    props.use_transform = True
                    props.type = "ShaderNodeBsdfAnisotropic"

                props = flow.operator("node.add_node", text = "", icon = "NODE_DIFFUSESHADER")
                props.use_transform = True
                props.type = "ShaderNodeBsdfDiffuse"

                props = flow.operator("node.add_node", text = "", icon = "NODE_EMISSION")
                props.use_transform = True
                props.type = "ShaderNodeEmission"

                props = flow.operator("node.add_node", text = "", icon = "NODE_GLASSHADER")
                props.use_transform = True
                props.type = "ShaderNodeBsdfGlass"

                props = flow.operator("node.add_node", text = "", icon = "NODE_GLOSSYSHADER")
                props.use_transform = True
                props.type = "ShaderNodeBsdfGlossy"

                props = flow.operator("node.add_node", text = "", icon = "NODE_HOLDOUTSHADER")
                props.use_transform = True
                props.type = "ShaderNodeHoldout"

                props = flow.operator("node.add_node", text = "", icon = "NODE_MIXSHADER")
                props.use_transform = True
                props.type = "ShaderNodeMixShader"

                props = flow.operator("node.add_node", text="", icon = "NODE_PRINCIPLED")
                props.use_transform = True
                props.type = "ShaderNodeBsdfPrincipled"

                if engine == 'CYCLES':

                    props = flow.operator("node.add_node", text="", icon = "CURVES")
                    props.use_transform = True
                    props.type = "ShaderNodeBsdfHairPrincipled"

                props = flow.operator("node.add_node", text="", icon = "NODE_VOLUMEPRINCIPLED")
                props.use_transform = True
                props.type = "ShaderNodeVolumePrincipled"

                if engine == 'CYCLES':
                    props = flow.operator("node.add_node", text="", icon = "NODE_RAY_PORTAL")
                    props.use_transform = True
                    props.type = "ShaderNodeRayPortal"

                if engine == 'BLENDER_EEVEE':

                    props = flow.operator("node.add_node", text="", icon = "NODE_GLOSSYSHADER")
                    props.use_transform = True
                    props.type = "ShaderNodeEeveeSpecular"

                props = flow.operator("node.add_node", text = "", icon = "NODE_SSS")
                props.use_transform = True
                props.type = "ShaderNodeSubsurfaceScattering"

                if engine == 'CYCLES':

                    props = flow.operator("node.add_node", text = "", icon = "NODE_TOONSHADER")
                    props.use_transform = True
                    props.type = "ShaderNodeBsdfToon"

                props = flow.operator("node.add_node", text = "", icon = "NODE_TRANSLUCENT")
                props.use_transform = True
                props.type = "ShaderNodeBsdfTranslucent"

                props = flow.operator("node.add_node", text = "", icon = "NODE_TRANSPARENT")
                props.use_transform = True
                props.type = "ShaderNodeBsdfTransparent"

                if engine == 'CYCLES':

                    props = flow.operator("node.add_node", text = "", icon = "NODE_VELVET")
                    props.use_transform = True
                    props.type = "ShaderNodeBsdfSheen"

                props = flow.operator("node.add_node", text="", icon = "NODE_VOLUMEABSORPTION")
                props.use_transform = True
                props.type = "ShaderNodeVolumeAbsorption"

                props = flow.operator("node.add_node", text="", icon = "NODE_VOLUMESCATTER")
                props.use_transform = True
                props.type = "ShaderNodeVolumeScatter"

                props = flow.operator("node.add_node", text="", icon = "NODE_VOLUME_COEFFICIENTS")
                props.use_transform = True
                props.type = "ShaderNodeVolumeCoefficients"

            if context.space_data.shader_type == 'WORLD':

                props = flow.operator("node.add_node", text = "", icon = "NODE_BACKGROUNDSHADER")
                props.use_transform = True
                props.type = "ShaderNodeBackground"

                props = flow.operator("node.add_node", text = "", icon = "NODE_EMISSION")
                props.use_transform = True
                props.type = "ShaderNodeEmission"

                props = flow.operator("node.add_node", text="", icon = "NODE_VOLUMEPRINCIPLED")
                props.use_transform = True
                props.type = "ShaderNodeVolumePrincipled"

                props = flow.operator("node.add_node", text = "", icon = "NODE_MIXSHADER")
                props.use_transform = True
                props.type = "ShaderNodeMixShader"


#Shader Editor - Texture panel
class NODES_PT_shader_add_texture(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Texture"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        return addon_prefs.Node_shader_add_common == False and (context.space_data.tree_type == 'ShaderNodeTree') # Just in shader and texture mode

    @staticmethod
    def draw(self, context):
        layout = self.layout#### Textbuttons
        default_context = bpy.app.translations.contexts.default

        scene = context.scene
        engine = context.engine

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        ##### Textbuttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Brick Texture            ", icon = "NODE_BRICK")
            props.use_transform = True
            props.type = "ShaderNodeTexBrick"

            props = col.operator("node.add_node", text=" Checker Texture       ", icon = "NODE_CHECKER")
            props.use_transform = True
            props.type = "ShaderNodeTexChecker"

            props = col.operator("node.add_node", text=" Environment Texture", icon = "NODE_ENVIRONMENT")
            props.use_transform = True
            props.type = "ShaderNodeTexEnvironment"

            props = col.operator("node.add_node", text=" Gabor Texture        ", icon = "GABOR_NOISE")
            props.use_transform = True
            props.type = "ShaderNodeTexGabor"

            props = col.operator("node.add_node", text=" Gradient Texture      ", icon = "NODE_GRADIENT")
            props.use_transform = True
            props.type = "ShaderNodeTexGradient"

            props = col.operator("node.add_node", text=" IES Texture             ", icon = "LIGHT")
            props.use_transform = True
            props.type = "ShaderNodeTexIES"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Image Texture         ", icon = "FILE_IMAGE")
            props.use_transform = True
            props.type = "ShaderNodeTexImage"

            props = col.operator("node.add_node", text=" Magic Texture         ", icon = "MAGIC_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexMagic"

            props = col.operator("node.add_node", text=" Noise Texture         ", icon = "NOISE_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexNoise"

            props = col.operator("node.add_node", text=" Sky Texture             ", icon = "NODE_SKY")
            props.use_transform = True
            props.type = "ShaderNodeTexSky"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Voronoi Texture       ", icon = "VORONI_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexVoronoi"

            props = col.operator("node.add_node", text=" Wave Texture          ", icon = "NODE_WAVES")
            props.use_transform = True
            props.type = "ShaderNodeTexWave"

            props = col.operator("node.add_node", text = " White Noise             ", icon = "NODE_WHITE_NOISE")
            props.use_transform = True
            props.type = "ShaderNodeTexWhiteNoise"


        #### Icon Buttons
        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_BRICK")
            props.use_transform = True
            props.type = "ShaderNodeTexBrick"

            props = flow.operator("node.add_node", text = "", icon = "NODE_CHECKER")
            props.use_transform = True
            props.type = "ShaderNodeTexChecker"

            props = flow.operator("node.add_node", text = "", icon = "NODE_ENVIRONMENT")
            props.use_transform = True
            props.type = "ShaderNodeTexEnvironment"

            props = flow.operator("node.add_node", text="", icon = "GABOR_NOISE")
            props.use_transform = True
            props.type = "ShaderNodeTexGabor"

            props = flow.operator("node.add_node", text = "", icon = "NODE_GRADIENT")
            props.use_transform = True
            props.type = "ShaderNodeTexGradient"

            props = flow.operator("node.add_node", text="", icon = "LIGHT")
            props.use_transform = True
            props.type = "ShaderNodeTexIES"

            props = flow.operator("node.add_node", text = "", icon = "FILE_IMAGE")
            props.use_transform = True
            props.type = "ShaderNodeTexImage"

            props = flow.operator("node.add_node", text = "", icon = "MAGIC_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexMagic"

            props = flow.operator("node.add_node", text = "", icon = "NOISE_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexNoise"

            props = flow.operator("node.add_node", text = "", icon = "NODE_SKY")
            props.use_transform = True
            props.type = "ShaderNodeTexSky"

            props = flow.operator("node.add_node", text = "", icon = "VORONI_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexVoronoi"

            props = flow.operator("node.add_node", text = "", icon = "NODE_WAVES")
            props.use_transform = True
            props.type = "ShaderNodeTexWave"

            props = flow.operator("node.add_node", text = "", icon = "NODE_WHITE_NOISE")
            props.use_transform = True
            props.type = "ShaderNodeTexWhiteNoise"


#Shader Editor - Color panel
class NODES_PT_shader_add_color(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Color"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        return addon_prefs.Node_shader_add_common == False and (context.space_data.tree_type == 'ShaderNodeTree')

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        ##### Textbuttons
        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Bright / Contrast ", icon = "BRIGHTNESS_CONTRAST")
            props.use_transform = True
            props.type = "ShaderNodeBrightContrast"

            props = col.operator("node.add_node", text=" Gamma              ", icon = "NODE_GAMMA")
            props.use_transform = True
            props.type = "ShaderNodeGamma"

            props = col.operator("node.add_node", text=" Hue / Saturation ", icon = "NODE_HUESATURATION")
            props.use_transform = True
            props.type = "ShaderNodeHueSaturation"

            props = col.operator("node.add_node", text=" Invert Color         ", icon = "NODE_INVERT")
            props.use_transform = True
            props.type = "ShaderNodeInvert"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Light Falloff      ", icon = "NODE_LIGHTFALLOFF")
            props.use_transform = True
            props.type = "ShaderNodeLightFalloff"

            props = col.operator("node.add_node", text=" Mix Color          ", icon = "NODE_MIX")
            props.use_transform = True
            props.type = "ShaderNodeMix"
            ops = props.settings.add()
            ops.name = "data_type"
            ops.value = "'RGBA'"

            props = col.operator("node.add_node", text="  RGB Curves        ", icon = "NODE_RGBCURVE")
            props.use_transform = True
            props.type = "ShaderNodeRGBCurve"

        ##### Icon Buttons
        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "BRIGHTNESS_CONTRAST")
            props.use_transform = True
            props.type = "ShaderNodeBrightContrast"

            props = flow.operator("node.add_node", text = "", icon = "NODE_GAMMA")
            props.use_transform = True
            props.type = "ShaderNodeGamma"

            props = flow.operator("node.add_node", text = "", icon = "NODE_HUESATURATION")
            props.use_transform = True
            props.type = "ShaderNodeHueSaturation"

            props = flow.operator("node.add_node", text = "", icon = "NODE_INVERT")
            props.use_transform = True
            props.type = "ShaderNodeInvert"

            props = flow.operator("node.add_node", text = "", icon = "NODE_LIGHTFALLOFF")
            props.use_transform = True
            props.type = "ShaderNodeLightFalloff"

            props = flow.operator("node.add_node", text = "", icon = "NODE_MIX")
            props.use_transform = True
            props.type = "ShaderNodeMix"
            ops = props.settings.add()
            ops.name = "data_type"
            ops.value = "'RGBA'"

            props = flow.operator("node.add_node", text = "", icon = "NODE_RGBCURVE")
            props.use_transform = True
            props.type = "ShaderNodeRGBCurve"


#Input nodes tab, Input panel. Just in texture mode
class NODES_PT_Input_input_advanced_tex(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Input Advanced"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Input"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'TextureNodeTree') # Just in texture mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)

            props = col.operator("node.add_node", text=" Coordinates       ", icon = "NODE_TEXCOORDINATE")
            props.use_transform = True
            props.type = "TextureNodeCoordinates"

            props = col.operator("node.add_node", text=" Curve Time        ", icon = "NODE_CURVE_TIME")
            props.use_transform = True
            props.type = "TextureNodeCurveTime"

        #### Icon Buttons

        else:
            row = layout.row()
            row.alignment = 'LEFT'

            props = row.operator("node.add_node", text="", icon = "NODE_TEXCOORDINATE")
            props.use_transform = True
            props.type = "TextureNodeCoordinates"

            props = row.operator("node.add_node", text="", icon = "NODE_CURVE_TIME")
            props.use_transform = True
            props.type = "TextureNodeCurveTime"


#Input nodes tab, Pattern panel. # Just in texture mode
class NODES_PT_Input_pattern(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Pattern"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Input"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'TextureNodeTree') # Just in texture mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)

            props = col.operator("node.add_node", text=" Bricks               ", icon = "NODE_BRICK")
            props.use_transform = True
            props.type = "TextureNodeBricks"

            props = col.operator("node.add_node", text=" Checker            ", icon = "NODE_CHECKER")
            props.use_transform = True
            props.type = "TextureNodeChecker"

        #### Icon Buttons

        else:

            row = layout.row()
            row.alignment = 'LEFT'

            props = row.operator("node.add_node", text="", icon = "NODE_BRICK")
            props.use_transform = True
            props.type = "TextureNodeBricks"

            props = row.operator("node.add_node", text="", icon = "NODE_CHECKER")
            props.use_transform = True
            props.type = "TextureNodeChecker"


#Input nodes tab, Color panel. Just in texture mode
class NODES_PT_Input_color_tex(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Color"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Input"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'TextureNodeTree') # Just in texture and compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout#### Textbuttons
        default_context = bpy.app.translations.contexts.default

        scene = context.scene

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)

            props = col.operator("node.add_node", text=" RGB Curves       ", icon = "NODE_RGBCURVE")
            props.use_transform = True
            props.type = "TextureNodeCurveRGB"

            props = col.operator("node.add_node", text=" Hue / Saturation", icon = "NODE_HUESATURATION")
            props.use_transform = True
            props.type = "TextureNodeHueSaturation"

            props = col.operator("node.add_node", text=" Invert Color       ", icon = "NODE_INVERT")
            props.use_transform = True
            props.type = "TextureNodeInvert"

            props = col.operator("node.add_node", text=" Mix RGB            ", icon = "NODE_MIXRGB")
            props.use_transform = True
            props.type = "TextureNodeMixRGB"

            col = layout.column(align=True)

            props = col.operator("node.add_node", text=" Combine RGBA ", icon = "NODE_COMBINERGB")
            props.use_transform = True
            props.type = "TextureNodeCompose"

            props = col.operator("node.add_node", text=" Separate RGBA ", icon = "NODE_SEPARATERGB")
            props.use_transform = True
            props.type = "TextureNodeDecompose"

        #### Icon Buttons

        else:

            row = layout.row()
            row.alignment = 'LEFT'

            props = row.operator("node.add_node", text="", icon = "NODE_RGBCURVE")
            props.use_transform = True
            props.type = "TextureNodeCurveRGB"

            props = row.operator("node.add_node", text="", icon = "NODE_HUESATURATION")
            props.use_transform = True
            props.type = "TextureNodeHueSaturation"

            props = row.operator("node.add_node", text="", icon = "NODE_INVERT")
            props.use_transform = True
            props.type = "TextureNodeInvert"

            props = row.operator("node.add_node", text="", icon = "NODE_MIXRGB")
            props.use_transform = True
            props.type = "TextureNodeMixRGB"

            row = layout.row()
            row.alignment = 'LEFT'

            props = row.operator("node.add_node", text="", icon = "NODE_COMBINERGB")
            props.use_transform = True
            props.type = "TextureNodeCompose"

            props = row.operator("node.add_node", text="", icon = "NODE_SEPARATERGB")
            props.use_transform = True
            props.type = "TextureNodeDecompose"


#Input nodes tab, Output panel, Texture mode
class NODES_PT_Input_output_tex(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Output"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Input"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'TextureNodeTree') # Just in texture mode

    @staticmethod
    def draw(self, context):
        layout = self.layout#### Textbuttons
        default_context = bpy.app.translations.contexts.default

        scene = context.scene

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences


        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)

            props = col.operator("node.add_node", text=" Output               ", icon = "NODE_OUTPUT")
            props.use_transform = True
            props.type = "TextureNodeOutput"

            props = col.operator("node.add_node", text=" Viewer              ", icon = "NODE_VIEWER")
            props.use_transform = True
            props.type = "TextureNodeViewer"

        #### Icon Buttons

        else:

            row = layout.row()
            row.alignment = 'LEFT'

            props = row.operator("node.add_node", text="", icon = "NODE_OUTPUT")
            props.use_transform = True
            props.type = "TextureNodeOutput"

            props = row.operator("node.add_node", text="", icon = "NODE_VIEWER")
            props.use_transform = True
            props.type = "TextureNodeViewer"


#Modify nodes tab, converter panel. Just in texture mode
class NODES_PT_Modify_converter_tex(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Converter"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Modify"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'TextureNodeTree') # Just in texture mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)

            props = col.operator("node.add_node", text=" Color Ramp      ", icon = "NODE_COLORRAMP")
            props.use_transform = True
            props.type = "TextureNodeValToRGB"

            props = col.operator("node.add_node", text=" Distance           ", icon = "DRIVER_DISTANCE")
            props.use_transform = True
            props.type = "TextureNodeDistance"

            props = col.operator("node.add_node", text=" Math                 ", icon = "NODE_MATH")
            props.use_transform = True
            props.type = "TextureNodeMath"

            props = col.operator("node.add_node", text=" RGB to BW       ", icon = "NODE_RGBTOBW")
            props.use_transform = True
            props.type = "TextureNodeRGBToBW"

            col = layout.column(align=True)

            props = col.operator("node.add_node", text=" Value to Normal ", icon = "RECALC_NORMALS")
            props.use_transform = True
            props.type = "TextureNodeValToNor"

        #### Icon Buttons

        else:

            row = layout.row()
            row.alignment = 'LEFT'

            props = row.operator("node.add_node", text="", icon = "NODE_COLORRAMP")
            props.use_transform = True
            props.type = "TextureNodeValToRGB"

            props = row.operator("node.add_node", text="", icon = "DRIVER_DISTANCE")
            props.use_transform = True
            props.type = "TextureNodeDistance"

            props = row.operator("node.add_node", text="", icon = "NODE_MATH")
            props.use_transform = True
            props.type = "TextureNodeMath"

            props = row.operator("node.add_node", text="", icon = "NODE_RGBTOBW")
            props.use_transform = True
            props.type = "TextureNodeRGBToBW"

            row = layout.row()
            row.alignment = 'LEFT'

            props = row.operator("node.add_node", text="", icon = "RECALC_NORMALS")
            props.use_transform = True
            props.type = "TextureNodeValToNor"


#Shader Editor - Vector panel
class NODES_PT_shader_add_vector(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Vector"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        return addon_prefs.Node_shader_add_common == False and context.space_data.tree_type == 'ShaderNodeTree' # Just in shader and compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        ##### Textbuttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Bump               ", icon = "NODE_BUMP")
            props.use_transform = True
            props.type = "ShaderNodeBump"

            props = col.operator("node.add_node", text=" Displacement ", icon = "MOD_DISPLACE")
            props.use_transform = True
            props.type = "ShaderNodeDisplacement"

            props = col.operator("node.add_node", text=" Mapping           ", icon = "NODE_MAPPING")
            props.use_transform = True
            props.type = "ShaderNodeMapping"

            props = col.operator("node.add_node", text=" Normal            ", icon = "RECALC_NORMALS")
            props.use_transform = True
            props.type = "ShaderNodeNormal"

            props = col.operator("node.add_node", text=" Normal Map     ", icon = "NODE_NORMALMAP")
            props.use_transform = True
            props.type = "ShaderNodeNormalMap"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Vector Curves   ", icon = "NODE_VECTOR")
            props.use_transform = True
            props.type = "ShaderNodeVectorCurve"

            props = col.operator("node.add_node", text=" Vector Displacement ", icon = "VECTOR_DISPLACE")
            props.use_transform = True
            props.type = "ShaderNodeVectorDisplacement"

            props = col.operator("node.add_node", text=" Vector Rotate   ", icon = "TRANSFORM_ROTATE")
            props.use_transform = True
            props.type = "ShaderNodeVectorRotate"

            props = col.operator("node.add_node", text=" Vector Transform ", icon = "NODE_VECTOR_TRANSFORM")
            props.use_transform = True
            props.type = "ShaderNodeVectorTransform"

        ##### Icon Buttons

        else:

            ##### --------------------------------- Vector ------------------------------------------- ####

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_BUMP")
            props.use_transform = True
            props.type = "ShaderNodeBump"

            props = flow.operator("node.add_node", text="", icon = "MOD_DISPLACE")
            props.use_transform = True
            props.type = "ShaderNodeDisplacement"

            props = flow.operator("node.add_node", text = "", icon = "NODE_MAPPING")
            props.use_transform = True
            props.type = "ShaderNodeMapping"

            props = flow.operator("node.add_node", text = "", icon = "RECALC_NORMALS")
            props.use_transform = True
            props.type = "ShaderNodeNormal"

            props = flow.operator("node.add_node", text = "", icon = "NODE_NORMALMAP")
            props.use_transform = True
            props.type = "ShaderNodeNormalMap"

            props = flow.operator("node.add_node", text = "", icon = "NODE_VECTOR")
            props.use_transform = True
            props.type = "ShaderNodeVectorCurve"

            props = flow.operator("node.add_node", text="", icon = "VECTOR_DISPLACE")
            props.use_transform = True
            props.type = "ShaderNodeVectorDisplacement"

            props = flow.operator("node.add_node", text="", icon = "TRANSFORM_ROTATE")
            props.use_transform = True
            props.type = "ShaderNodeVectorRotate"

            props = flow.operator("node.add_node", text = "", icon = "NODE_VECTOR_TRANSFORM")
            props.use_transform = True
            props.type = "ShaderNodeVectorTransform"


#Shader Editor - Converter panel
class NODES_PT_shader_add_converter(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Converter"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        return addon_prefs.Node_shader_add_common == False and context.space_data.tree_type == 'ShaderNodeTree' # Just in shader and compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene
        engine = context.engine

        ##### Textbuttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Blackbody        ", icon = "NODE_BLACKBODY")
            props.use_transform = True
            props.type = "ShaderNodeBlackbody"

            props = col.operator("node.add_node", text=" Clamp              ", icon = "NODE_CLAMP")
            props.use_transform = True
            props.type = "ShaderNodeClamp"

            props = col.operator("node.add_node", text=" ColorRamp       ", icon = "NODE_COLORRAMP")
            props.use_transform = True
            props.type = "ShaderNodeValToRGB"

            props = col.operator("node.add_node", text=" Combine Color ", icon = "COMBINE_COLOR")
            props.use_transform = True
            props.type = "ShaderNodeCombineColor"

            props = col.operator("node.add_node", text=" Combine XYZ   ", icon = "NODE_COMBINEXYZ")
            props.use_transform = True
            props.type = "ShaderNodeCombineXYZ"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Float Curve      ", icon = "FLOAT_CURVE")
            props.use_transform = True
            props.type = "ShaderNodeFloatCurve"

            props = col.operator("node.add_node", text=" Map Range       ", icon = "NODE_MAP_RANGE")
            props.use_transform = True
            props.type = "ShaderNodeMapRange"

            props = col.operator("node.add_node", text=" Math                 ", icon = "NODE_MATH")
            props.use_transform = True
            props.type = "ShaderNodeMath"

            props = col.operator("node.add_node", text=" Mix                   ", icon = "NODE_MIXSHADER")
            props.use_transform = True
            props.type = "ShaderNodeMix"

            props = col.operator("node.add_node", text=" RGB to BW      ", icon = "NODE_RGBTOBW")
            props.use_transform = True
            props.type = "ShaderNodeRGBToBW"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Separate Color ", icon = "SEPARATE_COLOR")
            props.use_transform = True
            props.type = "ShaderNodeSeparateColor"

            props = col.operator("node.add_node", text=" Separate XYZ   ", icon = "NODE_SEPARATEXYZ")
            props.use_transform = True
            props.type = "ShaderNodeSeparateXYZ"

            if engine == 'BLENDER_EEVEE_NEXT':

                props = col.operator("node.add_node", text=" Shader to RGB   ", icon = "NODE_RGB")
                props.use_transform = True
                props.type = "ShaderNodeShaderToRGB"

            props = col.operator("node.add_node", text=" Vector Math     ", icon = "NODE_VECTORMATH")
            props.use_transform = True
            props.type = "ShaderNodeVectorMath"

            props = col.operator("node.add_node", text=" Wavelength     ", icon = "NODE_WAVELENGTH")
            props.use_transform = True
            props.type = "ShaderNodeWavelength"

        ##### Icon Buttons
        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon= "NODE_BLACKBODY")
            props.use_transform = True
            props.type = "ShaderNodeBlackbody"

            props = flow.operator("node.add_node", text="", icon = "NODE_CLAMP")
            props.use_transform = True
            props.type = "ShaderNodeClamp"

            props = flow.operator("node.add_node", text = "", icon = "NODE_COLORRAMP")
            props.use_transform = True
            props.type = "ShaderNodeValToRGB"

            props = flow.operator("node.add_node", text = "", icon = "COMBINE_COLOR")
            props.use_transform = True
            props.type = "ShaderNodeCombineColor"

            props = flow.operator("node.add_node", text = "", icon = "NODE_COMBINEXYZ")
            props.use_transform = True
            props.type = "ShaderNodeCombineXYZ"

            props = flow.operator("node.add_node", text = "", icon = "FLOAT_CURVE")
            props.use_transform = True
            props.type = "ShaderNodeFloatCurve"

            props = flow.operator("node.add_node", text="", icon = "NODE_MAP_RANGE")
            props.use_transform = True
            props.type = "ShaderNodeMapRange"

            props = flow.operator("node.add_node", text = "", icon = "NODE_MATH")
            props.use_transform = True
            props.type = "ShaderNodeMath"

            props = flow.operator("node.add_node", text="", icon = "NODE_MIXSHADER")
            props.use_transform = True
            props.type = "ShaderNodeMix"

            props = flow.operator("node.add_node", text = "", icon = "NODE_RGBTOBW")
            props.use_transform = True
            props.type = "ShaderNodeRGBToBW"

            props = flow.operator("node.add_node", text = "", icon = "SEPARATE_COLOR")
            props.use_transform = True
            props.type = "ShaderNodeSeparateColor"

            props = flow.operator("node.add_node", text = "", icon = "NODE_SEPARATEXYZ")
            props.use_transform = True
            props.type = "ShaderNodeSeparateXYZ"

            if engine == 'BLENDER_EEVEE':

                props = flow.operator("node.add_node", text="", icon = "NODE_RGB")
                props.use_transform = True
                props.type = "ShaderNodeShaderToRGB"

            props = flow.operator("node.add_node", text = "", icon = "NODE_VECTORMATH")
            props.use_transform = True
            props.type = "ShaderNodeVectorMath"

            props = flow.operator("node.add_node", text = "", icon = "NODE_WAVELENGTH")
            props.use_transform = True
            props.type = "ShaderNodeWavelength"


#Modify nodes tab, distort panel. Just in texture mode
class NODES_PT_Modify_distort_tex(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Distort"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Modify"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'TextureNodeTree') # Just in texture mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

            #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)

            props = col.operator("node.add_node", text=" At                      ", icon = "NODE_AT")
            props.use_transform = True
            props.type = "TextureNodeAt"

            props = col.operator("node.add_node", text=" Rotate              ", icon = "TRANSFORM_ROTATE")
            props.use_transform = True
            props.type = "TextureNodeRotate"

            props = col.operator("node.add_node", text=" Scale                ", icon = "TRANSFORM_SCALE")
            props.use_transform = True
            props.type = "TextureNodeScale"

            props = col.operator("node.add_node", text=" Translate          ", icon = "TRANSFORM_MOVE")
            props.use_transform = True
            props.type = "TextureNodeTranslate"

        #### Icon Buttons

        else:

            row = layout.row()
            row.alignment = 'LEFT'

            props = row.operator("node.add_node", text="", icon = "NODE_AT")
            props.use_transform = True
            props.type = "TextureNodeAt"

            props = row.operator("node.add_node", text="", icon = "TRANSFORM_ROTATE")
            props.use_transform = True
            props.type = "TextureNodeRotate"

            props = row.operator("node.add_node", text="", icon = "TRANSFORM_SCALE")
            props.use_transform = True
            props.type = "TextureNodeScale"

            props = row.operator("node.add_node", text="", icon = "TRANSFORM_MOVE")
            props.use_transform = True
            props.type = "TextureNodeTranslate"


# ------------- Relations tab -------------------------------

#Shader Editor - Relations tab, Group Panel
class NODES_PT_Relations_group(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Group"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Relations"

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        ##### Textbuttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            space_node = context.space_data
            node_tree = space_node.edit_tree
            all_node_groups = context.blend_data.node_groups

            if node_tree in all_node_groups.values():
                props = col.operator("node.add_node", text = " Group Input      ", icon = "GROUPINPUT")
                props.use_transform = True
                props.type = "NodeGroupInput"

                props = col.operator("node.add_node", text = " Group Output    ", icon = "GROUPOUTPUT")
                props.use_transform = True
                props.type = "NodeGroupOutput"

            add_empty_group(col)

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            space_node = context.space_data
            node_tree = space_node.edit_tree
            all_node_groups = context.blend_data.node_groups

            if node_tree in all_node_groups.values():
                props = flow.operator("node.add_node", text = "", icon = "GROUPINPUT")
                props.use_transform = True
                props.type = "NodeGroupInput"

                props = flow.operator("node.add_node", text = "", icon = "GROUPOUTPUT")
                props.use_transform = True
                props.type = "NodeGroupOutput"

            # Add empty group without label
            props = flow.operator("node.add_empty_group", text="", icon="ADD")
            props.use_transform = True


#Shader Editor - Relations tab, Node Group Panel
# from nodeitems_builtin, not directly importable
def contains_group(nodetree, group):
    if nodetree == group:
        return True
    else:
        for node in nodetree.nodes:
            if node.bl_idname in node_tree_group_type.values() and node.node_tree is not None:
                if contains_group(node.node_tree, group):
                    return True
    return False

class NODES_PT_Input_node_group(bpy.types.Panel):
    bl_label = "Nodegroups"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Relations"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type in node_tree_group_type)

    def draw(self, context):
        layout = self.layout

        if context is None:
            return
        space = context.space_data
        if not space:
            return
        ntree = space.edit_tree
        if not ntree:
            return

        col = layout.column(align=True)
        col.scale_y = 1.5
        draw_node_groups(context, col)
        return


#Relations tab, Layout Panel
class NODES_PT_Relations_layout(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Layout"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Relations"

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        ##### Textbuttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Frame               ", icon = "NODE_FRAME")
            props.use_transform = True
            props.type = "NodeFrame"

            props = col.operator("node.add_node", text=" Reroute             ", icon = "NODE_REROUTE")
            props.use_transform = True
            props.type = "NodeReroute"



        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_FRAME")
            props.use_transform = True
            props.type = "NodeFrame"

            props = flow.operator("node.add_node", text = "", icon = "NODE_REROUTE")
            props.use_transform = True
            props.type = "NodeReroute"



# ------------- Geometry Nodes Editor - Add tab -------------------------------

#add attribute panel
class NODES_PT_geom_add_attribute(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Attribute"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Attribute Statistics  ", icon = "ATTRIBUTE_STATISTIC")
            props.use_transform = True
            props.type = "GeometryNodeAttributeStatistic"

            props = col.operator("node.add_node", text=" Domain Size            ", icon = "DOMAIN_SIZE")
            props.use_transform = True
            props.type = "GeometryNodeAttributeDomainSize"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Blur Attribute          ", icon = "BLUR_ATTRIBUTE")
            props.use_transform = True
            props.type = "GeometryNodeBlurAttribute"

            props = col.operator("node.add_node", text=" Capture Attribute    ", icon = "ATTRIBUTE_CAPTURE")
            props.use_transform = True
            props.type = "GeometryNodeCaptureAttribute"

            props = col.operator("node.add_node", text=" Remove Attribute   ", icon = "ATTRIBUTE_REMOVE")
            props.use_transform = True
            props.type = "GeometryNodeRemoveAttribute"

            props = col.operator("node.add_node", text=" Store Named Attribute ", icon = "ATTRIBUTE_STORE")
            props.use_transform = True
            props.type = "GeometryNodeStoreNamedAttribute"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text="", icon = "ATTRIBUTE_STATISTIC")
            props.use_transform = True
            props.type = "GeometryNodeAttributeStatistic"

            props = flow.operator("node.add_node", text="", icon = "DOMAIN_SIZE")
            props.use_transform = True
            props.type = "GeometryNodeAttributeDomainSize"

            props = flow.operator("node.add_node", text="", icon = "BLUR_ATTRIBUTE")
            props.use_transform = True
            props.type = "GeometryNodeBlurAttribute"

            props = flow.operator("node.add_node", text="", icon = "ATTRIBUTE_CAPTURE")
            props.use_transform = True
            props.type = "GeometryNodeCaptureAttribute"

            props = flow.operator("node.add_node", text="", icon = "ATTRIBUTE_REMOVE")
            props.use_transform = True
            props.type = "GeometryNodeRemoveAttribute"

            props = flow.operator("node.add_node", text="", icon = "ATTRIBUTE_STORE")
            props.use_transform = True
            props.type = "GeometryNodeStoreNamedAttribute"


#add input panel
class NODES_PT_geom_add_input(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Input"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout


#add input panel, constant supbanel
class NODES_PT_geom_add_input_constant(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Constant"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_input"

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Boolean                ", icon = "INPUT_BOOL")
            props.use_transform = True
            props.type = "FunctionNodeInputBool"

            props = col.operator("node.add_node", text = "Collection           ", icon = "OUTLINER_COLLECTION")
            props.use_transform = True
            props.type = "GeometryNodeInputCollection"

            props = col.operator("node.add_node", text=" Color                    ", icon = "COLOR")
            props.use_transform = True
            props.type = "FunctionNodeInputColor"

            props = col.operator("node.add_node", text=" Image                  ", icon = "FILE_IMAGE")
            props.use_transform = True
            props.type = "GeometryNodeInputImage"

            props = col.operator("node.add_node", text=" Integer                 ", icon = "INTEGER")
            props.use_transform = True
            props.type = "FunctionNodeInputInt"

            props = col.operator("node.add_node", text=" Material               ", icon = "NODE_MATERIAL")
            props.use_transform = True
            props.type = "GeometryNodeInputMaterial"

            props = col.operator("node.add_node", text = "Object               ", icon = "OBJECT_DATA")
            props.use_transform = True
            props.type = "GeometryNodeInputObject"

            props = col.operator("node.add_node", text=" Rotation               ", icon = "ROTATION")
            props.use_transform = True
            props.type = "FunctionNodeInputRotation"

            props = col.operator("node.add_node", text=" String                    ", icon = "STRING")
            props.use_transform = True
            props.type = "FunctionNodeInputString"

            props = col.operator("node.add_node", text=" Value                    ", icon = "NODE_VALUE")
            props.use_transform = True
            props.type = "ShaderNodeValue"

            props = col.operator("node.add_node", text=" Vector                   ", icon = "NODE_VECTOR")
            props.use_transform = True
            props.type = "FunctionNodeInputVector"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5


            props = flow.operator("node.add_node", text = "", icon = "INPUT_BOOL")
            props.use_transform = True
            props.type = "FunctionNodeInputBool"

            props = flow.operator("node.add_node", text = "", icon = "OUTLINER_COLLECTION")
            props.use_transform = True
            props.type = "GeometryNodeInputCollection"

            props = flow.operator("node.add_node", text = "", icon = "COLOR")
            props.use_transform = True
            props.type = "FunctionNodeInputColor"

            props = flow.operator("node.add_node", text="", icon = "FILE_IMAGE")
            props.use_transform = True
            props.type = "GeometryNodeInputImage"

            props = flow.operator("node.add_node", text = "", icon = "INTEGER")
            props.use_transform = True
            props.type = "FunctionNodeInputInt"

            props = flow.operator("node.add_node", text = "", icon = "NODE_MATERIAL")
            props.use_transform = True
            props.type = "GeometryNodeInputMaterial"

            props = flow.operator("node.add_node", text = "", icon = "OBJECT_DATA")
            props.use_transform = True
            props.type = "GeometryNodeInputObject"

            props = flow.operator("node.add_node", text="", icon = "ROTATION")
            props.use_transform = True
            props.type = "FunctionNodeInputRotation"

            props = flow.operator("node.add_node", text = "", icon = "STRING")
            props.use_transform = True
            props.type = "FunctionNodeInputString"

            props = flow.operator("node.add_node", text = "", icon = "NODE_VALUE")
            props.use_transform = True
            props.type = "ShaderNodeValue"

            props = flow.operator("node.add_node", text = "", icon = "NODE_VECTOR")
            props.use_transform = True
            props.type = "FunctionNodeInputVector"


#add input panel, gizmo supbanel
class NODES_PT_geom_add_input_gizmo(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Gizmo"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_input"

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Dial Gizmo           ", icon = "DIAL_GIZMO")
            props.use_transform = True
            props.type = "GeometryNodeGizmoDial"

            props = col.operator("node.add_node", text=" Linear Gizmo        ", icon = "LINEAR_GIZMO")
            props.use_transform = True
            props.type = "GeometryNodeGizmoLinear"

            props = col.operator("node.add_node", text=" Transform Gizmo ", icon = "TRANSFORM_GIZMO")
            props.use_transform = True
            props.type = "GeometryNodeGizmoTransform"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5


            props = flow.operator("node.add_node", text = "", icon = "DIAL_GIZMO")
            props.use_transform = True
            props.type = "GeometryNodeGizmoDial"

            props = flow.operator("node.add_node", text = "", icon = "LINEAR_GIZMO")
            props.use_transform = True
            props.type = "GeometryNodeGizmoLinear"

            props = flow.operator("node.add_node", text="", icon = "TRANSFORM_GIZMO")
            props.use_transform = True
            props.type = "GeometryNodeGizmoTransform"


#add input panel, file supbanel
class NODES_PT_geom_add_input_file(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Import"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_input"

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Import OBJ           ", icon = "LOAD_OBJ")
            props.use_transform = True
            props.type = "GeometryNodeImportOBJ"

            props = col.operator("node.add_node", text=" Import PLY           ", icon = "LOAD_PLY")
            props.use_transform = True
            props.type = "GeometryNodeImportPLY"

            props = col.operator("node.add_node", text=" Import STL           ", icon = "LOAD_STL")
            props.use_transform = True
            props.type = "GeometryNodeImportSTL"

            props = col.operator("node.add_node", text=" Import CSV           ", icon = "LOAD_CSV")
            props.use_transform = True
            props.type = "GeometryNodeImportCSV"

            props = col.operator("node.add_node", text=" Import Text           ", icon = "FILE_TEXT")
            props.use_transform = True
            props.type = "GeometryNodeImportText"

            props = col.operator("node.add_node", text=" Import OpenVDB   ", icon = "FILE_VOLUME")
            props.use_transform = True
            props.type = "GeometryNodeImportVDB"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "LOAD_OBJ")
            props.use_transform = True
            props.type = "GeometryNodeImportOBJ"

            props = flow.operator("node.add_node", text = "", icon = "LOAD_PLY")
            props.use_transform = True
            props.type = "GeometryNodeImportPLY"

            props = flow.operator("node.add_node", text = "", icon = "LOAD_STL")
            props.use_transform = True
            props.type = "GeometryNodeImportSTL"

            props = flow.operator("node.add_node", text = "", icon = "LOAD_CSV")
            props.use_transform = True
            props.type = "GeometryNodeImportCSV"

            props = flow.operator("node.add_node", text = "", icon = "FILE_TEXT")
            props.use_transform = True
            props.type = "GeometryNodeImportText"

            props = flow.operator("node.add_node", text = "", icon = "FILE_VOLUME")
            props.use_transform = True
            props.type = "GeometryNodeImportVDB"



#add input panel, scene subpanel
class NODES_PT_geom_add_input_scene(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Scene"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_input"

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            if context.space_data.geometry_nodes_type == 'TOOL':
                props = col.operator("node.add_node", text=" Cursor                  ", icon = "CURSOR")
                props.use_transform = True
                props.type = "GeometryNodeTool3DCursor"

            props = col.operator("node.add_node", text=" Active Camera     ", icon = "VIEW_SWITCHTOCAM")
            props.use_transform = True
            props.type = "GeometryNodeInputActiveCamera"

            props = col.operator("node.add_node", text=" Camera Info     ", icon = "CAMERA_DATA")
            props.use_transform = True
            props.type = "GeometryNodeCameraInfo"

            props = col.operator("node.add_node", text=" Collection Info     ", icon = "COLLECTION_INFO")
            props.use_transform = True
            props.type = "GeometryNodeCollectionInfo"

            props = col.operator("node.add_node", text=" Image Info           ", icon = "IMAGE_INFO")
            props.use_transform = True
            props.type = "GeometryNodeImageInfo"

            props = col.operator("node.add_node", text=" Is Viewport          ", icon = "VIEW")
            props.use_transform = True
            props.type = "GeometryNodeIsViewport"

            props = col.operator("node.add_node", text=" Named Layer Selection  ", icon = "NAMED_LAYER_SELECTION")
            props.use_transform = True
            props.type = "GeometryNodeInputNamedLayerSelection"

            if context.space_data.geometry_nodes_type == 'TOOL':
                props = col.operator("node.add_node", text=" Mouse Position    ", icon = "MOUSE_POSITION")
                props.use_transform = True
                props.type = "GeometryNodeToolMousePosition"

            props = col.operator("node.add_node", text=" Object Info           ", icon = "NODE_OBJECTINFO")
            props.use_transform = True
            props.type = "GeometryNodeObjectInfo"

            props = col.operator("node.add_node", text=" Scene Time          ", icon = "TIME")
            props.use_transform = True
            props.type = "GeometryNodeInputSceneTime"

            props = col.operator("node.add_node", text=" Self Object           ", icon = "SELF_OBJECT")
            props.use_transform = True
            props.type = "GeometryNodeSelfObject"

            if context.space_data.geometry_nodes_type == 'TOOL':
                props = col.operator("node.add_node", text=" Viewport Transform ", icon = "VIEWPORT_TRANSFORM")
                props.use_transform = True
                props.type = "GeometryNodeViewportTransform"


        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            if context.space_data.geometry_nodes_type == 'TOOL':
                props = flow.operator("node.add_node", text="", icon = "CURSOR")
                props.use_transform = True
                props.type = "GeometryNodeTool3DCursor"

            props = flow.operator("node.add_node", text="", icon = "VIEW_SWITCHTOCAM")
            props.use_transform = True
            props.type = "GeometryNodeInputActiveCamera"

            props = flow.operator("node.add_node", text="", icon = "CAMERA_DATA")
            props.use_transform = True
            props.type = "GeometryNodeCameraInfo"

            props = flow.operator("node.add_node", text = "", icon = "COLLECTION_INFO")
            props.use_transform = True
            props.type = "GeometryNodeCollectionInfo"

            props = flow.operator("node.add_node", text="", icon = "IMAGE_INFO")
            props.use_transform = True
            props.type = "GeometryNodeImageInfo"

            props = flow.operator("node.add_node", text = "", icon = "VIEW")
            props.use_transform = True
            props.type = "GeometryNodeIsViewport"

            props = flow.operator("node.add_node", text="", icon = "NAMED_LAYER_SELECTION")
            props.use_transform = True
            props.type = "GeometryNodeInputNamedLayerSelection"

            if context.space_data.geometry_nodes_type == 'TOOL':
                props = flow.operator("node.add_node", text="", icon = "MOUSE_POSITION")
                props.use_transform = True
                props.type = "GeometryNodeToolMousePosition"

            props = flow.operator("node.add_node", text = "", icon = "NODE_OBJECTINFO")
            props.use_transform = True
            props.type = "GeometryNodeObjectInfo"

            props = flow.operator("node.add_node", text = "", icon = "TIME")
            props.use_transform = True
            props.type = "GeometryNodeInputSceneTime"

            props = flow.operator("node.add_node", text="", icon = "SELF_OBJECT")
            props.use_transform = True
            props.type = "GeometryNodeSelfObject"

            if context.space_data.geometry_nodes_type == 'TOOL':
                props = flow.operator("node.add_node", text="", icon = "VIEWPORT_TRANSFORM")
                props.use_transform = True
                props.type = "GeometryNodeViewportTransform"


#add output panel
class NODES_PT_geom_add_output(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Output"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Viewer   ", icon = "NODE_VIEWER")
            props.use_transform = True
            props.type = "GeometryNodeViewer"

            props = col.operator("node.add_node", text=" Warning   ", icon = "ERROR")
            props.use_transform = True
            props.type = "GeometryNodeWarning"


        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_VIEWER")
            props.use_transform = True
            props.type = "GeometryNodeViewer"

            props = flow.operator("node.add_node", text="", icon = "ERROR")
            props.use_transform = True
            props.type = "GeometryNodeWarning"


#add geometry panel
class NODES_PT_geom_add_geometry(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Geometry"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Geometry to Instance", icon = "GEOMETRY_INSTANCE")
            props.use_transform = True
            props.type = "GeometryNodeGeometryToInstance"

            props = col.operator("node.add_node", text=" Join Geometry           ", icon = "JOIN")
            props.use_transform = True
            props.type = "GeometryNodeJoinGeometry"


        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "GEOMETRY_INSTANCE")
            props.use_transform = True
            props.type = "GeometryNodeGeometryToInstance"

            props = flow.operator("node.add_node", text = "", icon = "JOIN")
            props.use_transform = True
            props.type = "GeometryNodeJoinGeometry"


#add geometry panel, read subpanel
class NODES_PT_geom_add_geometry_read(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Read"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_geometry"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" ID                               ", icon = "GET_ID")
            props.use_transform = True
            props.type = "GeometryNodeInputID"

            props = col.operator("node.add_node", text=" Index                          ", icon = "INDEX")
            props.use_transform = True
            props.type = "GeometryNodeInputIndex"

            props = col.operator("node.add_node", text=" Named Attribute       ", icon = "NAMED_ATTRIBUTE")
            props.use_transform = True
            props.type = "GeometryNodeInputNamedAttribute"

            props = col.operator("node.add_node", text=" Normal                      ", icon = "RECALC_NORMALS")
            props.use_transform = True
            props.type = "GeometryNodeInputNormal"

            props = col.operator("node.add_node", text=" Position                     ", icon = "POSITION")
            props.use_transform = True
            props.type = "GeometryNodeInputPosition"

            props = col.operator("node.add_node", text=" Radius                       ", icon = "RADIUS")
            props.use_transform = True
            props.type = "GeometryNodeInputRadius"

            if context.space_data.geometry_nodes_type == 'TOOL':
                props = col.operator("node.add_node", text=" Selection                    ", icon = "RESTRICT_SELECT_OFF")
                props.use_transform = True
                props.type = "GeometryNodeToolSelection"

                props = col.operator("node.add_node", text=" Active Element          ", icon = "ACTIVE_ELEMENT")
                props.use_transform = True
                props.type = "GeometryNodeToolActiveElement"


        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "GET_ID")
            props.use_transform = True
            props.type = "GeometryNodeInputID"

            props = flow.operator("node.add_node", text = "", icon = "INDEX")
            props.use_transform = True
            props.type = "GeometryNodeInputIndex"

            props = flow.operator("node.add_node", text = "", icon = "NAMED_ATTRIBUTE")
            props.use_transform = True
            props.type = "GeometryNodeInputNamedAttribute"

            props = flow.operator("node.add_node", text = "", icon = "RECALC_NORMALS")
            props.use_transform = True
            props.type = "GeometryNodeInputNormal"

            props = flow.operator("node.add_node", text = "", icon = "POSITION")
            props.use_transform = True
            props.type = "GeometryNodeInputPosition"

            props = flow.operator("node.add_node", text = "", icon = "RADIUS")
            props.use_transform = True
            props.type = "GeometryNodeInputRadius"

            if context.space_data.geometry_nodes_type == 'TOOL':
                props = flow.operator("node.add_node", text="", icon = "RESTRICT_SELECT_OFF")
                props.use_transform = True
                props.type = "GeometryNodeToolSelection"

                props = flow.operator("node.add_node", text="", icon = "ACTIVE_ELEMENT")
                props.use_transform = True
                props.type = "GeometryNodeToolActiveElement"



#add geometry panel, sample subpanel
class NODES_PT_geom_add_geometry_sample(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Sample"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_geometry"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Geometry Proximity   ", icon = "GEOMETRY_PROXIMITY")
            props.use_transform = True
            props.type = "GeometryNodeProximity"

            props = col.operator("node.add_node", text=" Index of Nearest        ", icon = "INDEX_OF_NEAREST")
            props.use_transform = True
            props.type = "GeometryNodeIndexOfNearest"

            props = col.operator("node.add_node", text=" Raycast                      ", icon = "RAYCAST")
            props.use_transform = True
            props.type = "GeometryNodeRaycast"

            props = col.operator("node.add_node", text=" Sample Index             ", icon = "SAMPLE_INDEX")
            props.use_transform = True
            props.type = "GeometryNodeSampleIndex"

            props = col.operator("node.add_node", text=" Sample Nearest        ", icon = "SAMPLE_NEAREST")
            props.use_transform = True
            props.type = "GeometryNodeSampleNearest"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "GEOMETRY_PROXIMITY")
            props.use_transform = True
            props.type = "GeometryNodeMergeByDistance"

            props = flow.operator("node.add_node", text="", icon = "INDEX_OF_NEAREST")
            props.use_transform = True
            props.type = "GeometryNodeIndexOfNearest"

            props = flow.operator("node.add_node", text = "", icon = "RAYCAST")
            props.use_transform = True
            props.type = "GeometryNodeRaycast"

            props = flow.operator("node.add_node", text="", icon = "SAMPLE_INDEX")
            props.use_transform = True
            props.type = "GeometryNodeSampleIndex"

            props = flow.operator("node.add_node", text="", icon = "SAMPLE_NEAREST")
            props.use_transform = True
            props.type = "GeometryNodeSampleNearest"


#add geometry panel, write subpanel
class NODES_PT_geom_add_geometry_write(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Write"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_geometry"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Set Geometry Name  ", icon = "GEOMETRY_NAME")
            props.use_transform = True
            props.type = "GeometryNodeSetGeometryName"

            props = col.operator("node.add_node", text=" Set ID                          ", icon = "SET_ID")
            props.use_transform = True
            props.type = "GeometryNodeSetID"

            props = col.operator("node.add_node", text=" Set Postion                 ", icon = "SET_POSITION")
            props.use_transform = True
            props.type = "GeometryNodeSetPosition"

            if context.space_data.geometry_nodes_type == 'TOOL':
                props = col.operator("node.add_node", text=" Set Selection                 ", icon = "SET_SELECTION")
                props.use_transform = True
                props.type = "GeometryNodeToolSetSelection"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "GEOMETRY_NAME")
            props.use_transform = True
            props.type = "GeometryNodeSetGeometryName"

            props = flow.operator("node.add_node", text = "", icon = "SET_ID")
            props.use_transform = True
            props.type = "GeometryNodeSetID"

            props = flow.operator("node.add_node", text="", icon = "SET_POSITION")
            props.use_transform = True
            props.type = "GeometryNodeSetPosition"

            if context.space_data.geometry_nodes_type == 'TOOL':
                props = flow.operator("node.add_node", text="", icon = "SET_SELECTION")
                props.use_transform = True
                props.type = "GeometryNodeToolSetSelection"


#add geometry panel, operations subpanel
class NODES_PT_geom_add_geometry_operations(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Operations"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_geometry"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Bake                            ", icon = "BAKE")
            props.use_transform = True
            props.type = "GeometryNodeBake"

            props = col.operator("node.add_node", text=" Bounding Box             ", icon = "PIVOT_BOUNDBOX")
            props.use_transform = True
            props.type = "GeometryNodeBoundBox"

            props = col.operator("node.add_node", text=" Convex Hull                ", icon = "CONVEXHULL")
            props.use_transform = True
            props.type = "GeometryNodeConvexHull"

            props = col.operator("node.add_node", text=" Delete Geometry       ", icon = "DELETE")
            props.use_transform = True
            props.type = "GeometryNodeDeleteGeometry"

            props = col.operator("node.add_node", text=" Duplicate Geometry ", icon = "DUPLICATE")
            props.use_transform = True
            props.type = "GeometryNodeDuplicateElements"

            props = col.operator("node.add_node", text=" Merge by Distance    ", icon = "REMOVE_DOUBLES")
            props.use_transform = True
            props.type = "GeometryNodeMergeByDistance"

            props = col.operator("node.add_node", text=" Sort Elements    ", icon = "SORTSIZE")
            props.use_transform = True
            props.type = "GeometryNodeSortElements"

            props = col.operator("node.add_node", text=" Transform Geometry  ", icon = "NODE_TRANSFORM")
            props.use_transform = True
            props.type = "GeometryNodeTransform"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Separate Components", icon = "SEPARATE")
            props.use_transform = True
            props.type = "GeometryNodeSeparateComponents"

            props = col.operator("node.add_node", text=" Separate Geometry   ", icon = "SEPARATE_GEOMETRY")
            props.use_transform = True
            props.type = "GeometryNodeSeparateGeometry"

            props = col.operator("node.add_node", text=" Split to Instances   ", icon = "SPLIT_TO_INSTANCES")
            props.use_transform = True
            props.type = "GeometryNodeSplitToInstances"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "BAKE")
            props.use_transform = True
            props.type = "GeometryNodeBake"

            props = flow.operator("node.add_node", text = "", icon = "PIVOT_BOUNDBOX")
            props.use_transform = True
            props.type = "GeometryNodeBoundBox"

            props = flow.operator("node.add_node", text = "", icon = "CONVEXHULL")
            props.use_transform = True
            props.type = "GeometryNodeConvexHull"

            props = flow.operator("node.add_node", text = "", icon = "DELETE")
            props.use_transform = True
            props.type = "GeometryNodeDeleteGeometry"

            props = flow.operator("node.add_node", text = "", icon = "DUPLICATE")
            props.use_transform = True
            props.type = "GeometryNodeDuplicateElements"

            props = flow.operator("node.add_node", text = "", icon = "REMOVE_DOUBLES")
            props.use_transform = True
            props.type = "GeometryNodeMergeByDistance"

            props = flow.operator("node.add_node", text="", icon = "SORTSIZE")
            props.use_transform = True
            props.type = "GeometryNodeSortElements"

            props = flow.operator("node.add_node", text = "", icon = "NODE_TRANSFORM")
            props.use_transform = True
            props.type = "GeometryNodeTransform"

            props = flow.operator("node.add_node", text = "", icon = "SEPARATE")
            props.use_transform = True
            props.type = "GeometryNodeSeparateComponents"

            props = flow.operator("node.add_node", text = "", icon = "SEPARATE_GEOMETRY")
            props.use_transform = True
            props.type = "GeometryNodeSeparateGeometry"

            props = flow.operator("node.add_node", text = "", icon = "SPLIT_TO_INSTANCES")
            props.use_transform = True
            props.type = "GeometryNodeSplitToInstances"


#add Curves panel
class NODES_PT_geom_add_curve(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Curve"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout

#add Curves panel, read subpanel
class NODES_PT_geom_add_curve_read(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Read"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_curve"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Curve Handle Positions ", icon = "CURVE_HANDLE_POSITIONS")
            props.use_transform = True
            props.type = "GeometryNodeInputCurveHandlePositions"

            props = col.operator("node.add_node", text=" Curve Length              ", icon = "PARTICLEBRUSH_LENGTH")
            props.use_transform = True
            props.type = "GeometryNodeCurveLength"

            props = col.operator("node.add_node", text=" Curve Tangent           ", icon = "CURVE_TANGENT")
            props.use_transform = True
            props.type = "GeometryNodeInputTangent"

            props = col.operator("node.add_node", text=" Curve Tilt                 ", icon = "CURVE_TILT")
            props.use_transform = True
            props.type = "GeometryNodeInputCurveTilt"

            props = col.operator("node.add_node", text=" Endpoint Selection    ", icon = "SELECT_LAST")
            props.use_transform = True
            props.type = "GeometryNodeCurveEndpointSelection"

            props = col.operator("node.add_node", text=" Handle Type Selection", icon = "SELECT_HANDLETYPE")
            props.use_transform = True
            props.type = "GeometryNodeCurveHandleTypeSelection"

            props = col.operator("node.add_node", text=" Is Spline Cyclic          ", icon = "IS_SPLINE_CYCLIC")
            props.use_transform = True
            props.type = "GeometryNodeInputSplineCyclic"

            props = col.operator("node.add_node", text=" Spline Length             ", icon = "SPLINE_LENGTH")
            props.use_transform = True
            props.type = "GeometryNodeSplineLength"

            props = col.operator("node.add_node", text=" Spline Parameter      ", icon = "CURVE_PARAMETER")
            props.use_transform = True
            props.type = "GeometryNodeSplineParameter"

            props = col.operator("node.add_node", text=" Spline Resolution        ", icon = "SPLINE_RESOLUTION")
            props.use_transform = True
            props.type = "GeometryNodeInputSplineResolution"

        #### Icon Buttons

        else:
            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "CURVE_HANDLE_POSITIONS")
            props.use_transform = True
            props.type = "GeometryNodeInputCurveHandlePositions"

            props = flow.operator("node.add_node", text = "", icon = "PARTICLEBRUSH_LENGTH")
            props.use_transform = True
            props.type = "GeometryNodeCurveLength"

            props = flow.operator("node.add_node", text = "", icon = "CURVE_TANGENT")
            props.use_transform = True
            props.type = "GeometryNodeInputTangent"

            props = flow.operator("node.add_node", text="", icon = "CURVE_TILT")
            props.use_transform = True
            props.type = "GeometryNodeInputCurveTilt"

            props = flow.operator("node.add_node", text="", icon = "SELECT_LAST")
            props.use_transform = True
            props.type = "GeometryNodeCurveEndpointSelection"

            props = flow.operator("node.add_node", text="", icon = "SELECT_HANDLETYPE")
            props.use_transform = True
            props.type = "GeometryNodeCurveHandleTypeSelection"

            props = flow.operator("node.add_node", text = "", icon = "IS_SPLINE_CYCLIC")
            props.use_transform = True
            props.type = "GeometryNodeInputSplineCyclic"

            props = flow.operator("node.add_node", text = "", icon = "SPLINE_LENGTH")
            props.use_transform = True
            props.type = "GeometryNodeSplineLength"

            props = flow.operator("node.add_node", text = "", icon = "CURVE_PARAMETER")
            props.use_transform = True
            props.type = "GeometryNodeSplineParameter"

            props = flow.operator("node.add_node", text = "", icon = "SPLINE_RESOLUTION")
            props.use_transform = True
            props.type = "GeometryNodeInputSplineResolution"


#add Curves panel, read subpanel
class NODES_PT_geom_add_curve_sample(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Sample"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_curve"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Sample Curve ", icon = "CURVE_SAMPLE")
            props.use_transform = True
            props.type = "GeometryNodeSampleCurve"

        #### Icon Buttons

        else:
            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "CURVE_SAMPLE")
            props.use_transform = True
            props.type = "GeometryNodeSampleCurve"




#add Curves panel, write subpanel
class NODES_PT_geom_add_curve_write(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Write"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_curve"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Set Curve Normal        ", icon = "CURVE_NORMAL")
            props.use_transform = True
            props.type = "GeometryNodeSetCurveNormal"

            props = col.operator("node.add_node", text=" Set Curve Radius        ", icon = "SET_CURVE_RADIUS")
            props.use_transform = True
            props.type = "GeometryNodeSetCurveRadius"

            props = col.operator("node.add_node", text=" Set Curve Tilt             ", icon = "SET_CURVE_TILT")
            props.use_transform = True
            props.type = "GeometryNodeSetCurveTilt"

            props = col.operator("node.add_node", text=" Set Handle Positions   ", icon = "SET_CURVE_HANDLE_POSITIONS")
            props.use_transform = True
            props.type = "GeometryNodeSetCurveHandlePositions"

            props = col.operator("node.add_node", text=" Set Handle Type         ", icon = "HANDLE_AUTO")
            props.use_transform = True
            props.type = "GeometryNodeCurveSetHandles"

            props = col.operator("node.add_node", text=" Set Spline Cyclic        ", icon = "TOGGLE_CYCLIC")
            props.use_transform = True
            props.type = "GeometryNodeSetSplineCyclic"

            props = col.operator("node.add_node", text=" Set Spline Resolution   ", icon = "SET_SPLINE_RESOLUTION")
            props.use_transform = True
            props.type = "GeometryNodeSetSplineResolution"

            props = col.operator("node.add_node", text=" Set Spline Type            ", icon = "SPLINE_TYPE")
            props.use_transform = True
            props.type = "GeometryNodeCurveSplineType"

        #### Icon Buttons

        else:
            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text="", icon = "CURVE_NORMAL")
            props.use_transform = True
            props.type = "GeometryNodeSetCurveNormal"

            props = flow.operator("node.add_node", text = "", icon = "SET_CURVE_RADIUS")
            props.use_transform = True
            props.type = "GeometryNodeSetCurveRadius"

            props = flow.operator("node.add_node", text = "", icon = "SET_CURVE_TILT")
            props.use_transform = True
            props.type = "GeometryNodeSetCurveTilt"

            props = flow.operator("node.add_node", text = "", icon = "SET_CURVE_HANDLE_POSITIONS")
            props.use_transform = True
            props.type = "GeometryNodeSetCurveHandlePositions"

            props = flow.operator("node.add_node", text = "", icon = "HANDLE_AUTO")
            props.use_transform = True
            props.type = "GeometryNodeCurveSetHandles"

            props = flow.operator("node.add_node", text = "", icon = "TOGGLE_CYCLIC")
            props.use_transform = True
            props.type = "GeometryNodeSetSplineCyclic"

            props = flow.operator("node.add_node", text = "", icon = "SET_SPLINE_RESOLUTION")
            props.use_transform = True
            props.type = "GeometryNodeSetSplineResolution"

            props = flow.operator("node.add_node", text = "", icon = "SPLINE_TYPE")
            props.use_transform = True
            props.type = "GeometryNodeCurveSplineType"


#add Curves panel, operations subpanel
class NODES_PT_geom_add_curve_operations(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Operations"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_curve"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Curves to Grease Pencil", icon = "OUTLINER_OB_GREASEPENCIL")
            props.use_transform = True
            props.type = "GeometryNodeCurvesToGreasePencil"

            props = col.operator("node.add_node", text=" Curve to Mesh            ", icon = "OUTLINER_OB_MESH")
            props.use_transform = True
            props.type = "GeometryNodeCurveToMesh"

            props = col.operator("node.add_node", text=" Curve to Points          ", icon = "POINTCLOUD_DATA")
            props.use_transform = True
            props.type = "GeometryNodeCurveToPoints"

            props = col.operator("node.add_node", text=" Deform Curves on Surface ", icon = "DEFORM_CURVES")
            props.use_transform = True
            props.type = "GeometryNodeDeformCurvesOnSurface"

            props = col.operator("node.add_node", text=" Fill Curve                   ", icon = "CURVE_FILL")
            props.use_transform = True
            props.type = "GeometryNodeFillCurve"

            props = col.operator("node.add_node", text=" Fillet Curve                ", icon = "CURVE_FILLET")
            props.use_transform = True
            props.type = "GeometryNodeFilletCurve"

            props = col.operator("node.add_node", text=" Grease Pencil to Curves", icon = "OUTLINER_OB_CURVES")
            props.use_transform = True
            props.type = "GeometryNodeGreasePencilToCurves"

            props = col.operator("node.add_node", text=" Interpolate Curve    ", icon = "INTERPOLATE_CURVE")
            props.use_transform = True
            props.type = "GeometryNodeInterpolateCurves"

            props = col.operator("node.add_node", text=" Merge Layers            ", icon = "MERGE")
            props.use_transform = True
            props.type = "GeometryNodeInterpolateCurves"

            props = col.operator("node.add_node", text=" Resample Curve        ", icon = "CURVE_RESAMPLE")
            props.use_transform = True
            props.type = "GeometryNodeResampleCurve"

            props = col.operator("node.add_node", text=" Reverse Curve           ", icon = "SWITCH_DIRECTION")
            props.use_transform = True
            props.type = "GeometryNodeReverseCurve"

            props = col.operator("node.add_node", text=" Subdivide Curve       ", icon = "SUBDIVIDE_EDGES")
            props.use_transform = True
            props.type = "GeometryNodeSubdivideCurve"

            props = col.operator("node.add_node", text=" Trim Curve                  ", icon = "CURVE_TRIM")
            props.use_transform = True
            props.type = "GeometryNodeTrimCurve"

        #### Icon Buttons

        else:
            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text="", icon = "OUTLINER_OB_GREASEPENCIL")
            props.use_transform = True
            props.type = "GeometryNodeCurvesToGreasePencil"

            props = flow.operator("node.add_node", text = "", icon = "OUTLINER_OB_MESH")
            props.use_transform = True
            props.type = "GeometryNodeCurveToMesh"

            props = flow.operator("node.add_node", text = "", icon = "POINTCLOUD_DATA")
            props.use_transform = True
            props.type = "GeometryNodeCurveToPoints"

            props = flow.operator("node.add_node", text = "", icon = "DEFORM_CURVES")
            props.use_transform = True
            props.type = "GeometryNodeDeformCurvesOnSurface"

            props = flow.operator("node.add_node", text = "", icon = "CURVE_FILL")
            props.use_transform = True
            props.type = "GeometryNodeFillCurve"

            props = flow.operator("node.add_node", text = "", icon = "CURVE_FILLET")
            props.use_transform = True
            props.type = "GeometryNodeFilletCurve"

            props = flow.operator("node.add_node", text="", icon = "OUTLINER_OB_CURVES")
            props.use_transform = True
            props.type = "GeometryNodeGreasePencilToCurves"

            props = flow.operator("node.add_node", text="", icon = "INTERPOLATE_CURVE")
            props.use_transform = True
            props.type = "GeometryNodeInterpolateCurves"

            props = flow.operator("node.add_node", text="", icon = "MERGE")
            props.use_transform = True
            props.type = "GeometryNodeInterpolateCurves"

            props = flow.operator("node.add_node", text = "", icon = "CURVE_RESAMPLE")
            props.use_transform = True
            props.type = "GeometryNodeResampleCurve"

            props = flow.operator("node.add_node", text = "", icon = "SWITCH_DIRECTION")
            props.use_transform = True
            props.type = "GeometryNodeReverseCurve"

            props = flow.operator("node.add_node", text = "", icon = "SUBDIVIDE_EDGES")
            props.use_transform = True
            props.type = "GeometryNodeSubdivideCurve"

            props = flow.operator("node.add_node", text="", icon = "CURVE_TRIM")
            props.use_transform = True
            props.type = "GeometryNodeTrimCurve"


#add Curves panel, Primitives subpanel
class NODES_PT_geom_add_curve_primitives(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Primitives"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_curve"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Arc                        ", icon = "CURVE_ARC")
            props.use_transform = True
            props.type = "GeometryNodeCurveArc"

            props = col.operator("node.add_node", text=" Bezier Segment     ", icon = "CURVE_BEZCURVE")
            props.use_transform = True
            props.type = "GeometryNodeCurvePrimitiveBezierSegment"

            props = col.operator("node.add_node", text=" Curve Circle           ", icon = "CURVE_BEZCIRCLE")
            props.use_transform = True
            props.type = "GeometryNodeCurvePrimitiveCircle"

            props = col.operator("node.add_node", text=" Curve Line             ", icon = "CURVE_LINE")
            props.use_transform = True
            props.type = "GeometryNodeCurvePrimitiveLine"

            props = col.operator("node.add_node", text=" Curve Spiral           ", icon = "CURVE_SPIRAL")
            props.use_transform = True
            props.type = "GeometryNodeCurveSpiral"

            props = col.operator("node.add_node", text=" Quadratic Bezier    ", icon = "CURVE_NCURVE")
            props.use_transform = True
            props.type = "GeometryNodeCurveQuadraticBezier"

            props = col.operator("node.add_node", text=" Quadrilateral         ", icon = "CURVE_QUADRILATERAL")
            props.use_transform = True
            props.type = "GeometryNodeCurvePrimitiveQuadrilateral"

            props = col.operator("node.add_node", text=" Star                       ", icon = "CURVE_STAR")
            props.use_transform = True
            props.type = "GeometryNodeCurveStar"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "CURVE_ARC")
            props.use_transform = True
            props.type = "GeometryNodeCurveArc"

            props = flow.operator("node.add_node", text = "", icon = "CURVE_BEZCURVE")
            props.use_transform = True
            props.type = "GeometryNodeCurvePrimitiveBezierSegment"

            props = flow.operator("node.add_node", text = "", icon = "CURVE_BEZCIRCLE")
            props.use_transform = True
            props.type = "GeometryNodeCurvePrimitiveCircle"

            props = flow.operator("node.add_node", text = "", icon = "CURVE_LINE")
            props.use_transform = True
            props.type = "GeometryNodeCurvePrimitiveLine"

            props = flow.operator("node.add_node", text="", icon = "CURVE_SPIRAL")
            props.use_transform = True
            props.type = "GeometryNodeCurveSpiral"

            props = flow.operator("node.add_node", text = "", icon = "CURVE_NCURVE")
            props.use_transform = True
            props.type = "GeometryNodeCurveQuadraticBezier"

            props = flow.operator("node.add_node", text = "", icon = "CURVE_QUADRILATERAL")
            props.use_transform = True
            props.type = "GeometryNodeCurvePrimitiveQuadrilateral"

            props = flow.operator("node.add_node", text = "", icon = "CURVE_STAR")
            props.use_transform = True
            props.type = "GeometryNodeCurveStar"


#add Curve panel, Topology subpanel
class NODES_PT_geom_add_curve_topology(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Topology"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_curve"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Curve of Point              ", icon = "CURVE_OF_POINT")
            props.use_transform = True
            props.type = "GeometryNodeCurveOfPoint"

            props = col.operator("node.add_node", text=" Offset Point in Curve   ", icon = "OFFSET_POINT_IN_CURVE")
            props.use_transform = True
            props.type = "GeometryNodeOffsetPointInCurve"

            props = col.operator("node.add_node", text=" Points of Curve            ", icon = "POINT_OF_CURVE")
            props.use_transform = True
            props.type = "GeometryNodePointsOfCurve"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "CURVE_OF_POINT")
            props.use_transform = True
            props.type = "GeometryNodeCurveOfPoint"

            props = flow.operator("node.add_node", text = "", icon = "OFFSET_POINT_IN_CURVE")
            props.use_transform = True
            props.type = "GeometryNodeOffsetPointInCurve"

            props = flow.operator("node.add_node", text = "", icon = "POINT_OF_CURVE")
            props.use_transform = True
            props.type = "GeometryNodePointsOfCurve"


#add Grease Pencil panel
class NODES_PT_geom_add_grease_pencil(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Grease Pencil"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout


#add Grease Pencil panel, Read subpanel
class NODES_PT_geom_add_grease_pencil_read(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Read"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_grease_pencil"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Named Layer Selection              ", icon = "NAMED_LAYER_SELECTION")
            props.use_transform = True
            props.type = "GeometryNodeInputNamedLayerSelection"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NAMED_LAYER_SELECTION")
            props.use_transform = True
            props.type = "GeometryNodeInputNamedLayerSelection"


#add Grease Pencil panel, Read subpanel
class NODES_PT_geom_add_grease_pencil_write(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Write"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_grease_pencil"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Set Grease Pencil Color              ", icon = "COLOR")
            props.use_transform = True
            props.type = "GeometryNodeSetGreasePencilColor"

            props = col.operator("node.add_node", text=" Set Grease Pencil Depth             ", icon = "DEPTH")
            props.use_transform = True
            props.type = "GeometryNodeSetGreasePencilDepth"

            props = col.operator("node.add_node", text=" Set Grease Pencil Softness             ", icon = "FALLOFFSTROKE")
            props.use_transform = True
            props.type = "GeometryNodeSetGreasePencilSoftness"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "COLOR")
            props.use_transform = True
            props.type = "GeometryNodeSetGreasePencilColor"

            props = flow.operator("node.add_node", text = "", icon = "DEPTH")
            props.use_transform = True
            props.type = "GeometryNodeSetGreasePencilDepth"

            props = flow.operator("node.add_node", text = "", icon = "FALLOFFSTROKE")
            props.use_transform = True
            props.type = "GeometryNodeSetGreasePencilSoftness"


#add Grease Pencil panel, Read subpanel
class NODES_PT_geom_add_grease_pencil_operations(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Operations"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_grease_pencil"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Set Grease Pencil to Curves              ", icon = "OUTLINER_OB_CURVES")
            props.use_transform = True
            props.type = "GeometryNodeGreasePencilToCurves"

            props = col.operator("node.add_node", text=" Merge Layers                  ", icon = "MERGE")
            props.use_transform = True
            props.type = "GeometryNodeMergeLayers"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "OUTLINER_OB_CURVES")
            props.use_transform = True
            props.type = "GeometryNodeGreasePencilToCurves"

            props = flow.operator("node.add_node", text = "", icon = "MERGE")
            props.use_transform = True
            props.type = "GeometryNodeMergeLayers"


#add mesh panel
class NODES_PT_geom_add_instances(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Instances"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Instances on Points       ", icon = "POINT_INSTANCE")
            props.use_transform = True
            props.type = "GeometryNodeInstanceOnPoints"

            props = col.operator("node.add_node", text=" Instances to Points       ", icon = "INSTANCES_TO_POINTS")
            props.use_transform = True
            props.type = "GeometryNodeInstancesToPoints"

            props = col.operator("node.add_node", text=" Realize Instances         ", icon = "MOD_INSTANCE")
            props.use_transform = True
            props.type = "GeometryNodeRealizeInstances"

            props = col.operator("node.add_node", text=" Rotate Instances          ", icon = "ROTATE_INSTANCE")
            props.use_transform = True
            props.type = "GeometryNodeRotateInstances"

            props = col.operator("node.add_node", text=" Scale Instances            ", icon = "SCALE_INSTANCE")
            props.use_transform = True
            props.type = "GeometryNodeScaleInstances"

            props = col.operator("node.add_node", text=" Translate Instances      ", icon = "TRANSLATE_INSTANCE")
            props.use_transform = True
            props.type = "GeometryNodeTranslateInstances"

            props = col.operator("node.add_node", text=" Set Instance Transform      ", icon = "INSTANCE_TRANSFORM")
            props.use_transform = True
            props.type = "GeometryNodeSetInstanceTransform"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text = " Instance Bounds     ", icon = "INSTANCE_BOUNDS")
            props.use_transform = True
            props.type = "GeometryNodeInputInstanceBounds"

            props = col.operator("node.add_node", text = " Instance Transform     ", icon = "INSTANCE_TRANSFORM_GET")
            props.use_transform = True
            props.type = "GeometryNodeInstanceTransform"

            props = col.operator("node.add_node", text = " Instance Rotation     ", icon = "INSTANCE_ROTATE")
            props.use_transform = True
            props.type = "GeometryNodeInputInstanceRotation"

            props = col.operator("node.add_node", text = " Instance Scale      ", icon = "INSTANCE_SCALE")
            props.use_transform = True
            props.type = "GeometryNodeInputInstanceScale"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "POINT_INSTANCE")
            props.use_transform = True
            props.type = "GeometryNodeInstanceOnPoints"

            props = flow.operator("node.add_node", text = "", icon = "INSTANCES_TO_POINTS")
            props.use_transform = True
            props.type = "GeometryNodeInstancesToPoints"

            props = flow.operator("node.add_node", text = "", icon = "MOD_INSTANCE")
            props.use_transform = True
            props.type = "GeometryNodeRealizeInstances"

            props = flow.operator("node.add_node", text = "", icon = "ROTATE_INSTANCE")
            props.use_transform = True
            props.type = "GeometryNodeRotateInstances"

            props = flow.operator("node.add_node", text = "", icon = "SCALE_INSTANCE")
            props.use_transform = True
            props.type = "GeometryNodeTriangulate"

            props = flow.operator("node.add_node", text = "", icon = "TRANSLATE_INSTANCE")
            props.use_transform = True
            props.type = "GeometryNodeTranslateInstances"

            props = flow.operator("node.add_node", text="", icon = "INSTANCE_TRANSFORM")
            props.use_transform = True
            props.type = "GeometryNodeSetInstanceTransform"

            props = flow.operator("node.add_node", text = "", icon = "INSTANCE_BOUNDS")
            props.use_transform = True
            props.type = "GeometryNodeInputInstanceBounds"

            props = flow.operator("node.add_node", text = "", icon = "INSTANCE_TRANSFORM_GET")
            props.use_transform = True
            props.type = "GeometryNodeInstanceTransform"

            props = flow.operator("node.add_node", text = "", icon = "INSTANCE_ROTATE")
            props.use_transform = True
            props.type = "GeometryNodeInputInstanceRotation"

            props = flow.operator("node.add_node", text = "", icon = "INSTANCE_SCALE")
            props.use_transform = True
            props.type = "GeometryNodeInputInstanceScale"


#add mesh panel
class NODES_PT_geom_add_mesh(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Mesh"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout


#add mesh panel, read subpanel
class NODES_PT_geom_add_mesh_read(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Read"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_mesh"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Edge Angle              ", icon = "EDGE_ANGLE")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshEdgeAngle"

            props = col.operator("node.add_node", text=" Edge Neighbors       ", icon = "EDGE_NEIGHBORS")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshEdgeNeighbors"

            props = col.operator("node.add_node", text=" Edge Vertices          ", icon = "EDGE_VERTICES")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshEdgeVertices"

            props = col.operator("node.add_node", text=" Edges to Face Groups ", icon = "FACEGROUP")
            props.use_transform = True
            props.type = "GeometryNodeEdgesToFaceGroups"

            props = col.operator("node.add_node", text=" Face Area                ", icon = "FACEREGIONS")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshFaceArea"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Face Group Boundaries ", icon = "SELECT_BOUNDARY")
            props.use_transform = True
            props.type = "GeometryNodeMeshFaceSetBoundaries"

            props = col.operator("node.add_node", text=" Face Neighbors        ", icon = "FACE_NEIGHBORS")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshFaceNeighbors"

            if context.space_data.geometry_nodes_type == 'TOOL':
                props = col.operator("node.add_node", text=" Face Set        ", icon = "FACE_SET")
                props.use_transform = True
                props.type = "GeometryNodeToolFaceSet"

            props = col.operator("node.add_node", text=" Is Face Planar         ", icon = "PLANAR")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshFaceIsPlanar"

            props = col.operator("node.add_node", text=" Is Face Smooth     ", icon = "SHADING_SMOOTH")
            props.use_transform = True
            props.type = "GeometryNodeInputShadeSmooth"

            props = col.operator("node.add_node", text=" is Edge Smooth      ", icon = "SHADING_EDGE_SMOOTH")
            props.use_transform = True
            props.type = "GeometryNodeInputEdgeSmooth"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Mesh Island             ", icon = "UV_ISLANDSEL")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshIsland"

            props = col.operator("node.add_node", text = " Shortest Edge Path ", icon = "SELECT_SHORTESTPATH")
            props.use_transform = True
            props.type = "GeometryNodeInputShortestEdgePaths"

            props = col.operator("node.add_node", text=" Vertex Neighbors   ", icon = "VERTEX_NEIGHBORS")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshVertexNeighbors"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "EDGE_ANGLE")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshEdgeAngle"

            props = flow.operator("node.add_node", text="", icon = "EDGE_NEIGHBORS")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshEdgeNeighbors"

            props = flow.operator("node.add_node", text="", icon = "EDGE_VERTICES")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshEdgeVertices"

            props = flow.operator("node.add_node", text="", icon = "FACEGROUP")
            props.use_transform = True
            props.type = "GeometryNodeEdgesToFaceGroups"

            props = flow.operator("node.add_node", text="", icon = "FACEREGIONS")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshFaceArea"

            props = flow.operator("node.add_node", text="", icon = "SELECT_BOUNDARY")
            props.use_transform = True
            props.type = "GeometryNodeMeshFaceSetBoundaries"

            props = flow.operator("node.add_node", text = "", icon = "FACE_NEIGHBORS")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshFaceNeighbors"

            if context.space_data.geometry_nodes_type == 'TOOL':
                props = flow.operator("node.add_node", text="", icon = "FACE_SET")
                props.use_transform = True
                props.type = "GeometryNodeToolFaceSet"

            props = flow.operator("node.add_node", text="", icon = "PLANAR")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshFaceIsPlanar"

            props = flow.operator("node.add_node", text = "", icon = "SHADING_SMOOTH")
            props.use_transform = True
            props.type = "GeometryNodeInputShadeSmooth"

            props = flow.operator("node.add_node", text="", icon = "SHADING_EDGE_SMOOTH")
            props.use_transform = True
            props.type = "GeometryNodeInputEdgeSmooth"

            props = flow.operator("node.add_node", text="", icon = "UV_ISLANDSEL")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshIsland"

            props = flow.operator("node.add_node", text = "", icon = "SELECT_SHORTESTPATH")
            props.use_transform = True
            props.type = "GeometryNodeInputShortestEdgePaths"

            props = flow.operator("node.add_node", text = "", icon = "VERTEX_NEIGHBORS")
            props.use_transform = True
            props.type = "GeometryNodeInputMeshVertexNeighbors"


#add mesh panel, sample subpanel
class NODES_PT_geom_add_mesh_sample(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Sample"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_mesh"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Sample Nearest Surface ", icon = "SAMPLE_NEAREST_SURFACE")
            props.use_transform = True
            props.type = "GeometryNodeSampleNearestSurface"

            props = col.operator("node.add_node", text=" Sample UV Surface   ", icon = "SAMPLE_UV_SURFACE")
            props.use_transform = True
            props.type = "GeometryNodeSampleUVSurface"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text="", icon = "SAMPLE_NEAREST_SURFACE")
            props.use_transform = True
            props.type = "GeometryNodeSampleNearestSurface"

            props = flow.operator("node.add_node", text="", icon = "SAMPLE_UV_SURFACE")
            props.use_transform = True
            props.type = "GeometryNodeSampleUVSurface"


#add mesh panel, write subpanel
class NODES_PT_geom_add_mesh_write(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Write"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_mesh"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            if context.space_data.geometry_nodes_type == 'TOOL':
                props = col.operator("node.add_node", text=" Set Face Set   ", icon = "FACE_SET")
                props.use_transform = True
                props.type = "GeometryNodeToolFaceSet"

            props = col.operator("node.add_node", text=" Set Mesh Normal   ", icon = "SET_SMOOTH")
            props.use_transform = True
            props.type = "GeometryNodeSetMeshNormal"

            props = col.operator("node.add_node", text=" Set Shade Smooth   ", icon = "SET_SHADE_SMOOTH")
            props.use_transform = True
            props.type = "GeometryNodeSetShadeSmooth"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            if context.space_data.geometry_nodes_type == 'TOOL':
                props = flow.operator("node.add_node", text="", icon = "SET_FACE_SET")
                props.use_transform = True
                props.type = "GeometryNodeToolSetFaceSet"

            props = flow.operator("node.add_node", text = "", icon = "SET_SMOOTH")
            props.use_transform = True
            props.type = "GeometryNodeSetMeshNormal"

            props = flow.operator("node.add_node", text = "", icon = "SET_SHADE_SMOOTH")
            props.use_transform = True
            props.type = "GeometryNodeSetShadeSmooth"


#add mesh panel, operations subpanel
class NODES_PT_geom_add_mesh_operations(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Operations"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_mesh"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Dual Mesh               ", icon = "DUAL_MESH")
            props.use_transform = True
            props.type = "GeometryNodeDualMesh"

            props = col.operator("node.add_node", text=" Edge Paths to Curves ", icon = "EDGE_PATHS_TO_CURVES")
            props.use_transform = True
            props.type = "GeometryNodeEdgePathsToCurves"

            props = col.operator("node.add_node", text=" Edge Paths to Selection ", icon = "EDGE_PATH_TO_SELECTION")
            props.use_transform = True
            props.type = "GeometryNodeEdgePathsToSelection"

            props = col.operator("node.add_node", text=" Extrude Mesh             ", icon = "EXTRUDE_REGION")
            props.use_transform = True
            props.type = "GeometryNodeExtrudeMesh"

            props = col.operator("node.add_node", text=" Flip Faces               ", icon = "FLIP_NORMALS")
            props.use_transform = True
            props.type = "GeometryNodeFlipFaces"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Mesh Boolean           ", icon = "MOD_BOOLEAN")
            props.use_transform = True
            props.type = "GeometryNodeMeshBoolean"

            props = col.operator("node.add_node", text=" Mesh to Curve          ", icon = "OUTLINER_OB_CURVE")
            props.use_transform = True
            props.type = "GeometryNodeMeshToCurve"

            props = col.operator("node.add_node", text=" Mesh to Points          ", icon = "MESH_TO_POINTS")
            props.use_transform = True
            props.type = "GeometryNodeMeshToPoints"

            props = col.operator("node.add_node", text=" Mesh to Volume         ", icon = "MESH_TO_VOLUME")
            props.use_transform = True
            props.type = "GeometryNodeMeshToVolume"

            props = col.operator("node.add_node", text=" Scale Elements        ", icon = "TRANSFORM_SCALE")
            props.use_transform = True
            props.type = "GeometryNodeScaleElements"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Split Edges               ", icon = "SPLITEDGE")
            props.use_transform = True
            props.type = "GeometryNodeSplitEdges"

            props = col.operator("node.add_node", text=" Subdivide Mesh        ", icon = "SUBDIVIDE_MESH")
            props.use_transform = True
            props.type = "GeometryNodeSubdivideMesh"

            props = col.operator("node.add_node", text=" Subdivision Surface ", icon = "SUBDIVIDE_EDGES")
            props.use_transform = True
            props.type = "GeometryNodeSubdivisionSurface"

            props = col.operator("node.add_node", text=" Triangulate              ", icon = "MOD_TRIANGULATE")
            props.use_transform = True
            props.type = "GeometryNodeTriangulate"


        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "DUAL_MESH")
            props.use_transform = True
            props.type = "GeometryNodeDualMesh"

            props = flow.operator("node.add_node", text="", icon = "EDGE_PATHS_TO_CURVES")
            props.use_transform = True
            props.type = "GeometryNodeEdgePathsToCurves"

            props = flow.operator("node.add_node", text="", icon = "EDGE_PATH_TO_SELECTION")
            props.use_transform = True
            props.type = "GeometryNodeEdgePathsToSelection"

            props = flow.operator("node.add_node", text = "", icon = "EXTRUDE_REGION")
            props.use_transform = True
            props.type = "GeometryNodeExtrudeMesh"

            props = flow.operator("node.add_node", text = "", icon = "FLIP_NORMALS")
            props.use_transform = True
            props.type = "GeometryNodeFlipFaces"

            props = flow.operator("node.add_node", text = "", icon = "MOD_BOOLEAN")
            props.use_transform = True
            props.type = "GeometryNodeMeshBoolean"

            props = flow.operator("node.add_node", text = "", icon = "OUTLINER_OB_CURVE")
            props.use_transform = True
            props.type = "GeometryNodeMeshToCurve"

            props = flow.operator("node.add_node", text = "", icon = "MESH_TO_POINTS")
            props.use_transform = True
            props.type = "GeometryNodeMeshToPoints"

            props = flow.operator("node.add_node", text="", icon = "MESH_TO_VOLUME")
            props.use_transform = True
            props.type = "GeometryNodeMeshToVolume"

            props = flow.operator("node.add_node", text = "", icon = "TRANSFORM_SCALE")
            props.use_transform = True
            props.type = "GeometryNodeScaleElements"

            props = flow.operator("node.add_node", text = "", icon = "SPLITEDGE")
            props.use_transform = True
            props.type = "GeometryNodeSplitEdges"

            props = flow.operator("node.add_node", text = "", icon = "SUBDIVIDE_MESH")
            props.use_transform = True
            props.type = "GeometryNodeSubdivideMesh"

            props = flow.operator("node.add_node", text = "", icon = "SUBDIVIDE_EDGES")
            props.use_transform = True
            props.type = "GeometryNodeSubdivisionSurface"

            props = flow.operator("node.add_node", text = "", icon = "MOD_TRIANGULATE")
            props.use_transform = True
            props.type = "GeometryNodeTriangulate"


#add mesh panel, primitives subpanel
class NODES_PT_geom_add_mesh_primitives(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Primitives"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_mesh"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Cone                       ", icon = "MESH_CONE")
            props.use_transform = True
            props.type = "GeometryNodeMeshCone"

            props = col.operator("node.add_node", text=" Cube                       ", icon = "MESH_CUBE")
            props.use_transform = True
            props.type = "GeometryNodeMeshCube"

            props = col.operator("node.add_node", text=" Cylinder                   ", icon = "MESH_CYLINDER")
            props.use_transform = True
            props.type = "GeometryNodeMeshCylinder"

            props = col.operator("node.add_node", text=" Grid                         ", icon = "MESH_GRID")
            props.use_transform = True
            props.type = "GeometryNodeMeshGrid"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Ico Sphere               ", icon = "MESH_ICOSPHERE")
            props.use_transform = True
            props.type = "GeometryNodeMeshIcoSphere"

            props = col.operator("node.add_node", text=" Mesh Circle            ", icon = "MESH_CIRCLE")
            props.use_transform = True
            props.type = "GeometryNodeMeshCircle"

            props = col.operator("node.add_node", text=" Mesh Line                 ", icon = "MESH_LINE")
            props.use_transform = True
            props.type = "GeometryNodeMeshLine"

            props = col.operator("node.add_node", text=" UV Sphere                ", icon = "MESH_UVSPHERE")
            props.use_transform = True
            props.type = "GeometryNodeMeshUVSphere"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "MESH_CONE")
            props.use_transform = True
            props.type = "GeometryNodeMeshCone"

            props = flow.operator("node.add_node", text = "", icon = "MESH_CUBE")
            props.use_transform = True
            props.type = "GeometryNodeMeshCube"

            props = flow.operator("node.add_node", text = "", icon = "MESH_CYLINDER")
            props.use_transform = True
            props.type = "GeometryNodeMeshCylinder"

            props = flow.operator("node.add_node", text = "", icon = "MESH_GRID")
            props.use_transform = True
            props.type = "GeometryNodeMeshGrid"

            props = flow.operator("node.add_node", text = "", icon = "MESH_ICOSPHERE")
            props.use_transform = True
            props.type = "GeometryNodeMeshIcoSphere"

            props = flow.operator("node.add_node", text = "", icon = "MESH_CIRCLE")
            props.use_transform = True
            props.type = "GeometryNodeMeshCircle"

            props = flow.operator("node.add_node", text = "", icon = "MESH_LINE")
            props.use_transform = True
            props.type = "GeometryNodeMeshLine"

            props = flow.operator("node.add_node", text = "", icon = "MESH_UVSPHERE")
            props.use_transform = True
            props.type = "GeometryNodeMeshUVSphere"


#add mesh panel, topology subpanel
class NODES_PT_geom_add_mesh_topology(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Topology"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_mesh"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Corners of Edge          ", icon = "CORNERS_OF_EDGE")
            props.use_transform = True
            props.type = "GeometryNodeCornersOfEdge"

            props = col.operator("node.add_node", text=" Corners of Face          ", icon = "CORNERS_OF_FACE")
            props.use_transform = True
            props.type = "GeometryNodeCornersOfFace"

            props = col.operator("node.add_node", text=" Corners of Vertex       ", icon = "CORNERS_OF_VERTEX")
            props.use_transform = True
            props.type = "GeometryNodeCornersOfVertex"

            props = col.operator("node.add_node", text=" Edges of Corner          ", icon = "EDGES_OF_CORNER")
            props.use_transform = True
            props.type = "GeometryNodeEdgesOfCorner"

            col = layout.column(align=True)
            col.scale_y = 1.5


            props = col.operator("node.add_node", text=" Edges of Vertex          ", icon = "EDGES_OF_VERTEX")
            props.use_transform = True
            props.type = "GeometryNodeEdgesOfVertex"

            props = col.operator("node.add_node", text=" Face of Corner             ", icon = "FACE_OF_CORNER")
            props.use_transform = True
            props.type = "GeometryNodeFaceOfCorner"

            props = col.operator("node.add_node", text=" Offset Corner In Face  ", icon = "OFFSET_CORNER_IN_FACE")
            props.use_transform = True
            props.type = "GeometryNodeOffsetCornerInFace"

            props = col.operator("node.add_node", text=" Vertex of Corner          ", icon = "VERTEX_OF_CORNER")
            props.use_transform = True
            props.type = "GeometryNodeVertexOfCorner"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "CORNERS_OF_EDGE")
            props.use_transform = True
            props.type = "GeometryNodeCornersOfEdge"

            props = flow.operator("node.add_node", text = "", icon = "CORNERS_OF_FACE")
            props.use_transform = True
            props.type = "GeometryNodeCornersOfFace"

            props = flow.operator("node.add_node", text = "", icon = "CORNERS_OF_VERTEX")
            props.use_transform = True
            props.type = "GeometryNodeCornersOfVertex"

            props = flow.operator("node.add_node", text = "", icon = "EDGES_OF_CORNER")
            props.use_transform = True
            props.type = "GeometryNodeEdgesOfCorner"

            props = flow.operator("node.add_node", text = "", icon = "EDGES_OF_VERTEX")
            props.use_transform = True
            props.type = "GeometryNodeEdgesOfVertex"

            props = flow.operator("node.add_node", text = "", icon = "FACE_OF_CORNER")
            props.use_transform = True
            props.type = "GeometryNodeFaceOfCorner"

            props = flow.operator("node.add_node", text = "", icon = "OFFSET_CORNER_IN_FACE")
            props.use_transform = True
            props.type = "GeometryNodeOffsetCornerInFace"

            props = flow.operator("node.add_node", text = "", icon = "VERTEX_OF_CORNER")
            props.use_transform = True
            props.type = "GeometryNodeVertexOfCorner"


#add volume panel
class NODES_PT_geom_add_mesh_uv(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "UV"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_mesh"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Pack UV Islands  ", icon = "PACKISLAND")
            props.use_transform = True
            props.type = "GeometryNodeUVPackIslands"

            props = col.operator("node.add_node", text=" UV Unwrap      ", icon = "UNWRAP_ABF")
            props.use_transform = True
            props.type = "GeometryNodeUVUnwrap"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text="", icon = "VOLUME_CUBE")
            props.use_transform = True
            props.type = "GeometryNodeUVPackIslands"

            props = flow.operator("node.add_node", text="", icon = "VOLUME_TO_MESH")
            props.use_transform = True
            props.type = "GeometryNodeUVUnwrap"


#add mesh panel
class NODES_PT_geom_add_point(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Point"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Distribute Points in Volume  ", icon = "VOLUME_DISTRIBUTE")
            props.use_transform = True
            props.type = "GeometryNodeDistributePointsInVolume"

            props = col.operator("node.add_node", text=" Distribute Points on Faces  ", icon = "POINT_DISTRIBUTE")
            props.use_transform = True
            props.type = "GeometryNodeDistributePointsOnFaces"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Points                          ", icon = "DECORATE")
            props.use_transform = True
            props.type = "GeometryNodePoints"

            props = col.operator("node.add_node", text=" Points to Curves          ", icon = "POINTS_TO_CURVES")
            props.use_transform = True
            props.type = "GeometryNodePointsToCurves"

            props = col.operator("node.add_node", text=" Points to Vertices         ", icon = "POINTS_TO_VERTICES")
            props.use_transform = True
            props.type = "GeometryNodePointsToVertices"

            props = col.operator("node.add_node", text=" Points to Volume         ", icon = "POINT_TO_VOLUME")
            props.use_transform = True
            props.type = "GeometryNodePointsToVolume"

            props = col.operator("node.add_node", text=" Set Point Radius          ", icon = "SET_CURVE_RADIUS")
            props.use_transform = True
            props.type = "GeometryNodeSetPointRadius"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text="", icon = "VOLUME_DISTRIBUTE")
            props.use_transform = True
            props.type = "GeometryNodeDistributePointsInVolume"

            props = flow.operator("node.add_node", text = "", icon = "POINT_DISTRIBUTE")
            props.use_transform = True
            props.type = "GeometryNodeDistributePointsOnFaces"

            props = flow.operator("node.add_node", text="", icon = "DECORATE")
            props.use_transform = True
            props.type = "GeometryNodePoints"

            props = flow.operator("node.add_node", text="", icon = "POINTS_TO_CURVES")
            props.use_transform = True
            props.type = "GeometryNodePointsToCurves"

            props = flow.operator("node.add_node", text = "", icon = "POINTS_TO_VERTICES")
            props.use_transform = True
            props.type = "GeometryNodePointsToVertices"

            props = flow.operator("node.add_node", text = "", icon = "POINT_TO_VOLUME")
            props.use_transform = True
            props.type = "GeometryNodePointsToVolume"

            props = flow.operator("node.add_node", text = "", icon = "SET_CURVE_RADIUS")
            props.use_transform = True
            props.type = "GeometryNodeSetPointRadius"


#add volume panel
class NODES_PT_geom_add_volume(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Volume"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Volume Cube       ", icon = "VOLUME_CUBE")
            props.use_transform = True
            props.type = "GeometryNodeVolumeCube"

            props = col.operator("node.add_node", text=" Volume to Mesh       ", icon = "VOLUME_TO_MESH")
            props.use_transform = True
            props.type = "GeometryNodeVolumeToMesh"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text="", icon = "VOLUME_CUBE")
            props.use_transform = True
            props.type = "GeometryNodeVolumeCube"

            props = flow.operator("node.add_node", text="", icon = "VOLUME_TO_MESH")
            props.use_transform = True
            props.type = "GeometryNodeVolumeToMesh"

#add simulation panel
class NODES_PT_geom_add_simulation(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Simulation"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_simulation_zone", text=" Simulation Zone       ", icon = "TIME")
            props.use_transform = True
            #props.type = "GeometryNodeVolumeCube"


        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_simulation_zone", text="", icon = "TIME")
            props.use_transform = True
            #props.type = "GeometryNodeVolumeCube"


#add material panel
class NODES_PT_geom_add_material(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Material"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Replace Material      ", icon = "MATERIAL_REPLACE")
            props.use_transform = True
            props.type = "GeometryNodeReplaceMaterial"

            props = col.operator("node.add_node", text=" Material Index           ", icon = "MATERIAL_INDEX")
            props.use_transform = True
            props.type = "GeometryNodeInputMaterialIndex"

            props = col.operator("node.add_node", text=" Material Selection    ", icon = "SELECT_BY_MATERIAL")
            props.use_transform = True
            props.type = "GeometryNodeMaterialSelection"

            props = col.operator("node.add_node", text=" Set Material              ", icon = "MATERIAL_ADD")
            props.use_transform = True
            props.type = "GeometryNodeSetMaterial"

            props = col.operator("node.add_node", text=" Set Material Index   ", icon = "SET_MATERIAL_INDEX")
            props.use_transform = True
            props.type = "GeometryNodeSetMaterialIndex"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "MATERIAL_REPLACE")
            props.use_transform = True
            props.type = "GeometryNodeReplaceMaterial"

            props = flow.operator("node.add_node", text = "", icon = "MATERIAL_INDEX")
            props.use_transform = True
            props.type = "GeometryNodeInputMaterialIndex"

            props = flow.operator("node.add_node", text = "", icon = "SELECT_BY_MATERIAL")
            props.use_transform = True
            props.type = "GeometryNodeMaterialSelection"

            props = flow.operator("node.add_node", text = "", icon = "MATERIAL_ADD")
            props.use_transform = True
            props.type = "GeometryNodeSetMaterial"

            props = flow.operator("node.add_node", text = "", icon = "SET_MATERIAL_INDEX")
            props.use_transform = True
            props.type = "GeometryNodeSetMaterialIndex"


#add vector panel
class NODES_PT_geom_add_texture(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Texture"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Brick Texture        ", icon = "NODE_BRICK")
            props.use_transform = True
            props.type = "ShaderNodeTexBrick"

            props = col.operator("node.add_node", text=" Checker Texture   ", icon = "NODE_CHECKER")
            props.use_transform = True
            props.type = "ShaderNodeTexChecker"

            props = col.operator("node.add_node", text=" Gradient Texture  ", icon = "NODE_GRADIENT")
            props.use_transform = True
            props.type = "ShaderNodeTexGradient"

            props = col.operator("node.add_node", text=" Image Texture      ", icon = "FILE_IMAGE")
            props.use_transform = True
            props.type = "GeometryNodeImageTexture"

            props = col.operator("node.add_node", text=" Magic Texture       ", icon = "MAGIC_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexMagic"

            props = col.operator("node.add_node", text=" Noise Texture        ", icon = "NOISE_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexNoise"

            props = col.operator("node.add_node", text=" Voronoi Texture     ", icon = "VORONI_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexVoronoi"

            props = col.operator("node.add_node", text=" Wave Texture         ", icon = "NODE_WAVES")
            props.use_transform = True
            props.type = "ShaderNodeTexWave"

            props = col.operator("node.add_node", text=" White Noise            ", icon = "NODE_WHITE_NOISE")
            props.use_transform = True
            props.type = "ShaderNodeTexWhiteNoise"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_BRICK")
            props.use_transform = True
            props.type = "ShaderNodeTexBrick"

            props = flow.operator("node.add_node", text = "", icon = "NODE_CHECKER")
            props.use_transform = True
            props.type = "ShaderNodeTexChecker"

            props = flow.operator("node.add_node", text = "", icon = "NODE_GRADIENT")
            props.use_transform = True
            props.type = "ShaderNodeTexGradient"

            props = flow.operator("node.add_node", text = "", icon = "FILE_IMAGE")
            props.use_transform = True
            props.type = "GeometryNodeImageTexture"

            props = flow.operator("node.add_node", text = "", icon = "MAGIC_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexMagic"

            props = flow.operator("node.add_node", text = "", icon = "NOISE_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexNoise"

            props = flow.operator("node.add_node", text = "", icon = "VORONI_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexVoronoi"

            props = flow.operator("node.add_node", text = "", icon = "NODE_WAVES")
            props.use_transform = True
            props.type = "ShaderNodeTexWave"

            props = flow.operator("node.add_node", text = "", icon = "NODE_WHITE_NOISE")
            props.use_transform = True
            props.type = "ShaderNodeTexWhiteNoise"


#add utilities panel
class NODES_PT_geom_add_utilities(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Utilities"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_foreach_geometry_element_zone", text=" For Each Element    ", icon = "FOR_EACH")
            props.use_transform = True
            #props.type = ""

            props = col.operator("node.add_node", text=" Index Switch    ", icon = "INDEX_SWITCH")
            props.use_transform = True
            props.type = "GeometryNodeIndexSwitch"

            props = col.operator("node.add_node", text=" Menu Switch    ", icon = "MENU_SWITCH")
            props.use_transform = True
            props.type = "GeometryNodeMenuSwitch"

            props = col.operator("node.add_node", text=" Random Value  ", icon = "RANDOM_FLOAT")
            props.use_transform = True
            props.type = "FunctionNodeRandomValue"

            props = col.operator("node.add_repeat_zone", text=" Repeat Zone      ", icon = "REPEAT")
            props.use_transform = True
            #props.type = ""

            props = col.operator("node.add_node", text=" Switch               ", icon = "SWITCH")
            props.use_transform = True
            props.type = "GeometryNodeSwitch"



        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "INDEX_SWITCH")
            props.use_transform = True
            props.type = "GeometryNodeIndexSwitch"

            props = flow.operator("node.add_node", text = "", icon = "MENU_SWITCH")
            props.use_transform = True
            props.type = "GeometryNodeMenuSwitch"

            props = flow.operator("node.add_node", text = "", icon = "RANDOM_FLOAT")
            props.use_transform = True
            props.type = "FunctionNodeRandomValue"

            props = flow.operator("node.add_repeat_zone", text="", icon = "REPEAT")
            props.use_transform = True
            #props.type = ""

            props = flow.operator("node.add_node", text = "", icon = "SWITCH")
            props.use_transform = True
            props.type = "GeometryNodeSwitch"




#add utilities panel, color subpanel
class NODES_PT_geom_add_utilities_color(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Color"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_utilities"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" ColorRamp           ", icon = "NODE_COLORRAMP")
            props.use_transform = True
            props.type = "ShaderNodeValToRGB"

            props = col.operator("node.add_node", text=" RGB Curves          ", icon = "NODE_RGBCURVE")
            props.use_transform = True
            props.type = "ShaderNodeRGBCurve"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Combine Color      ", icon = "COMBINE_COLOR")
            props.use_transform = True
            props.type = "FunctionNodeCombineColor"


            props = col.operator("node.add_node", text=" Separate Color      ", icon = "SEPARATE_COLOR")
            props.use_transform = True
            props.type = "FunctionNodeSeparateColor"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_COLORRAMP")
            props.use_transform = True
            props.type = "ShaderNodeValToRGB"

            props = flow.operator("node.add_node", text = "", icon = "NODE_RGBCURVE")
            props.use_transform = True
            props.type = "ShaderNodeRGBCurve"

            props = flow.operator("node.add_node", text = "", icon = "COMBINE_COLOR")
            props.use_transform = True
            props.type = "FunctionNodeCombineColor"

            props = flow.operator("node.add_node", text="", icon = "NODE_MIX")
            props.use_transform = True
            props.type = "ShaderNodeMix"
            ops = props.settings.add()
            ops.name = "data_type"
            ops.value = "'RGBA'"
            #props.settings = [{"name":"data_type", "value":"'RGBA'"}] # halp :(

            props = flow.operator("node.add_node", text = "", icon = "SEPARATE_COLOR")
            props.use_transform = True
            props.type = "FunctionNodeSeparateColor"


#add utilities panel, text subpanel
class NODES_PT_geom_add_utilities_text(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Text"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_utilities"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Format String            ", icon = "FORMAT_STRING")
            props.use_transform = True
            props.type = "FunctionNodeFormatString"

            props = col.operator("node.add_node", text=" Join Strings             ", icon = "STRING_JOIN")
            props.use_transform = True
            props.type = "GeometryNodeStringJoin"

            props = col.operator("node.add_node", text=" Match String            ", icon = "MATCH_STRING")
            props.use_transform = True
            props.type = "FunctionNodeMatchString"

            props = col.operator("node.add_node", text=" Replace Strings       ", icon = "REPLACE_STRING")
            props.use_transform = True
            props.type = "FunctionNodeReplaceString"

            props = col.operator("node.add_node", text=" Slice Strings            ", icon = "STRING_SUBSTRING")
            props.use_transform = True
            props.type = "FunctionNodeSliceString"

            props = col.operator("node.add_node", text=" String Length           ", icon = "STRING_LENGTH")
            props.use_transform = True
            props.type = "FunctionNodeStringLength"

            props = col.operator("node.add_node", text=" Find in String           ", icon = "STRING_FIND")
            props.use_transform = True
            props.type = "FunctionNodeFindInString"

            props = col.operator("node.add_node", text=" String to Curves       ", icon = "STRING_TO_CURVE")
            props.use_transform = True
            props.type = "GeometryNodeStringToCurves"

            props = col.operator("node.add_node", text=" Value to String         ", icon = "VALUE_TO_STRING")
            props.use_transform = True
            props.type = "FunctionNodeValueToString"

            props = col.operator("node.add_node", text=" Special Characters  ", icon = "SPECIAL")
            props.use_transform = True
            props.type = "FunctionNodeInputSpecialCharacters"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text="", icon = "FORMAT_STRING")
            props.use_transform = True
            props.type = "FunctionNodeFormatString"

            props = flow.operator("node.add_node", text="", icon = "STRING_JOIN")
            props.use_transform = True
            props.type = "GeometryNodeStringJoin"

            props = flow.operator("node.add_node", text="", icon = "MATCH_STRING")
            props.use_transform = True
            props.type = "FunctionNodeMatchString"

            props = flow.operator("node.add_node", text="", icon = "REPLACE_STRING")
            props.use_transform = True
            props.type = "FunctionNodeReplaceString"

            props = flow.operator("node.add_node", text="", icon = "STRING_SUBSTRING")
            props.use_transform = True
            props.type = "FunctionNodeSliceString"

            props = flow.operator("node.add_node", text = "", icon = "STRING_LENGTH")
            props.use_transform = True
            props.type = "FunctionNodeStringLength"

            props = flow.operator("node.add_node", text="", icon = "STRING_FIND")
            props.use_transform = True
            props.type = "FunctionNodeFindInString"

            props = flow.operator("node.add_node", text = "", icon = "STRING_TO_CURVE")
            props.use_transform = True
            props.type = "GeometryNodeStringToCurves"

            props = flow.operator("node.add_node", text="", icon = "VALUE_TO_STRING")
            props.use_transform = True
            props.type = "FunctionNodeValueToString"

            props = flow.operator("node.add_node", text = "", icon = "SPECIAL")
            props.use_transform = True
            props.type = "FunctionNodeInputSpecialCharacters"


#add utilities panel, vector subpanel
class NODES_PT_geom_add_utilities_vector(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Vector"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_utilities"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Vector Curves  ", icon = "NODE_VECTOR")
            props.use_transform = True
            props.type = "ShaderNodeVectorCurve"

            props = col.operator("node.add_node", text=" Vector Math      ", icon = "NODE_VECTORMATH")
            props.use_transform = True
            props.type = "ShaderNodeVectorMath"

            props = col.operator("node.add_node", text=" Vector Rotate    ", icon = "NODE_VECTORROTATE")
            props.use_transform = True
            props.type = "ShaderNodeVectorRotate"

            props = col.operator("node.add_node", text=" Combine XYZ   ", icon = "NODE_COMBINEXYZ")
            props.use_transform = True
            props.type = "ShaderNodeCombineXYZ"

            props = col.operator("node.add_node", text=" Mix Vector       ", icon = "NODE_MIX")
            props.use_transform = True
            props.type = "ShaderNodeMix"
            ops = props.settings.add()
            ops.name = "data_type"
            ops.value = "'VECTOR'"

            props = col.operator("node.add_node", text=" Separate XYZ   ", icon = "NODE_SEPARATEXYZ")
            props.use_transform = True
            props.type = "ShaderNodeSeparateXYZ"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_VECTOR")
            props.use_transform = True
            props.type = "ShaderNodeVectorCurve"

            props = flow.operator("node.add_node", text = "", icon = "NODE_VECTORMATH")
            props.use_transform = True
            props.type = "ShaderNodeVectorMath"

            props = flow.operator("node.add_node", text = "", icon = "NODE_VECTORROTATE")
            props.use_transform = True
            props.type = "ShaderNodeVectorRotate"

            props = flow.operator("node.add_node", text = "", icon = "NODE_COMBINEXYZ")
            props.use_transform = True
            props.type = "ShaderNodeCombineXYZ"

            props = flow.operator("node.add_node", text = "", icon = "NODE_MIX")
            props.use_transform = True
            props.type = "ShaderNodeMix"
            ops = props.settings.add()
            ops.name = "data_type"
            ops.value = "'VECTOR'"

            props = flow.operator("node.add_node", text = "", icon = "NODE_SEPARATEXYZ")
            props.use_transform = True
            props.type = "ShaderNodeSeparateXYZ"


#add utilities panel, field subpanel
class NODES_PT_geom_add_utilities_field(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Field"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_utilities"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Accumulate Field  ", icon = "ACCUMULATE")
            props.use_transform = True
            props.type = "GeometryNodeAccumulateField"

            props = col.operator("node.add_node", text=" Evaluate at Index ", icon = "FIELD_AT_INDEX")
            props.use_transform = True
            props.type = "GeometryNodeFieldAtIndex"

            props = col.operator("node.add_node", text=" Evaluate On Domain ", icon = "FIELD_DOMAIN")
            props.use_transform = True
            props.type = "GeometryNodeFieldOnDomain"

            props = col.operator("node.add_node", text="Field Average        ", icon = "AVERAGE")
            props.use_transform = True
            props.type = "GeometryNodeFieldAverage"

            props = col.operator("node.add_node", text=" Field Min & Max     ", icon = "MINMAX")
            props.use_transform = True
            props.type = "GeometryNodeFieldMinAndMax"

            props = col.operator("node.add_node", text=" Field Variance        ", icon = "VARIANCE")
            props.use_transform = True
            props.type = "GeometryNodeFieldVariance"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "ACCUMULATE")
            props.use_transform = True
            props.type = "GeometryNodeAccumulateField"

            props = flow.operator("node.add_node", text = "", icon = "FIELD_AT_INDEX")
            props.use_transform = True
            props.type = "GeometryNodeFieldAtIndex"

            props = flow.operator("node.add_node", text="", icon = "FIELD_DOMAIN")
            props.use_transform = True
            props.type = "GeometryNodeFieldOnDomain"

            props = flow.operator("node.add_node", text = "", icon = "AVERAGE")
            props.use_transform = True
            props.type = "GeometryNodeFieldAverage"

            props = flow.operator("node.add_node", text = "", icon = "MINMAX")
            props.use_transform = True
            props.type = "GeometryNodeFieldMinAndMax"

            props = flow.operator("node.add_node", text="", icon = "VARIANCE")
            props.use_transform = True
            props.type = "GeometryNodeFieldVariance"


#add utilities panel, math subpanel
class NODES_PT_geom_add_utilities_math(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Math"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_utilities"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Bit Math          ", icon = "BITMATH")
            props.use_transform = True
            props.type = "FunctionNodeBitMath"

            props = col.operator("node.add_node", text=" Boolean Math  ", icon = "BOOLEAN_MATH")
            props.use_transform = True
            props.type = "FunctionNodeBooleanMath"

            props = col.operator("node.add_node", text=" Integer Math  ", icon = "INTEGER_MATH")
            props.use_transform = True
            props.type = "FunctionNodeIntegerMath"

            props = col.operator("node.add_node", text=" Clamp              ", icon = "NODE_CLAMP")
            props.use_transform = True
            props.type = "ShaderNodeClamp"

            props = col.operator("node.add_node", text=" Compare          ", icon = "FLOAT_COMPARE")
            props.use_transform = True
            props.type = "FunctionNodeCompare"

            props = col.operator("node.add_node", text=" Float Curve      ", icon = "FLOAT_CURVE")
            props.use_transform = True
            props.type = "ShaderNodeFloatCurve"

            col = layout.column(align=True)
            col.scale_y = 1.5


            props = col.operator("node.add_node", text=" Float to Integer ", icon = "FLOAT_TO_INT")
            props.use_transform = True
            props.type = "FunctionNodeFloatToInt"

            props = col.operator("node.add_node", text=" Hash Value      ", icon = "HASH")
            props.use_transform = True
            props.type = "FunctionNodeHashValue"

            props = col.operator("node.add_node", text=" Map Range       ", icon = "NODE_MAP_RANGE")
            props.use_transform = True
            props.type = "ShaderNodeMapRange"

            props = col.operator("node.add_node", text=" Math                 ", icon = "NODE_MATH")
            props.use_transform = True
            props.type = "ShaderNodeMath"

            props = col.operator("node.add_node", text=" Mix                   ", icon = "NODE_MIXSHADER")
            props.use_transform = True
            props.type = "ShaderNodeMix"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "BITMATH")
            props.use_transform = True
            props.type = "FunctionNodeBitMath"

            props = flow.operator("node.add_node", text = "", icon = "BOOLEAN_MATH")
            props.use_transform = True
            props.type = "FunctionNodeBooleanMath"

            props = flow.operator("node.add_node", text="", icon = "INTEGER_MATH")
            props.use_transform = True
            props.type = "FunctionNodeIntegerMath"

            props = flow.operator("node.add_node", text="", icon = "NODE_CLAMP")
            props.use_transform = True
            props.type = "ShaderNodeClamp"

            props = flow.operator("node.add_node", text = "", icon = "FLOAT_COMPARE")
            props.use_transform = True
            props.type = "FunctionNodeCompare"

            props = flow.operator("node.add_node", text = "", icon = "FLOAT_CURVE")
            props.use_transform = True
            props.type = "ShaderNodeFloatCurve"

            props = flow.operator("node.add_node", text="", icon = "FLOAT_TO_INT")
            props.use_transform = True
            props.type = "FunctionNodeFloatToInt"

            props = flow.operator("node.add_node", text="", icon = "HASH")
            props.use_transform = True
            props.type = "FunctionNodeHashValue"

            props = flow.operator("node.add_node", text="", icon = "NODE_MAP_RANGE")
            props.use_transform = True
            props.type = "ShaderNodeMapRange"

            props = flow.operator("node.add_node", text = "", icon = "NODE_MATH")
            props.use_transform = True
            props.type = "ShaderNodeMath"

            props = flow.operator("node.add_node", text="", icon = "NODE_MIXSHADER")
            props.use_transform = True
            props.type = "ShaderNodeMix"


#add utilities panel, matrix subpanel
class NODES_PT_geom_add_utilities_matrix(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Matrix"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_utilities"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Combine Matrix     ", icon = "COMBINE_MATRIX")
            props.use_transform = True
            props.type = "FunctionNodeCombineMatrix"

            props = col.operator("node.add_node", text=" Combine Transform     ", icon = "COMBINE_TRANSFORM")
            props.use_transform = True
            props.type = "FunctionNodeCombineTransform"

            props = col.operator("node.add_node", text=" Matrix Determinant     ", icon = "MATRIX_DETERMINANT")
            props.use_transform = True
            props.type = "FunctionNodeMatrixDeterminant"

            props = col.operator("node.add_node", text=" Invert Matrix", icon = "INVERT_MATRIX")
            props.use_transform = True
            props.type = "FunctionNodeInvertMatrix"

            props = col.operator("node.add_node", text=" Multiply Matrix ", icon = "MULTIPLY_MATRIX")
            props.use_transform = True
            props.type = "FunctionNodeMatrixMultiply"

            props = col.operator("node.add_node", text=" Project Point   ", icon = "PROJECT_POINT")
            props.use_transform = True
            props.type = "FunctionNodeProjectPoint"

            props = col.operator("node.add_node", text=" Separate Matrix   ", icon = "SEPARATE_MATRIX")
            props.use_transform = True
            props.type = "FunctionNodeSeparateMatrix"

            props = col.operator("node.add_node", text=" Separate Transform   ", icon = "SEPARATE_TRANSFORM")
            props.use_transform = True
            props.type = "FunctionNodeSeparateTransform"

            props = col.operator("node.add_node", text=" Transform Direction  ", icon = "TRANSFORM_DIRECTION")
            props.use_transform = True
            props.type = "FunctionNodeTransformDirection"

            props = col.operator("node.add_node", text=" Transform Point  ", icon = "TRANSFORM_POINT")
            props.use_transform = True
            props.type = "FunctionNodeTransformPoint"

            props = col.operator("node.add_node", text=" Transpose Matrix ", icon = "TRANSPOSE_MATRIX")
            props.use_transform = True
            props.type = "FunctionNodeTransposeMatrix"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text="", icon = "COMBINE_MATRIX")
            props.use_transform = True
            props.type = "FunctionNodeCombineMatrix"

            props = flow.operator("node.add_node", text="", icon = "COMBINE_TRANSFORM")
            props.use_transform = True
            props.type = "FunctionNodeCombineTransform"

            props = flow.operator("node.add_node", text="", icon = "MATRIX_DETERMINANT")
            props.use_transform = True
            props.type = "FunctionNodeMatrixDeterminant"

            props = flow.operator("node.add_node", text="", icon = "INVERT_MATRIX")
            props.use_transform = True
            props.type = "FunctionNodeInvertMatrix"

            props = flow.operator("node.add_node", text="", icon = "MULTIPLY_MATRIX")
            props.use_transform = True
            props.type = "FunctionNodeMatrixMultiply"

            props = flow.operator("node.add_node", text="", icon = "PROJECT_POINT")
            props.use_transform = True
            props.type = "FunctionNodeProjectPoint"

            props = flow.operator("node.add_node", text="", icon = "SEPARATE_MATRIX")
            props.use_transform = True
            props.type = "FunctionNodeSeparateMatrix"

            props = flow.operator("node.add_node", text="", icon = "SEPARATE_TRANSFORM")
            props.use_transform = True
            props.type = "FunctionNodeSeparateTransform"

            props = flow.operator("node.add_node", text="", icon = "TRANSFORM_DIRECTION")
            props.use_transform = True
            props.type = "FunctionNodeTransformDirection"

            props = flow.operator("node.add_node", text="", icon = "TRANSFORM_POINT")
            props.use_transform = True
            props.type = "FunctionNodeTransformPoint"

            props = flow.operator("node.add_node", text="", icon = "TRANSPOSE_MATRIX")
            props.use_transform = True
            props.type = "FunctionNodeTransposeMatrix"


#add utilities panel, rotation subpanel
class NODES_PT_geom_add_utilities_rotation(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Rotation"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_utilities"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Align Rotation to Vector", icon = "ALIGN_ROTATION_TO_VECTOR")
            props.use_transform = True
            props.type = "FunctionNodeAlignRotationToVector"

            props = col.operator("node.add_node", text=" Axes to Rotation ", icon = "AXES_TO_ROTATION")
            props.use_transform = True
            props.type = "FunctionNodeAxesToRotation"

            props = col.operator("node.add_node", text=" Axis Angle to Rotation", icon = "AXIS_ANGLE_TO_ROTATION")
            props.use_transform = True
            props.type = "FunctionNodeAxisAngleToRotation"

            props = col.operator("node.add_node", text=" Euler to Rotation ", icon = "EULER_TO_ROTATION")
            props.use_transform = True
            props.type = "FunctionNodeEulerToRotation"

            props = col.operator("node.add_node", text=" Invert Rotation    ", icon = "INVERT_ROTATION")
            props.use_transform = True
            props.type = "FunctionNodeInvertRotation"

            props = col.operator("node.add_node", text=" Rotate Rotation         ", icon = "ROTATE_EULER")
            props.use_transform = True
            props.type = "FunctionNodeRotateRotation"



            props = col.operator("node.add_node", text=" Rotate Vector      ", icon = "NODE_VECTORROTATE")
            props.use_transform = True
            props.type = "FunctionNodeRotateVector"

            props = col.operator("node.add_node", text=" Rotation to Axis Angle", icon = "ROTATION_TO_AXIS_ANGLE")
            props.use_transform = True
            props.type = "FunctionNodeRotationToAxisAngle"

            props = col.operator("node.add_node", text=" Rotation to Euler  ", icon = "ROTATION_TO_EULER")
            props.use_transform = True
            props.type = "FunctionNodeRotationToEuler"

            props = col.operator("node.add_node", text=" Rotation to Quaternion ", icon = "ROTATION_TO_QUATERNION")
            props.use_transform = True
            props.type = "FunctionNodeRotationToQuaternion"

            props = col.operator("node.add_node", text=" Quaternion to Rotation ", icon = "QUATERNION_TO_ROTATION")
            props.use_transform = True
            props.type = "FunctionNodeQuaternionToRotation"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text="", icon = "ALIGN_ROTATION_TO_VECTOR")
            props.use_transform = True
            props.type = "FunctionNodeAlignRotationToVector"

            props = flow.operator("node.add_node", text="", icon = "AXES_TO_ROTATION")
            props.use_transform = True
            props.type = "FunctionNodeAxesToRotation"

            props = flow.operator("node.add_node", text="", icon = "AXIS_ANGLE_TO_ROTATION")
            props.use_transform = True
            props.type = "FunctionNodeAxisAngleToRotation"

            props = flow.operator("node.add_node", text="", icon = "EULER_TO_ROTATION")
            props.use_transform = True
            props.type = "FunctionNodeEulerToRotation"

            props = flow.operator("node.add_node", text="", icon = "INVERT_ROTATION")
            props.use_transform = True
            props.type = "FunctionNodeInvertRotation"

            props = flow.operator("node.add_node", text="", icon = "ROTATE_EULER")
            props.use_transform = True
            props.type = "FunctionNodeRotateRotation"

            props = flow.operator("node.add_node", text="", icon = "NODE_VECTORROTATE")
            props.use_transform = True
            props.type = "FunctionNodeRotateVector"

            props = flow.operator("node.add_node", text="", icon = "ROTATION_TO_AXIS_ANGLE")
            props.use_transform = True
            props.type = "FunctionNodeRotationToAxisAngle"

            props = flow.operator("node.add_node", text="", icon = "ROTATION_TO_EULER")
            props.use_transform = True
            props.type = "FunctionNodeRotationToEuler"

            props = flow.operator("node.add_node", text="", icon = "ROTATION_TO_QUATERNION")
            props.use_transform = True
            props.type = "FunctionNodeRotationToQuaternion"

            props = flow.operator("node.add_node", text="", icon = "QUATERNION_TO_ROTATION")
            props.use_transform = True
            props.type = "FunctionNodeQuaternionToRotation"


#add utilities panel, deprecated subpanel
class NODES_PT_geom_add_utilities_deprecated(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Deprecated"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "NODES_PT_geom_add_utilities"

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'GeometryNodeTree') # Just in geometry node editor

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Align Euler to Vector", icon = "ALIGN_EULER_TO_VECTOR")
            props.use_transform = True
            props.type = "FunctionNodeAlignEulerToVector"

            props = col.operator("node.add_node", text=" Rotate Euler (Depreacated)        ", icon = "ROTATE_EULER")
            props.use_transform = True
            props.type = "FunctionNodeRotateEuler"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "ALIGN_EULER_TO_VECTOR")
            props.use_transform = True
            props.type = "FunctionNodeAlignEulerToVector"

            props = flow.operator("node.add_node", text = "", icon = "ROTATE_EULER")
            props.use_transform = True
            props.type = "FunctionNodeRotateEuler"


# ---------------- shader editor common. This content shows when you activate the common switch in the display panel.

# Shader editor, Input panel
class NODES_PT_shader_add_input_common(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Input"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"

    @classmethod
    def poll(cls, context):

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        return addon_prefs.Node_shader_add_common == True and context.space_data.tree_type == 'ShaderNodeTree' # Just in shader mode

    @staticmethod
    def draw(self, context):
        layout = self.layout#### Textbuttons
        default_context = bpy.app.translations.contexts.default

        scene = context.scene

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        ##### Textbuttons

        if not addon_prefs.Node_text_or_icon:

        ##### --------------------------------- Textures common ------------------------------------------- ####

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Fresnel              ", icon = "NODE_FRESNEL")
            props.use_transform = True
            props.type = "ShaderNodeFresnel"

            props = col.operator("node.add_node", text=" Geometry        ", icon = "NODE_GEOMETRY")
            props.use_transform = True
            props.type = "ShaderNodeNewGeometry"

            props = col.operator("node.add_node", text=" RGB                 ", icon = "NODE_RGB")
            props.use_transform = True
            props.type = "ShaderNodeRGB"

            props = col.operator("node.add_node", text = "Texture Coordinate   ", icon = "NODE_TEXCOORDINATE")
            props.use_transform = True
            props.type = "ShaderNodeTexCoord"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_FRESNEL")
            props.use_transform = True
            props.type = "ShaderNodeFresnel"

            props = flow.operator("node.add_node", text = "", icon = "NODE_GEOMETRY")
            props.use_transform = True
            props.type = "ShaderNodeNewGeometry"

            props = flow.operator("node.add_node", text = "", icon = "NODE_RGB")
            props.use_transform = True
            props.type = "ShaderNodeRGB"

            props = flow.operator("node.add_node", text = "", icon = "NODE_TEXCOORDINATE")
            props.use_transform = True
            props.type = "ShaderNodeTexCoord"


#Shader editor , Output panel
class NODES_PT_shader_add_output_common(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Output"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences
        return addon_prefs.Node_shader_add_common == True and context.space_data.tree_type == 'ShaderNodeTree' # Just in shader mode

    @staticmethod
    def draw(self, context):
        layout = self.layout#### Textbuttons
        default_context = bpy.app.translations.contexts.default

        scene = context.scene

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        engine = context.engine

        ##### Textbuttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            if context.space_data.shader_type == 'OBJECT':

                props = col.operator("node.add_node", text=" Material Output", icon = "NODE_MATERIAL")
                props.use_transform = True
                props.type = "ShaderNodeOutputMaterial"

            elif context.space_data.shader_type == 'WORLD':

                props = col.operator("node.add_node", text=" World Output    ", icon = "WORLD")
                props.use_transform = True
                props.type = "ShaderNodeOutputWorld"

            elif context.space_data.shader_type == 'LINESTYLE':

                props = col.operator("node.add_node", text=" Line Style Output", icon = "NODE_LINESTYLE_OUTPUT")
                props.use_transform = True
                props.type = "ShaderNodeOutputLineStyle"

        #### Image Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            if context.space_data.shader_type == 'OBJECT':

                props = flow.operator("node.add_node", text="", icon = "NODE_MATERIAL")
                props.use_transform = True
                props.type = "ShaderNodeOutputMaterial"

            elif context.space_data.shader_type == 'WORLD':

                props = flow.operator("node.add_node", text="", icon = "WORLD")
                props.use_transform = True
                props.type = "ShaderNodeOutputWorld"

            elif context.space_data.shader_type == 'LINESTYLE':

                props = flow.operator("node.add_node", text="", icon = "NODE_LINESTYLE_OUTPUT")
                props.use_transform = True
                props.type = "ShaderNodeOutputLineStyle"


#Shader Editor - Shader panel
class NODES_PT_shader_add_shader_common(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Shader"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        return addon_prefs.Node_shader_add_common == True and (context.space_data.tree_type == 'ShaderNodeTree' and context.space_data.shader_type in ( 'OBJECT', 'WORLD')) # Just in shader mode, Just in Object and World

    @staticmethod
    def draw(self, context):
        layout = self.layout#### Textbuttons
        default_context = bpy.app.translations.contexts.default

        scene = context.scene
        engine = context.engine

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        #### Text Buttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Add                   ", icon = "NODE_ADD_SHADER")
            props.use_transform = True
            props.type = "ShaderNodeAddShader"

            if context.space_data.shader_type == 'OBJECT':

                if engine == 'CYCLES':

                    props = col.operator("node.add_node", text=" Hair BSDF          ", icon = "CURVES")
                    props.use_transform = True
                    props.type = "ShaderNodeBsdfHairPrincipled"

                props = col.operator("node.add_node", text=" Mix Shader        ", icon = "NODE_MIXSHADER")
                props.use_transform = True
                props.type = "ShaderNodeMixShader"

                props = col.operator("node.add_node", text=" Principled BSDF", icon = "NODE_PRINCIPLED")
                props.use_transform = True
                props.type = "ShaderNodeBsdfPrincipled"

                col = layout.column(align=True)
                col.scale_y = 1.5

                props = col.operator("node.add_node", text=" Principled Volume", icon = "NODE_VOLUMEPRINCIPLED")
                props.use_transform = True
                props.type = "ShaderNodeVolumePrincipled"

                if engine == 'CYCLES':

                    props = col.operator("node.add_node", text=" Toon BSDF           ", icon = "NODE_TOONSHADER")
                    props.use_transform = True
                    props.type = "ShaderNodeBsdfToon"

                col = layout.column(align=True)
                col.scale_y = 1.5


                props = col.operator("node.add_node", text=" Volume Absorption ", icon = "NODE_VOLUMEABSORPTION")
                props.use_transform = True
                props.type = "ShaderNodeVolumeAbsorption"

                props = col.operator("node.add_node", text=" Volume Scatter   ", icon = "NODE_VOLUMESCATTER")
                props.use_transform = True

            props.type = "ShaderNodeVolumeScatter"

            if context.space_data.shader_type == 'WORLD':
                col = layout.column(align=True)
                col.scale_y = 1.5

                props = col.operator("node.add_node", text=" Background    ", icon = "NODE_BACKGROUNDSHADER")
                props.use_transform = True
                props.type = "ShaderNodeBackground"

                props = col.operator("node.add_node", text=" Emission           ", icon = "NODE_EMISSION")
                props.use_transform = True
                props.type = "ShaderNodeEmission"

                props = col.operator("node.add_node", text=" Principled Volume       ", icon = "NODE_VOLUMEPRINCIPLED")
                props.use_transform = True
                props.type = "ShaderNodeVolumePrincipled"

                props = col.operator("node.add_node", text=" Mix                   ", icon = "NODE_MIXSHADER")
                props.use_transform = True
                props.type = "ShaderNodeMixShader"

        #### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5


            props = flow.operator("node.add_node", text="", icon = "NODE_ADD_SHADER")
            props.use_transform = True
            props.type = "ShaderNodeAddShader"

            if context.space_data.shader_type == 'OBJECT':

                if engine == 'CYCLES':

                    props = flow.operator("node.add_node", text="", icon = "CURVES")
                    props.use_transform = True
                    props.type = "ShaderNodeBsdfHairPrincipled"

                props = flow.operator("node.add_node", text = "", icon = "NODE_MIXSHADER")
                props.use_transform = True
                props.type = "ShaderNodeMixShader"

                props = flow.operator("node.add_node", text="", icon = "NODE_PRINCIPLED")
                props.use_transform = True
                props.type = "ShaderNodeBsdfPrincipled"

                props = flow.operator("node.add_node", text="", icon = "NODE_VOLUMEPRINCIPLED")
                props.use_transform = True
                props.type = "ShaderNodeVolumePrincipled"

                if engine == 'CYCLES':

                    props = flow.operator("node.add_node", text = "", icon = "NODE_TOONSHADER")
                    props.use_transform = True
                    props.type = "ShaderNodeBsdfToon"

                props = flow.operator("node.add_node", text="", icon = "NODE_VOLUMEABSORPTION")
                props.use_transform = True
                props.type = "ShaderNodeVolumeAbsorption"

                props = flow.operator("node.add_node", text="", icon = "NODE_VOLUMESCATTER")
                props.use_transform = True
                props.type = "ShaderNodeVolumeScatter"

            if context.space_data.shader_type == 'WORLD':

                props = flow.operator("node.add_node", text = "", icon = "NODE_BACKGROUNDSHADER")
                props.use_transform = True
                props.type = "ShaderNodeBackground"

                props = flow.operator("node.add_node", text = "", icon = "NODE_EMISSION")
                props.use_transform = True
                props.type = "ShaderNodeEmission"

                props = flow.operator("node.add_node", text="", icon = "NODE_VOLUMEPRINCIPLED")
                props.use_transform = True
                props.type = "ShaderNodeVolumePrincipled"

                props = flow.operator("node.add_node", text = "", icon = "NODE_MIXSHADER")
                props.use_transform = True
                props.type = "ShaderNodeMixShader"


#Shader Editor - Texture panel
class NODES_PT_shader_add_texture_common(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Texture"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        return addon_prefs.Node_shader_add_common == True and context.space_data.tree_type == 'ShaderNodeTree' # Just in shader and texture mode

    @staticmethod
    def draw(self, context):
        layout = self.layout#### Textbuttons
        default_context = bpy.app.translations.contexts.default

        scene = context.scene
        engine = context.engine

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        ##### Textbuttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Environment Texture", icon = "NODE_ENVIRONMENT")
            props.use_transform = True
            props.type = "ShaderNodeTexEnvironment"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Image Texture         ", icon = "FILE_IMAGE")
            props.use_transform = True
            props.type = "ShaderNodeTexImage"

            props = col.operator("node.add_node", text=" Noise Texture         ", icon = "NOISE_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexNoise"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Sky Texture             ", icon = "NODE_SKY")
            props.use_transform = True
            props.type = "ShaderNodeTexSky"

            props = col.operator("node.add_node", text=" Voronoi Texture       ", icon = "VORONI_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexVoronoi"


        #### Icon Buttons
        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_ENVIRONMENT")
            props.use_transform = True
            props.type = "ShaderNodeTexEnvironment"

            props = flow.operator("node.add_node", text = "", icon = "FILE_IMAGE")
            props.use_transform = True
            props.type = "ShaderNodeTexImage"

            props = flow.operator("node.add_node", text = "", icon = "NOISE_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexNoise"

            props = flow.operator("node.add_node", text = "", icon = "NODE_SKY")
            props.use_transform = True
            props.type = "ShaderNodeTexSky"

            props = flow.operator("node.add_node", text = "", icon = "VORONI_TEX")
            props.use_transform = True
            props.type = "ShaderNodeTexVoronoi"


#Shader Editor - Color panel
class NODES_PT_shader_add_color_common(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Color"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        return addon_prefs.Node_shader_add_common == True and context.space_data.tree_type == 'ShaderNodeTree'

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        ##### Textbuttons
        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Bright / Contrast ", icon = "BRIGHTNESS_CONTRAST")
            props.use_transform = True
            props.type = "ShaderNodeBrightContrast"

            props = col.operator("node.add_node", text=" Gamma             ", icon = "NODE_GAMMA")
            props.use_transform = True
            props.type = "ShaderNodeGamma"

            props = col.operator("node.add_node", text=" Hue / Saturation ", icon = "NODE_HUESATURATION")
            props.use_transform = True
            props.type = "ShaderNodeHueSaturation"

            props = col.operator("node.add_node", text=" Invert                 ", icon = "NODE_INVERT")
            props.use_transform = True
            props.type = "ShaderNodeInvert"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Mix RGB           ", icon = "NODE_MIXRGB")
            props.use_transform = True
            props.type = "ShaderNodeMixRGB"

            props = col.operator("node.add_node", text="  RGB Curves        ", icon = "NODE_RGBCURVE")
            props.use_transform = True
            props.type = "ShaderNodeRGBCurve"

        ##### Icon Buttons
        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "BRIGHTNESS_CONTRAST")
            props.use_transform = True
            props.type = "ShaderNodeBrightContrast"

            props = flow.operator("node.add_node", text = "", icon = "NODE_GAMMA")
            props.use_transform = True
            props.type = "ShaderNodeGamma"

            props = flow.operator("node.add_node", text = "", icon = "NODE_HUESATURATION")
            props.use_transform = True
            props.type = "ShaderNodeHueSaturation"

            props = flow.operator("node.add_node", text = "", icon = "NODE_INVERT")
            props.use_transform = True
            props.type = "ShaderNodeInvert"

            props = flow.operator("node.add_node", text = "", icon = "NODE_MIXRGB")
            props.use_transform = True
            props.type = "ShaderNodeMixRGB"

            props = flow.operator("node.add_node", text = "", icon = "NODE_RGBCURVE")
            props.use_transform = True
            props.type = "ShaderNodeRGBCurve"


#Shader Editor - Vector panel
class NODES_PT_shader_add_vector_common(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Vector"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        return addon_prefs.Node_shader_add_common == True and context.space_data.tree_type == 'ShaderNodeTree' # Just in shader and compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        ##### Textbuttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Mapping           ", icon = "NODE_MAPPING")
            props.use_transform = True
            props.type = "ShaderNodeMapping"

            props = col.operator("node.add_node", text=" Normal            ", icon = "RECALC_NORMALS")
            props.use_transform = True
            props.type = "ShaderNodeNormal"

            props = col.operator("node.add_node", text=" Normal Map     ", icon = "NODE_NORMALMAP")
            props.use_transform = True
            props.type = "ShaderNodeNormalMap"

        ##### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "NODE_MAPPING")
            props.use_transform = True
            props.type = "ShaderNodeMapping"

            props = flow.operator("node.add_node", text = "", icon = "RECALC_NORMALS")
            props.use_transform = True
            props.type = "ShaderNodeNormal"

            props = flow.operator("node.add_node", text = "", icon = "NODE_NORMALMAP")
            props.use_transform = True
            props.type = "ShaderNodeNormalMap"


#Shader Editor - Converter panel
class NODES_PT_shader_add_converter_common(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Converter"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        return addon_prefs.Node_shader_add_common == True and context.space_data.tree_type == 'ShaderNodeTree' # Just in shader and compositing mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene
        engine = context.engine

        ##### Textbuttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Clamp              ", icon = "NODE_CLAMP")
            props.use_transform = True
            props.type = "ShaderNodeClamp"

            props = col.operator("node.add_node", text=" ColorRamp       ", icon = "NODE_COLORRAMP")
            props.use_transform = True
            props.type = "ShaderNodeValToRGB"

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Float Curve      ", icon = "FLOAT_CURVE")
            props.use_transform = True
            props.type = "ShaderNodeFloatCurve"

            props = col.operator("node.add_node", text=" Map Range       ", icon = "NODE_MAP_RANGE")
            props.use_transform = True
            props.type = "ShaderNodeMapRange"

            props = col.operator("node.add_node", text=" Math                 ", icon = "NODE_MATH")
            props.use_transform = True
            props.type = "ShaderNodeMath"

            props = col.operator("node.add_node", text=" RGB to BW      ", icon = "NODE_RGBTOBW")
            props.use_transform = True
            props.type = "ShaderNodeRGBToBW"

        ##### Icon Buttons
        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text="", icon = "NODE_CLAMP")
            props.use_transform = True
            props.type = "ShaderNodeClamp"

            props = flow.operator("node.add_node", text = "", icon = "NODE_COLORRAMP")
            props.use_transform = True
            props.type = "ShaderNodeValToRGB"

            props = flow.operator("node.add_node", text = "", icon = "FLOAT_CURVE")
            props.use_transform = True
            props.type = "ShaderNodeFloatCurve"

            props = flow.operator("node.add_node", text="", icon = "NODE_MAP_RANGE")
            props.use_transform = True
            props.type = "ShaderNodeMapRange"

            props = flow.operator("node.add_node", text = "", icon = "NODE_MATH")
            props.use_transform = True
            props.type = "ShaderNodeMath"

            props = flow.operator("node.add_node", text = "", icon = "NODE_RGBTOBW")
            props.use_transform = True
            props.type = "ShaderNodeRGBToBW"


#Shader Editor - Script panel
class NODES_PT_shader_add_script(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Script"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Add"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'ShaderNodeTree') # Just in shader mode

    @staticmethod
    def draw(self, context):
        layout = self.layout
        default_context = bpy.app.translations.contexts.default

        preferences = context.preferences
        addon_prefs = preferences.addons["bforartists_toolbar_settings"].preferences

        scene = context.scene

        ##### Textbuttons

        if not addon_prefs.Node_text_or_icon:

            col = layout.column(align=True)
            col.scale_y = 1.5

            props = col.operator("node.add_node", text=" Script               ", icon = "FILE_SCRIPT")
            props.use_transform = True
            props.type = "ShaderNodeScript"

        ##### Icon Buttons

        else:

            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
            flow.scale_x = 1.5
            flow.scale_y = 1.5

            props = flow.operator("node.add_node", text = "", icon = "FILE_SCRIPT")
            props.use_transform = True
            props.type = "ShaderNodeScript"


classes = (
    NODES_PT_shader_comp_textoricon_shader_add,
    NODES_PT_shader_comp_textoricon_compositor_add,
    NODES_PT_shader_comp_textoricon_relations,
    NODES_PT_geom_textoricon_add,
    NODES_PT_geom_textoricon_relations,
    NODES_PT_shader_add_input,
    NODES_PT_shader_add_output,

    #-----------------------

    #Compositor nodes add tab
    NODES_PT_comp_add_input,
    NODES_PT_comp_add_input_constant,
    NODES_PT_comp_add_input_scene,
    NODES_PT_comp_add_output,
    NODES_PT_comp_add_color,
    NODES_PT_comp_add_color_adjust,
    NODES_PT_comp_add_color_mix,
    NODES_PT_comp_add_filter,
    NODES_PT_comp_add_filter_blur,
    NODES_PT_comp_add_keying,
    NODES_PT_comp_add_mask,
    NODES_PT_comp_add_texture,
    NODES_PT_comp_add_tracking,
    NODES_PT_comp_add_transform,
    NODES_PT_comp_add_utility,
    NODES_PT_comp_add_vector,

    #-----------------------

    NODES_PT_Input_input_tex,
    NODES_PT_Input_textures_tex,
    NODES_PT_shader_add_shader,
    NODES_PT_shader_add_texture,
    NODES_PT_shader_add_color,
    NODES_PT_Input_input_advanced_tex,
    NODES_PT_Input_pattern,
    NODES_PT_Input_color_tex,
    NODES_PT_Input_output_tex,
    NODES_PT_Modify_converter_tex,
    NODES_PT_shader_add_vector,
    NODES_PT_shader_add_converter,
    NODES_PT_Modify_distort_tex,


    #-----------------------

    #geometry nodes relations tab
    NODES_PT_Relations_group,
    NODES_PT_Input_node_group,
    NODES_PT_Relations_layout,

    #geometry nodes add tab
    NODES_PT_geom_add_attribute,

    NODES_PT_geom_add_input,
    NODES_PT_geom_add_input_constant,
    NODES_PT_geom_add_input_gizmo,
    NODES_PT_geom_add_input_file,
    NODES_PT_geom_add_input_scene,

    NODES_PT_geom_add_output,

    NODES_PT_geom_add_geometry,
    NODES_PT_geom_add_geometry_read,
    NODES_PT_geom_add_geometry_sample,
    NODES_PT_geom_add_geometry_write,
    NODES_PT_geom_add_geometry_operations,

    NODES_PT_geom_add_curve,
    NODES_PT_geom_add_curve_read,
    NODES_PT_geom_add_curve_sample,
    NODES_PT_geom_add_curve_write,
    NODES_PT_geom_add_curve_operations,
    NODES_PT_geom_add_curve_primitives,
    NODES_PT_geom_add_curve_topology,

    NODES_PT_geom_add_grease_pencil,
    NODES_PT_geom_add_grease_pencil_read,
    NODES_PT_geom_add_grease_pencil_write,
    NODES_PT_geom_add_grease_pencil_operations,

    NODES_PT_geom_add_instances,

    NODES_PT_geom_add_mesh,
    NODES_PT_geom_add_mesh_read,
    NODES_PT_geom_add_mesh_sample,
    NODES_PT_geom_add_mesh_write,
    NODES_PT_geom_add_mesh_operations,
    NODES_PT_geom_add_mesh_primitives,
    NODES_PT_geom_add_mesh_topology,
    NODES_PT_geom_add_mesh_uv,

    NODES_PT_geom_add_point,
    NODES_PT_geom_add_volume,
    NODES_PT_geom_add_simulation,
    NODES_PT_geom_add_material,
    NODES_PT_geom_add_texture,

    NODES_PT_geom_add_utilities,
    NODES_PT_geom_add_utilities_color,
    NODES_PT_geom_add_utilities_text,
    NODES_PT_geom_add_utilities_vector,
    NODES_PT_geom_add_utilities_field,
    NODES_PT_geom_add_utilities_math,
    NODES_PT_geom_add_utilities_matrix,
    NODES_PT_geom_add_utilities_rotation,
    NODES_PT_geom_add_utilities_deprecated,

    #----------------------------------

    #- shader editor common classes
    NODES_PT_shader_add_input_common,
    NODES_PT_shader_add_output_common,
    NODES_PT_shader_add_shader_common,
    NODES_PT_shader_add_texture_common,
    NODES_PT_shader_add_color_common,
    NODES_PT_shader_add_vector_common,
    NODES_PT_shader_add_converter_common,

    NODES_PT_shader_add_script,
)

if __name__ == "__main__":  # only for live edit.
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

