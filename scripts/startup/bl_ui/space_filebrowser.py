# SPDX-FileCopyrightText: 2009-2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy

from bpy.types import Header, Panel, Menu, UIList

from bpy_extras import (
    asset_utils,
)

from bpy.app.translations import contexts as i18n_contexts

# BFA - Added icons and floated properties left


class FILEBROWSER_HT_header(Header):
    bl_space_type = "FILE_BROWSER"

    def draw_asset_browser_buttons(self, context):
        layout = self.layout

        space_data = context.space_data
        params = space_data.params

        layout.separator_spacer()

        # BFA - Check if we have a valid asset context first
        if hasattr(context, 'asset') and context.asset is not None:
            if params.asset_library_reference not in {"LOCAL", "ESSENTIALS"}:

                # BFA - Determine if the selected asset is a collection in the FILE_BROWSER
                is_collection = False
                asset = getattr(context, "asset", None)
                if asset is not None:
                    id_type = getattr(asset, "id_type", None)
                    if id_type == 'COLLECTION':
                        is_collection = True

                if params.import_method == 'LINK_OVERRIDE':
                    pass
                else:
                    row = layout.row(align=True)
                    row.enabled = is_collection
                    row.prop(params, "instance_collections_on_append", icon_only=True, icon="OUTLINER_OB_GROUP_INSTANCE")
                    row.prop(params, "drop_instances_to_origin", icon_only=True, icon="CENTER")

        if params.asset_library_reference not in {"LOCAL", "ESSENTIALS"}:
            row = layout.row(align=True)  # BFA - change to make row of buttons
            row.prop(
                params,
                "import_method",
                text="",
                expand=True,
                icon_only=True,
            )  # BFA - change to make row of buttons

        # BFA - not used, exposed these to header for a top level UX
        #if params.asset_library_reference not in {"LOCAL", "ESSENTIALS"}:
        #    layout.popover("ASSETBROWSER_PT_import_settings", text="")

        # layout.separator_spacer() #BFA

        # Uses prop_with_popover() as popover() only adds the triangle icon in headers.
        row = layout.row(align=True)
        row.prop(params, "display_type", expand=True, icon_only=True)
        row.prop_with_popover(
            params,
            "display_type",
            panel="ASSETBROWSER_PT_display",
            text="",
            icon_only=True,
        )

        sub = layout.row()
        sub.ui_units_x = 8
        sub.prop(params, "filter_search", text="", icon="VIEWZOOM")

        layout.popover(
            panel="ASSETBROWSER_PT_filter",
            text="",
            icon="FILTER",
        )

        layout.operator(
            "screen.region_toggle",
            text="",
            icon="PREFERENCES",
            depress=is_option_region_visible(context, space_data),
        ).region_type = 'TOOL_PROPS'

    def draw(self, context):
        from bpy_extras.asset_utils import SpaceAssetInfo

        layout = self.layout

        space_data = context.space_data

        if space_data.active_operator is None:
            # layout.template_header()
            ALL_MT_editormenu_filebrowser.draw_hidden(
                context, layout
            )  # bfa - show hide the editormenu, editor suffix is needed.

        if SpaceAssetInfo.is_asset_browser(space_data):
            ASSETBROWSER_MT_editor_menus.draw_collapsible(context, layout)
            layout.separator()
            self.draw_asset_browser_buttons(context)
        else:
            FILEBROWSER_MT_editor_menus.draw_collapsible(context, layout)
            layout.separator_spacer()

        if not context.screen.show_statusbar:
            layout.template_running_jobs()


# bfa - show hide the editormenu, editor suffix is needed.
class ALL_MT_editormenu_filebrowser(Menu):
    bl_label = ""

    def draw(self, context):
        self.draw_menus(self.layout, context)

    @staticmethod
    def draw_menus(layout, context):
        row = layout.row(align=True)
        row.template_header()  # editor type menus


class FileBrowserPanel:
    bl_space_type = 'FILE_BROWSER'

    @classmethod
    def poll(cls, context):
        space_data = context.space_data

        # can be None when save/reload with a file selector open
        if space_data.params is None:
            return False

        return space_data and space_data.type == 'FILE_BROWSER' and space_data.browse_mode == 'FILES'


