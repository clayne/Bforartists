# SPDX-FileCopyrightText: 2012-2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import bpy
from bpy.types import (
    FileHandler,
    Operator,
    PropertyGroup,
)
from bpy.props import (
    BoolProperty,
    CollectionProperty,
    EnumProperty,
    FloatVectorProperty,
    StringProperty,
    IntProperty,
)
from mathutils import (
    Vector,
)

from bpy.app.translations import (
    pgettext_tip as tip_,
    pgettext_rpt as rpt_,
)


# BFA - Helper function to make socket type matching easier
def compare_attributes(item, *_, **keywords):
    for key, value in keywords.items():
        if getattr(item, key, None) != value:
            return False
        
    return True


# BFA - Helper function to make checking boolean inputs easier
def is_boolean_input(item):
    return compare_attributes(item, in_out="INPUT", socket_type="NodeSocketBool")


# BFA - Helper function to make panel toggle checking easier
def is_panel_toggle(item):
    return compare_attributes(item, in_out="INPUT", socket_type="NodeSocketBool", is_panel_toggle=True, )


# BFA - Helper function to make panel toggle fetching easier
def get_panel_toggle(panel):
    try:
        first_item = panel.interface_items[0]
        if is_panel_toggle(first_item):
            return first_item
        else:
            return None
    except (AttributeError, IndexError):
        return None


#BFA - Helper functions for detecting different group item types
def is_input(item):
    return compare_attributes(item, item_type="SOCKET", in_out="INPUT", is_panel_toggle=False)


def is_output(item):
    return compare_attributes(item, item_type="SOCKET", in_out="OUTPUT", is_panel_toggle=False)


def is_panel(item):
    return compare_attributes(item, item_type="PANEL")

#BFA - Helper functions for detecting different group item types - END


#BFA - Helper function for filtering item types, needed by the "Move Item" operator
def get_similar_items(item):
    items = item.parent.interface_items

    if is_panel(item):
        similar_items = filter(is_panel, items)
    elif is_input(item):
        similar_items = filter(is_input, items)
    elif is_output(item):
        similar_items = filter(is_output, items)
    elif is_panel_toggle(item):
        similar_items = filter(is_panel_toggle, items)
    else:
        raise ValueError(f"Unrecognized Type: \"{item}\"")

    return tuple(similar_items)

    
class NodeSetting(PropertyGroup):
    value: StringProperty(
        name="Value",
        description="Python expression to be evaluated "
        "as the initial node setting",
        default="",
    )


# Base class for node "Add" operators.
class NodeAddOperator:

    use_transform: BoolProperty(
        name="Use Transform",
        description="Start transform operator after inserting the node",
        default=False,
    )
    settings: CollectionProperty(
        name="Settings",
        description="Settings to be applied on the newly created node",
        type=NodeSetting,
        options={'SKIP_SAVE'},
    )

    @staticmethod
    def store_mouse_cursor(context, event):
        space = context.space_data
        tree = space.edit_tree

        # convert mouse position to the View2D for later node placement
        if context.region.type == 'WINDOW':
            # convert mouse position to the View2D for later node placement
            space.cursor_location_from_region(event.mouse_region_x, event.mouse_region_y)
        else:
            space.cursor_location = tree.view_center

    # Deselect all nodes in the tree.
    @staticmethod
    def deselect_nodes(context):
        space = context.space_data
        tree = space.edit_tree
        for n in tree.nodes:
            n.select = False

    def create_node(self, context, node_type):
        space = context.space_data
        tree = space.edit_tree

        try:
            node = tree.nodes.new(type=node_type)
        except RuntimeError as ex:
            self.report({'ERROR'}, str(ex))
            return None

        for setting in self.settings:
            # XXX catch exceptions here?
            value = eval(setting.value)
            node_data = node
            node_attr_name = setting.name

            # Support path to nested data.
            if '.' in node_attr_name:
                node_data_path, node_attr_name = node_attr_name.rsplit(".", 1)
                node_data = node.path_resolve(node_data_path)

            try:
                setattr(node_data, node_attr_name, value)
            except AttributeError as ex:
                self.report(
                    {'ERROR_INVALID_INPUT'},
                    rpt_("Node has no attribute {:s}").format(setting.name))
                print(str(ex))
                # Continue despite invalid attribute

        node.select = True
        tree.nodes.active = node
        node.location = space.cursor_location
        return node

    @classmethod
    def poll(cls, context):
        space = context.space_data
        # needs active node editor and a tree to add nodes to
        return (space and (space.type == 'NODE_EDITOR') and
                space.edit_tree and space.edit_tree.is_editable)

    # Default invoke stores the mouse position to place the node correctly
    # and optionally invokes the transform operator
    def invoke(self, context, event):
        self.store_mouse_cursor(context, event)
        result = self.execute(context)

        if self.use_transform and ('FINISHED' in result):
            # removes the node again if transform is canceled
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        return result


