/* SPDX-FileCopyrightText: 2023 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

#pragma once

#include <Python.h>

#include "intern/bpy_rna.hh"

/** \file
 * \ingroup pythonintern
 */

extern char pyrna_struct_keyframe_insert_doc[];
extern char pyrna_struct_keyframe_delete_doc[];
extern char pyrna_struct_driver_add_doc[];
extern char pyrna_struct_driver_remove_doc[];

[[nodiscard]] PyObject *pyrna_struct_keyframe_insert(BPy_StructRNA *self,
                                                     PyObject *args,
                                                     PyObject *kw);
[[nodiscard]] PyObject *pyrna_struct_keyframe_delete(BPy_StructRNA *self,
                                                     PyObject *args,
                                                     PyObject *kw);
[[nodiscard]] PyObject *pyrna_struct_driver_add(BPy_StructRNA *self, PyObject *args);
[[nodiscard]] PyObject *pyrna_struct_driver_remove(BPy_StructRNA *self, PyObject *args);
