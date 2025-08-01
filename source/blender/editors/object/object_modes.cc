/* SPDX-FileCopyrightText: 2023 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

/** \file
 * \ingroup edobj
 *
 * General utils to handle mode switching,
 * actual mode switching logic is per-object type.
 */

#include "DNA_object_enums.h"
#include "DNA_object_types.h"
#include "DNA_scene_types.h"

#include "BLI_time.h"
#include "BLI_utildefines.h"

#include "BKE_context.hh"
#include "BKE_layer.hh"
#include "BKE_library.hh"
#include "BKE_modifier.hh"
#include "BKE_object.hh"
#include "BKE_paint.hh"
#include "BKE_report.hh"

#include "BLI_math_vector.h"

#include "WM_api.hh"
#include "WM_types.hh"

#include "RNA_access.hh"
#include "RNA_define.hh"

#include "DEG_depsgraph.hh"
#include "DEG_depsgraph_query.hh"

#include "ED_armature.hh"
#include "ED_gpencil_legacy.hh"
#include "ED_outliner.hh"
#include "ED_paint.hh"
#include "ED_physics.hh"
#include "ED_sculpt.hh"
#include "ED_undo.hh"
#include "ED_view3d.hh"

#include "WM_toolsystem.hh"

#include "ED_object.hh" /* own include */
#include "object_intern.hh"

