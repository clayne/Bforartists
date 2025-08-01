/* SPDX-FileCopyrightText: 2023 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

/** \file
 * \ingroup RNA
 */

#include <cfloat>
#include <climits>
#include <cstdlib>

#include "DNA_gpencil_legacy_types.h"
#include "DNA_shader_fx_types.h"

#include "BLI_math_rotation.h"

#include "BLT_translation.hh"

#include "BKE_animsys.h"

#include "RNA_define.hh"
#include "RNA_enum_types.hh"

#include "rna_internal.hh"

#include "WM_api.hh"
#include "WM_types.hh"

const EnumPropertyItem rna_enum_object_shaderfx_type_items[] = {
    {eShaderFxType_Blur, "FX_BLUR", ICON_SHADERFX, "Blur", "Apply Gaussian Blur to object"},
    {eShaderFxType_Colorize,
     "FX_COLORIZE",
     ICON_COLOR,
     "Colorize",
     "Apply different tint effects"},
    {eShaderFxType_Flip, "FX_FLIP", ICON_FLIP, "Flip", "Flip image"},
    {eShaderFxType_Glow, "FX_GLOW", ICON_LIGHT, "Glow", "Create a glow effect"},
    {eShaderFxType_Pixel, "FX_PIXEL", ICON_NODE_PIXELATED, "Pixelate", "Pixelate image"},
    {eShaderFxType_Rim, "FX_RIM", ICON_RIMLIGHT, "Rim", "Add a rim to the image"},
    {eShaderFxType_Shadow, "FX_SHADOW", ICON_NODE_AMBIENT_OCCLUSION, "Shadow", "Create a shadow effect"},
    {eShaderFxType_Swirl, "FX_SWIRL", ICON_SWIRL, "Swirl", "Create a rotation distortion"},
    {eShaderFxType_Wave,
     "FX_WAVE",
     ICON_MOD_WAVE,
     "Wave Distortion",
     "Apply sinusoidal deformation"},
    {0, nullptr, 0, nullptr, nullptr},
};

static const EnumPropertyItem rna_enum_shaderfx_rim_modes_items[] = {
    {eShaderFxRimMode_Normal, "NORMAL", 0, "Regular", ""},
    {eShaderFxRimMode_Overlay, "OVERLAY", 0, "Overlay", ""},
    {eShaderFxRimMode_Add, "ADD", 0, "Add", ""},
    {eShaderFxRimMode_Subtract, "SUBTRACT", 0, "Subtract", ""},
    {eShaderFxRimMode_Multiply, "MULTIPLY", 0, "Multiply", ""},
    {eShaderFxRimMode_Divide, "DIVIDE", 0, "Divide", ""},
    {0, nullptr, 0, nullptr, nullptr}};

static const EnumPropertyItem rna_enum_shaderfx_glow_modes_items[] = {
    {eShaderFxGlowMode_Luminance, "LUMINANCE", 0, "Luminance", ""},
    {eShaderFxGlowMode_Color, "COLOR", 0, "Color", ""},
    {0, nullptr, 0, nullptr, nullptr}};

static const EnumPropertyItem rna_enum_shaderfx_colorize_modes_items[] = {
    {eShaderFxColorizeMode_GrayScale, "GRAYSCALE", 0, "Gray Scale", ""},
    {eShaderFxColorizeMode_Sepia, "SEPIA", 0, "Sepia", ""},
    {eShaderFxColorizeMode_Duotone, "DUOTONE", 0, "Duotone", ""},
    {eShaderFxColorizeMode_Transparent, "TRANSPARENT", 0, "Transparent", ""},
    {eShaderFxColorizeMode_Custom, "CUSTOM", 0, "Custom", ""},
    {0, nullptr, 0, nullptr, nullptr}};

static const EnumPropertyItem rna_enum_glow_blend_modes_items[] = {
    {eGplBlendMode_Regular, "REGULAR", 0, "Regular", ""},
    {eGplBlendMode_Add, "ADD", 0, "Add", ""},
    {eGplBlendMode_Subtract, "SUBTRACT", 0, "Subtract", ""},
    {eGplBlendMode_Multiply, "MULTIPLY", 0, "Multiply", ""},
    {eGplBlendMode_Divide, "DIVIDE", 0, "Divide", ""},
    {0, nullptr, 0, nullptr, nullptr}};

