/* SPDX-FileCopyrightText: 2023 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

/** \file
 * \ingroup RNA
 */

#include "BKE_attribute.h"
#include "BKE_global.hh"

#include "BLI_string.h"

#include "DNA_grease_pencil_types.h"

#include "RNA_access.hh"
#include "RNA_define.hh"
#include "RNA_enum_types.hh"

#include "rna_internal.hh"

#include "WM_api.hh"

const EnumPropertyItem rna_enum_tree_node_move_type_items[] = {
    {-1, "DOWN", 0, "Down", ""},
    {1, "UP", 0, "Up", ""},
    {0, nullptr, 0, nullptr, nullptr},
};

#ifdef RNA_RUNTIME

#  include <fmt/format.h>

#  include "BKE_attribute.hh"
#  include "BKE_grease_pencil.hh"

#  include "BLI_math_matrix.hh"
#  include "BLI_span.hh"

#  include "DEG_depsgraph.hh"
#  include "DEG_depsgraph_build.hh"

static GreasePencil *rna_grease_pencil(const PointerRNA *ptr)
{
  return reinterpret_cast<GreasePencil *>(ptr->owner_id);
}

static void rna_grease_pencil_update(Main * /*bmain*/, Scene * /*scene*/, PointerRNA *ptr)
{
  DEG_id_tag_update(&rna_grease_pencil(ptr)->id, ID_RECALC_GEOMETRY);
  WM_main_add_notifier(NC_GPENCIL | NA_EDITED, rna_grease_pencil(ptr));
}

static void rna_grease_pencil_autolock(Main * /*bmain*/, Scene * /*scene*/, PointerRNA *ptr)
{
  using namespace blender::bke::greasepencil;
  GreasePencil *grease_pencil = rna_grease_pencil(ptr);
  if (grease_pencil->flag & GREASE_PENCIL_AUTOLOCK_LAYERS) {
    grease_pencil->autolock_inactive_layers();
  }
  else {
    for (Layer *layer : grease_pencil->layers_for_write()) {
      layer->set_locked(false);
    }
  }

  rna_grease_pencil_update(nullptr, nullptr, ptr);
}

static void rna_grease_pencil_dependency_update(Main *bmain, Scene * /*scene*/, PointerRNA *ptr)
{
  DEG_id_tag_update(&rna_grease_pencil(ptr)->id, ID_RECALC_GEOMETRY);
  DEG_relations_tag_update(bmain);
  WM_main_add_notifier(NC_GPENCIL | NA_EDITED, rna_grease_pencil(ptr));
}

static void rna_grease_pencil_layer_mask_name_get(PointerRNA *ptr, char *dst)
{
  using namespace blender;
  GreasePencilLayerMask *mask = static_cast<GreasePencilLayerMask *>(ptr->data);
  if (mask->layer_name != nullptr) {
    strcpy(dst, mask->layer_name);
  }
  else {
    dst[0] = '\0';
  }
}

static int rna_grease_pencil_layer_mask_name_length(PointerRNA *ptr)
{
  using namespace blender;
  GreasePencilLayerMask *mask = static_cast<GreasePencilLayerMask *>(ptr->data);
  if (mask->layer_name != nullptr) {
    return strlen(mask->layer_name);
  }
  return 0;
}

static void rna_grease_pencil_layer_mask_name_set(PointerRNA *ptr, const char *value)
{
  using namespace blender;
  GreasePencil *grease_pencil = rna_grease_pencil(ptr);
  GreasePencilLayerMask *mask = static_cast<GreasePencilLayerMask *>(ptr->data);

  const std::string oldname(mask->layer_name);
  if (bke::greasepencil::TreeNode *node = grease_pencil->find_node_by_name(oldname)) {
    grease_pencil->rename_node(*G_MAIN, *node, value);
  }
}

static int rna_grease_pencil_active_mask_index_get(PointerRNA *ptr)
{
  GreasePencilLayer *layer = static_cast<GreasePencilLayer *>(ptr->data);
  return layer->active_mask_index;
}

static void rna_grease_pencil_active_mask_index_set(PointerRNA *ptr, int value)
{
  GreasePencilLayer *layer = static_cast<GreasePencilLayer *>(ptr->data);
  layer->active_mask_index = value;
}

static void rna_grease_pencil_active_mask_index_range(
    PointerRNA *ptr, int *min, int *max, int * /*softmin*/, int * /*softmax*/)
{
  GreasePencilLayer *layer = static_cast<GreasePencilLayer *>(ptr->data);
  *min = 0;
  *max = max_ii(0, BLI_listbase_count(&layer->masks) - 1);
}

static void rna_iterator_grease_pencil_layers_begin(CollectionPropertyIterator *iter,
                                                    PointerRNA *ptr)
{
  using namespace blender::bke::greasepencil;
  GreasePencil *grease_pencil = rna_grease_pencil(ptr);
  blender::Span<Layer *> layers = grease_pencil->layers_for_write();

  rna_iterator_array_begin(
      iter, (void *)layers.data(), sizeof(Layer *), layers.size(), 0, nullptr);
}

static int rna_iterator_grease_pencil_layers_length(PointerRNA *ptr)
{
  GreasePencil *grease_pencil = rna_grease_pencil(ptr);
  return grease_pencil->layers().size();
}

static void tree_node_name_get(blender::bke::greasepencil::TreeNode &node, char *dst)
{
  if (!node.name().is_empty()) {
    strcpy(dst, node.name().c_str());
  }
  else {
    dst[0] = '\0';
  }
}

static int tree_node_name_length(blender::bke::greasepencil::TreeNode &node)
{
  if (!node.name().is_empty()) {
    return node.name().size();
  }
  return 0;
}

static std::optional<std::string> tree_node_name_path(blender::bke::greasepencil::TreeNode &node,
                                                      const char *prefix)
{
  using namespace blender::bke::greasepencil;
  BLI_assert(!node.name().is_empty());
  const size_t name_length = node.name().size();
  std::string name_esc(name_length * 2, '\0');
  BLI_str_escape(name_esc.data(), node.name().c_str(), name_length * 2);
  return fmt::format("{}[\"{}\"]", prefix, name_esc.c_str());
}

static std::optional<std::string> rna_GreasePencilLayer_path(const PointerRNA *ptr)
{
  GreasePencilLayer *layer = static_cast<GreasePencilLayer *>(ptr->data);
  return tree_node_name_path(layer->wrap().as_node(), "layers");
}

static void rna_GreasePencilLayer_name_get(PointerRNA *ptr, char *value)
{
  GreasePencilLayer *layer = static_cast<GreasePencilLayer *>(ptr->data);
  tree_node_name_get(layer->wrap().as_node(), value);
}

static int rna_GreasePencilLayer_name_length(PointerRNA *ptr)
{
  GreasePencilLayer *layer = static_cast<GreasePencilLayer *>(ptr->data);
  return tree_node_name_length(layer->wrap().as_node());
}

static void rna_GreasePencilLayer_name_set(PointerRNA *ptr, const char *value)
{
  GreasePencil *grease_pencil = rna_grease_pencil(ptr);
  GreasePencilLayer *layer = static_cast<GreasePencilLayer *>(ptr->data);

  grease_pencil->rename_node(*G_MAIN, layer->wrap().as_node(), value);
}

static int rna_GreasePencilLayer_pass_index_get(PointerRNA *ptr)
{
  using namespace blender;
  const GreasePencil &grease_pencil = *rna_grease_pencil(ptr);
  const bke::greasepencil::Layer &layer =
      static_cast<const GreasePencilLayer *>(ptr->data)->wrap();
  const int layer_idx = *grease_pencil.get_layer_index(layer);

  const VArray layer_passes = *grease_pencil.attributes().lookup_or_default<int>(
      "pass_index", bke::AttrDomain::Layer, 0);
  return layer_passes[layer_idx];
}

