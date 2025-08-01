# SPDX-FileCopyrightText: 2017-2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

from bpy.types import (
    Collection,
    Menu,
    Panel,
)

from rna_prop_ui import PropertyPanel


class CollectionButtonsPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "collection"

    @classmethod
    def poll(cls, context):
        return context.collection != context.scene.collection


def lineart_make_line_type_entry(col, line_type, text_disp, expand, search_from):
    col.prop(line_type, "use", text=text_disp)
    if line_type.use and expand:
        col.prop_search(line_type, "layer", search_from, "layers", icon='GREASEPENCIL')
        col.prop_search(line_type, "material", search_from, "materials", icon='SHADING_TEXTURE')


class COLLECTION_PT_collection_flags(CollectionButtonsPanel, Panel):
    bl_label = "Visibility"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False # BFA
        layout.use_property_decorate = False

        collection = context.collection

        col = layout.column(align = True)
        col.prop(collection, "hide_select", text="Selectable", toggle=False, invert_checkbox=True)
        col.prop(collection, "hide_render", text="Show in Renders", toggle=False, invert_checkbox=True)


class COLLECTION_PT_viewlayer_flags(CollectionButtonsPanel, Panel):
    bl_label = "View Layer"
    bl_parent_id = "COLLECTION_PT_collection_flags"

    def draw(self, context):
        vl = context.view_layer
        vlc = vl.active_layer_collection

        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        col = layout.column(align=True)
        col.prop(vlc, "exclude", text="Include", toggle=False, invert_checkbox=True)
        col.prop(vlc, "holdout", toggle=False)
        col.prop(vlc, "indirect_only", toggle=False)


class COLLECTION_PT_exporters(CollectionButtonsPanel, Panel):
    bl_label = "Exporters"

    def draw(self, context):
        layout = self.layout

        layout.template_collection_exporters()


class COLLECTION_MT_context_menu_instance_offset(Menu):
    bl_label = "Instance Offset"

    def draw(self, _context):
        layout = self.layout
        layout.operator("object.instance_offset_from_cursor")
        layout.operator("object.instance_offset_from_object")
        layout.operator("object.instance_offset_to_cursor")


class COLLECTION_PT_instancing(CollectionButtonsPanel, Panel):
    bl_label = "Instancing"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        collection = context.collection

        row = layout.row(align=True)
        row.prop(collection, "instance_offset")
        row.menu("COLLECTION_MT_context_menu_instance_offset", icon='DOWNARROW_HLT', text="")


class COLLECTION_PT_lineart_collection(CollectionButtonsPanel, Panel):
    bl_label = "Line Art"
    bl_order = 10

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        collection = context.collection

        row = layout.row()
        row.prop(collection, "lineart_usage")

        # BFA - Float left
        split = layout.split()
        col = split.column()
        col.use_property_split = False
        col.prop(collection, "lineart_use_intersection_mask", text="Collection Mask")
        col = split.column()
        if collection.lineart_use_intersection_mask:
            col.label(icon='DISCLOSURE_TRI_DOWN')
        else:
            col.label(icon='DISCLOSURE_TRI_RIGHT')

        if collection.lineart_use_intersection_mask:
            split = layout.split(factor=0.2)
            split.use_property_split = False
            col = split.column()
            row = col.row()
            row.separator()
            row.label(text="Masks")

            col = split.column()
            row = col.row(align=True)
            for i in range(8):
                row.prop(collection, "lineart_intersection_mask", index=i, text="", toggle=True)

        split = layout.split()
        col = split.column()
        col.use_property_split = False
        col.prop(collection, "use_lineart_intersection_priority", text="Intersection Priority")
        col = split.column()
        if collection.use_lineart_intersection_priority:
            col.prop(collection, "lineart_intersection_priority", text="")
        else:
            col.label(icon='DISCLOSURE_TRI_RIGHT')


class COLLECTION_PT_collection_custom_props(CollectionButtonsPanel, PropertyPanel, Panel):
    _context_path = "collection"
    _property_type = Collection


classes = (
    COLLECTION_MT_context_menu_instance_offset,
    COLLECTION_PT_collection_flags,
    COLLECTION_PT_viewlayer_flags,
    COLLECTION_PT_instancing,
    COLLECTION_PT_lineart_collection,
    COLLECTION_PT_collection_custom_props,
    COLLECTION_PT_exporters,
)

if __name__ == "__main__":  # only for live edit.
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