# Simple basic operator for adding a node.
class NODE_OT_add_node(NodeAddOperator, Operator):
    """Add a node to the active tree"""
    bl_idname = "node.add_node"
    bl_label = "Add Node"
    bl_options = {'REGISTER', 'UNDO'}

    type: StringProperty(
        name="Node Type",
        description="Node type",
    )

    visible_output: StringProperty(
        name="Output Name",
        description="If provided, all outputs that are named differently will be hidden",
        options={'SKIP_SAVE'},
    )

    # Default execute simply adds a node.
    def execute(self, context):
        if self.properties.is_property_set("type"):
            self.deselect_nodes(context)
            if node := self.create_node(context, self.type):
                if self.visible_output:
                    for socket in node.outputs:
                        if socket.name != self.visible_output:
                            socket.hide = True
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

    @classmethod
    def description(cls, _context, properties):
        from nodeitems_builtins import node_tree_group_type

        nodetype = properties["type"]
        if nodetype in node_tree_group_type.values():
            for setting in properties.settings:
                if setting.name == "node_tree":
                    node_group = eval(setting.value)
                    if node_group.description:
                        return node_group.description
        bl_rna = bpy.types.Node.bl_rna_get_subclass(nodetype)
        if bl_rna is not None:
            return tip_(bl_rna.description)
        else:
            return ""


class NODE_OT_add_empty_group(NodeAddOperator, bpy.types.Operator):
    bl_idname = "node.add_empty_group"
    bl_label = "Add Empty Group"
    bl_description = "Add a group node with an empty group"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        from nodeitems_builtins import node_tree_group_type
        tree = context.space_data.edit_tree
        group = self.create_empty_group(tree.bl_idname)
        self.deselect_nodes(context)
        node = self.create_node(context, node_tree_group_type[tree.bl_idname])
        node.node_tree = group
        return {"FINISHED"}

    @staticmethod
    def create_empty_group(idname):
        group = bpy.data.node_groups.new(name="NodeGroup", type=idname)
        input_node = group.nodes.new('NodeGroupInput')
        input_node.select = False
        input_node.location.x = -200 - input_node.width

        output_node = group.nodes.new('NodeGroupOutput')
        output_node.is_active_output = True
        output_node.select = False
        output_node.location.x = 200
        return group


class NodeAddZoneOperator(NodeAddOperator):
    offset: FloatVectorProperty(
        name="Offset",
        description="Offset of nodes from the cursor when added",
        size=2,
        default=(150, 0),
    )

    add_default_geometry_link = True

    def execute(self, context):
        space = context.space_data
        tree = space.edit_tree

        self.deselect_nodes(context)
        input_node = self.create_node(context, self.input_node_type)
        output_node = self.create_node(context, self.output_node_type)
        if input_node is None or output_node is None:
            return {'CANCELLED'}

        # Simulation input must be paired with the output.
        input_node.pair_with_output(output_node)

        input_node.location -= Vector(self.offset)
        output_node.location += Vector(self.offset)

        if self.add_default_geometry_link:
            # Connect geometry sockets by default if available.
            # Get the sockets by their types, because the name is not guaranteed due to i18n.
            from_socket = next(s for s in input_node.outputs if s.type == 'GEOMETRY')
            to_socket = next(s for s in output_node.inputs if s.type == 'GEOMETRY')
            tree.links.new(to_socket, from_socket)

        return {'FINISHED'}