#ifdef RNA_RUNTIME

#  include <fmt/format.h>

#  include "BKE_shader_fx.h"

#  include "DEG_depsgraph.hh"
#  include "DEG_depsgraph_build.hh"

static StructRNA *rna_ShaderFx_refine(PointerRNA *ptr)
{
  ShaderFxData *md = (ShaderFxData *)ptr->data;

  switch ((ShaderFxType)md->type) {
    case eShaderFxType_Blur:
      return &RNA_ShaderFxBlur;
    case eShaderFxType_Colorize:
      return &RNA_ShaderFxColorize;
    case eShaderFxType_Wave:
      return &RNA_ShaderFxWave;
    case eShaderFxType_Pixel:
      return &RNA_ShaderFxPixel;
    case eShaderFxType_Rim:
      return &RNA_ShaderFxRim;
    case eShaderFxType_Shadow:
      return &RNA_ShaderFxShadow;
    case eShaderFxType_Swirl:
      return &RNA_ShaderFxSwirl;
    case eShaderFxType_Flip:
      return &RNA_ShaderFxFlip;
    case eShaderFxType_Glow:
      return &RNA_ShaderFxGlow;
      /* Default */
    case eShaderFxType_None:
    case NUM_SHADER_FX_TYPES:
    default:
      return &RNA_ShaderFx;
  }

  return &RNA_ShaderFx;
}

static void rna_ShaderFx_name_set(PointerRNA *ptr, const char *value)
{
  ShaderFxData *gmd = static_cast<ShaderFxData *>(ptr->data);
  char oldname[sizeof(gmd->name)];

  /* make a copy of the old name first */
  STRNCPY(oldname, gmd->name);

  /* copy the new name into the name slot */
  STRNCPY_UTF8(gmd->name, value);

  /* make sure the name is truly unique */
  if (ptr->owner_id) {
    Object *ob = (Object *)ptr->owner_id;
    BKE_shaderfx_unique_name(&ob->shader_fx, gmd);
  }

  /* fix all the animation data which may link to this */
  BKE_animdata_fix_paths_rename_all(nullptr, "shader_effects", oldname, gmd->name);
}

static std::optional<std::string> rna_ShaderFx_path(const PointerRNA *ptr)
{
  const ShaderFxData *gmd = static_cast<ShaderFxData *>(ptr->data);
  char name_esc[sizeof(gmd->name) * 2];

  BLI_str_escape(name_esc, gmd->name, sizeof(name_esc));
  return fmt::format("shader_effects[\"{}\"]", name_esc);
}

static void rna_ShaderFx_update(Main * /*bmain*/, Scene * /*scene*/, PointerRNA *ptr)
{
  DEG_id_tag_update(ptr->owner_id, ID_RECALC_GEOMETRY);
  WM_main_add_notifier(NC_OBJECT | ND_SHADERFX, ptr->owner_id);
}

static void rna_ShaderFx_dependency_update(Main *bmain, Scene *scene, PointerRNA *ptr)
{
  rna_ShaderFx_update(bmain, scene, ptr);
  DEG_relations_tag_update(bmain);
}

/* Objects */

static void shaderfx_object_set(Object *self, Object **ob_p, int type, PointerRNA value)
{
  Object *ob = static_cast<Object *>(value.data);

  if (!self || ob != self) {
    if (!ob || type == OB_EMPTY || ob->type == type) {
      id_lib_extern((ID *)ob);
      *ob_p = ob;
    }
  }
}

#  define RNA_FX_OBJECT_SET(_type, _prop, _obtype) \
    static void rna_##_type##ShaderFx_##_prop##_set( \
        PointerRNA *ptr, PointerRNA value, ReportList * /*reports*/) \
    { \
      _type##ShaderFxData *tmd = (_type##ShaderFxData *)ptr->data; \
      shaderfx_object_set((Object *)ptr->owner_id, &tmd->_prop, _obtype, value); \
    }

RNA_FX_OBJECT_SET(Shadow, object, OB_EMPTY);
RNA_FX_OBJECT_SET(Swirl, object, OB_EMPTY);

#  undef RNA_FX_OBJECT_SET

#else