class FILEBROWSER_PT_display(FileBrowserPanel, Panel):
    bl_region_type = 'HEADER'
    bl_label = "Display Settings"  # Shows as tooltip in popover
    bl_ui_units_x = 16

    def draw(self, context):
        layout = self.layout

        space = context.space_data
        params = space.params

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if params.display_type == 'THUMBNAIL':
            layout.prop(
                params, "display_size_discrete", text="Thumbnail Presets", expand=True
            )  # BFA - added quick thumbnail sizes.
            layout.prop(params, "display_size", text="Size")
        else:
            col = layout.column(align=True)
            col.label(text="Columns")
            row = col.row()
            row.use_property_split = False
            row.separator()
            row.prop(params, "show_details_size", text="Size")
            row = col.row()
            row.use_property_split = False
            row.separator()
            row.prop(params, "show_details_datetime", text="Date")

        layout.prop(params, "recursion_level", text="Recursions")

        layout.label(text="Sort By")  # BFA - added label

        layout.column().prop(params, "sort_method", text="Sort By", expand=True)
        layout.use_property_split = False
        layout.prop(params, "use_sort_invert")


class FILEBROWSER_PT_filter(FileBrowserPanel, Panel):
    bl_space_type = "FILE_BROWSER" # BFA
    bl_region_type = 'HEADER'
    bl_label = "Filter Settings"  # Shows as tooltip in popover
    bl_ui_units_x = 10

    def draw(self, context):
        layout = self.layout

        space = context.space_data
        params = space.params
        is_lib_browser = params.use_library_browsing

        col = layout.column()
        col.active = params.use_filter

        row = col.row()
        row.label(icon="FILE_FOLDER")
        row.prop(params, "use_filter_folder", text="Folders", toggle=False)

        if params.filter_glob:
            col.label(text=params.filter_glob)
        else:
            row = col.row()
            row.label(icon="FILE_BLEND")
            row.prop(params, "use_filter_blender", text=".blend Files", toggle=False)
            row = col.row()
            row.label(icon="FILE_BACKUP")
            row.prop(
                params, "use_filter_backup", text="Backup .blend Files", toggle=False
            )
            row = col.row()
            row.label(icon="FILE_IMAGE")
            row.prop(params, "use_filter_image", text="Image Files", toggle=False)
            row = col.row()
            row.label(icon="FILE_MOVIE")
            row.prop(params, "use_filter_movie", text="Movie Files", toggle=False)
            row = col.row()
            row.label(icon="FILE_SCRIPT")
            row.prop(params, "use_filter_script", text="Script Files", toggle=False)
            row = col.row()
            row.label(icon="FILE_FONT")
            row.prop(params, "use_filter_font", text="Font Files", toggle=False)
            row = col.row()
            row.label(icon="FILE_SOUND")
            row.prop(params, "use_filter_sound", text="Sound Files", toggle=False)
            row = col.row()
            row.label(icon="FILE_TEXT")
            row.prop(params, "use_filter_text", text="Text Files", toggle=False)
            row = col.row()
            row.label(icon="FILE_VOLUME")
            row.prop(params, "use_filter_volume", text="Volume Files", toggle=False)

        col.separator()

        if is_lib_browser:
            row = col.row()
            row.label(icon="BLANK1")  # Indentation
            row.prop(params, "use_filter_blendid", text="Blender IDs", toggle=False)
            if params.use_filter_blendid:
                row = col.row()
                row.label(icon="BLANK1")  # Indentation

                sub = row.column(align=True)

                sub.prop(params, "use_filter_asset_only")

                filter_id = params.filter_id
                for identifier in dir(filter_id):
                    if identifier.startswith("category_"):
                        subrow = sub.row()
                        subrow.label(icon=filter_id.bl_rna.properties[identifier].icon)
                        subrow.prop(filter_id, identifier, toggle=False)

                col.separator()

        layout.prop(params, "show_hidden")


def panel_poll_is_upper_region(region):
    # The upper region is left-aligned, the lower is split into it then.
    # Note that after "Flip Regions" it's right-aligned.
    return region.alignment in {'LEFT', 'RIGHT'}


def panel_poll_is_asset_browsing(context):
    from bpy_extras.asset_utils import SpaceAssetInfo
    return SpaceAssetInfo.is_asset_browser_poll(context)


class FILEBROWSER_UL_dir(UIList):
    def draw_item(self, _context, layout, _data, item, icon, _active_data, _active_propname, _index):
        direntry = item
        # space = context.space_data

        row = layout.row(align=True)
        row.enabled = direntry.is_valid
        # Non-editable entries would show grayed-out, which is bad in this specific case, so switch to mere label.
        if direntry.is_property_readonly("name"):
            row.label(text=direntry.name, icon_value=icon)
        else:
            row.prop(direntry, "name", text="", emboss=False, icon_value=icon)