class NODE_OT_add_simulation_zone(NodeAddZoneOperator, Operator):
    """Add simulation zone input and output nodes to the active tree"""
    bl_idname = "node.add_simulation_zone"
    bl_label = "Add Simulation Zone"
    bl_options = {'REGISTER', 'UNDO'}

    input_node_type = "GeometryNodeSimulationInput"
    output_node_type = "GeometryNodeSimulationOutput"


class NODE_OT_add_repeat_zone(NodeAddZoneOperator, Operator):
    """Add a repeat zone that allows executing nodes a dynamic number of times"""
    bl_idname = "node.add_repeat_zone"
    bl_label = "Add Repeat Zone"
    bl_options = {'REGISTER', 'UNDO'}

    input_node_type = "GeometryNodeRepeatInput"
    output_node_type = "GeometryNodeRepeatOutput"


class NODE_OT_add_foreach_geometry_element_zone(NodeAddZoneOperator, Operator):
    """Add a For Each Geometry Element zone that allows executing nodes e.g. for each vertex separately"""
    bl_idname = "node.add_foreach_geometry_element_zone"
    bl_label = "Add For Each Geometry Element Zone"
    bl_options = {'REGISTER', 'UNDO'}

    input_node_type = "GeometryNodeForeachGeometryElementInput"
    output_node_type = "GeometryNodeForeachGeometryElementOutput"
    add_default_geometry_link = False


class NODE_OT_add_closure_zone(NodeAddZoneOperator, Operator):
    """Add a Closure zone"""
    bl_idname = "node.add_closure_zone"
    bl_label = "Add Closure Zone"
    bl_options = {'REGISTER', 'UNDO'}

    input_node_type = "GeometryNodeClosureInput"
    output_node_type = "GeometryNodeClosureOutput"
    add_default_geometry_link = False


class NODE_OT_collapse_hide_unused_toggle(Operator):
    """Toggle collapsed nodes and hide unused sockets"""
    bl_idname = "node.collapse_hide_unused_toggle"
    bl_label = "Collapse and Hide Unused Sockets"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        space = context.space_data
        # needs active node editor and a tree
        return (space and (space.type == 'NODE_EDITOR') and
                (space.edit_tree and space.edit_tree.is_editable))

    def execute(self, context):
        space = context.space_data
        tree = space.edit_tree

        for node in tree.nodes:
            if node.select:
                hide = (not node.hide)

                node.hide = hide
                # Note: connected sockets are ignored internally
                for socket in node.inputs:
                    socket.hide = hide
                for socket in node.outputs:
                    socket.hide = hide

        return {'FINISHED'}


class NODE_OT_tree_path_parent(Operator):
    """Go to parent node tree"""
    bl_idname = "node.tree_path_parent"
    bl_label = "Parent Node Tree"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        space = context.space_data
        # needs active node editor and a tree
        return (space and (space.type == 'NODE_EDITOR') and len(space.path) > 1)

    def execute(self, context):
        space = context.space_data

        space.path.pop()

        return {'FINISHED'}


class NodeInterfaceOperator():
    @classmethod
    def poll(cls, context):
        space = context.space_data
        if not space or space.type != 'NODE_EDITOR' or not space.edit_tree:
            return False
        if space.edit_tree.is_embedded_data:
            return False
        return True