static void rna_GreasePencilLayer_pass_index_set(PointerRNA *ptr, int value)
{
  using namespace blender;
  GreasePencil &grease_pencil = *rna_grease_pencil(ptr);
  const bke::greasepencil::Layer &layer =
      static_cast<const GreasePencilLayer *>(ptr->data)->wrap();
  const int layer_idx = *grease_pencil.get_layer_index(layer);

  bke::SpanAttributeWriter<int> layer_passes =
      grease_pencil.attributes_for_write().lookup_or_add_for_write_span<int>(
          "pass_index", bke::AttrDomain::Layer);
  layer_passes.span[layer_idx] = std::max(0, value);
  layer_passes.finish();
}

static void rna_GreasePencilLayer_matrix_local_get(PointerRNA *ptr, float *values)
{
  const blender::bke::greasepencil::Layer &layer =
      static_cast<const GreasePencilLayer *>(ptr->data)->wrap();
  std::copy_n(layer.local_transform().base_ptr(), 16, values);
}

static void rna_GreasePencilLayer_matrix_parent_inverse_get(PointerRNA *ptr, float *values)
{
  const blender::bke::greasepencil::Layer &layer =
      static_cast<const GreasePencilLayer *>(ptr->data)->wrap();
  std::copy_n(layer.parent_inverse().base_ptr(), 16, values);
}

static PointerRNA rna_GreasePencilLayer_parent_layer_group_get(PointerRNA *ptr)
{
  blender::bke::greasepencil::Layer &layer = static_cast<GreasePencilLayer *>(ptr->data)->wrap();
  blender::bke::greasepencil::LayerGroup *layer_group = &layer.parent_group();
  /* Return None when layer is in the root group. */
  if (!layer_group->as_node().parent_group()) {
    return PointerRNA_NULL;
  }
  return rna_pointer_inherit_refine(
      ptr, &RNA_GreasePencilLayerGroup, static_cast<void *>(layer_group));
}

static PointerRNA rna_GreasePencil_layer_group_new(GreasePencil *grease_pencil,
                                                   const char *name,
                                                   PointerRNA *parent_group_ptr)
{
  using namespace blender::bke::greasepencil;
  LayerGroup *parent_group;
  if (parent_group_ptr && parent_group_ptr->data) {
    parent_group = static_cast<LayerGroup *>(parent_group_ptr->data);
  }
  else {
    parent_group = &grease_pencil->root_group();
  }
  LayerGroup *new_layer_group = &grease_pencil->add_layer_group(*parent_group, name);

  WM_main_add_notifier(NC_GPENCIL | NA_EDITED, grease_pencil);

  PointerRNA ptr = RNA_pointer_create(
      &grease_pencil->id, &RNA_GreasePencilLayerGroup, new_layer_group);
  return ptr;
}

static void rna_GreasePencil_layer_group_remove(GreasePencil *grease_pencil,
                                                PointerRNA *layer_group_ptr,
                                                bool keep_children)
{
  using namespace blender::bke::greasepencil;
  LayerGroup &layer_group = *static_cast<LayerGroup *>(layer_group_ptr->data);
  grease_pencil->remove_group(layer_group, keep_children);

  RNA_POINTER_INVALIDATE(layer_group_ptr);
  DEG_id_tag_update(&grease_pencil->id, ID_RECALC_GEOMETRY);
  WM_main_add_notifier(NC_GPENCIL | ND_DATA | NA_SELECTED, grease_pencil);
}

static void rna_GreasePencil_layer_group_move(GreasePencil *grease_pencil,
                                              PointerRNA *layer_group_ptr,
                                              int direction)
{
  if (direction == 0) {
    return;
  }

  blender::bke::greasepencil::TreeNode &layer_group_node =
      static_cast<blender::bke::greasepencil::LayerGroup *>(layer_group_ptr->data)->as_node();
  switch (direction) {
    case -1:
      grease_pencil->move_node_down(layer_group_node, 1);
      break;
    case 1:
      grease_pencil->move_node_up(layer_group_node, 1);
      break;
  }

  DEG_id_tag_update(&grease_pencil->id, ID_RECALC_GEOMETRY);
  WM_main_add_notifier(NC_GPENCIL | NA_EDITED, grease_pencil);
}

static void rna_GreasePencil_layer_group_move_top(GreasePencil *grease_pencil,
                                                  PointerRNA *layer_group_ptr)
{
  blender::bke::greasepencil::TreeNode &layer_group_node =
      static_cast<blender::bke::greasepencil::LayerGroup *>(layer_group_ptr->data)->as_node();
  grease_pencil->move_node_top(layer_group_node);

  DEG_id_tag_update(&grease_pencil->id, ID_RECALC_GEOMETRY);
  WM_main_add_notifier(NC_GPENCIL | NA_EDITED, grease_pencil);
}

static void rna_GreasePencil_layer_group_move_bottom(GreasePencil *grease_pencil,
                                                     PointerRNA *layer_group_ptr)
{
  blender::bke::greasepencil::TreeNode &layer_group_node =
      static_cast<blender::bke::greasepencil::LayerGroup *>(layer_group_ptr->data)->as_node();
  grease_pencil->move_node_bottom(layer_group_node);

  DEG_id_tag_update(&grease_pencil->id, ID_RECALC_GEOMETRY);
  WM_main_add_notifier(NC_GPENCIL | NA_EDITED, grease_pencil);
}

static void rna_GreasePencil_layer_group_move_to_layer_group(GreasePencil *grease_pencil,
                                                             PointerRNA *layer_group_ptr,
                                                             PointerRNA *parent_group_ptr)
{
  using namespace blender::bke::greasepencil;
  TreeNode &layer_group_node = static_cast<LayerGroup *>(layer_group_ptr->data)->as_node();
  LayerGroup *parent_group;
  if (parent_group_ptr && parent_group_ptr->data) {
    parent_group = static_cast<LayerGroup *>(parent_group_ptr->data);
  }
  else {
    parent_group = &grease_pencil->root_group();
  }
  grease_pencil->move_node_into(layer_group_node, *parent_group);

  DEG_id_tag_update(&grease_pencil->id, ID_RECALC_GEOMETRY);
  WM_main_add_notifier(NC_GPENCIL | NA_EDITED, grease_pencil);
}

static GreasePencilLayer *rna_GreasePencil_layer_new(GreasePencil *grease_pencil,
                                                     const char *name,
                                                     const bool set_active,
                                                     PointerRNA *layer_group_ptr)
{
  using namespace blender::bke::greasepencil;
  LayerGroup *layer_group = nullptr;
  if (layer_group_ptr && layer_group_ptr->data) {
    layer_group = static_cast<LayerGroup *>(layer_group_ptr->data);
  }
  Layer *layer;
  if (layer_group) {
    layer = &grease_pencil->add_layer(*layer_group, name);
  }
  else {
    layer = &grease_pencil->add_layer(name);
  }
  if (set_active) {
    grease_pencil->set_active_layer(layer);
  }

  WM_main_add_notifier(NC_GPENCIL | NA_EDITED, grease_pencil);

  return layer;
}

static void rna_GreasePencil_layer_remove(GreasePencil *grease_pencil, PointerRNA *layer_ptr)
{
  blender::bke::greasepencil::Layer &layer = *static_cast<blender::bke::greasepencil::Layer *>(
      layer_ptr->data);
  grease_pencil->remove_layer(layer);

  RNA_POINTER_INVALIDATE(layer_ptr);
  DEG_id_tag_update(&grease_pencil->id, ID_RECALC_GEOMETRY);
  WM_main_add_notifier(NC_GPENCIL | ND_DATA | NA_SELECTED, grease_pencil);
}