static void rna_def_shader_fx_blur(BlenderRNA *brna)
{
  StructRNA *srna;
  PropertyRNA *prop;

  srna = RNA_def_struct(brna, "ShaderFxBlur", "ShaderFx");
  RNA_def_struct_ui_text(srna, "Gaussian Blur Effect", "Gaussian Blur effect");
  RNA_def_struct_sdna(srna, "BlurShaderFxData");
  RNA_def_struct_ui_icon(srna, ICON_NODE_BLUR); /* BFA */

  RNA_define_lib_overridable(true);

  prop = RNA_def_property(srna, "size", PROP_FLOAT, PROP_XYZ);
  RNA_def_property_float_sdna(prop, nullptr, "radius");
  RNA_def_property_range(prop, 0.0f, FLT_MAX);
  RNA_def_property_ui_text(prop, "Size", "Factor of Blur");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "samples", PROP_INT, PROP_NONE);
  RNA_def_property_int_sdna(prop, nullptr, "samples");
  RNA_def_property_range(prop, 0, 32);
  RNA_def_property_ui_range(prop, 0, 32, 2, -1);
  RNA_def_property_int_default(prop, 4);
  RNA_def_property_ui_text(prop, "Samples", "Number of Blur Samples (zero, disable blur)");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "rotation", PROP_FLOAT, PROP_ANGLE);
  RNA_def_property_float_sdna(prop, nullptr, "rotation");
  RNA_def_property_range(prop, -FLT_MAX, FLT_MAX);
  RNA_def_property_ui_text(prop, "Rotation", "Rotation of the effect");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "use_dof_mode", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(prop, nullptr, "flag", FX_BLUR_DOF_MODE);
  RNA_def_property_ui_text(prop, "Use as Depth Of Field", "Blur using camera depth of field");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  RNA_define_lib_overridable(false);
}

static void rna_def_shader_fx_colorize(BlenderRNA *brna)
{
  StructRNA *srna;
  PropertyRNA *prop;

  srna = RNA_def_struct(brna, "ShaderFxColorize", "ShaderFx");
  RNA_def_struct_ui_text(srna, "Colorize Effect", "Colorize effect");
  RNA_def_struct_sdna(srna, "ColorizeShaderFxData");
  RNA_def_struct_ui_icon(srna, ICON_COLOR); /* BFA */

  RNA_define_lib_overridable(true);

  prop = RNA_def_property(srna, "factor", PROP_FLOAT, PROP_NONE);
  RNA_def_property_float_sdna(prop, nullptr, "factor");
  RNA_def_property_range(prop, 0, 1.0);
  RNA_def_property_ui_text(prop, "Factor", "Mix factor");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "low_color", PROP_FLOAT, PROP_COLOR);
  RNA_def_property_range(prop, 0.0, 1.0);
  RNA_def_property_float_sdna(prop, nullptr, "low_color");
  RNA_def_property_array(prop, 4);
  RNA_def_property_ui_text(prop, "Low Color", "First color used for effect");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "high_color", PROP_FLOAT, PROP_COLOR);
  RNA_def_property_range(prop, 0.0, 1.0);
  RNA_def_property_float_sdna(prop, nullptr, "high_color");
  RNA_def_property_array(prop, 4);
  RNA_def_property_ui_text(prop, "High Color", "Second color used for effect");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "mode", PROP_ENUM, PROP_NONE);
  RNA_def_property_enum_sdna(prop, nullptr, "mode");
  RNA_def_property_enum_items(prop, rna_enum_shaderfx_colorize_modes_items);
  RNA_def_property_ui_text(prop, "Mode", "Effect mode");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  RNA_define_lib_overridable(false);
}