class NODE_OT_interface_item_new(NodeInterfaceOperator, Operator):
    """Add a new item to the interface"""
    bl_idname = "node.interface_item_new"
    bl_label = "New Item"
    bl_options = {'REGISTER', 'UNDO'}

    def get_items(_self, context):
        snode = context.space_data
        tree = snode.edit_tree
        interface = tree.interface

        items = [
            ('INPUT', "Input", ""),
            ('OUTPUT', "Output", ""),
            ('PANEL', "Panel", ""),
        ]

        active_item = interface.active
        # Panels have the extra option to add a toggle.
        if active_item and active_item.item_type == 'PANEL':
            items.append(('PANEL_TOGGLE', "Panel Toggle", ""))

        return items

    item_type: EnumProperty(
        name="Item Type",
        description="Type of the item to create",
        items=get_items,
        default=0,
    )

    # Returns a valid socket type for the given tree or None.
    @staticmethod
    def find_valid_socket_type(tree):
        socket_type = 'NodeSocketFloat'
        # Socket type validation function is only available for custom
        # node trees. Assume that 'NodeSocketFloat' is valid for
        # built-in node tree types.
        if not hasattr(tree, "valid_socket_type") or tree.valid_socket_type(socket_type):
            return socket_type
        # Custom nodes may not support float sockets, search all
        # registered socket subclasses.
        types_to_check = [bpy.types.NodeSocket]
        while types_to_check:
            t = types_to_check.pop()
            idname = getattr(t, "bl_idname", "")
            if tree.valid_socket_type(idname):
                return idname
            # Test all subclasses
            types_to_check.extend(t.__subclasses__())

    def execute(self, context):
        snode = context.space_data
        tree = snode.edit_tree
        interface = tree.interface

        # Remember active item and position to determine target position.
        active_item = interface.active
        active_pos = active_item.position if active_item else -1

        if self.item_type == 'INPUT':
            item = interface.new_socket("Socket", socket_type=self.find_valid_socket_type(tree), in_out='INPUT')
        elif self.item_type == 'OUTPUT':
            item = interface.new_socket("Socket", socket_type=self.find_valid_socket_type(tree), in_out='OUTPUT')
        elif self.item_type == 'PANEL':
            item = interface.new_panel("Panel")
        elif self.item_type == 'PANEL_TOGGLE':
            active_panel = active_item
            if len(active_panel.interface_items) > 0:
                first_item = active_panel.interface_items[0]
                if type(first_item) is bpy.types.NodeTreeInterfaceSocketBool and first_item.is_panel_toggle:
                    self.report({'INFO'}, "Panel already has a toggle")
                    return {'CANCELLED'}
            item = interface.new_socket(active_panel.name, socket_type='NodeSocketBool', in_out='INPUT')
            item.is_panel_toggle = True
            interface.move_to_parent(item, active_panel, 0)
            # Return in this case because we don't want to move the item.
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

        if active_item:
            # Insert into active panel if possible, otherwise insert after active item.
            if active_item.item_type == 'PANEL' and item.item_type != 'PANEL':
                interface.move_to_parent(item, active_item, len(active_item.interface_items))
            else:
                interface.move_to_parent(item, active_item.parent, active_pos + 1)
        interface.active = item

        return {"FINISHED"}


class NODE_OT_interface_item_new_input(
    NODE_OT_interface_item_new
):  # -bfa separated add input operator with own description.
    """Add a new input socket"""

    bl_idname = "node.interface_item_new_input"
    bl_label = "New Input Socket"
    bl_options = {"REGISTER", "UNDO"}

    item_type: EnumProperty(
        name="Item Type", items=(("INPUT", "Input", ""),), default="INPUT"
    )


class NODE_OT_interface_item_new_panel(
    NODE_OT_interface_item_new
):  # -bfa separated add output operator with own description.
    """Add a new panel interface"""

    bl_idname = "node.interface_item_new_panel"
    bl_label = "New Panel Interface"
    bl_options = {"REGISTER", "UNDO"}

    item_type: EnumProperty(
        name="Item Type", items=(("PANEL", "Panel", ""),), default="PANEL"
    )