static void rna_GreasePencil_layer_move(GreasePencil *grease_pencil,
                                        PointerRNA *layer_ptr,
                                        const int direction)
{
  if (direction == 0) {
    return;
  }

  blender::bke::greasepencil::TreeNode &layer_node =
      static_cast<blender::bke::greasepencil::Layer *>(layer_ptr->data)->as_node();
  switch (direction) {
    case -1:
      grease_pencil->move_node_down(layer_node, 1);
      break;
    case 1:
      grease_pencil->move_node_up(layer_node, 1);
      break;
  }

  DEG_id_tag_update(&grease_pencil->id, ID_RECALC_GEOMETRY);
  WM_main_add_notifier(NC_GPENCIL | NA_EDITED, grease_pencil);
}

static void rna_GreasePencil_layer_move_top(GreasePencil *grease_pencil, PointerRNA *layer_ptr)
{
  blender::bke::greasepencil::TreeNode &layer_node =
      static_cast<blender::bke::greasepencil::Layer *>(layer_ptr->data)->as_node();
  grease_pencil->move_node_top(layer_node);

  DEG_id_tag_update(&grease_pencil->id, ID_RECALC_GEOMETRY);
  WM_main_add_notifier(NC_GPENCIL | NA_EDITED, grease_pencil);
}

static void rna_GreasePencil_layer_move_bottom(GreasePencil *grease_pencil, PointerRNA *layer_ptr)
{
  blender::bke::greasepencil::TreeNode &layer_node =
      static_cast<blender::bke::greasepencil::Layer *>(layer_ptr->data)->as_node();
  grease_pencil->move_node_bottom(layer_node);

  DEG_id_tag_update(&grease_pencil->id, ID_RECALC_GEOMETRY);
  WM_main_add_notifier(NC_GPENCIL | NA_EDITED, grease_pencil);
}

static void rna_GreasePencil_layer_move_to_layer_group(GreasePencil *grease_pencil,
                                                       PointerRNA *layer_ptr,
                                                       PointerRNA *layer_group_ptr)
{
  using namespace blender::bke::greasepencil;
  TreeNode &layer_node = static_cast<Layer *>(layer_ptr->data)->as_node();
  LayerGroup *layer_group;
  if (layer_group_ptr && layer_group_ptr->data) {
    layer_group = static_cast<LayerGroup *>(layer_group_ptr->data);
  }
  else {
    layer_group = &grease_pencil->root_group();
  }
  if (layer_group == nullptr) {
    return;
  }
  grease_pencil->move_node_into(layer_node, *layer_group);

  DEG_id_tag_update(&grease_pencil->id, ID_RECALC_GEOMETRY);
  WM_main_add_notifier(NC_GPENCIL | NA_EDITED, grease_pencil);
}

static PointerRNA rna_GreasePencil_active_layer_get(PointerRNA *ptr)
{
  GreasePencil *grease_pencil = rna_grease_pencil(ptr);
  if (grease_pencil->has_active_layer()) {
    return rna_pointer_inherit_refine(
        ptr, &RNA_GreasePencilLayer, static_cast<void *>(grease_pencil->get_active_layer()));
  }
  return rna_pointer_inherit_refine(ptr, nullptr, nullptr);
}

static void rna_GreasePencil_active_layer_set(PointerRNA *ptr,
                                              PointerRNA value,
                                              ReportList * /*reports*/)
{
  GreasePencil *grease_pencil = rna_grease_pencil(ptr);
  grease_pencil->set_active_layer(static_cast<blender::bke::greasepencil::Layer *>(value.data));
  WM_main_add_notifier(NC_GPENCIL | NA_EDITED | NA_SELECTED, grease_pencil);
}

static PointerRNA rna_GreasePencil_active_group_get(PointerRNA *ptr)
{
  GreasePencil *grease_pencil = rna_grease_pencil(ptr);
  if (grease_pencil->has_active_group()) {
    return rna_pointer_inherit_refine(
        ptr, &RNA_GreasePencilLayerGroup, static_cast<void *>(grease_pencil->get_active_group()));
  }
  return rna_pointer_inherit_refine(ptr, nullptr, nullptr);
}

static void rna_GreasePencil_active_group_set(PointerRNA *ptr,
                                              PointerRNA value,
                                              ReportList * /*reports*/)
{
  using namespace blender::bke::greasepencil;
  GreasePencil *grease_pencil = rna_grease_pencil(ptr);
  TreeNode *node = static_cast<TreeNode *>(value.data);
  if (node->is_group()) {
    grease_pencil->set_active_node(node);
    WM_main_add_notifier(NC_GPENCIL | NA_EDITED | NA_SELECTED, grease_pencil);
  }
}

static std::optional<std::string> rna_GreasePencilLayerGroup_path(const PointerRNA *ptr)
{
  GreasePencilLayerTreeGroup *group = static_cast<GreasePencilLayerTreeGroup *>(ptr->data);
  return tree_node_name_path(group->wrap().as_node(), "layer_groups");
}

static void rna_GreasePencilLayerGroup_name_get(PointerRNA *ptr, char *value)
{
  GreasePencilLayerTreeGroup *group = static_cast<GreasePencilLayerTreeGroup *>(ptr->data);
  tree_node_name_get(group->wrap().as_node(), value);
}

static int rna_GreasePencilLayerGroup_name_length(PointerRNA *ptr)
{
  GreasePencilLayerTreeGroup *group = static_cast<GreasePencilLayerTreeGroup *>(ptr->data);
  return tree_node_name_length(group->wrap().as_node());
}

static void rna_GreasePencilLayerGroup_name_set(PointerRNA *ptr, const char *value)
{
  GreasePencil *grease_pencil = rna_grease_pencil(ptr);
  GreasePencilLayerTreeGroup *group = static_cast<GreasePencilLayerTreeGroup *>(ptr->data);

  grease_pencil->rename_node(*G_MAIN, group->wrap().as_node(), value);
}

static void rna_iterator_grease_pencil_layer_groups_begin(CollectionPropertyIterator *iter,
                                                          PointerRNA *ptr)
{
  using namespace blender::bke::greasepencil;
  GreasePencil *grease_pencil = rna_grease_pencil(ptr);

  blender::Span<LayerGroup *> groups = grease_pencil->layer_groups_for_write();

  rna_iterator_array_begin(
      iter, (void *)groups.data(), sizeof(LayerGroup *), groups.size(), 0, nullptr);
}

static int rna_iterator_grease_pencil_layer_groups_length(PointerRNA *ptr)
{
  GreasePencil *grease_pencil = rna_grease_pencil(ptr);
  return grease_pencil->layer_groups().size();
}

#else

static void rna_def_grease_pencil_layers_mask_api(BlenderRNA *brna, PropertyRNA *cprop)
{
  StructRNA *srna;
  PropertyRNA *prop;

  RNA_def_property_srna(cprop, "GreasePencilLayerMasks");
  srna = RNA_def_struct(brna, "GreasePencilLayerMasks", nullptr);
  RNA_def_struct_sdna(srna, "GreasePencilLayer");
  RNA_def_struct_ui_text(
      srna, "Grease Pencil Mask Layers", "Collection of grease pencil masking layers");

  prop = RNA_def_property(srna, "active_mask_index", PROP_INT, PROP_UNSIGNED);
  RNA_def_property_clear_flag(prop, PROP_ANIMATABLE);
  RNA_def_property_int_funcs(prop,
                             "rna_grease_pencil_active_mask_index_get",
                             "rna_grease_pencil_active_mask_index_set",
                             "rna_grease_pencil_active_mask_index_range");
  RNA_def_property_ui_text(prop, "Active Layer Mask Index", "Active index in layer mask array");
}