static void rna_def_shader_fx_wave(BlenderRNA *brna)
{
  StructRNA *srna;
  PropertyRNA *prop;

  static const EnumPropertyItem prop_shaderfx_wave_type_items[] = {
      {0, "HORIZONTAL", 0, "Horizontal", ""},
      {1, "VERTICAL", 0, "Vertical", ""},
      {0, nullptr, 0, nullptr, nullptr}};

  srna = RNA_def_struct(brna, "ShaderFxWave", "ShaderFx");
  RNA_def_struct_ui_text(srna, "Wave Deformation Effect", "Wave Deformation effect");
  RNA_def_struct_sdna(srna, "WaveShaderFxData");
  RNA_def_struct_ui_icon(srna, ICON_MOD_WAVE);

  RNA_define_lib_overridable(true);

  prop = RNA_def_property(srna, "orientation", PROP_ENUM, PROP_NONE);
  RNA_def_property_enum_sdna(prop, nullptr, "orientation");
  RNA_def_property_enum_items(prop, prop_shaderfx_wave_type_items);
  RNA_def_property_ui_text(prop, "Orientation", "Direction of the wave");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "amplitude", PROP_FLOAT, PROP_NONE);
  RNA_def_property_float_sdna(prop, nullptr, "amplitude");
  RNA_def_property_range(prop, 0, FLT_MAX);
  RNA_def_property_ui_text(prop, "Amplitude", "Amplitude of Wave");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "period", PROP_FLOAT, PROP_NONE);
  RNA_def_property_float_sdna(prop, nullptr, "period");
  RNA_def_property_range(prop, 0, FLT_MAX);
  RNA_def_property_ui_text(prop, "Period", "Period of Wave");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "phase", PROP_FLOAT, PROP_NONE);
  RNA_def_property_float_sdna(prop, nullptr, "phase");
  RNA_def_property_range(prop, -FLT_MAX, FLT_MAX);
  RNA_def_property_ui_text(prop, "Phase", "Phase Shift of Wave");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  RNA_define_lib_overridable(false);
}

static void rna_def_shader_fx_pixel(BlenderRNA *brna)
{
  StructRNA *srna;
  PropertyRNA *prop;

  srna = RNA_def_struct(brna, "ShaderFxPixel", "ShaderFx");
  RNA_def_struct_ui_text(srna, "Pixelate Effect", "Pixelate effect");
  RNA_def_struct_sdna(srna, "PixelShaderFxData");
  RNA_def_struct_ui_icon(srna, ICON_NODE_PIXELATED); /* BFA */

  RNA_define_lib_overridable(true);

  prop = RNA_def_property(srna, "size", PROP_INT, PROP_PIXEL);
  RNA_def_property_int_sdna(prop, nullptr, "size");
  RNA_def_property_range(prop, 1, SHRT_MAX);
  RNA_def_property_array(prop, 2);
  RNA_def_property_ui_text(prop, "Size", "Pixel size");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "use_antialiasing", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_negative_sdna(prop, nullptr, "flag", FX_PIXEL_FILTER_NEAREST);
  RNA_def_property_ui_text(prop, "Antialiasing", "Antialias pixels");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  RNA_define_lib_overridable(false);
}

static void rna_def_shader_fx_rim(BlenderRNA *brna)
{
  StructRNA *srna;
  PropertyRNA *prop;

  srna = RNA_def_struct(brna, "ShaderFxRim", "ShaderFx");
  RNA_def_struct_ui_text(srna, "Rim Effect", "Rim effect");
  RNA_def_struct_sdna(srna, "RimShaderFxData");
  RNA_def_struct_ui_icon(srna, ICON_RIMLIGHT); /* BFA */

  RNA_define_lib_overridable(true);

  prop = RNA_def_property(srna, "offset", PROP_INT, PROP_PIXEL);
  RNA_def_property_int_sdna(prop, nullptr, "offset");
  RNA_def_property_range(prop, SHRT_MIN, SHRT_MAX);
  RNA_def_property_ui_text(prop, "Offset", "Offset of the rim");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "rim_color", PROP_FLOAT, PROP_COLOR);
  RNA_def_property_range(prop, 0.0, 1.0);
  RNA_def_property_float_sdna(prop, nullptr, "rim_rgb");
  RNA_def_property_array(prop, 3);
  RNA_def_property_ui_text(prop, "Rim Color", "Color used for Rim");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "mask_color", PROP_FLOAT, PROP_COLOR);
  RNA_def_property_range(prop, 0.0, 1.0);
  RNA_def_property_float_sdna(prop, nullptr, "mask_rgb");
  RNA_def_property_array(prop, 3);
  RNA_def_property_ui_text(prop, "Mask Color", "Color that must be kept");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "mode", PROP_ENUM, PROP_NONE);
  RNA_def_property_enum_sdna(prop, nullptr, "mode");
  RNA_def_property_enum_items(prop, rna_enum_shaderfx_rim_modes_items);
  RNA_def_property_ui_text(prop, "Mode", "Blend mode");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "blur", PROP_INT, PROP_PIXEL);
  RNA_def_property_int_sdna(prop, nullptr, "blur");
  RNA_def_property_range(prop, 0, SHRT_MAX);
  RNA_def_property_ui_text(
      prop, "Blur", "Number of pixels for blurring rim (set to 0 to disable)");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "samples", PROP_INT, PROP_NONE);
  RNA_def_property_int_sdna(prop, nullptr, "samples");
  RNA_def_property_range(prop, 0, 32);
  RNA_def_property_ui_range(prop, 0, 32, 2, -1);
  RNA_def_property_int_default(prop, 4);
  RNA_def_property_ui_text(prop, "Samples", "Number of Blur Samples (zero, disable blur)");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  RNA_define_lib_overridable(false);
}