class NODE_OT_interface_item_new_output(
    NODE_OT_interface_item_new
):  # -bfa separated add panel operator with own description.
    """Add a new output socket"""

    bl_idname = "node.interface_item_new_output"
    bl_label = "New Output Socket"
    bl_options = {"REGISTER", "UNDO"}

    item_type: EnumProperty(
        name="Item Type", items=(("OUTPUT", "Output", ""),), default="OUTPUT"
    )

# BFA - Create dedicated operator for adding panel checkbox
class NODE_OT_interface_item_new_panel_toggle(Operator):
    '''Add a new panel toggle to the currently selected panel'''
    bl_idname = "node.interface_item_new_panel_toggle"
    bl_label = "New Panel Checkbox"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            snode = context.space_data
            tree = snode.edit_tree
            interface = tree.interface

            active_item = interface.active

            if active_item.item_type != 'PANEL':
                cls.poll_message_set("Active item is not a panel")
                return False
            
            if get_panel_toggle(active_item) is not None:
                cls.poll_message_set("Panel already has a toggle")
                return False
            
            return True
        except AttributeError:
            return False

    def execute(self, context):
        snode = context.space_data
        tree = snode.edit_tree

        interface = tree.interface
        active_panel = interface.active

        item = interface.new_socket(active_panel.name, socket_type='NodeSocketBool', in_out='INPUT')
        item.is_panel_toggle = True
        interface.move_to_parent(item, active_panel, 0)
        return {'FINISHED'}


class NODE_OT_interface_item_duplicate(NodeInterfaceOperator, Operator):
    """Add a copy of the active item to the interface"""
    bl_idname = "node.interface_item_duplicate"
    bl_label = "Duplicate Item"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not super().poll(context):
            return False

        snode = context.space_data
        tree = snode.edit_tree
        interface = tree.interface
        return interface.active is not None

    def execute(self, context):
        snode = context.space_data
        tree = snode.edit_tree
        interface = tree.interface
        item = interface.active

        if item:
            item_copy = interface.copy(item)
            interface.active = item_copy

        return {'FINISHED'}


class NODE_OT_interface_item_remove(NodeInterfaceOperator, Operator):
    """Remove active item from the interface"""
    bl_idname = "node.interface_item_remove"
    bl_label = "Remove Item"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        snode = context.space_data
        tree = snode.edit_tree
        interface = tree.interface
        item = interface.active

        if item:
            if item.item_type == 'PANEL':
                children = item.interface_items
                if len(children) > 0:
                    first_child = children[0]
                    if isinstance(first_child, bpy.types.NodeTreeInterfaceSocket) and first_child.is_panel_toggle:
                        interface.remove(first_child)
            interface.remove(item)
            interface.active_index = min(interface.active_index, len(interface.items_tree) - 1)

        return {'FINISHED'}


class NODE_OT_interface_item_make_panel_toggle(NodeInterfaceOperator, Operator):
    """Make the selected active boolean input socket a top-level toggle located in its parent panel""" # BFA

    bl_idname = "node.interface_item_make_panel_toggle"
    bl_label = "Make Panel Toggle"
    bl_options = {'REGISTER', 'UNDO'}

    # BFA - Make poll function easier to read through
    @classmethod
    def poll(cls, context):
        try:
            snode = context.space_data
            tree = snode.edit_tree
            active_item = tree.interface.active

            if not is_boolean_input(active_item):
                cls.poll_message_set("Active item is not a boolean input socket")
                return False

            panel = active_item.parent

            if panel.parent is None:
                cls.poll_message_set("Socket must be in a panel")
                return False
            
            if get_panel_toggle(panel) is not None:
                cls.poll_message_set("Panel already has a toggle")
                return False
                
            return True
            
        except AttributeError:
            return False

    def execute(self, context):
        snode = context.space_data
        tree = snode.edit_tree
        interface = tree.interface
        active_item = interface.active

        parent_panel = active_item.parent
        if not parent_panel:
            return {'CANCELLED'}

        if type(active_item) is not bpy.types.NodeTreeInterfaceSocketBool:
            return {'CANCELLED'}

        active_item.is_panel_toggle = True
        # Use the same name as the panel in the UI for clarity.
        active_item.name = parent_panel.name

        # Move the socket to the first position.
        interface.move_to_parent(active_item, parent_panel, 0)
        # Make the panel active.
        interface.active = parent_panel

        return {'FINISHED'}