static void rna_def_grease_pencil_layer_mask(BlenderRNA *brna)
{
  StructRNA *srna;
  PropertyRNA *prop;

  srna = RNA_def_struct(brna, "GreasePencilLayerMask", nullptr);
  RNA_def_struct_sdna(srna, "GreasePencilLayerMask");
  RNA_def_struct_ui_text(srna, "Grease Pencil Masking Layers", "List of Mask Layers");
  // RNA_def_struct_path_func(srna, "rna_GreasePencilLayerMask_path");

  prop = RNA_def_property(srna, "name", PROP_STRING, PROP_NONE);
  RNA_def_property_ui_text(prop, "Layer", "Mask layer name");
  RNA_def_property_string_sdna(prop, nullptr, "layer_name");
  RNA_def_property_string_funcs(prop,
                                "rna_grease_pencil_layer_mask_name_get",
                                "rna_grease_pencil_layer_mask_name_length",
                                "rna_grease_pencil_layer_mask_name_set");
  RNA_def_struct_name_property(srna, prop);
  RNA_def_property_clear_flag(prop, PROP_ANIMATABLE);
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA | NA_RENAME, nullptr);

  prop = RNA_def_property(srna, "hide", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(prop, nullptr, "flag", GP_LAYER_MASK_HIDE);
  RNA_def_property_ui_icon(prop, ICON_HIDE_OFF, -1);
  RNA_def_property_ui_text(prop, "Hide", "Set mask Visibility");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "invert", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(prop, nullptr, "flag", GP_LAYER_MASK_INVERT);
  RNA_def_property_ui_icon(prop, ICON_SELECT_INTERSECT, 1);
  RNA_def_property_ui_text(prop, "Invert", "Invert mask");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");
}

static void rna_def_grease_pencil_layer(BlenderRNA *brna)
{
  StructRNA *srna;
  PropertyRNA *prop;

  static const float scale_defaults[3] = {1.0f, 1.0f, 1.0f};

  static const EnumPropertyItem rna_enum_layer_blend_modes_items[] = {
      {GP_LAYER_BLEND_NONE, "REGULAR", 0, "Regular", ""},
      {GP_LAYER_BLEND_HARDLIGHT, "HARDLIGHT", 0, "Hard Light", ""},
      {GP_LAYER_BLEND_ADD, "ADD", 0, "Add", ""},
      {GP_LAYER_BLEND_SUBTRACT, "SUBTRACT", 0, "Subtract", ""},
      {GP_LAYER_BLEND_MULTIPLY, "MULTIPLY", 0, "Multiply", ""},
      {GP_LAYER_BLEND_DIVIDE, "DIVIDE", 0, "Divide", ""},
      {0, nullptr, 0, nullptr, nullptr}};

  srna = RNA_def_struct(brna, "GreasePencilLayer", nullptr);
  RNA_def_struct_sdna(srna, "GreasePencilLayer");
  RNA_def_struct_ui_text(srna, "Grease Pencil Layer", "Collection of related drawings");
  RNA_def_struct_path_func(srna, "rna_GreasePencilLayer_path");

  /* Name */
  prop = RNA_def_property(srna, "name", PROP_STRING, PROP_NONE);
  RNA_def_property_ui_text(prop, "Name", "Layer name");
  RNA_def_property_string_funcs(prop,
                                "rna_GreasePencilLayer_name_get",
                                "rna_GreasePencilLayer_name_length",
                                "rna_GreasePencilLayer_name_set");
  RNA_def_struct_name_property(srna, prop);
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA | NA_RENAME, "rna_grease_pencil_update");

  /* Mask Layers */
  prop = RNA_def_property(srna, "mask_layers", PROP_COLLECTION, PROP_NONE);
  RNA_def_property_collection_sdna(prop, nullptr, "masks", nullptr);
  RNA_def_property_struct_type(prop, "GreasePencilLayerMask");
  RNA_def_property_ui_text(prop, "Masks", "List of Masking Layers");
  rna_def_grease_pencil_layers_mask_api(brna, prop);

  /* Visibility */
  prop = RNA_def_property(srna, "hide", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(
      prop, "GreasePencilLayerTreeNode", "flag", GP_LAYER_TREE_NODE_HIDE);
  RNA_def_property_ui_icon(prop, ICON_HIDE_OFF, -1);
  RNA_def_property_ui_text(prop, "Hide", "Set layer visibility");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  /* Lock */
  prop = RNA_def_property(srna, "lock", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(
      prop, "GreasePencilLayerTreeNode", "flag", GP_LAYER_TREE_NODE_LOCKED);
  RNA_def_property_ui_icon(prop, ICON_UNLOCKED, 1);
  RNA_def_property_ui_text(
      prop, "Locked", "Protect layer from further editing and/or frame changes");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  /* Select. */
  prop = RNA_def_property(srna, "select", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(
      prop, "GreasePencilLayerTreeNode", "flag", GP_LAYER_TREE_NODE_SELECT);
  RNA_def_property_ui_text(prop, "Select", "Layer is selected for editing in the Dope Sheet");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  /* Lock Frame. */
  prop = RNA_def_property(srna, "lock_frame", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(
      prop, "GreasePencilLayerTreeNode", "flag", GP_LAYER_TREE_NODE_MUTE);
  RNA_def_property_ui_icon(prop, ICON_UNLOCKED, 1);
  RNA_def_property_clear_flag(prop, PROP_ANIMATABLE);
  RNA_def_property_ui_text(prop, "Frame Locked", "Lock current frame displayed by layer");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  /* Opacity */
  prop = RNA_def_property(srna, "opacity", PROP_FLOAT, PROP_FACTOR);
  RNA_def_property_float_sdna(prop, "GreasePencilLayer", "opacity");
  RNA_def_property_ui_text(prop, "Opacity", "Layer Opacity");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  /* Onion Skinning. */
  prop = RNA_def_property(srna, "use_onion_skinning", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_ui_icon(prop, ICON_ONIONSKIN_OFF, 1);
  RNA_def_property_boolean_negative_sdna(
      prop, "GreasePencilLayerTreeNode", "flag", GP_LAYER_TREE_NODE_HIDE_ONION_SKINNING);
  RNA_def_property_ui_text(
      prop, "Onion Skinning", "Display onion skins before and after the current frame");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  /* Use Masks. */
  prop = RNA_def_property(srna, "use_masks", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_ui_icon(prop, ICON_CLIPUV_HLT, -1);
  RNA_def_property_boolean_negative_sdna(
      prop, "GreasePencilLayerTreeNode", "flag", GP_LAYER_TREE_NODE_HIDE_MASKS);
  RNA_def_property_ui_text(
      prop,
      "Use Masks",
      "The visibility of drawings on this layer is affected by the layers in its masks list");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "use_lights", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(
      prop, "GreasePencilLayerTreeNode", "flag", GP_LAYER_TREE_NODE_USE_LIGHTS);
  RNA_def_property_ui_text(
      prop, "Use Lights", "Enable the use of lights on stroke and fill materials");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  /* pass index for compositing and modifiers */
  prop = RNA_def_property(srna, "pass_index", PROP_INT, PROP_UNSIGNED);
  RNA_def_property_ui_text(prop, "Pass Index", "Index number for the \"Layer Index\" pass");
  RNA_def_property_int_funcs(prop,
                             "rna_GreasePencilLayer_pass_index_get",
                             "rna_GreasePencilLayer_pass_index_set",
                             nullptr);
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "parent", PROP_POINTER, PROP_NONE);
  RNA_def_property_struct_type(prop, "Object");
  RNA_def_property_flag(prop, PROP_EDITABLE | PROP_ID_SELF_CHECK);
  RNA_def_property_override_flag(prop, PROPOVERRIDE_OVERRIDABLE_LIBRARY);
  RNA_def_property_ui_text(prop, "Parent", "Parent object");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_dependency_update");

  prop = RNA_def_property(srna, "parent_bone", PROP_STRING, PROP_NONE);
  RNA_def_property_string_sdna(prop, nullptr, "parsubstr");
  RNA_def_property_ui_text(
      prop, "Parent Bone", "Name of parent bone. Only used when the parent object is an armature");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_dependency_update");

  prop = RNA_def_property(srna, "translation", PROP_FLOAT, PROP_TRANSLATION);
  RNA_def_property_array(prop, 3);
  RNA_def_property_float_sdna(prop, nullptr, "translation");
  RNA_def_property_ui_range(prop, -FLT_MAX, FLT_MAX, 1, RNA_TRANSLATION_PREC_DEFAULT);
  RNA_def_property_ui_text(prop, "Translation", "Translation of the layer");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "rotation", PROP_FLOAT, PROP_EULER);
  RNA_def_property_array(prop, 3);
  RNA_def_property_float_sdna(prop, nullptr, "rotation");
  RNA_def_property_ui_range(prop, -FLT_MAX, FLT_MAX, 1, RNA_TRANSLATION_PREC_DEFAULT);
  RNA_def_property_ui_text(prop, "Rotation", "Euler rotation of the layer");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "scale", PROP_FLOAT, PROP_XYZ);
  RNA_def_property_array(prop, 3);
  RNA_def_property_float_sdna(prop, nullptr, "scale");
  RNA_def_property_float_array_default(prop, scale_defaults);
  RNA_def_property_ui_range(prop, -FLT_MAX, FLT_MAX, 1, 3);
  RNA_def_property_ui_text(prop, "Scale", "Scale of the layer");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "viewlayer_render", PROP_STRING, PROP_NONE);
  RNA_def_property_string_sdna(prop, nullptr, "viewlayername");
  RNA_def_property_ui_text(
      prop,
      "ViewLayer",
      "Only include Layer in this View Layer render output (leave blank to include always)");

  prop = RNA_def_property(srna, "use_viewlayer_masks", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_negative_sdna(
      prop, "GreasePencilLayerTreeNode", "flag", GP_LAYER_TREE_NODE_DISABLE_MASKS_IN_VIEWLAYER);
  RNA_def_property_ui_text(
      prop, "Use Masks in Render", "Include the mask layers when rendering the view-layer");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "blend_mode", PROP_ENUM, PROP_NONE);
  RNA_def_property_enum_sdna(prop, nullptr, "blend_mode");
  RNA_def_property_enum_items(prop, rna_enum_layer_blend_modes_items);
  RNA_def_property_ui_text(prop, "Blend Mode", "Blend mode");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "use_locked_material", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(
      prop, "GreasePencilLayerTreeNode", "flag", GP_LAYER_TREE_NODE_USE_LOCKED_MATERIAL);
  RNA_def_property_clear_flag(prop, PROP_ANIMATABLE);
  RNA_def_property_ui_text(
      prop, "Use Locked Materials Editing", "Allow editing locked materials in the layer");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, nullptr);
  /* Local transformation matrix. */
  prop = RNA_def_property(srna, "matrix_local", PROP_FLOAT, PROP_MATRIX);
  RNA_def_property_multi_array(prop, 2, rna_matrix_dimsize_4x4);
  RNA_def_property_clear_flag(prop, PROP_EDITABLE);
  RNA_def_property_ui_text(prop, "Local Matrix", "Local transformation matrix of the layer");
  RNA_def_property_float_funcs(prop, "rna_GreasePencilLayer_matrix_local_get", nullptr, nullptr);
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  /* Inverse transform of layer's parent. */
  prop = RNA_def_property(srna, "matrix_parent_inverse", PROP_FLOAT, PROP_MATRIX);
  RNA_def_property_multi_array(prop, 2, rna_matrix_dimsize_4x4);
  RNA_def_property_clear_flag(prop, PROP_EDITABLE);
  RNA_def_property_ui_text(
      prop, "Inverse Parent Matrix", "Inverse of layer's parent transformation matrix");
  RNA_def_property_float_funcs(
      prop, "rna_GreasePencilLayer_matrix_parent_inverse_get", nullptr, nullptr);

  /* Parent layer group. */
  prop = RNA_def_property(srna, "parent_group", PROP_POINTER, PROP_NONE);
  RNA_def_property_struct_type(prop, "GreasePencilLayerGroup");
  RNA_def_property_pointer_funcs(
      prop, "rna_GreasePencilLayer_parent_layer_group_get", nullptr, nullptr, nullptr);
  RNA_def_property_ui_text(
      prop, "Parent Layer Group", "The parent layer group this layer is part of");
}

