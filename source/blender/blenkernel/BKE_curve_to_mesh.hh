/* SPDX-FileCopyrightText: 2023 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

/** \file
 * \ingroup bke
 */

#pragma once

struct Mesh;

#include "BLI_virtual_array_fwd.hh"

#include "BKE_attribute_filter.hh"

namespace blender::bke {

class CurvesGeometry;

/**
 * Extrude all splines in the profile curve along the path of every spline in the curve input.
 * Transfer curve attributes to the mesh.
 *
 * \note Normal calculation is by far the slowest part of calculations relating to the result mesh.
 * Although it would be a sensible decision to use the better topology information available while
 * generating the mesh to also generate the normals, that work may wasted if the output mesh is
 * changed anyway in a way that affects the normals. So currently this code uses the safer /
 * simpler solution of deferring normal calculation to the rest of Blender.
 */
Mesh *curve_to_mesh_sweep(const CurvesGeometry &main,
                          const CurvesGeometry &profile,
                          const VArray<float> &scales,
                          bool fill_caps,
                          const bke::AttributeFilter &attribute_filter = {});
/**
 * Create a loose-edge mesh based on the evaluated path of the curve's splines.
 * Transfer curve attributes to the mesh.
 */
Mesh *curve_to_wire_mesh(const CurvesGeometry &curve,
                         const bke::AttributeFilter &attribute_filter = {});

}  // namespace blender::bke