class NODE_OT_interface_item_unlink_panel_toggle(NodeInterfaceOperator, Operator):
    """Make the panel toggle a stand-alone socket"""
    bl_idname = "node.interface_item_unlink_panel_toggle"
    bl_label = "Unlink Panel Toggle"
    bl_options = {'REGISTER', 'UNDO'}

    # BFA - Add proper poll messages when operator is not executable
    @classmethod
    def poll(cls, context):
        try:
            snode = context.space_data
            tree = snode.edit_tree
            active_item = tree.interface.active

            if active_item.item_type != 'PANEL':
                cls.poll_message_set("Active item is not a panel")
                return False

            if get_panel_toggle(active_item) is None:
                cls.poll_message_set("Panel does not have a toggle")
                return False
            
            return True

        except AttributeError:
            return False

    def execute(self, context):
        snode = context.space_data
        tree = snode.edit_tree
        interface = tree.interface
        active_item = interface.active

        if not active_item or active_item.item_type != 'PANEL':
            return {'CANCELLED'}

        if len(active_item.interface_items) == 0:
            return {'CANCELLED'}

        first_item = active_item.interface_items[0]
        if type(first_item) is not bpy.types.NodeTreeInterfaceSocketBool or not first_item.is_panel_toggle:
            return {'CANCELLED'}

        first_item.is_panel_toggle = False
        first_item.name = active_item.name

        # Make the socket active.
        interface.active = first_item

        return {"FINISHED"}