static void rna_def_grease_pencil_layers_api(BlenderRNA *brna, PropertyRNA *cprop)
{
  StructRNA *srna;
  PropertyRNA *prop;

  FunctionRNA *func;
  PropertyRNA *parm;

  RNA_def_property_srna(cprop, "GreasePencilv3Layers");
  srna = RNA_def_struct(brna, "GreasePencilv3Layers", nullptr);
  RNA_def_struct_sdna(srna, "GreasePencil");
  RNA_def_struct_ui_text(srna, "Grease Pencil Layers", "Collection of Grease Pencil layers");

  func = RNA_def_function(srna, "new", "rna_GreasePencil_layer_new");
  RNA_def_function_ui_description(func, "Add a new Grease Pencil layer");
  parm = RNA_def_string(func, "name", "GreasePencilLayer", MAX_NAME, "Name", "Name of the layer");
  RNA_def_parameter_flags(parm, PropertyFlag(0), PARM_REQUIRED);
  RNA_def_boolean(
      func, "set_active", true, "Set Active", "Set the newly created layer as the active layer");
  parm = RNA_def_pointer(
      func,
      "layer_group",
      "GreasePencilLayerGroup",
      "",
      "The layer group the new layer will be created in (use None for the main stack)");
  RNA_def_parameter_flags(parm, PropertyFlag(0), PARM_RNAPTR);
  parm = RNA_def_pointer(func, "layer", "GreasePencilLayer", "", "The newly created layer");
  RNA_def_function_return(func, parm);

  func = RNA_def_function(srna, "remove", "rna_GreasePencil_layer_remove");
  RNA_def_function_ui_description(func, "Remove a Grease Pencil layer");
  parm = RNA_def_pointer(func, "layer", "GreasePencilLayer", "", "The layer to remove");
  RNA_def_parameter_flags(parm, PROP_NEVER_NULL, PARM_REQUIRED | PARM_RNAPTR);
  RNA_def_parameter_clear_flags(parm, PROP_THICK_WRAP, ParameterFlag(0));

  func = RNA_def_function(srna, "move", "rna_GreasePencil_layer_move");
  RNA_def_function_ui_description(func,
                                  "Move a Grease Pencil layer in the layer group or main stack");
  parm = RNA_def_pointer(func, "layer", "GreasePencilLayer", "", "The layer to move");
  RNA_def_parameter_flags(parm, PROP_NEVER_NULL, PARM_REQUIRED | PARM_RNAPTR);
  RNA_def_parameter_clear_flags(parm, PROP_THICK_WRAP, ParameterFlag(0));
  parm = RNA_def_enum(
      func, "type", rna_enum_tree_node_move_type_items, 1, "", "Direction of movement");
  RNA_def_parameter_flags(parm, PropertyFlag(0), PARM_REQUIRED);

  func = RNA_def_function(srna, "move_top", "rna_GreasePencil_layer_move_top");
  RNA_def_function_ui_description(
      func, "Move a Grease Pencil layer to the top of the layer group or main stack");
  parm = RNA_def_pointer(func, "layer", "GreasePencilLayer", "", "The layer to move");
  RNA_def_parameter_flags(parm, PROP_NEVER_NULL, PARM_REQUIRED | PARM_RNAPTR);
  RNA_def_parameter_clear_flags(parm, PROP_THICK_WRAP, ParameterFlag(0));

  func = RNA_def_function(srna, "move_bottom", "rna_GreasePencil_layer_move_bottom");
  RNA_def_function_ui_description(
      func, "Move a Grease Pencil layer to the bottom of the layer group or main stack");
  parm = RNA_def_pointer(func, "layer", "GreasePencilLayer", "", "The layer to move");
  RNA_def_parameter_flags(parm, PROP_NEVER_NULL, PARM_REQUIRED | PARM_RNAPTR);
  RNA_def_parameter_clear_flags(parm, PROP_THICK_WRAP, ParameterFlag(0));

  func = RNA_def_function(
      srna, "move_to_layer_group", "rna_GreasePencil_layer_move_to_layer_group");
  RNA_def_function_ui_description(func, "Move a Grease Pencil layer into a layer group");
  parm = RNA_def_pointer(func, "layer", "GreasePencilLayer", "", "The layer to move");
  RNA_def_parameter_flags(parm, PROP_NEVER_NULL, PARM_REQUIRED | PARM_RNAPTR);
  RNA_def_parameter_clear_flags(parm, PROP_THICK_WRAP, ParameterFlag(0));
  parm = RNA_def_pointer(
      func,
      "layer_group",
      "GreasePencilLayerGroup",
      "",
      "The layer group the layer will be moved into (use None for the main stack)");
  RNA_def_parameter_flags(parm, PropertyFlag(0), PARM_REQUIRED | PARM_RNAPTR);
  RNA_def_parameter_clear_flags(parm, PROP_THICK_WRAP, ParameterFlag(0));

  prop = RNA_def_property(srna, "active", PROP_POINTER, PROP_NONE);
  RNA_def_property_struct_type(prop, "GreasePencilLayer");
  RNA_def_property_pointer_funcs(prop,
                                 "rna_GreasePencil_active_layer_get",
                                 "rna_GreasePencil_active_layer_set",
                                 nullptr,
                                 nullptr);
  RNA_def_property_flag(prop, PROP_EDITABLE);
  RNA_def_property_ui_text(prop, "Active Layer", "Active Grease Pencil layer");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA | NA_SELECTED, nullptr);
}