namespace blender::ed::object {

/* -------------------------------------------------------------------- */
/** \name High Level Mode Operations
 * \{ */

static const char *object_mode_op_string(eObjectMode mode)
{
  if (mode & OB_MODE_EDIT) {
    return "OBJECT_OT_editmode_toggle";
  }
  if (mode == OB_MODE_SCULPT) {
    return "SCULPT_OT_sculptmode_toggle";
  }
  if (mode == OB_MODE_VERTEX_PAINT) {
    return "PAINT_OT_vertex_paint_toggle";
  }
  if (mode == OB_MODE_WEIGHT_PAINT) {
    return "PAINT_OT_weight_paint_toggle";
  }
  if (mode == OB_MODE_TEXTURE_PAINT) {
    return "PAINT_OT_texture_paint_toggle";
  }
  if (mode == OB_MODE_PARTICLE_EDIT) {
    return "PARTICLE_OT_particle_edit_toggle";
  }
  if (mode == OB_MODE_POSE) {
    return "OBJECT_OT_posemode_toggle";
  }
  if (mode == OB_MODE_PAINT_GREASE_PENCIL) {
    return "GREASE_PENCIL_OT_paintmode_toggle";
  }
  if (mode == OB_MODE_SCULPT_GREASE_PENCIL) {
    return "GREASE_PENCIL_OT_sculptmode_toggle";
  }
  if (mode == OB_MODE_WEIGHT_GREASE_PENCIL) {
    return "GREASE_PENCIL_OT_weightmode_toggle";
  }
  if (mode == OB_MODE_VERTEX_GREASE_PENCIL) {
    return "GREASE_PENCIL_OT_vertexmode_toggle";
  }
  if (mode == OB_MODE_SCULPT_CURVES) {
    return "CURVES_OT_sculptmode_toggle";
  }
  return nullptr;
}

bool mode_compat_test(const Object *ob, eObjectMode mode)
{
  if (mode == OB_MODE_OBJECT) {
    return true;
  }

  switch (ob->type) {
    case OB_MESH:
      if (mode & (OB_MODE_EDIT | OB_MODE_SCULPT | OB_MODE_VERTEX_PAINT | OB_MODE_WEIGHT_PAINT |
                  OB_MODE_TEXTURE_PAINT))
      {
        return true;
      }
      if (mode & OB_MODE_PARTICLE_EDIT) {
        if (ED_object_particle_edit_mode_supported(ob)) {
          return true;
        }
      }
      break;
    case OB_CURVES_LEGACY:
    case OB_SURF:
    case OB_FONT:
    case OB_MBALL:
    case OB_POINTCLOUD:
    case OB_LATTICE:
      if (mode & OB_MODE_EDIT) {
        return true;
      }
      break;
    case OB_ARMATURE:
      if (mode & (OB_MODE_EDIT | OB_MODE_POSE)) {
        return true;
      }
      break;
    case OB_CURVES:
      if (mode & (OB_MODE_EDIT | OB_MODE_SCULPT_CURVES)) {
        return true;
      }
      break;
    case OB_GREASE_PENCIL:
      if (mode & (OB_MODE_EDIT | OB_MODE_PAINT_GREASE_PENCIL | OB_MODE_SCULPT_GREASE_PENCIL |
                  OB_MODE_WEIGHT_GREASE_PENCIL | OB_MODE_VERTEX_GREASE_PENCIL))
      {
        return true;
      }
      break;
  }

  return false;
}

bool mode_compat_set(bContext *C, Object *ob, eObjectMode mode, ReportList *reports)
{
  bool ok;
  if (!ELEM(ob->mode, mode, OB_MODE_OBJECT)) {
    const char *opstring = object_mode_op_string(eObjectMode(ob->mode));

    WM_operator_name_call(C, opstring, WM_OP_EXEC_REGION_WIN, nullptr, nullptr);
    ok = ELEM(ob->mode, mode, OB_MODE_OBJECT);
    if (!ok) {
      wmOperatorType *ot = WM_operatortype_find(opstring, false);
      BKE_reportf(reports, RPT_ERROR, "Unable to execute '%s', error changing modes", ot->name);
    }
  }
  else {
    ok = true;
  }

  return ok;
}

/** \} */

/* -------------------------------------------------------------------- */
/** \name Generic Mode Enter/Exit
 *
 * Supports exiting a mode without it being in the current context.
 * This could be done for entering modes too if it's needed.
 *
 * \{ */

bool mode_set_ex(bContext *C, eObjectMode mode, bool use_undo, ReportList *reports)
{
  wmWindowManager *wm = CTX_wm_manager(C);
  const Scene *scene = CTX_data_scene(C);
  ViewLayer *view_layer = CTX_data_view_layer(C);

  BKE_view_layer_synced_ensure(scene, view_layer);
  Object *ob = BKE_view_layer_active_object_get(view_layer);
  if (ob == nullptr) {
    return (mode == OB_MODE_OBJECT);
  }

  if (ob->mode == mode) {
    return true;
  }

  if (!mode_compat_test(ob, mode)) {
    return false;
  }

  const char *opstring = object_mode_op_string((mode == OB_MODE_OBJECT) ? eObjectMode(ob->mode) :
                                                                          mode);
  wmOperatorType *ot = WM_operatortype_find(opstring, false);

  if (!use_undo) {
    wm->op_undo_depth++;
  }
  WM_operator_name_call_ptr(C, ot, WM_OP_EXEC_REGION_WIN, nullptr, nullptr);
  if (!use_undo) {
    wm->op_undo_depth--;
  }

  if (ob->mode != mode) {
    BKE_reportf(reports, RPT_ERROR, "Unable to execute '%s', error changing modes", ot->name);
    return false;
  }

  return true;
}

bool mode_set(bContext *C, eObjectMode mode)
{
  /* Don't do undo push by default, since this may be called by lower level code. */
  return mode_set_ex(C, mode, true, nullptr);
}

/**
 * Use for changing works-paces or changing active object.
 * Caller can check #OB_MODE_ALL_MODE_DATA to test if this needs to be run.
 */
static bool ed_object_mode_generic_exit_ex(
    Main *bmain, Depsgraph *depsgraph, Scene *scene, Object *ob, bool only_test)
{
  BLI_assert((bmain == nullptr) == only_test);
  if (ob->mode & OB_MODE_EDIT) {
    if (BKE_object_is_in_editmode(ob)) {
      if (only_test) {
        return true;
      }
      editmode_exit_ex(bmain, scene, ob, EM_FREEDATA);
    }
  }
  else if (ob->mode & OB_MODE_VERTEX_PAINT) {
    if (ob->sculpt && (ob->sculpt->mode_type == OB_MODE_VERTEX_PAINT)) {
      if (only_test) {
        return true;
      }
      ED_object_vpaintmode_exit_ex(*ob);
    }
  }
  else if (ob->mode & OB_MODE_WEIGHT_PAINT) {
    if (ob->sculpt && (ob->sculpt->mode_type == OB_MODE_WEIGHT_PAINT)) {
      if (only_test) {
        return true;
      }
      ED_object_wpaintmode_exit_ex(*ob);
    }
  }
  else if (ob->mode & OB_MODE_SCULPT) {
    if (ob->sculpt && (ob->sculpt->mode_type == OB_MODE_SCULPT)) {
      if (only_test) {
        return true;
      }
      sculpt_paint::object_sculpt_mode_exit(*bmain, *depsgraph, *scene, *ob);
    }
  }
  else if (ob->mode & OB_MODE_POSE) {
    if (ob->pose != nullptr) {
      if (only_test) {
        return true;
      }
      ED_object_posemode_exit_ex(bmain, ob);
    }
  }
  else if (ob->mode & OB_MODE_TEXTURE_PAINT) {
    if (only_test) {
      return true;
    }
    ED_object_texture_paint_mode_exit_ex(*bmain, *scene, *ob);
  }
  else if (ob->mode & OB_MODE_PARTICLE_EDIT) {
    if (only_test) {
      return true;
    }
    ED_object_particle_edit_mode_exit_ex(scene, ob);
  }
  else if (ob->type == OB_GREASE_PENCIL) {
    BLI_assert((ob->mode & OB_MODE_OBJECT) == 0);
    if (only_test) {
      return true;
    }
    ob->restore_mode = ob->mode;
    ob->mode &= ~(OB_MODE_PAINT_GREASE_PENCIL | OB_MODE_EDIT | OB_MODE_SCULPT_GREASE_PENCIL |
                  OB_MODE_WEIGHT_GREASE_PENCIL | OB_MODE_VERTEX_GREASE_PENCIL);

    /* Inform all evaluated versions that we changed the mode. */
    DEG_id_tag_update_ex(bmain, &ob->id, ID_RECALC_SYNC_TO_EVAL);
  }
  else {
    if (only_test) {
      return false;
    }
    BLI_assert((ob->mode & OB_MODE_ALL_MODE_DATA) == 0);
  }

  return false;
}

/* When locked, it's almost impossible to select the pose-object
 * then the mesh-object to enter weight paint mode.
 * Even when the object mode is not locked this is inconvenient - so allow in either case.
 *
 * In this case move our pose object in/out of pose mode.
 * This is in fits with the convention of selecting multiple objects and entering a mode.
 */
static void ed_object_posemode_set_for_weight_paint_ex(bContext *C,
                                                       Main *bmain,
                                                       Object *ob_arm,
                                                       const bool is_mode_set)
{
  View3D *v3d = CTX_wm_view3d(C);
  const Scene *scene = CTX_data_scene(C);
  ViewLayer *view_layer = CTX_data_view_layer(C);

  if (ob_arm != nullptr) {
    BKE_view_layer_synced_ensure(scene, view_layer);
    const Base *base_arm = BKE_view_layer_base_find(view_layer, ob_arm);
    if (base_arm && BASE_VISIBLE(v3d, base_arm)) {
      if (is_mode_set) {
        if ((ob_arm->mode & OB_MODE_POSE) != 0) {
          ED_object_posemode_exit_ex(bmain, ob_arm);
        }
      }
      else {
        /* Only check selected status when entering weight-paint mode
         * because we may have multiple armature objects.
         * Selecting one will de-select the other, which would leave it in pose-mode
         * when exiting weight paint mode. While usable, this looks like inconsistent
         * behavior from a user perspective. */
        if (base_arm->flag & BASE_SELECTED) {
          if ((ob_arm->mode & OB_MODE_POSE) == 0) {
            ED_object_posemode_enter_ex(bmain, ob_arm);
          }
        }
      }
    }
  }
}

void posemode_set_for_weight_paint(bContext *C, Main *bmain, Object *ob, const bool is_mode_set)
{
  VirtualModifierData virtual_modifier_data;
  ModifierData *md = BKE_modifiers_get_virtual_modifierlist(ob, &virtual_modifier_data);
  for (; md; md = md->next) {
    if (md->type == eModifierType_Armature) {
      ArmatureModifierData *amd = reinterpret_cast<ArmatureModifierData *>(md);
      Object *ob_arm = amd->object;
      ed_object_posemode_set_for_weight_paint_ex(C, bmain, ob_arm, is_mode_set);
    }
    else if (md->type == eModifierType_GreasePencilArmature) {
      GreasePencilArmatureModifierData *amd = reinterpret_cast<GreasePencilArmatureModifierData *>(
          md);
      Object *ob_arm = amd->object;
      ed_object_posemode_set_for_weight_paint_ex(C, bmain, ob_arm, is_mode_set);
    }
  }
}

void mode_generic_exit(Main *bmain, Depsgraph *depsgraph, Scene *scene, Object *ob)
{
  ed_object_mode_generic_exit_ex(bmain, depsgraph, scene, ob, false);
}

bool mode_generic_has_data(Depsgraph *depsgraph, const Object *ob)
{
  return ed_object_mode_generic_exit_ex(nullptr, depsgraph, nullptr, (Object *)ob, true);
}

/** \} */

/* -------------------------------------------------------------------- */
/** \name Transfer Mode
 *
 * Enters the same mode of the current active object in another object,
 * leaving the mode of the current object.
 * \{ */

static bool object_transfer_mode_poll(bContext *C)
{
  if (!CTX_wm_region_view3d(C)) {
    return false;
  }
  const Object *ob = CTX_data_active_object(C);
  return ob && (ob->mode != OB_MODE_OBJECT);
}

/* Update the viewport rotation origin to the mouse cursor. */
static void object_transfer_mode_reposition_view_pivot(ARegion *region,
                                                       Paint *paint,
                                                       const int mval[2])
{
  float global_loc[3];
  if (!ED_view3d_autodist_simple(region, mval, global_loc, 0, nullptr)) {
    return;
  }
  UnifiedPaintSettings *ups = &paint->unified_paint_settings;
  copy_v3_v3(ups->average_stroke_accum, global_loc);
  ups->average_stroke_counter = 1;
  ups->last_stroke_valid = true;
}

constexpr float mode_transfer_flash_length = 0.55f;

static auto &mode_transfer_overlay_start_times()
{
  static Map<std::string, double> map;
  return map;
}

static float alpha_from_time_get(const float anim_time)
{
  if (anim_time < 0.0f) {
    return 0.0f;
  }
  return (1.0f - (anim_time / mode_transfer_flash_length));
}

Map<std::string, float, 1> mode_transfer_overlay_current_state()
{
  const double now = BLI_time_now_seconds();

  /* Protect against possible concurrent access from multiple renderers or viewports. */
  static Mutex mutex;
  std::scoped_lock lock(mutex);

  /* Remove finished animations form the global map. */
  Map<std::string, double> &start_times = mode_transfer_overlay_start_times();
  start_times.remove_if(
      [&](const auto &item) { return (now - item.value) > mode_transfer_flash_length; });

  Map<std::string, float, 1> factors;
  for (const auto &item : start_times.items()) {
    const float alpha = alpha_from_time_get(now - item.value);
    if (alpha > 0.0f) {
      factors.add_new(item.key, alpha);
    }
  }
  return factors;
}

static void object_overlay_mode_transfer_animation_start(bContext *C, Object *ob_dst)
{
  Depsgraph *depsgraph = CTX_data_depsgraph_pointer(C);
  Object *ob_dst_eval = DEG_get_evaluated(depsgraph, ob_dst);
  mode_transfer_overlay_start_times().add_as(ob_dst_eval->id.name, BLI_time_now_seconds());
}

static bool object_transfer_mode_to_base(bContext *C,
                                         wmOperator *op,
                                         Scene *scene,
                                         Object * /*ob_src*/,
                                         Object *ob_dst,
                                         const eObjectMode mode_dst)
{
  ViewLayer *view_layer = CTX_data_view_layer(C);

  /* Undo is handled manually here, such that the entry in the user-visible undo history is named
   * from the expected mode toggle operator name, and not the 'Transfer Mode' operator itself.
   *
   * The undo grouping is needed to ensure that only one step is visible, even though there may be
   * two undo steps stored when executed successfully (moving source object to Object mode, and
   * then target object to the previous mode of source object). */
  ED_undo_group_begin(C);

  const bool mode_transferred = mode_set_ex(C, OB_MODE_OBJECT, true, op->reports);
  if (mode_transferred) {
    BKE_view_layer_synced_ensure(scene, view_layer);
    Base *base_dst = BKE_view_layer_base_find(view_layer, ob_dst);
    BKE_view_layer_base_deselect_all(scene, view_layer);
    BKE_view_layer_base_select_and_set_active(view_layer, base_dst);

    /* Not entirely clear why, but this extra undo step (the two calls to #mode_set_ex should
     * already create their own) is required. Otherwise some mode switching does not work as
     * expected on undo/redo (see #130420 with Sculpt mode). */
    ED_undo_push(C, "Change Active");

    mode_set_ex(C, mode_dst, true, op->reports);

    if (RNA_boolean_get(op->ptr, "use_flash_on_transfer")) {
      object_overlay_mode_transfer_animation_start(C, ob_dst);
    }
  }

  ED_undo_group_end(C);

  return mode_transferred;
}

static wmOperatorStatus object_transfer_mode_invoke(bContext *C,
                                                    wmOperator *op,
                                                    const wmEvent *event)
{
  Scene *scene = CTX_data_scene(C);
  ARegion *region = CTX_wm_region(C);
  Object *ob_src = CTX_data_active_object(C);
  const eObjectMode mode_src = eObjectMode(ob_src->mode);

  Base *base_dst = ED_view3d_give_base_under_cursor(C, event->mval);
  if (!base_dst) {
    BKE_reportf(op->reports, RPT_ERROR, "No target object to transfer the mode to");
    return OPERATOR_CANCELLED;
  }

  Object *ob_dst = base_dst->object;

  if (ob_src == ob_dst) {
    return OPERATOR_CANCELLED;
  }

  BLI_assert(ob_dst->id.orig_id == nullptr);
  if (!ID_IS_EDITABLE(ob_dst) || !ID_IS_EDITABLE(ob_src)) {
    BKE_reportf(op->reports,
                RPT_ERROR,
                "Unable to transfer mode, the source and/or target objects are not editable");
    return OPERATOR_CANCELLED;
  }
  if (ID_IS_OVERRIDE_LIBRARY(ob_dst) && !ELEM(mode_src, OB_MODE_OBJECT, OB_MODE_POSE)) {
    BKE_reportf(
        op->reports,
        RPT_ERROR,
        "Current mode of source object '%s' is not compatible with target liboverride object '%s'",
        ob_src->id.name + 2,
        ob_dst->id.name + 2);
    return OPERATOR_CANCELLED;
  }
  if (!mode_compat_test(ob_dst, mode_src)) {
    BKE_reportf(op->reports,
                RPT_ERROR,
                "Current mode of source object '%s' is not compatible with target object '%s'",
                ob_src->id.name + 2,
                ob_dst->id.name + 2);
    return OPERATOR_CANCELLED;
  }

  const bool mode_transferred = object_transfer_mode_to_base(
      C, op, scene, ob_src, ob_dst, mode_src);
  if (!mode_transferred) {
    /* Error report should have been set by #object_transfer_mode_to_base call here. */
    return OPERATOR_CANCELLED;
  }

  DEG_id_tag_update(&scene->id, ID_RECALC_SELECT);
  WM_event_add_notifier(C, NC_SCENE | ND_OB_SELECT, scene);
  ED_outliner_select_sync_from_object_tag(C);

  WM_toolsystem_update_from_context_view3d(C);
  if (mode_src & OB_MODE_ALL_PAINT) {
    Paint *paint = BKE_paint_get_active_from_context(C);
    object_transfer_mode_reposition_view_pivot(region, paint, event->mval);
  }

  return OPERATOR_FINISHED;
}

void OBJECT_OT_transfer_mode(wmOperatorType *ot)
{
  /* identifiers */
  ot->name = "Transfer Mode";
  ot->idname = "OBJECT_OT_transfer_mode";
  ot->description =
      "Switch to another object without leaving the mode\nHotkey in the default keymap: D\nThe "
      "menu operator calls an object picker\nThe hotkey switches directly to the object under the "
      "mouse"; /* BFA - more explicit*/

  /* API callbacks. */
  ot->invoke = object_transfer_mode_invoke;
  ot->poll = object_transfer_mode_poll;

  /* Undo push is handled by the operator, see #object_transfer_mode_to_base for details. */
  ot->flag = OPTYPE_REGISTER | OPTYPE_DEPENDS_ON_CURSOR;

  ot->cursor_pending = WM_CURSOR_EYEDROPPER;

  RNA_def_boolean(ot->srna,
                  "use_flash_on_transfer",
                  true,
                  "Flash On Transfer",
                  "Flash the target object when transferring the mode");
}

/** \} */

}  // namespace blender::ed::object