static void rna_def_shader_fx_shadow(BlenderRNA *brna)
{
  static const EnumPropertyItem prop_shaderfx_shadow_type_items[] = {
      {0, "HORIZONTAL", 0, "Horizontal", ""},
      {1, "VERTICAL", 0, "Vertical", ""},
      {0, nullptr, 0, nullptr, nullptr}};

  StructRNA *srna;
  PropertyRNA *prop;

  srna = RNA_def_struct(brna, "ShaderFxShadow", "ShaderFx");
  RNA_def_struct_ui_text(srna, "Shadow Effect", "Shadow effect");
  RNA_def_struct_sdna(srna, "ShadowShaderFxData");
  RNA_def_struct_ui_icon(srna, ICON_NODE_AMBIENT_OCCLUSION); /* BFA */

  RNA_define_lib_overridable(true);

  prop = RNA_def_property(srna, "object", PROP_POINTER, PROP_NONE);
  RNA_def_property_ui_text(prop, "Object", "Object to determine center of rotation");
  RNA_def_property_pointer_funcs(prop, nullptr, "rna_ShadowShaderFx_object_set", nullptr, nullptr);
  RNA_def_property_flag(prop, PROP_EDITABLE | PROP_ID_SELF_CHECK);
  RNA_def_property_update(prop, 0, "rna_ShaderFx_dependency_update");

  prop = RNA_def_property(srna, "offset", PROP_INT, PROP_PIXEL);
  RNA_def_property_int_sdna(prop, nullptr, "offset");
  RNA_def_property_range(prop, SHRT_MIN, SHRT_MAX);
  RNA_def_property_ui_text(prop, "Offset", "Offset of the shadow");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "scale", PROP_FLOAT, PROP_XYZ);
  RNA_def_property_float_sdna(prop, nullptr, "scale");
  RNA_def_property_range(prop, -FLT_MAX, FLT_MAX);
  RNA_def_property_ui_text(prop, "Scale", "Scale of the shadow");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "shadow_color", PROP_FLOAT, PROP_COLOR);
  RNA_def_property_range(prop, 0.0, 1.0);
  RNA_def_property_float_sdna(prop, nullptr, "shadow_rgba");
  RNA_def_property_array(prop, 4);
  RNA_def_property_ui_text(prop, "Shadow Color", "Color used for Shadow");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "orientation", PROP_ENUM, PROP_NONE);
  RNA_def_property_enum_sdna(prop, nullptr, "orientation");
  RNA_def_property_enum_items(prop, prop_shaderfx_shadow_type_items);
  RNA_def_property_ui_text(prop, "Orientation", "Direction of the wave");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "amplitude", PROP_FLOAT, PROP_NONE);
  RNA_def_property_float_sdna(prop, nullptr, "amplitude");
  RNA_def_property_range(prop, 0, FLT_MAX);
  RNA_def_property_ui_text(prop, "Amplitude", "Amplitude of Wave");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "period", PROP_FLOAT, PROP_NONE);
  RNA_def_property_float_sdna(prop, nullptr, "period");
  RNA_def_property_range(prop, 0, FLT_MAX);
  RNA_def_property_ui_text(prop, "Period", "Period of Wave");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "phase", PROP_FLOAT, PROP_NONE);
  RNA_def_property_float_sdna(prop, nullptr, "phase");
  RNA_def_property_range(prop, -FLT_MAX, FLT_MAX);
  RNA_def_property_ui_text(prop, "Phase", "Phase Shift of Wave");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "rotation", PROP_FLOAT, PROP_ANGLE);
  RNA_def_property_float_sdna(prop, nullptr, "rotation");
  RNA_def_property_range(prop, DEG2RAD(-360), DEG2RAD(360));
  RNA_def_property_ui_range(prop, DEG2RAD(-360), DEG2RAD(360), 5, 2);
  RNA_def_property_ui_text(prop, "Rotation", "Rotation around center or object");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "blur", PROP_INT, PROP_PIXEL);
  RNA_def_property_int_sdna(prop, nullptr, "blur");
  RNA_def_property_range(prop, 0, SHRT_MAX);
  RNA_def_property_ui_text(
      prop, "Blur", "Number of pixels for blurring shadow (set to 0 to disable)");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "samples", PROP_INT, PROP_NONE);
  RNA_def_property_int_sdna(prop, nullptr, "samples");
  RNA_def_property_range(prop, 0, 32);
  RNA_def_property_ui_range(prop, 0, 32, 2, -1);
  RNA_def_property_int_default(prop, 4);
  RNA_def_property_ui_text(prop, "Samples", "Number of Blur Samples (zero, disable blur)");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "use_object", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(prop, nullptr, "flag", FX_SHADOW_USE_OBJECT);
  RNA_def_property_ui_text(prop, "Use Object", "Use object as center of rotation");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "use_wave", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(prop, nullptr, "flag", FX_SHADOW_USE_WAVE);
  RNA_def_property_ui_text(prop, "Wave", "Use wave effect");
  RNA_def_property_translation_context(prop, BLT_I18NCONTEXT_ID_GPENCIL);
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  RNA_define_lib_overridable(false);
}