static void rna_def_grease_pencil_layer_group(BlenderRNA *brna)
{
  StructRNA *srna;
  PropertyRNA *prop;

  srna = RNA_def_struct(brna, "GreasePencilLayerGroup", nullptr);
  RNA_def_struct_sdna(srna, "GreasePencilLayerTreeGroup");
  RNA_def_struct_ui_text(srna, "Grease Pencil Layer Group", "Group of Grease Pencil layers");
  RNA_def_struct_path_func(srna, "rna_GreasePencilLayerGroup_path");

  /* Name */
  prop = RNA_def_property(srna, "name", PROP_STRING, PROP_NONE);
  RNA_def_property_ui_text(prop, "Name", "Group name");
  RNA_def_property_string_funcs(prop,
                                "rna_GreasePencilLayerGroup_name_get",
                                "rna_GreasePencilLayerGroup_name_length",
                                "rna_GreasePencilLayerGroup_name_set");
  RNA_def_struct_name_property(srna, prop);
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA | NA_RENAME, "rna_grease_pencil_update");

  /* Visibility */
  prop = RNA_def_property(srna, "hide", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(
      prop, "GreasePencilLayerTreeNode", "flag", GP_LAYER_TREE_NODE_HIDE);
  RNA_def_property_ui_icon(prop, ICON_HIDE_OFF, -1);
  RNA_def_property_ui_text(prop, "Hide", "Set layer group visibility");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  /* Lock */
  prop = RNA_def_property(srna, "lock", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(
      prop, "GreasePencilLayerTreeNode", "flag", GP_LAYER_TREE_NODE_LOCKED);
  RNA_def_property_ui_icon(prop, ICON_UNLOCKED, 1);
  RNA_def_property_ui_text(
      prop, "Locked", "Protect group from further editing and/or frame changes");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  /* Use Masks. */
  prop = RNA_def_property(srna, "use_masks", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_negative_sdna(
      prop, "GreasePencilLayerTreeNode", "flag", GP_LAYER_TREE_NODE_HIDE_MASKS);
  RNA_def_property_ui_text(prop,
                           "Use Masks",
                           "The visibility of drawings in the layers in this group is affected by "
                           "the layers in the masks lists");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "use_onion_skinning", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_ui_icon(prop, ICON_ONIONSKIN_OFF, 1);
  RNA_def_property_boolean_negative_sdna(
      prop, "GreasePencilLayerTreeNode", "flag", GP_LAYER_TREE_NODE_HIDE_ONION_SKINNING);
  RNA_def_property_ui_text(
      prop, "Onion Skinning", "Display onion skins before and after the current frame");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");
}

static void rna_def_grease_pencil_layer_group_api(BlenderRNA *brna, PropertyRNA *cprop)
{
  StructRNA *srna;
  PropertyRNA *prop;

  FunctionRNA *func;
  PropertyRNA *parm;

  RNA_def_property_srna(cprop, "GreasePencilv3LayerGroup");
  srna = RNA_def_struct(brna, "GreasePencilv3LayerGroup", nullptr);
  RNA_def_struct_sdna(srna, "GreasePencil");
  RNA_def_struct_ui_text(srna, "Grease Pencil Group", "Collection of Grease Pencil layers");

  func = RNA_def_function(srna, "new", "rna_GreasePencil_layer_group_new");
  RNA_def_function_ui_description(func, "Add a new Grease Pencil layer group");
  parm = RNA_def_string(
      func, "name", "GreasePencilLayerGroup", MAX_NAME, "Name", "Name of the layer group");
  RNA_def_parameter_flags(parm, PropertyFlag(0), PARM_REQUIRED);
  parm = RNA_def_pointer(
      func,
      "parent_group",
      "GreasePencilLayerGroup",
      "",
      "The parent layer group the new group will be created in (use None for the main stack)");
  RNA_def_parameter_flags(parm, PropertyFlag(0), PARM_RNAPTR);
  parm = RNA_def_pointer(
      func, "layer_group", "GreasePencilLayerGroup", "", "The newly created layer group");
  RNA_def_parameter_flags(parm, PropertyFlag(0), PARM_RNAPTR);
  RNA_def_function_return(func, parm);

  func = RNA_def_function(srna, "remove", "rna_GreasePencil_layer_group_remove");
  RNA_def_function_ui_description(func, "Remove a new Grease Pencil layer group");
  parm = RNA_def_pointer(
      func, "layer_group", "GreasePencilLayerGroup", "", "The layer group to remove");
  RNA_def_parameter_flags(parm, PROP_NEVER_NULL, PARM_REQUIRED | PARM_RNAPTR);
  RNA_def_parameter_clear_flags(parm, PROP_THICK_WRAP, ParameterFlag(0));
  parm = RNA_def_boolean(func,
                         "keep_children",
                         false,
                         "",
                         "Keep the children nodes of the group and only delete the group itself");

  func = RNA_def_function(srna, "move", "rna_GreasePencil_layer_group_move");
  RNA_def_function_ui_description(func,
                                  "Move a layer group in the parent layer group or main stack");
  parm = RNA_def_pointer(
      func, "layer_group", "GreasePencilLayerGroup", "", "The layer group to move");
  RNA_def_parameter_flags(parm, PROP_NEVER_NULL, PARM_REQUIRED | PARM_RNAPTR);
  RNA_def_parameter_clear_flags(parm, PROP_THICK_WRAP, ParameterFlag(0));
  parm = RNA_def_enum(
      func, "type", rna_enum_tree_node_move_type_items, 1, "", "Direction of movement");
  RNA_def_parameter_flags(parm, PropertyFlag(0), PARM_REQUIRED);

  func = RNA_def_function(srna, "move_top", "rna_GreasePencil_layer_group_move_top");
  RNA_def_function_ui_description(
      func, "Move a layer group to the top of the parent layer group or main stack");
  parm = RNA_def_pointer(
      func, "layer_group", "GreasePencilLayerGroup", "", "The layer group to move");
  RNA_def_parameter_flags(parm, PROP_NEVER_NULL, PARM_REQUIRED | PARM_RNAPTR);
  RNA_def_parameter_clear_flags(parm, PROP_THICK_WRAP, ParameterFlag(0));

  func = RNA_def_function(srna, "move_bottom", "rna_GreasePencil_layer_group_move_bottom");
  RNA_def_function_ui_description(
      func, "Move a layer group to the bottom of the parent layer group or main stack");
  parm = RNA_def_pointer(
      func, "layer_group", "GreasePencilLayerGroup", "", "The layer group to move");
  RNA_def_parameter_flags(parm, PROP_NEVER_NULL, PARM_REQUIRED | PARM_RNAPTR);
  RNA_def_parameter_clear_flags(parm, PROP_THICK_WRAP, ParameterFlag(0));

  func = RNA_def_function(
      srna, "move_to_layer_group", "rna_GreasePencil_layer_group_move_to_layer_group");
  RNA_def_function_ui_description(func, "Move a layer group into a parent layer group");
  parm = RNA_def_pointer(
      func, "layer_group", "GreasePencilLayerGroup", "", "The layer group to move");
  RNA_def_parameter_flags(parm, PROP_NEVER_NULL, PARM_REQUIRED | PARM_RNAPTR);
  RNA_def_parameter_clear_flags(parm, PROP_THICK_WRAP, ParameterFlag(0));
  parm = RNA_def_pointer(
      func,
      "parent_group",
      "GreasePencilLayerGroup",
      "",
      "The parent layer group the layer group will be moved into (use None for the main stack)");
  RNA_def_parameter_flags(parm, PropertyFlag(0), PARM_REQUIRED | PARM_RNAPTR);
  RNA_def_parameter_clear_flags(parm, PROP_THICK_WRAP, ParameterFlag(0));

  prop = RNA_def_property(srna, "active", PROP_POINTER, PROP_NONE);
  RNA_def_property_struct_type(prop, "GreasePencilLayerGroup");
  RNA_def_property_pointer_funcs(prop,
                                 "rna_GreasePencil_active_group_get",
                                 "rna_GreasePencil_active_group_set",
                                 nullptr,
                                 nullptr);
  RNA_def_property_flag(prop, PROP_EDITABLE);
  RNA_def_property_ui_text(prop, "Active Layer Group", "Active Grease Pencil layer group");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA | NA_SELECTED, nullptr);
}

static void rna_def_grease_pencil_onion_skinning(StructRNA *srna)
{
  PropertyRNA *prop;

  static EnumPropertyItem prop_enum_onion_modes_items[] = {
      {GP_ONION_SKINNING_MODE_ABSOLUTE,
       "ABSOLUTE",
       0,
       "Frames",
       "Frames in absolute range of the scene frame"},
      {GP_ONION_SKINNING_MODE_RELATIVE,
       "RELATIVE",
       0,
       "Keyframes",
       "Frames in relative range of the Grease Pencil keyframes"},
      {GP_ONION_SKINNING_MODE_SELECTED, "SELECTED", 0, "Selected", "Only selected keyframes"},
      {0, nullptr, 0, nullptr, nullptr},
  };

  static EnumPropertyItem prop_enum_onion_keyframe_type_items[] = {
      {GREASE_PENCIL_ONION_SKINNING_FILTER_ALL, "ALL", 0, "All", "Include all Keyframe types"},
      {GP_ONION_SKINNING_FILTER_KEYTYPE_KEYFRAME,
       "KEYFRAME",
       ICON_KEYTYPE_KEYFRAME_VEC,
       "Keyframe",
       "Normal keyframe, e.g. for key poses"},
      {GP_ONION_SKINNING_FILTER_KEYTYPE_BREAKDOWN,
       "BREAKDOWN",
       ICON_KEYTYPE_BREAKDOWN_VEC,
       "Breakdown",
       "A breakdown pose, e.g. for transitions between key poses"},
      {GP_ONION_SKINNING_FILTER_KEYTYPE_MOVEHOLD,
       "MOVING_HOLD",
       ICON_KEYTYPE_MOVING_HOLD_VEC,
       "Moving Hold",
       "A keyframe that is part of a moving hold"},
      {GP_ONION_SKINNING_FILTER_KEYTYPE_EXTREME,
       "EXTREME",
       ICON_KEYTYPE_EXTREME_VEC,
       "Extreme",
       "An 'extreme' pose, or some other purpose as needed"},
      {GP_ONION_SKINNING_FILTER_KEYTYPE_JITTER,
       "JITTER",
       ICON_KEYTYPE_JITTER_VEC,
       "Jitter",
       "A filler or baked keyframe for keying on ones, or some other purpose as needed"},
      {BEZT_KEYTYPE_GENERATED,
       "GENERATED",
       ICON_KEYTYPE_GENERATED_VEC,
       "Generated",
       "A key generated automatically by a tool, not manually created"},
      {0, nullptr, 0, nullptr, nullptr},
  };

  prop = RNA_def_property(srna, "ghost_before_range", PROP_INT, PROP_NONE);
  RNA_def_property_int_sdna(prop, nullptr, "onion_skinning_settings.num_frames_before");
  RNA_def_property_range(prop, 0, 120);
  RNA_def_parameter_clear_flags(prop, PROP_ANIMATABLE, ParameterFlag(0));
  RNA_def_property_ui_text(prop,
                           "Frames Before",
                           "Maximum number of frames to show before current frame "
                           "(0 = don't show any frames before current)");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "ghost_after_range", PROP_INT, PROP_NONE);
  RNA_def_property_int_sdna(prop, nullptr, "onion_skinning_settings.num_frames_after");
  RNA_def_property_range(prop, 0, 120);
  RNA_def_parameter_clear_flags(prop, PROP_ANIMATABLE, ParameterFlag(0));
  RNA_def_property_ui_text(prop,
                           "Frames After",
                           "Maximum number of frames to show after current frame "
                           "(0 = don't show any frames after current)");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "use_ghost_custom_colors", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(
      prop, nullptr, "onion_skinning_settings.flag", GP_ONION_SKINNING_USE_CUSTOM_COLORS);
  RNA_def_parameter_clear_flags(prop, PROP_ANIMATABLE, ParameterFlag(0));
  RNA_def_property_ui_text(prop, "Use Custom Ghost Colors", "Use custom colors for ghost frames");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "before_color", PROP_FLOAT, PROP_COLOR);
  RNA_def_property_float_sdna(prop, nullptr, "onion_skinning_settings.color_before");
  RNA_def_property_array(prop, 3);
  RNA_def_property_range(prop, 0.0f, 1.0f);
  RNA_def_parameter_clear_flags(prop, PROP_ANIMATABLE, ParameterFlag(0));
  RNA_def_property_ui_text(prop, "Before Color", "Base color for ghosts before the active frame");
  RNA_def_property_update(prop,
                          NC_SCREEN | NC_SCENE | ND_TOOLSETTINGS | ND_DATA | NC_GPENCIL,
                          "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "after_color", PROP_FLOAT, PROP_COLOR);
  RNA_def_property_float_sdna(prop, nullptr, "onion_skinning_settings.color_after");
  RNA_def_property_array(prop, 3);
  RNA_def_property_range(prop, 0.0f, 1.0f);
  RNA_def_parameter_clear_flags(prop, PROP_ANIMATABLE, ParameterFlag(0));
  RNA_def_property_ui_text(prop, "After Color", "Base color for ghosts after the active frame");
  RNA_def_property_update(prop,
                          NC_SCREEN | NC_SCENE | ND_TOOLSETTINGS | ND_DATA | NC_GPENCIL,
                          "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "onion_mode", PROP_ENUM, PROP_NONE);
  RNA_def_property_enum_sdna(prop, nullptr, "onion_skinning_settings.mode");
  RNA_def_property_enum_items(prop, prop_enum_onion_modes_items);
  RNA_def_parameter_clear_flags(prop, PROP_ANIMATABLE, ParameterFlag(0));
  RNA_def_property_ui_text(prop, "Mode", "Mode to display frames");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "onion_keyframe_type", PROP_ENUM, PROP_NONE);
  RNA_def_property_enum_sdna(prop, nullptr, "onion_skinning_settings.filter");
  RNA_def_parameter_clear_flags(prop, PROP_ANIMATABLE, ParameterFlag(0));
  RNA_def_property_enum_items(prop, prop_enum_onion_keyframe_type_items);
  RNA_def_property_ui_text(prop, "Filter by Type", "Type of keyframe (for filtering)");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "use_onion_fade", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(
      prop, nullptr, "onion_skinning_settings.flag", GP_ONION_SKINNING_USE_FADE);
  RNA_def_parameter_clear_flags(prop, PROP_ANIMATABLE, ParameterFlag(0));
  RNA_def_property_ui_text(
      prop, "Fade", "Display onion keyframes with a fade in color transparency");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "use_onion_loop", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(
      prop, nullptr, "onion_skinning_settings.flag", GP_ONION_SKINNING_SHOW_LOOP);
  RNA_def_parameter_clear_flags(prop, PROP_ANIMATABLE, ParameterFlag(0));
  RNA_def_property_ui_text(
      prop, "Show Start Frame", "Display onion keyframes for looping animations");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  prop = RNA_def_property(srna, "onion_factor", PROP_FLOAT, PROP_NONE);
  RNA_def_property_float_sdna(prop, nullptr, "onion_skinning_settings.opacity");
  RNA_def_property_range(prop, 0.0, 1.0f);
  RNA_def_parameter_clear_flags(prop, PROP_ANIMATABLE, ParameterFlag(0));
  RNA_def_property_ui_text(prop, "Onion Opacity", "Change fade opacity of displayed onion frames");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");
}

