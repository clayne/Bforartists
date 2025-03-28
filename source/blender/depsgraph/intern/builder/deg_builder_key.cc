/* SPDX-FileCopyrightText: 2013 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

/** \file
 * \ingroup depsgraph
 *
 * Methods for constructing depsgraph
 */

#include "intern/builder/deg_builder_key.h"

#include "RNA_access.hh"
#include "RNA_path.hh"

namespace blender::deg {

/* -------------------------------------------------------------------- */
/** \name Time source
 * \{ */

std::string TimeSourceKey::identifier() const
{
  return std::string("TimeSourceKey");
}

/** \} */

/* -------------------------------------------------------------------- */
/** \name Component
 * \{ */

std::string ComponentKey::identifier() const
{
  const char *idname = (id) ? id->name : "<None>";
  std::string result = std::string("ComponentKey(");
  result += idname;
  result += ", " + std::string(nodeTypeAsString(type));
  if (name[0] != '\0') {
    result += ", '" + std::string(name) + "'";
  }
  result += ')';
  return result;
}

/** \} */

/* -------------------------------------------------------------------- */
/** \name Operation
 * \{ */

std::string OperationKey::identifier() const
{
  std::string result = std::string("OperationKey(");
  result += "type: " + std::string(nodeTypeAsString(component_type));
  result += ", component name: '" + std::string(component_name) + "'";
  result += ", operation code: " + std::string(operationCodeAsString(opcode));
  if (name[0] != '\0') {
    result += ", '" + std::string(name) + "'";
  }
  result += ")";
  return result;
}

/** \} */

/* -------------------------------------------------------------------- */
/** \name RNA path
 * \{ */

RNAPathKey::RNAPathKey(ID *id, const char *path, RNAPointerSource source) : id(id), source(source)
{
  /* Create ID pointer for root of path lookup. */
  PointerRNA id_ptr = RNA_id_pointer_create(id);
  /* Try to resolve path. */
  int index;
  if (!RNA_path_resolve_full(&id_ptr, path, &ptr, &prop, &index)) {
    ptr = PointerRNA_NULL;
    prop = nullptr;
  }
}

RNAPathKey::RNAPathKey(ID *id, const PointerRNA &ptr, PropertyRNA *prop, RNAPointerSource source)
    : id(id), ptr(ptr), prop(prop), source(source)
{
}

RNAPathKey::RNAPathKey(const PointerRNA &target_prop,
                       const char *rna_path_from_target_prop,
                       const RNAPointerSource source)
    : id(target_prop.owner_id), source(source)
{
  /* Try to resolve path. */
  int index;
  if (!RNA_path_resolve_full(&target_prop, rna_path_from_target_prop, &ptr, &prop, &index)) {
    ptr = PointerRNA_NULL;
    prop = nullptr;
  }
}

std::string RNAPathKey::identifier() const
{
  const char *id_name = (id) ? id->name : "<No ID>";
  const char *prop_name = (prop) ? RNA_property_identifier(prop) : "<No Prop>";
  return std::string("RnaPathKey(") + "id: " + id_name + ", prop: '" + prop_name + "')";
}

/** \} */

}  // namespace blender::deg
