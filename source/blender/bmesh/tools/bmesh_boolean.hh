/* SPDX-FileCopyrightText: 2023 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

#pragma once

/** \file
 * \ingroup bmesh
 */

#include <array>

#include "BLI_span.hh"

#include "bmesh_class.hh"

bool BM_mesh_boolean(BMesh *bm,
                     blender::Span<std::array<BMLoop *, 3>> looptris,
                     int (*test_fn)(BMFace *f, void *user_data),
                     void *user_data,
                     int nshapes,
                     bool use_self,
                     bool keep_hidden,
                     bool hole_tolerant,
                     int boolean_mode);

/**
 * Perform a Knife Intersection operation on the mesh `bm`.
 * There are either one or two operands, the same as described above for #BM_mesh_boolean().
 *
 * \param use_separate_all: When true, each edge that is created from the intersection should
 * be used to separate all its incident faces. TODO: implement that.
 *
 * TODO: need to ensure that "selected/non-selected" flag of original faces gets propagated
 * to the intersection result faces.
 */
bool BM_mesh_boolean_knife(BMesh *bm,
                           blender::Span<std::array<BMLoop *, 3>> looptris,
                           int (*test_fn)(BMFace *f, void *user_data),
                           void *user_data,
                           int nshapes,
                           bool use_self,
                           bool use_separate_all,
                           bool hole_tolerant,
                           bool keep_hidden);