class FILEBROWSER_PT_bookmarks_volumes(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks"
    bl_label = "Volumes"
    bl_translation_context = i18n_contexts.editor_filebrowser

    @classmethod
    def poll(cls, context):
        return panel_poll_is_upper_region(
            context.region
        ) and not panel_poll_is_asset_browsing(context)

    def draw(self, context):
        layout = self.layout
        space = context.space_data

        if space.system_folders:
            row = layout.row()
            row.template_list(
                "FILEBROWSER_UL_dir",
                "system_folders",
                space,
                "system_folders",
                space,
                "system_folders_active",
                item_dyntip_propname="path",
                rows=1,
                maxrows=10,
            )


class FILEBROWSER_PT_bookmarks_system(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks"
    bl_label = "System"

    @classmethod
    def poll(cls, context):
        return (
            context.preferences.filepaths.show_system_bookmarks
            and panel_poll_is_upper_region(context.region)
            and not panel_poll_is_asset_browsing(context)
        )

    def draw(self, context):
        layout = self.layout
        space = context.space_data

        if space.system_bookmarks:
            row = layout.row()
            row.template_list(
                "FILEBROWSER_UL_dir",
                "system_bookmarks",
                space,
                "system_bookmarks",
                space,
                "system_bookmarks_active",
                item_dyntip_propname="path",
                rows=1,
                maxrows=10,
            )


class FILEBROWSER_MT_bookmarks_context_menu(Menu):
    bl_label = "Bookmarks Specials"

    def draw(self, _context):
        layout = self.layout
        layout.operator("file.bookmark_cleanup", icon="X", text="Cleanup")

        layout.separator()
        layout.operator(
            "file.bookmark_move", icon="TRIA_UP_BAR", text="Move to Top"
        ).direction = "TOP"
        layout.operator(
            "file.bookmark_move", icon="TRIA_DOWN_BAR", text="Move to Bottom"
        ).direction = "BOTTOM"


class FILEBROWSER_PT_bookmarks_favorites(FileBrowserPanel, Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks"
    bl_label = "Bookmarks"

    @classmethod
    def poll(cls, context):
        return panel_poll_is_upper_region(
            context.region
        ) and not panel_poll_is_asset_browsing(context)

    def draw(self, context):
        layout = self.layout
        space = context.space_data

        if space.bookmarks:
            row = layout.row()
            num_rows = len(space.bookmarks)
            row.template_list(
                "FILEBROWSER_UL_dir",
                "bookmarks",
                space,
                "bookmarks",
                space,
                "bookmarks_active",
                item_dyntip_propname="path",
                rows=(2 if num_rows < 2 else 4),
                maxrows=10,
            )

            col = row.column(align=True)
            col.operator("file.bookmark_add", icon="ADD", text="")
            col.operator("file.bookmark_delete", icon="REMOVE", text="")
            col.menu(
                "FILEBROWSER_MT_bookmarks_context_menu", icon="DOWNARROW_HLT", text=""
            )

            if num_rows > 1:
                col.separator()
                col.operator(
                    "file.bookmark_move", icon="TRIA_UP", text=""
                ).direction = "UP"
                col.operator(
                    "file.bookmark_move", icon="TRIA_DOWN", text=""
                ).direction = "DOWN"
        else:
            layout.operator("file.bookmark_add", icon="ADD")


class FILEBROWSER_MT_bookmarks_recents_specials_menu(Menu):
    bl_label = "Recent Items Specials"

    def draw(self, _context):
        layout = self.layout

        layout.operator("file.reset_recent", icon="X", text="Clear Recent Items")


class FILEBROWSER_PT_bookmarks_recents(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks"
    bl_label = "Recent"

    @classmethod
    def poll(cls, context):
        return (
            context.preferences.filepaths.show_recent_locations
            and panel_poll_is_upper_region(context.region)
            and not panel_poll_is_asset_browsing(context)
        )

    def draw(self, context):
        layout = self.layout
        space = context.space_data

        if space.recent_folders:
            row = layout.row()
            row.template_list(
                "FILEBROWSER_UL_dir", "recent_folders", space, "recent_folders",
                space, "recent_folders_active", item_dyntip_propname="path", rows=1, maxrows=10,
            )

            col = row.column(align=True)
            col.menu("FILEBROWSER_MT_bookmarks_recents_specials_menu", icon='DOWNARROW_HLT', text="")


class FILEBROWSER_PT_advanced_filter(Panel):
    bl_space_type = "FILE_BROWSER"
    bl_region_type = 'TOOL_PROPS'
    bl_category = "Filter"
    bl_label = "Advanced Filter"

    @classmethod
    def poll(cls, context):
        # only useful in append/link (library) context currently...
        return (
            context.space_data.params and
            context.space_data.params.use_library_browsing and
            panel_poll_is_upper_region(context.region) and
            not panel_poll_is_asset_browsing(context)
        )

    def draw(self, context):
        layout = self.layout
        space = context.space_data
        params = space.params

        layout.prop(params, "use_filter_blendid")
        if params.use_filter_blendid:
            layout.separator()
            col = layout.column(align=True)

            col.prop(params, "use_filter_asset_only")

            filter_id = params.filter_id
            for identifier in dir(filter_id):
                if identifier.startswith("filter_"):
                    row = col.row()
                    row.label(icon=filter_id.bl_rna.properties[identifier].icon)
                    row.prop(filter_id, identifier, toggle=False)


def is_option_region_visible(context, space):
    from bpy_extras.asset_utils import SpaceAssetInfo

    if SpaceAssetInfo.is_asset_browser(space):
        pass
    # For the File Browser, there must be an operator for there to be options
    # (irrelevant for the Asset Browser).
    elif not space.active_operator:
        return False

    for region in context.area.regions:
        if region.type == 'TOOL_PROPS' and region.width <= 1:
            return False

    return True


class FILEBROWSER_PT_directory_path(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'UI'
    bl_label = "Directory Path"
    bl_category = "Attributes"
    bl_options = {'HIDE_HEADER'}

    def is_header_visible(self, context):
        for region in context.area.regions:
            if region.type == 'HEADER' and region.height <= 1:
                return False

        return True

    @classmethod
    def poll(cls, context):
        return context.space_data.params

    def draw(self, context):
        layout = self.layout
        space = context.space_data
        params = space.params

        layout.scale_x = 1.3
        layout.scale_y = 1.3

        row = layout.row()
        flow = row.grid_flow(row_major=True, columns=0, even_columns=False, even_rows=False, align=False)

        subrow = flow.row()

        subsubrow = subrow.row(align=True)
        subsubrow.operator("file.previous", text="", icon="BACK")
        subsubrow.operator("file.next", text="", icon="FORWARD")
        subsubrow.operator("file.parent", text="", icon="FILE_PARENT")
        subsubrow.operator("file.refresh", text="", icon="FILE_REFRESH")

        subsubrow = subrow.row()
        subsubrow.operator_context = 'EXEC_DEFAULT'
        subsubrow.operator("file.directory_new", icon="NEWFOLDER", text="")

        subrow.template_file_select_path(params)

        subrow = flow.row()

        subsubrow = subrow.row()
        subsubrow.scale_x = 0.6
        subsubrow.prop(params, "filter_search", text="", icon="VIEWZOOM")

        subsubrow = subrow.row(align=True)
        subsubrow.prop(params, "display_type", expand=True, icon_only=True)
        subsubrow.popover("FILEBROWSER_PT_display", text="")

        subsubrow = subrow.row(align=True)
        subsubrow.prop(params, "use_filter", toggle=True, icon="FILTER", icon_only=True)
        subsubrow.popover("FILEBROWSER_PT_filter", text="")

        if space.active_operator:
            subrow.operator(
                "screen.region_toggle",
                text="",
                icon="PREFERENCES",
                depress=is_option_region_visible(context, space),
            ).region_type = 'TOOL_PROPS'


class FileBrowserMenu:
    @classmethod
    def poll(cls, context):
        space_data = context.space_data
        return (
            space_data
            and space_data.type == "FILE_BROWSER"
            and space_data.browse_mode == "FILES"
        )


class FILEBROWSER_MT_editor_menus(FileBrowserMenu, Menu):
    bl_idname = "FILEBROWSER_MT_editor_menus"
    bl_label = ""

    def draw(self, _context):
        layout = self.layout

        layout.menu("FILEBROWSER_MT_view")
        layout.menu("FILEBROWSER_MT_select")


class FILEBROWSER_MT_view(FileBrowserMenu, Menu):
    bl_label = "View"

    def draw(self, context):
        layout = self.layout
        st = context.space_data
        params = st.params

        layout.prop(st, "show_region_toolbar", text="Source List")
        layout.prop(st, "show_region_ui", text="File Path")
        layout.operator("file.view_selected", icon="VIEW_SELECTED")

        layout.separator()

        layout.menu("INFO_MT_area")

        layout.menu("FILEBROWSER_MT_view_pie_menus")


class FILEBROWSER_MT_select(FileBrowserMenu, Menu):
    bl_label = "Select"

    def draw(self, _context):
        layout = self.layout

        layout.operator(
            "file.select_all", text="All", icon="SELECT_ALL"
        ).action = "SELECT"
        layout.operator(
            "file.select_all", text="None", icon="SELECT_NONE"
        ).action = "DESELECT"
        layout.operator(
            "file.select_all", text="Invert", icon="INVERSE"
        ).action = "INVERT"

        layout.separator()

        layout.operator("file.select_box", icon="BORDER_RECT")


class FILEBROWSER_MT_context_menu(FileBrowserMenu, Menu):
    bl_label = "Files"

    def draw(self, context):
        layout = self.layout
        st = context.space_data
        params = st.params

        layout.operator("file.previous", text="Back", icon="BACK")
        layout.operator("file.next", text="Forward", icon="FORWARD")
        layout.operator("file.parent", text="Go to Parent", icon="FILE_PARENT")
        layout.operator("file.refresh", text="Refresh", icon="FILE_REFRESH")
        layout.menu("FILEBROWSER_MT_operations_menu")

        layout.separator()

        layout.operator(
            "file.filenum", text="Increase Number", icon="ADD"
        ).increment = 1
        layout.operator(
            "file.filenum", text="Decrease Number", icon="REMOVE"
        ).increment = -1

        layout.separator()

        layout.operator("file.rename", text="Rename", icon="RENAME")
        sub = layout.row()
        sub.operator_context = 'EXEC_DEFAULT'
        sub.operator("file.delete", text="Delete", icon="DELETE")

        layout.separator()

        sub = layout.row()
        sub.operator_context = 'EXEC_DEFAULT'
        sub.operator("file.directory_new", text="New Folder", icon="FILE_FOLDER")
        layout.operator("file.bookmark_add", text="Add Bookmark", icon="BOOKMARKS")

        layout.separator()

        layout.prop_menu_enum(params, "display_type")
        if params.display_type == 'THUMBNAIL':
            layout.prop_menu_enum(params, "display_size_discrete")
        layout.prop_menu_enum(params, "recursion_level", text="Recursions")
        layout.prop_menu_enum(params, "sort_method")


class FILEBROWSER_MT_view_pie(Menu):
    bl_label = "View"
    bl_idname = "FILEBROWSER_MT_view_pie"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        view = context.space_data

        pie.prop_enum(view.params, "display_type", value="LIST_VERTICAL")
        pie.prop_enum(view.params, "display_type", value="LIST_HORIZONTAL")
        pie.prop_enum(view.params, "display_type", value="THUMBNAIL")


class ASSETBROWSER_PT_display(asset_utils.AssetBrowserPanel, Panel):
    bl_region_type = 'HEADER'
    bl_label = "Display Settings"  # Shows as tooltip in popover
    bl_ui_units_x = 10

    def draw(self, context):
        layout = self.layout

        space = context.space_data
        params = space.params

        layout.use_property_split = False
        layout.use_property_decorate = False  # No animation.

        if params.display_type == "THUMBNAIL":
            layout.prop(
                params, "display_size_discrete", text="Text", expand=True
            )  # BFA - added quick thumbnail sizes.
            layout.prop(params, "display_size", text="Size")
        else:
            layout.column().prop(params, "list_display_size", text="Preview Size")
        if params.display_type == "LIST_HORIZONTAL":
            layout.column().prop(params, "list_column_size", text="Column Size")

        layout.label(text="Sort By")  # BFA - added label

        layout.column().prop(params, "sort_method", text="Sort By", expand=True)


class ASSETBROWSER_PT_filter(asset_utils.AssetBrowserPanel, Panel):
    bl_region_type = 'HEADER'
    bl_category = "Filter"
    bl_label = "Filter"

    def draw(self, context):
        layout = self.layout
        space = context.space_data
        params = space.params
        use_extended_browser = (
            context.preferences.experimental.use_extended_asset_browser
        )

        if params.use_filter_blendid:
            col = layout.column(align=True)

            filter_id = params.filter_asset_id
            for identifier in dir(filter_id):
                if identifier.startswith("filter_") or (
                    identifier.startswith("experimental_filter_")
                    and use_extended_browser
                ):
                    row = col.row()
                    row.label(icon=filter_id.bl_rna.properties[identifier].icon)
                    row.prop(filter_id, identifier, toggle=False)


class AssetBrowserMenu:
    @classmethod
    def poll(cls, context):
        from bpy_extras.asset_utils import SpaceAssetInfo
        return SpaceAssetInfo.is_asset_browser_poll(context)


class ASSETBROWSER_MT_editor_menus(AssetBrowserMenu, Menu):
    bl_idname = "ASSETBROWSER_MT_editor_menus"
    bl_label = ""

    def draw(self, _context):
        layout = self.layout

        layout.menu("ASSETBROWSER_MT_view")
        layout.menu("ASSETBROWSER_MT_select")
        layout.menu("ASSETBROWSER_MT_catalog")


class ASSETBROWSER_MT_view(AssetBrowserMenu, Menu):
    bl_label = "View"

    def draw(self, context):
        layout = self.layout
        st = context.space_data
        params = st.params

        layout.prop(st, "show_region_toolbar", text="Source List")
        layout.prop(st, "show_region_tool_props", text="Asset Details")
        layout.operator("file.view_selected", icon="VIEW_SELECTED")

        layout.separator()

        layout.prop_menu_enum(params, "display_size_discrete")

        layout.separator()

        layout.menu("INFO_MT_area")


class FILEBROWSER_MT_view_pie_menus(Menu):
    bl_label = "Pie Menus"

    def draw(self, _context):
        layout = self.layout

        layout.operator(
            "wm.call_menu_pie", text="View", icon="MENU_PANEL"
        ).name = "FILEBROWSER_MT_view_pie"


# BFA - menu
class ASSETBROWSER_MT_select(AssetBrowserMenu, Menu):
    bl_label = "Select"

    def draw(self, _context):
        layout = self.layout

        layout.operator(
            "file.select_all", text="All", icon="SELECT_ALL"
        ).action = "SELECT"
        layout.operator(
            "file.select_all", text="None", icon="SELECT_NONE"
        ).action = "DESELECT"
        layout.operator(
            "file.select_all", text="Inverse", icon="INVERSE"
        ).action = "INVERT"

        layout.separator()

        layout.operator("file.select_box", icon="BORDER_RECT")


class ASSETBROWSER_MT_catalog(AssetBrowserMenu, Menu):
    bl_label = "Catalog"

    def draw(self, _context):
        layout = self.layout

        layout.operator("asset.catalog_undo", text="Undo", icon="UNDO")
        layout.operator("asset.catalog_redo", text="Redo", icon="REDO")

        layout.separator()

        layout.operator(
            "preferences.filepaths_show",
            emboss=False,
            text="Asset Library Paths",
            icon="PREFERENCES",
        )

        layout.separator()
        layout.operator("asset.catalogs_save", icon="FILE_TICK")
        layout.operator("asset.catalog_new", icon="ADD").parent_path = ""


# BFA - not used
class ASSETBROWSER_PT_import_settings(asset_utils.AssetBrowserPanel, Panel):
    bl_idname = "ASSETBROWSER_PT_import_settings"
    bl_region_type = 'HEADER'
    bl_label = "Import Settings"
    bl_options = {'HIDE_HEADER'}
    bl_ui_units_x = 15

    def draw(self, context):
        layout = self.layout
        params = context.space_data.params

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(params, "import_method", text="Import Method")

        col = layout.column(heading="Collection Instances")
        col.prop(params, "instance_collections_on_link", text="Link")
        col.prop(params, "instance_collections_on_append", text="Append")
        col.prop(params, "drop_instances_to_origin", text="Drop To Origin") # BFA


class ASSETBROWSER_PT_metadata(asset_utils.AssetBrowserPanel, Panel):
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Asset Metadata"
    bl_options = {'HIDE_HEADER'}

    @staticmethod
    def metadata_prop(layout, asset_metadata, propname):
        """
        Only display properties that are either set or can be modified (i.e. the
        asset is in the current file). Empty, non-editable fields are not really useful.
        """
        if getattr(asset_metadata, propname) or not asset_metadata.is_property_readonly(
            propname
        ):
            layout.prop(asset_metadata, propname)

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        asset = context.asset

        if asset is None:
            layout.label(text="No active asset", icon="INFO")
            return

        prefs = context.preferences
        show_asset_debug_info = (
            prefs.view.show_developer_ui and prefs.experimental.show_asset_debug_info
        )
        is_local_asset = bool(asset.local_id)

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if is_local_asset:
            # If the active file is an ID, use its name directly so renaming is possible from right here.
            layout.prop(asset.local_id, "name")

            if show_asset_debug_info:
                col = layout.column(align=True)
                col.label(text="Asset Catalog:")
                col.prop(asset.local_id.asset_data, "catalog_id", text="UUID")
                col.prop(
                    asset.local_id.asset_data, "catalog_simple_name", text="Simple Name"
                )
        else:
            layout.prop(asset, "name")

            if show_asset_debug_info:
                col = layout.column(align=True)
                col.enabled = False
                col.label(text="Asset Catalog:")
                col.prop(asset.metadata, "catalog_id", text="UUID")
                col.prop(asset.metadata, "catalog_simple_name", text="Simple Name")


# BFA - we made this info into a panel you can collapse
class ASSETBROWSER_PT_metadata_info(asset_utils.AssetMetaDataPanel, Panel):
    bl_label = "Info"
    bl_options = {"DEFAULT_CLOSED"}  # BFA - not needed on first use

    @staticmethod
    def metadata_prop(layout, asset_metadata, propname):
        """
        Only display properties that are either set or can be modified (i.e. the
        asset is in the current file). Empty, non-editable fields are not really useful.
        """
        if getattr(asset_metadata, propname) or not asset_metadata.is_property_readonly(
            propname
        ):
            layout.prop(asset_metadata, propname)

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        asset = context.asset

        if asset is None:
            layout.label(text="No active asset", icon="INFO")
            return

        prefs = context.preferences
        show_asset_debug_info = (
            prefs.view.show_developer_ui and prefs.experimental.show_asset_debug_info
        )
        is_local_asset = bool(asset.local_id)

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if is_local_asset:
            # If the active file is an ID, use its name directly so renaming is possible from right here.
            # layout.prop(asset.local_id, "name") # BFA - redundant

            if show_asset_debug_info:
                col = layout.column(align=True)
                col.label(text="Asset Catalog:")
                col.prop(asset.local_id.asset_data, "catalog_id", text="UUID")
                col.prop(
                    asset.local_id.asset_data, "catalog_simple_name", text="Simple Name"
                )
        else:
            # layout.prop(asset, "name")  # BFA - redundant

            if show_asset_debug_info:
                col = layout.column(align=True)
                col.enabled = False
                col.label(text="Asset Catalog:")
                col.prop(asset.asset_data, "catalog_id", text="UUID")
                col.prop(asset.asset_data, "catalog_simple_name", text="Simple Name")

        row = layout.row(align=True)
        row.prop(
            wm,
            "asset_path_dummy",
            text="Source",
            icon="CURRENT_FILE" if is_local_asset else "NONE",
        )
        row.operator("asset.open_containing_blend_file", text="", icon="FILE_FOLDER")

        metadata = asset.metadata
        self.metadata_prop(layout, metadata, "description")
        self.metadata_prop(layout, metadata, "license")
        self.metadata_prop(layout, metadata, "copyright")
        self.metadata_prop(layout, metadata, "author")


class ASSETBROWSER_PT_metadata_preview(asset_utils.AssetMetaDataPanel, Panel):
    bl_label = "Preview"

    def draw(self, context):
        layout = self.layout
        active_file = context.active_file

        row = layout.row()
        box = row.box()
        box.template_icon(icon_value=active_file.preview_icon_id, scale=5.0)

        col = row.column(align=True)
        col.operator("ed.lib_id_load_custom_preview", icon="FILEBROWSER", text="")
        col.separator()
        col.operator("ed.lib_id_generate_preview", icon="FILE_REFRESH", text="")
        col.menu("ASSETBROWSER_MT_metadata_preview_menu", icon="DOWNARROW_HLT", text="")


class ASSETBROWSER_MT_metadata_preview_menu(Menu):
    bl_label = "Preview"

    def draw(self, _context):
        layout = self.layout
        layout.operator(
            "ed.lib_id_generate_preview_from_object", text="Render Active Object", icon='RENDER_STILL'
        )
        layout.separator()
        layout.operator("ed.lib_id_remove_preview", icon='REMOVE')
        layout.operator("asset.screenshot_preview", icon='MAKE_SCREENSHOT')


class ASSETBROWSER_PT_metadata_tags(asset_utils.AssetMetaDataPanel, Panel):
    bl_label = "Tags"

    def draw(self, context):
        layout = self.layout
        active_asset = context.asset
        asset_metadata = active_asset.metadata

        # BFA - Custom tags assignment for the shelves
        if context.asset and context.asset.id_type == "NODETREE":
            row = layout.row(align=True)
            row.label(text="Asset Shelf:")
            row.operator(
                "asset.tag_add_shelf", icon="NODE_COMPOSITING", text=""
            ).tag_type = "COMPOSITOR"
            row.operator(
                "asset.tag_add_shelf", icon="GEOMETRY_NODES", text=""
            ).tag_type = "GEOMETRY_NODES"
            if "Geometry Nodes" in context.asset.metadata.tags:
                row.operator(
                    "asset.tag_add_shelf", icon="OBJECT_DATA", text=""
                ).tag_type = "3D_VIEW"
            row.operator(
                "asset.tag_add_shelf", icon="NODE_MATERIAL", text=""
            ).tag_type = "SHADER"

        row = layout.row()
        row.template_list(
            "ASSETBROWSER_UL_metadata_tags", "asset_tags", asset_metadata, "tags",
            asset_metadata, "active_tag", rows=4,
        )

        col = row.column(align=True)
        col.operator("asset.tag_add", icon="ADD", text="")
        col.operator("asset.tag_remove", icon="REMOVE", text="")


class ASSETBROWSER_UL_metadata_tags(UIList):
    def draw_item(
        self,
        _context,
        layout,
        _data,
        item,
        icon,
        _active_data,
        _active_propname,
        _index,
    ):
        tag = item

        row = layout.row(align=True)
        # Non-editable entries would show grayed-out, which is bad in this specific case, so switch to mere label.
        if tag.is_property_readonly("name"):
            row.label(text=tag.name, icon_value=icon, translate=False)
        else:
            row.prop(tag, "name", text="", emboss=False, icon_value=icon)


class ASSETBROWSER_MT_context_menu(AssetBrowserMenu, Menu):
    bl_label = "Assets"

    def draw(self, context):
        layout = self.layout
        st = context.space_data
        params = st.params

        layout.operator("asset.library_refresh", icon="FILE_REFRESH")

        layout.separator()

        sub = layout.column()
        sub.operator_context = 'EXEC_DEFAULT'
        sub.operator(
            "asset.clear", text="Clear Asset", icon="CLEAR"
        ).set_fake_user = False
        sub.operator(
            "asset.clear", text="Clear Asset (Set Fake User)", icon="CLEAR"
        ).set_fake_user = True

        layout.separator()

        layout.operator("asset.open_containing_blend_file", icon="FILE_FOLDER")

        layout.separator()

        if params.display_type == "THUMBNAIL":
            layout.prop_menu_enum(params, "display_size_discrete")
        layout.prop_menu_enum(params, "sort_method")


classes = (
    ALL_MT_editormenu_filebrowser,  # BFA
    FILEBROWSER_HT_header,
    FILEBROWSER_PT_display,
    FILEBROWSER_PT_filter,
    FILEBROWSER_UL_dir,
    FILEBROWSER_MT_bookmarks_context_menu,
    FILEBROWSER_PT_bookmarks_favorites,
    FILEBROWSER_PT_bookmarks_system,
    FILEBROWSER_PT_bookmarks_volumes,
    FILEBROWSER_MT_bookmarks_recents_specials_menu,
    FILEBROWSER_PT_bookmarks_recents,
    FILEBROWSER_PT_advanced_filter,
    FILEBROWSER_PT_directory_path,
    FILEBROWSER_MT_editor_menus,
    FILEBROWSER_MT_view,
    FILEBROWSER_MT_view_pie_menus,  # BFA
    FILEBROWSER_MT_select,
    FILEBROWSER_MT_context_menu,
    FILEBROWSER_MT_view_pie,
    ASSETBROWSER_PT_display,
    ASSETBROWSER_PT_filter,
    ASSETBROWSER_MT_editor_menus,
    ASSETBROWSER_MT_view,
    ASSETBROWSER_MT_select,
    ASSETBROWSER_MT_catalog,
    ASSETBROWSER_PT_import_settings,
    ASSETBROWSER_MT_metadata_preview_menu,
    ASSETBROWSER_PT_metadata,
    ASSETBROWSER_PT_metadata_info,  # BFA
    ASSETBROWSER_PT_metadata_preview,
    ASSETBROWSER_PT_metadata_tags,
    ASSETBROWSER_UL_metadata_tags,
    ASSETBROWSER_MT_context_menu,
)


def asset_path_str_get(_self):
    asset = bpy.context.asset
    if asset is None:
        return ""

    if asset.local_id:
        return "Current File"

    return asset.full_library_path


def register_props():
    from bpy.props import (
        StringProperty,
    )
    from bpy.types import (
        WindowManager,
    )

    # Just a dummy property to be able to show a string in a label button via
    # UILayout.prop().
    WindowManager.asset_path_dummy = StringProperty(
        name="Asset Blend Path",
        description="Full path to the Blender file containing the active asset",
        get=asset_path_str_get,
    )


if __name__ == "__main__":  # only for live edit.
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)