static void rna_def_grease_pencil_data(BlenderRNA *brna)
{
  StructRNA *srna;
  PropertyRNA *prop;

  static EnumPropertyItem prop_stroke_depth_order_items[] = {
      {0, "2D", 0, "2D Layers", "Display strokes using grease pencil layers to define order"},
      {GREASE_PENCIL_STROKE_ORDER_3D,
       "3D",
       0,
       "3D Location",
       "Display strokes using real 3D position in 3D space"},
      {0, nullptr, 0, nullptr, nullptr},
  };

  srna = RNA_def_struct(brna, "GreasePencilv3", "ID");
  RNA_def_struct_sdna(srna, "GreasePencil");
  RNA_def_struct_ui_text(srna, "Grease Pencil", "Grease Pencil data-block");
  RNA_def_struct_ui_icon(srna, ICON_OUTLINER_DATA_GREASEPENCIL);

  /* attributes */
  rna_def_attributes_common(srna, AttributeOwnerType::GreasePencil);

  /* Animation Data */
  rna_def_animdata_common(srna);

  /* Materials */
  prop = RNA_def_property(srna, "materials", PROP_COLLECTION, PROP_NONE);
  RNA_def_property_collection_sdna(prop, nullptr, "material_array", "material_array_num");
  RNA_def_property_struct_type(prop, "Material");
  RNA_def_property_ui_text(prop, "Materials", "");
  RNA_def_property_srna(prop, "IDMaterials"); /* see rna_ID.cc */
  RNA_def_property_collection_funcs(prop,
                                    nullptr,
                                    nullptr,
                                    nullptr,
                                    nullptr,
                                    nullptr,
                                    nullptr,
                                    nullptr,
                                    "rna_IDMaterials_assign_int");

  /* Layers */
  prop = RNA_def_property(srna, "layers", PROP_COLLECTION, PROP_NONE);
  RNA_def_property_struct_type(prop, "GreasePencilLayer");
  RNA_def_property_collection_funcs(prop,
                                    "rna_iterator_grease_pencil_layers_begin",
                                    "rna_iterator_array_next",
                                    "rna_iterator_array_end",
                                    "rna_iterator_array_dereference_get",
                                    "rna_iterator_grease_pencil_layers_length",
                                    nullptr, /* TODO */
                                    nullptr, /* TODO */
                                    nullptr);
  RNA_def_property_ui_text(prop, "Layers", "Grease Pencil layers");
  rna_def_grease_pencil_layers_api(brna, prop);

  /* Layer Groups */
  prop = RNA_def_property(srna, "layer_groups", PROP_COLLECTION, PROP_NONE);
  RNA_def_property_struct_type(prop, "GreasePencilLayerGroup");
  RNA_def_property_collection_funcs(prop,
                                    "rna_iterator_grease_pencil_layer_groups_begin",
                                    "rna_iterator_array_next",
                                    "rna_iterator_array_end",
                                    "rna_iterator_array_dereference_get",
                                    "rna_iterator_grease_pencil_layer_groups_length",
                                    nullptr, /* TODO */
                                    nullptr, /* TODO */
                                    nullptr);
  RNA_def_property_ui_text(prop, "Layer Groups", "Grease Pencil layer groups");
  rna_def_grease_pencil_layer_group_api(brna, prop);

  prop = RNA_def_property(srna, "use_autolock_layers", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(prop, nullptr, "flag", GREASE_PENCIL_AUTOLOCK_LAYERS);
  RNA_def_property_ui_text(
      prop,
      "Auto-Lock Layers",
      "Automatically lock all layers except the active one to avoid accidental changes");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_autolock");

  /* Uses a single flag, because the depth order can only be 2D or 3D. */
  prop = RNA_def_property(srna, "stroke_depth_order", PROP_ENUM, PROP_NONE);
  RNA_def_property_enum_bitflag_sdna(prop, nullptr, "flag");
  RNA_def_property_enum_items(prop, prop_stroke_depth_order_items);
  RNA_def_property_ui_text(
      prop,
      "Stroke Depth Order",
      "Defines how the strokes are ordered in 3D space (for objects not displayed 'In Front')");
  RNA_def_property_update(prop, NC_GPENCIL | ND_DATA, "rna_grease_pencil_update");

  /* Onion skinning. */
  rna_def_grease_pencil_onion_skinning(srna);
}

void RNA_def_grease_pencil(BlenderRNA *brna)
{
  rna_def_grease_pencil_data(brna);
  rna_def_grease_pencil_layer(brna);
  rna_def_grease_pencil_layer_mask(brna);
  rna_def_grease_pencil_layer_group(brna);
}

#endif