## BFA - BFA operator for GUI buttons to re-order items - Start
class NODE_OT_interface_item_move(NodeInterfaceOperator, Operator):
    """Move the active item to the specified direction\nYou can also alternatively drag and drop the active item to reorder"""

    bl_idname = "node.interface_item_move"
    bl_label = "Move Item"
    bl_options = {"REGISTER", "UNDO"}

    direction: EnumProperty(
        name="Direction",
        description="Specifies which direction the active item is moved towards",
        items=(("UP", "Move Up", ""), ("DOWN", "Move Down", "")),
    )

    @classmethod
    def poll(cls, context):
        if not super().poll(context):
            return False

        snode = context.space_data
        tree = snode.edit_tree
        interface = tree.interface
        return interface.active is not None

    def should_change_parents(self, active_item):
        similar_items = get_similar_items(active_item)
        last_index = (len(similar_items) - 1)
        in_base_panel = active_item.parent.parent is None

        for i, item in enumerate(similar_items):
            if item == active_item:
                break

        if is_panel(active_item):
            if self.direction == "UP":
                return not (i == 0) or not in_base_panel
            elif self.direction == "DOWN":
                return not (i == last_index) or not in_base_panel
        else:
            if self.direction == "UP":
                return i == 0 and not in_base_panel
            elif self.direction == "DOWN":
                return i == last_index 
    
    @staticmethod
    def adjacent_panel(panel, direction):
        if panel.parent is None:
            return None

        items = filter(is_panel, panel.parent.interface_items)

        try:
            import itertools
            if direction == "UP":
                return next(i[0] for i in itertools.pairwise(items) if i[1] == panel)
            elif direction == "DOWN":
                return next(i[1] for i in itertools.pairwise(items) if i[0] == panel)
        except StopIteration:
            return None
        
    @staticmethod
    def endpoint_panel(panel, direction):
        items = panel.interface_items

        try:
            if direction == "UP":
                return next(i for i in filter(is_panel, reversed(items)))
            elif direction == "DOWN":
                return next(i for i in filter(is_panel, items))
        except StopIteration:
            return None
        
    def next_panel_up(self, panel):
        while True:
            target = panel
            panel = self.endpoint_panel(target, self.direction)
            
            if panel is None:
                return target

    def next_panel_down(self, panel):
        target = panel
        while True:
            if target.parent is None:
                return None

            panel = self.adjacent_panel(target, self.direction)
            if panel is not None:
                return panel
            
            target = target.parent

    def get_nearest_panel_up(self, active_item):
        if is_panel(active_item):
            target = self.adjacent_panel(active_item, self.direction)
            if target is not None:
                return target
        else:
            target = self.adjacent_panel(active_item.parent, self.direction)
            if target is not None:
                return self.next_panel_up(target)

        return active_item.parent.parent

    def get_nearest_panel_down(self, active_item):
        if is_panel(active_item):
            target = self.adjacent_panel(active_item, self.direction)
            if target is None:
                return active_item.parent.parent
        else:
            target = self.endpoint_panel(active_item.parent, self.direction)
            if target is None:
                return self.next_panel_down(active_item)
            
        return target

    def execute(self, context):
        snode = context.space_data
        tree = snode.edit_tree
        interface = tree.interface
        active_item = interface.active

        offset = -1 if self.direction == 'UP' else 2

        if not self.should_change_parents(active_item):
            old_position = active_item.position
            interface.move(active_item, active_item.position + offset)

            if old_position == active_item.position:
                return {'CANCELLED'}

            interface.active_index = active_item.index
            return {'FINISHED'}

        if self.direction == "UP":
            target_panel = self.get_nearest_panel_up(active_item)
            if is_panel(active_item) and (target_panel == active_item.parent.parent):
                target_index = active_item.parent.position
            else:
                target_index = len(target_panel.interface_items)
            
        elif self.direction == "DOWN":
            target_panel = self.get_nearest_panel_down(active_item)
            if is_panel(active_item) and (target_panel == active_item.parent.parent):
                target_index = active_item.parent.position + 1
            else:
                has_panel_toggle = get_panel_toggle(target_panel) is not None
                target_index = has_panel_toggle

        if target_panel is None:
            return {'CANCELLED'}
        
        interface.move_to_parent(active_item, target_panel, target_index)
        interface.active_index = active_item.index
        return {'FINISHED'}


## BFA - BFA operator for GUI buttons to re-order items - End


class NODE_OT_viewer_shortcut_set(Operator):
    """Create a compositor viewer shortcut for the selected node by pressing ctrl+1,2,..9"""
    bl_idname = "node.viewer_shortcut_set"
    bl_label = "Fast Preview"
    bl_options = {'REGISTER', 'UNDO'}

    viewer_index: IntProperty(
        name="Viewer Index",
        description="Index corresponding to the shortcut, e.g. number key 1 corresponds to index 1 etc..")

    def get_connected_viewer(self, node):
        for out in node.outputs:
            for link in out.links:
                nv = link.to_node
                if nv.type == 'VIEWER':
                    return nv
        return None

    @classmethod
    def poll(cls, context):
        del cls
        space = context.space_data
        return (
            (space is not None) and
            space.type == 'NODE_EDITOR' and
            space.node_tree is not None and
            space.tree_type in {'CompositorNodeTree', 'GeometryNodeTree'}
        )

    def execute(self, context):
        selected_nodes = context.selected_nodes

        if len(selected_nodes) == 0:
            self.report({'ERROR'}, "Select a node to assign a shortcut")
            return {'CANCELLED'}

        fav_node = selected_nodes[0]

        # Only viewer nodes can be set to favorites. However, the user can
        # create a new favorite viewer by selecting any node and pressing ctrl+1.
        if fav_node.type == 'VIEWER':
            viewer_node = fav_node
        else:
            viewer_node = self.get_connected_viewer(fav_node)
            if not viewer_node:
                # Calling `link_viewer()` if a viewer node is connected
                # will connect the next available socket to the viewer node.
                # This behavior is not desired as we want to create a shortcut to the existing connected viewer node.
                # Therefore `link_viewer()` is called only when no viewer node is connected.
                bpy.ops.node.link_viewer()
                viewer_node = self.get_connected_viewer(fav_node)

        if not viewer_node:
            self.report(
                {'ERROR'},
                "Unable to set shortcut, selected node is not a viewer node or does not support viewing",
            )
            return {'CANCELLED'}

        with bpy.context.temp_override(node=viewer_node):
            bpy.ops.node.activate_viewer()

        viewer_node.ui_shortcut = self.viewer_index
        self.report({'INFO'}, rpt_("Assigned shortcut {:d} to {:s}").format(self.viewer_index, viewer_node.name))

        return {'FINISHED'}