static void rna_def_shader_fx_glow(BlenderRNA *brna)
{
  StructRNA *srna;
  PropertyRNA *prop;

  srna = RNA_def_struct(brna, "ShaderFxGlow", "ShaderFx");
  RNA_def_struct_ui_text(srna, "Glow Effect", "Glow effect");
  RNA_def_struct_sdna(srna, "GlowShaderFxData");
  RNA_def_struct_ui_icon(srna, ICON_LIGHT); /* BFA */

  RNA_define_lib_overridable(true);

  prop = RNA_def_property(srna, "glow_color", PROP_FLOAT, PROP_COLOR);
  RNA_def_property_range(prop, 0.0, 1.0);
  RNA_def_property_float_sdna(prop, nullptr, "glow_color");
  RNA_def_property_array(prop, 3);
  RNA_def_property_ui_text(prop, "Glow Color", "Color used for generated glow");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "opacity", PROP_FLOAT, PROP_FACTOR);
  RNA_def_property_float_sdna(prop, nullptr, "glow_color[3]");
  RNA_def_property_range(prop, 0.0, 1.0f);
  RNA_def_property_ui_text(prop, "Opacity", "Effect Opacity");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "select_color", PROP_FLOAT, PROP_COLOR);
  RNA_def_property_range(prop, 0.0, 1.0);
  RNA_def_property_float_sdna(prop, nullptr, "select_color");
  RNA_def_property_array(prop, 3);
  RNA_def_property_ui_text(prop, "Select Color", "Color selected to apply glow");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "mode", PROP_ENUM, PROP_NONE);
  RNA_def_property_enum_sdna(prop, nullptr, "mode");
  RNA_def_property_enum_items(prop, rna_enum_shaderfx_glow_modes_items);
  RNA_def_property_ui_text(prop, "Mode", "Glow mode");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "threshold", PROP_FLOAT, PROP_FACTOR);
  RNA_def_property_float_sdna(prop, nullptr, "threshold");
  RNA_def_property_range(prop, 0.0f, 1.0f);
  RNA_def_property_ui_range(prop, 0.0f, 1.0f, 0.1f, 3);
  RNA_def_property_ui_text(prop, "Threshold", "Limit to select color for glow effect");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  /* Use blur fields to make compatible with blur filter */
  prop = RNA_def_property(srna, "size", PROP_FLOAT, PROP_XYZ);
  RNA_def_property_float_sdna(prop, nullptr, "blur");
  RNA_def_property_range(prop, 0.0f, FLT_MAX);
  RNA_def_property_ui_text(prop, "Size", "Size of the effect");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "samples", PROP_INT, PROP_NONE);
  RNA_def_property_int_sdna(prop, nullptr, "samples");
  RNA_def_property_range(prop, 1, 32);
  RNA_def_property_ui_range(prop, 1, 32, 2, -1);
  RNA_def_property_int_default(prop, 4);
  RNA_def_property_ui_text(prop, "Samples", "Number of Blur Samples");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "use_glow_under", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(prop, nullptr, "flag", FX_GLOW_USE_ALPHA);
  RNA_def_property_ui_text(
      prop, "Glow Under", "Glow only areas with alpha (not supported with Regular blend mode)");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "rotation", PROP_FLOAT, PROP_ANGLE);
  RNA_def_property_float_sdna(prop, nullptr, "rotation");
  RNA_def_property_range(prop, -FLT_MAX, FLT_MAX);
  RNA_def_property_ui_text(prop, "Rotation", "Rotation of the effect");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  /* blend mode */
  prop = RNA_def_property(srna, "blend_mode", PROP_ENUM, PROP_NONE);
  RNA_def_property_enum_sdna(prop, nullptr, "blend_mode");
  RNA_def_property_enum_items(prop, rna_enum_glow_blend_modes_items);
  RNA_def_property_ui_text(prop, "Blend Mode", "Blend mode");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  RNA_define_lib_overridable(false);
}

