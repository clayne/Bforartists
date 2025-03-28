/* SPDX-FileCopyrightText: 2023 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

#pragma once

#include <cstdint>
#include <memory>
#include <string>

#include "BLI_map.hh"
#include "BLI_math_vector_types.hh"

#include "DNA_texture_types.h"

#include "COM_cached_resource.hh"
#include "COM_result.hh"

namespace blender::compositor {

class Context;

/* ------------------------------------------------------------------------------------------------
 * Cached Texture Key.
 */
class CachedTextureKey {
 public:
  int2 size;
  float3 offset;
  float3 scale;

  CachedTextureKey(int2 size, float3 offset, float3 scale);

  uint64_t hash() const;
};

bool operator==(const CachedTextureKey &a, const CachedTextureKey &b);

/* -------------------------------------------------------------------------------------------------
 * Cached Texture.
 *
 * A cached resource that computes and caches a GPU texture containing the result of evaluating the
 * given texture ID on a space that spans the given size, parameterized by the given parameters. */
class CachedTexture : public CachedResource {
 private:
  Array<float4> color_pixels_;
  Array<float> value_pixels_;

 public:
  Result color_result;
  Result value_result;

  CachedTexture(Context &context,
                Tex *texture,
                bool use_color_management,
                int2 size,
                float3 offset,
                float3 scale);

  ~CachedTexture();
};

/* ------------------------------------------------------------------------------------------------
 * Cached Texture Container.
 */
class CachedTextureContainer : CachedResourceContainer {
 private:
  Map<std::string, Map<CachedTextureKey, std::unique_ptr<CachedTexture>>> map_;

  /* A map that stores the update counts of the textures at the moment they were cached. */
  Map<std::string, uint64_t> update_counts_;

 public:
  void reset() override;

  /* Check if the given texture ID has changed since the last time it was retrieved through its
   * recalculate flag, and if so, invalidate its corresponding cached textures and reset the
   * recalculate flag to ready it to track the next change. Then, check if there is an available
   * CachedTexture cached resource with the given parameters in the container, if one exists,
   * return it, otherwise, return a newly created one and add it to the container. In both cases,
   * tag the cached resource as needed to keep it cached for the next evaluation. */
  CachedTexture &get(Context &context,
                     Tex *texture,
                     bool use_color_management,
                     int2 size,
                     float3 offset,
                     float3 scale);
};

}  // namespace blender::compositor