class NODE_OT_viewer_shortcut_get(Operator):
    """Activate a specific compositor viewer node using 1,2,..,9 keys"""
    bl_idname = "node.viewer_shortcut_get"
    bl_label = "Fast Preview"
    bl_options = {'REGISTER', 'UNDO'}

    viewer_index: IntProperty(
        name="Viewer Index",
        description="Index corresponding to the shortcut, e.g. number key 1 corresponds to index 1 etc..")

    @classmethod
    def poll(cls, context):
        del cls
        space = context.space_data
        return (
            (space is not None) and
            space.type == 'NODE_EDITOR' and
            space.node_tree is not None and
            space.tree_type in {'CompositorNodeTree', 'GeometryNodeTree'}
        )

    def execute(self, context):
        nodes = context.space_data.edit_tree.nodes

        # Get viewer node with existing shortcut.
        viewer_node = None
        for n in nodes:
            if n.type == 'VIEWER' and n.ui_shortcut == self.viewer_index:
                viewer_node = n

        if not viewer_node:
            self.report({'INFO'}, rpt_("Shortcut {:d} is not assigned to a Viewer node yet").format(self.viewer_index))
            return {'CANCELLED'}

        with bpy.context.temp_override(node=viewer_node):
            bpy.ops.node.activate_viewer()

        return {'FINISHED'}


class NODE_FH_image_node(FileHandler):
    bl_idname = "NODE_FH_image_node"
    bl_label = "Image node"
    bl_import_operator = "node.add_image"
    bl_file_extensions = ";".join((*bpy.path.extensions_image, *bpy.path.extensions_movie))

    @classmethod
    def poll_drop(cls, context):
        return (
            (context.area is not None) and
            (context.area.type == 'NODE_EDITOR') and
            (context.region is not None) and
            (context.region.type == 'WINDOW')
        )


classes = (
    NodeSetting,

    NODE_FH_image_node,

    NODE_OT_add_empty_group,
    NODE_OT_add_node,
    NODE_OT_add_simulation_zone,
    NODE_OT_add_repeat_zone,
    NODE_OT_add_foreach_geometry_element_zone,
    NODE_OT_add_closure_zone,
    NODE_OT_collapse_hide_unused_toggle,
    NODE_OT_interface_item_new_input,  # BFA separated add input operator with own description.
    NODE_OT_interface_item_new_output,  # BFA separated add output operator with own description.
    NODE_OT_interface_item_new_panel,  # BFA separated add panel operator with own description.
    NODE_OT_interface_item_new_panel_toggle, # BFA - Create dedicated operator with separate poll function.
    NODE_OT_interface_item_duplicate,
    NODE_OT_interface_item_remove,
    NODE_OT_interface_item_make_panel_toggle,
    NODE_OT_interface_item_unlink_panel_toggle,
    NODE_OT_interface_item_move,  # BFA operator for GUI buttons to re-order items
    NODE_OT_tree_path_parent,
    NODE_OT_viewer_shortcut_get,
    NODE_OT_viewer_shortcut_set,
)