static void rna_def_shader_fx_swirl(BlenderRNA *brna)
{
  StructRNA *srna;
  PropertyRNA *prop;

  srna = RNA_def_struct(brna, "ShaderFxSwirl", "ShaderFx");
  RNA_def_struct_ui_text(srna, "Swirl Effect", "Swirl effect");
  RNA_def_struct_sdna(srna, "SwirlShaderFxData");
  RNA_def_struct_ui_icon(srna, ICON_SWIRL); /* BFA */

  RNA_define_lib_overridable(true);

  prop = RNA_def_property(srna, "radius", PROP_INT, PROP_PIXEL);
  RNA_def_property_int_sdna(prop, nullptr, "radius");
  RNA_def_property_range(prop, 0, SHRT_MAX);
  RNA_def_property_ui_text(prop, "Radius", "Radius to apply");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "angle", PROP_FLOAT, PROP_ANGLE);
  RNA_def_property_float_sdna(prop, nullptr, "angle");
  RNA_def_property_range(prop, DEG2RAD(-5 * 360), DEG2RAD(5 * 360));
  RNA_def_property_ui_range(prop, DEG2RAD(-5 * 360), DEG2RAD(5 * 360), 5, 2);
  RNA_def_property_ui_text(prop, "Angle", "Angle of rotation");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "use_transparent", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(prop, nullptr, "flag", FX_SWIRL_MAKE_TRANSPARENT);
  RNA_def_property_ui_text(prop, "Transparent", "Make image transparent outside of radius");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "object", PROP_POINTER, PROP_NONE);
  RNA_def_property_ui_text(prop, "Object", "Object to determine center location");
  RNA_def_property_pointer_funcs(prop, nullptr, "rna_SwirlShaderFx_object_set", nullptr, nullptr);
  RNA_def_property_flag(prop, PROP_EDITABLE | PROP_ID_SELF_CHECK);
  RNA_def_property_update(prop, 0, "rna_ShaderFx_dependency_update");

  RNA_define_lib_overridable(false);
}

