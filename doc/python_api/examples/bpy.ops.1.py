"""
Overriding Context
------------------

It is possible to override context members that the operator sees, so that they
act on specified rather than the selected or active data, or to execute an
operator in the different part of the user interface.

The context overrides are passed in as keyword arguments,
with keywords matching the context member names in ``bpy.context``.
For example to override ``bpy.context.active_object``,
you would pass ``active_object=object`` to :class:`bpy.types.Context.temp_override`.

.. note::

   You will nearly always want to use a copy of the actual current context as basis
   (otherwise, you'll have to find and gather all needed data yourself).

.. note::

   Context members are names which Blender uses for data access,
   overrides do not extend to overriding methods or any Python specific functionality.
"""

# Remove all objects in scene rather than the selected ones.
import bpy
from bpy import context
context_override = context.copy()
context_override["selected_objects"] = list(context.scene.objects)
with context.temp_override(**context_override):
    bpy.ops.object.delete()