static void rna_def_shader_fx_flip(BlenderRNA *brna)
{
  StructRNA *srna;
  PropertyRNA *prop;

  srna = RNA_def_struct(brna, "ShaderFxFlip", "ShaderFx");
  RNA_def_struct_ui_text(srna, "Flip Effect", "Flip effect");
  RNA_def_struct_sdna(srna, "FlipShaderFxData");
  RNA_def_struct_ui_icon(srna, ICON_FLIP); /* BFA */

  RNA_define_lib_overridable(true);

  prop = RNA_def_property(srna, "use_flip_x", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(prop, nullptr, "flag", FX_FLIP_HORIZONTAL);
  RNA_def_property_ui_text(prop, "Horizontal", "Flip image horizontally");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  prop = RNA_def_property(srna, "use_flip_y", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(prop, nullptr, "flag", FX_FLIP_VERTICAL);
  RNA_def_property_ui_text(prop, "Vertical", "Flip image vertically");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");

  RNA_define_lib_overridable(false);
}

void RNA_def_shader_fx(BlenderRNA *brna)
{
  StructRNA *srna;
  PropertyRNA *prop;

  /* data */
  srna = RNA_def_struct(brna, "ShaderFx", nullptr);
  RNA_def_struct_ui_text(srna, "ShaderFx", "Effect affecting the Grease Pencil object");
  RNA_def_struct_refine_func(srna, "rna_ShaderFx_refine");
  RNA_def_struct_path_func(srna, "rna_ShaderFx_path");
  RNA_def_struct_sdna(srna, "ShaderFxData");

  /* strings */
  prop = RNA_def_property(srna, "name", PROP_STRING, PROP_NONE);
  RNA_def_property_string_funcs(prop, nullptr, nullptr, "rna_ShaderFx_name_set");
  RNA_def_property_ui_text(prop, "Name", "Effect name");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX | NA_RENAME, nullptr);
  RNA_def_struct_name_property(srna, prop);

  /* enums */
  prop = RNA_def_property(srna, "type", PROP_ENUM, PROP_NONE);
  RNA_def_property_clear_flag(prop, PROP_EDITABLE);
  RNA_def_property_enum_sdna(prop, nullptr, "type");
  RNA_def_property_enum_items(prop, rna_enum_object_shaderfx_type_items);
  RNA_def_property_ui_text(prop, "Type", "");
  RNA_def_property_translation_context(prop, BLT_I18NCONTEXT_ID_ID); /* Abused, for "Light"... */

  /* flags */
  prop = RNA_def_property(srna, "show_viewport", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(prop, nullptr, "mode", eShaderFxMode_Realtime);
  RNA_def_property_ui_text(prop, "Realtime", "Display effect in viewport");
  RNA_def_property_flag(prop, PROP_LIB_EXCEPTION);
  RNA_def_property_override_flag(prop, PROPOVERRIDE_OVERRIDABLE_LIBRARY);
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");
  RNA_def_property_ui_icon(prop, ICON_RESTRICT_VIEW_ON, 1);

  prop = RNA_def_property(srna, "show_render", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(prop, nullptr, "mode", eShaderFxMode_Render);
  RNA_def_property_override_flag(prop, PROPOVERRIDE_OVERRIDABLE_LIBRARY);
  RNA_def_property_ui_text(prop, "Render", "Use effect during render");
  RNA_def_property_ui_icon(prop, ICON_RESTRICT_RENDER_ON, 1);
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, nullptr);

  prop = RNA_def_property(srna, "show_in_editmode", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(prop, nullptr, "mode", eShaderFxMode_Editmode);
  RNA_def_property_ui_text(prop, "Edit Mode", "Display effect in Edit mode");
  RNA_def_property_update(prop, NC_OBJECT | ND_SHADERFX, "rna_ShaderFx_update");
  RNA_def_property_ui_icon(prop, ICON_EDITMODE_HLT, 0);

  prop = RNA_def_property(srna, "show_expanded", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_flag(prop, PROP_NO_DEG_UPDATE);
  RNA_def_property_boolean_sdna(prop, nullptr, "ui_expand_flag", 0);
  RNA_def_property_override_flag(prop, PROPOVERRIDE_OVERRIDABLE_LIBRARY);
  RNA_def_property_ui_text(prop, "Expanded", "Set effect expansion in the user interface");
  RNA_def_property_ui_icon(prop, ICON_DISCLOSURE_TRI_RIGHT, 1); /* BFA */

  /* types */
  rna_def_shader_fx_blur(brna);
  rna_def_shader_fx_colorize(brna);
  rna_def_shader_fx_wave(brna);
  rna_def_shader_fx_pixel(brna);
  rna_def_shader_fx_rim(brna);
  rna_def_shader_fx_shadow(brna);
  rna_def_shader_fx_glow(brna);
  rna_def_shader_fx_swirl(brna);
  rna_def_shader_fx_flip(brna);
}

#endif
