/* SPDX-FileCopyrightText: 2009-2010 NVIDIA Corporation
 * SPDX-FileCopyrightText: 2011-2022 Blender Foundation
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Adapted code from NVIDIA Corporation. */

#include "bvh/build.h"

#include "bvh/binning.h"
#include "bvh/node.h"
#include "bvh/params.h"
#include "bvh/split.h"

#include "scene/curves.h"
#include "scene/hair.h"
#include "scene/mesh.h"
#include "scene/object.h"
#include "scene/pointcloud.h"
#include "scene/scene.h"

#include "util/algorithm.h"

#include "util/log.h"
#include "util/progress.h"
#include "util/stack_allocator.h"
#include "util/time.h"

CCL_NAMESPACE_BEGIN

/* Constructor / Destructor */

BVHBuild::BVHBuild(const vector<Object *> &objects_,
                   array<int> &prim_type_,
                   array<int> &prim_index_,
                   array<int> &prim_object_,
                   array<float2> &prim_time_,
                   const BVHParams &params_,
                   Progress &progress_)
    : objects(objects_),
      prim_type(prim_type_),
      prim_index(prim_index_),
      prim_object(prim_object_),
      prim_time(prim_time_),
      params(params_),
      progress(progress_),
      progress_start_time(0.0),
      unaligned_heuristic(objects_)
{
  spatial_min_overlap = 0.0f;
}

BVHBuild::~BVHBuild() = default;

/* Adding References */

void BVHBuild::add_reference_triangles(BoundBox &root,
                                       BoundBox &center,
                                       Mesh *mesh,
                                       const int object_index)
{
  const PrimitiveType primitive_type = mesh->primitive_type();
  const Attribute *attr_mP = nullptr;
  if (mesh->has_motion_blur()) {
    attr_mP = mesh->attributes.find(ATTR_STD_MOTION_VERTEX_POSITION);
  }
  const size_t num_triangles = mesh->num_triangles();
  for (uint j = 0; j < num_triangles; j++) {
    const Mesh::Triangle t = mesh->get_triangle(j);
    const float3 *verts = mesh->verts.data();
    if (attr_mP == nullptr) {
      BoundBox bounds = BoundBox::empty;
      t.bounds_grow(verts, bounds);
      if (bounds.valid() && t.valid(verts)) {
        references.push_back(BVHReference(bounds, j, object_index, primitive_type));
        root.grow(bounds);
        center.grow(bounds.center2());
      }
    }
    else if (params.num_motion_triangle_steps == 0 || params.use_spatial_split) {
      /* Motion triangles, simple case: single node for the whole
       * primitive. Lowest memory footprint and faster BVH build but
       * least optimal ray-tracing.
       */
      /* TODO(sergey): Support motion steps for spatially split BVH. */
      const size_t num_verts = mesh->verts.size();
      const size_t num_steps = mesh->motion_steps;
      const float3 *vert_steps = attr_mP->data_float3();
      BoundBox bounds = BoundBox::empty;
      t.bounds_grow(verts, bounds);
      for (size_t step = 0; step < num_steps - 1; step++) {
        t.bounds_grow(vert_steps + step * num_verts, bounds);
      }
      if (bounds.valid()) {
        references.push_back(BVHReference(bounds, j, object_index, primitive_type));
        root.grow(bounds);
        center.grow(bounds.center2());
      }
    }
    else {
      /* Motion triangles, trace optimized case:  we split triangle
       * primitives into separate nodes for each of the time steps.
       * This way we minimize overlap of neighbor triangle primitives.
       */
      const int num_bvh_steps = params.num_motion_triangle_steps * 2 + 1;
      const float num_bvh_steps_inv_1 = 1.0f / (num_bvh_steps - 1);
      const size_t num_verts = mesh->verts.size();
      const size_t num_steps = mesh->motion_steps;
      const float3 *vert_steps = attr_mP->data_float3();
      /* Calculate bounding box of the previous time step.
       * Will be reused later to avoid duplicated work on
       * calculating BVH time step boundbox.
       */
      float3 prev_verts[3];
      t.motion_verts(verts, vert_steps, num_verts, num_steps, 0.0f, prev_verts);
      BoundBox prev_bounds = BoundBox::empty;
      prev_bounds.grow(prev_verts[0]);
      prev_bounds.grow(prev_verts[1]);
      prev_bounds.grow(prev_verts[2]);
      /* Create all primitive time steps, */
      for (int bvh_step = 1; bvh_step < num_bvh_steps; ++bvh_step) {
        const float curr_time = (float)(bvh_step)*num_bvh_steps_inv_1;
        float3 curr_verts[3];
        t.motion_verts(verts, vert_steps, num_verts, num_steps, curr_time, curr_verts);
        BoundBox curr_bounds = BoundBox::empty;
        curr_bounds.grow(curr_verts[0]);
        curr_bounds.grow(curr_verts[1]);
        curr_bounds.grow(curr_verts[2]);
        BoundBox bounds = prev_bounds;
        bounds.grow(curr_bounds);
        if (bounds.valid()) {
          const float prev_time = (float)(bvh_step - 1) * num_bvh_steps_inv_1;
          references.push_back(
              BVHReference(bounds, j, object_index, primitive_type, prev_time, curr_time));
          root.grow(bounds);
          center.grow(bounds.center2());
        }
        /* Current time boundbox becomes previous one for the
         * next time step.
         */
        prev_bounds = curr_bounds;
      }
    }
  }
}

void BVHBuild::add_reference_curves(BoundBox &root,
                                    BoundBox &center,
                                    Hair *hair,
                                    const int object_index)
{
  const Attribute *curve_attr_mP = nullptr;
  if (hair->has_motion_blur()) {
    curve_attr_mP = hair->attributes.find(ATTR_STD_MOTION_VERTEX_POSITION);
  }

  const PrimitiveType primitive_type = hair->primitive_type();

  const size_t num_curves = hair->num_curves();
  for (uint j = 0; j < num_curves; j++) {
    const Hair::Curve curve = hair->get_curve(j);
    const float *curve_radius = hair->get_curve_radius().data();
    for (int k = 0; k < curve.num_keys - 1; k++) {
      if (curve_attr_mP == nullptr) {
        /* Really simple logic for static hair. */
        BoundBox bounds = BoundBox::empty;
        curve.bounds_grow(k, hair->get_curve_keys().data(), curve_radius, bounds);
        if (bounds.valid()) {
          const int packed_type = PRIMITIVE_PACK_SEGMENT(primitive_type, k);
          references.push_back(BVHReference(bounds, j, object_index, packed_type));
          root.grow(bounds);
          center.grow(bounds.center2());
        }
      }
      else if (params.num_motion_curve_steps == 0 || params.use_spatial_split) {
        /* Simple case of motion curves: single node for the while
         * shutter time. Lowest memory usage but less optimal
         * rendering.
         */
        /* TODO(sergey): Support motion steps for spatially split BVH. */
        BoundBox bounds = BoundBox::empty;
        curve.bounds_grow(k, hair->get_curve_keys().data(), curve_radius, bounds);
        const size_t num_keys = hair->get_curve_keys().size();
        const size_t num_steps = hair->get_motion_steps();
        const float4 *key_steps = curve_attr_mP->data_float4();
        for (size_t step = 0; step < num_steps - 1; step++) {
          curve.bounds_grow(k, key_steps + step * num_keys, bounds);
        }
        if (bounds.valid()) {
          const int packed_type = PRIMITIVE_PACK_SEGMENT(primitive_type, k);
          references.push_back(BVHReference(bounds, j, object_index, packed_type));
          root.grow(bounds);
          center.grow(bounds.center2());
        }
      }
      else {
        /* Motion curves, trace optimized case:  we split curve keys
         * primitives into separate nodes for each of the time steps.
         * This way we minimize overlap of neighbor curve primitives.
         */
        const int num_bvh_steps = params.num_motion_curve_steps * 2 + 1;
        const float num_bvh_steps_inv_1 = 1.0f / (num_bvh_steps - 1);
        const size_t num_steps = hair->get_motion_steps();
        const float3 *curve_keys = hair->get_curve_keys().data();
        const float4 *key_steps = curve_attr_mP->data_float4();
        const size_t num_keys = hair->get_curve_keys().size();
        /* Calculate bounding box of the previous time step.
         * Will be reused later to avoid duplicated work on
         * calculating BVH time step boundbox.
         */
        float4 prev_keys[4];
        curve.cardinal_motion_keys(curve_keys,
                                   curve_radius,
                                   key_steps,
                                   num_keys,
                                   num_steps,
                                   0.0f,
                                   k - 1,
                                   k,
                                   k + 1,
                                   k + 2,
                                   prev_keys);
        BoundBox prev_bounds = BoundBox::empty;
        curve.bounds_grow(prev_keys, prev_bounds);
        /* Create all primitive time steps, */
        for (int bvh_step = 1; bvh_step < num_bvh_steps; ++bvh_step) {
          const float curr_time = (float)(bvh_step)*num_bvh_steps_inv_1;
          float4 curr_keys[4];
          curve.cardinal_motion_keys(curve_keys,
                                     curve_radius,
                                     key_steps,
                                     num_keys,
                                     num_steps,
                                     curr_time,
                                     k - 1,
                                     k,
                                     k + 1,
                                     k + 2,
                                     curr_keys);
          BoundBox curr_bounds = BoundBox::empty;
          curve.bounds_grow(curr_keys, curr_bounds);
          BoundBox bounds = prev_bounds;
          bounds.grow(curr_bounds);
          if (bounds.valid()) {
            const float prev_time = (float)(bvh_step - 1) * num_bvh_steps_inv_1;
            const int packed_type = PRIMITIVE_PACK_SEGMENT(primitive_type, k);
            references.push_back(
                BVHReference(bounds, j, object_index, packed_type, prev_time, curr_time));
            root.grow(bounds);
            center.grow(bounds.center2());
          }
          /* Current time boundbox becomes previous one for the
           * next time step.
           */
          prev_bounds = curr_bounds;
        }
      }
    }
  }
}

void BVHBuild::add_reference_points(BoundBox &root,
                                    BoundBox &center,
                                    PointCloud *pointcloud,
                                    const int i)
{
  const Attribute *point_attr_mP = nullptr;
  if (pointcloud->has_motion_blur()) {
    point_attr_mP = pointcloud->attributes.find(ATTR_STD_MOTION_VERTEX_POSITION);
  }

  const float3 *points_data = pointcloud->points.data();
  const float *radius_data = pointcloud->radius.data();
  const size_t num_points = pointcloud->num_points();
  const float4 *motion_data = (point_attr_mP) ? point_attr_mP->data_float4() : nullptr;
  const size_t num_steps = pointcloud->get_motion_steps();

  if (point_attr_mP == nullptr) {
    /* Really simple logic for static points. */
    for (uint j = 0; j < num_points; j++) {
      const PointCloud::Point point = pointcloud->get_point(j);
      BoundBox bounds = BoundBox::empty;
      point.bounds_grow(points_data, radius_data, bounds);
      if (bounds.valid()) {
        references.push_back(BVHReference(bounds, j, i, PRIMITIVE_POINT));
        root.grow(bounds);
        center.grow(bounds.center2());
      }
    }
  }
  else if (params.num_motion_point_steps == 0 || params.use_spatial_split) {
    /* Simple case of motion points: single node for the whole
     * shutter time. Lowest memory usage but less optimal
     * rendering.
     */
    /* TODO(sergey): Support motion steps for spatially split BVH. */
    for (uint j = 0; j < num_points; j++) {
      const PointCloud::Point point = pointcloud->get_point(j);
      BoundBox bounds = BoundBox::empty;
      point.bounds_grow(points_data, radius_data, bounds);
      for (size_t step = 0; step < num_steps - 1; step++) {
        point.bounds_grow(motion_data[step * num_points + j], bounds);
      }
      if (bounds.valid()) {
        references.push_back(BVHReference(bounds, j, i, PRIMITIVE_MOTION_POINT));
        root.grow(bounds);
        center.grow(bounds.center2());
      }
    }
  }
  else {
    /* Motion points, trace optimized case:  we split point
     * primitives into separate nodes for each of the time steps.
     * This way we minimize overlap of neighbor point primitives.
     */
    const int num_bvh_steps = params.num_motion_point_steps * 2 + 1;
    const float num_bvh_steps_inv_1 = 1.0f / (num_bvh_steps - 1);

    for (uint j = 0; j < num_points; j++) {
      const PointCloud::Point point = pointcloud->get_point(j);
      const size_t num_steps = pointcloud->get_motion_steps();
      const float4 *point_steps = point_attr_mP->data_float4();

      /* Calculate bounding box of the previous time step.
       * Will be reused later to avoid duplicated work on
       * calculating BVH time step boundbox.
       */
      const float4 prev_key = point.motion_key(
          points_data, radius_data, point_steps, num_points, num_steps, 0.0f, j);
      BoundBox prev_bounds = BoundBox::empty;
      point.bounds_grow(prev_key, prev_bounds);
      /* Create all primitive time steps, */
      for (int bvh_step = 1; bvh_step < num_bvh_steps; ++bvh_step) {
        const float curr_time = (float)(bvh_step)*num_bvh_steps_inv_1;
        const float4 curr_key = point.motion_key(
            points_data, radius_data, point_steps, num_points, num_steps, curr_time, j);
        BoundBox curr_bounds = BoundBox::empty;
        point.bounds_grow(curr_key, curr_bounds);
        BoundBox bounds = prev_bounds;
        bounds.grow(curr_bounds);
        if (bounds.valid()) {
          const float prev_time = (float)(bvh_step - 1) * num_bvh_steps_inv_1;
          references.push_back(
              BVHReference(bounds, j, i, PRIMITIVE_MOTION_POINT, prev_time, curr_time));
          root.grow(bounds);
          center.grow(bounds.center2());
        }
        /* Current time boundbox becomes previous one for the
         * next time step.
         */
        prev_bounds = curr_bounds;
      }
    }
  }
}

void BVHBuild::add_reference_geometry(BoundBox &root,
                                      BoundBox &center,
                                      Geometry *geom,
                                      const int object_index)
{
  if (geom->is_mesh() || geom->is_volume()) {
    Mesh *mesh = static_cast<Mesh *>(geom);
    add_reference_triangles(root, center, mesh, object_index);
  }
  else if (geom->is_hair()) {
    Hair *hair = static_cast<Hair *>(geom);
    add_reference_curves(root, center, hair, object_index);
  }
  else if (geom->is_pointcloud()) {
    PointCloud *pointcloud = static_cast<PointCloud *>(geom);
    add_reference_points(root, center, pointcloud, object_index);
  }
}

void BVHBuild::add_reference_object(BoundBox &root, BoundBox &center, Object *ob, const int i)
{
  references.push_back(BVHReference(ob->bounds, -1, i, 0));
  root.grow(ob->bounds);
  center.grow(ob->bounds.center2());
}

static size_t count_curve_segments(Hair *hair)
{
  size_t num = 0;
  const size_t num_curves = hair->num_curves();

  for (size_t i = 0; i < num_curves; i++) {
    num += hair->get_curve(i).num_keys - 1;
  }

  return num;
}

static size_t count_primitives(Geometry *geom)
{
  if (geom->is_mesh() || geom->is_volume()) {
    Mesh *mesh = static_cast<Mesh *>(geom);
    return mesh->num_triangles();
  }
  if (geom->is_hair()) {
    Hair *hair = static_cast<Hair *>(geom);
    return count_curve_segments(hair);
  }
  if (geom->is_pointcloud()) {
    PointCloud *pointcloud = static_cast<PointCloud *>(geom);
    return pointcloud->num_points();
  }

  return 0;
}

void BVHBuild::add_references(BVHRange &root)
{
  /* reserve space for references */
  size_t num_alloc_references = 0;

  for (Object *ob : objects) {
    if (params.top_level) {
      if (!ob->is_traceable()) {
        continue;
      }
      if (!ob->get_geometry()->is_instanced()) {
        num_alloc_references += count_primitives(ob->get_geometry());
      }
      else {
        num_alloc_references++;
      }
    }
    else {
      num_alloc_references += count_primitives(ob->get_geometry());
    }
  }

  references.reserve(num_alloc_references);

  /* add references from objects */
  BoundBox bounds = BoundBox::empty;
  BoundBox center = BoundBox::empty;
  int i = 0;

  for (Object *ob : objects) {
    if (params.top_level) {
      if (!ob->is_traceable()) {
        ++i;
        continue;
      }
      if (!ob->get_geometry()->is_instanced()) {
        add_reference_geometry(bounds, center, ob->get_geometry(), i);
      }
      else {
        add_reference_object(bounds, center, ob, i);
      }
    }
    else {
      add_reference_geometry(bounds, center, ob->get_geometry(), i);
    }

    i++;

    if (progress.get_cancel()) {
      return;
    }
  }

  /* happens mostly on empty meshes */
  if (!bounds.valid()) {
    bounds.grow(zero_float3());
  }

  root = BVHRange(bounds, center, 0, references.size());
}

/* Build */

unique_ptr<BVHNode> BVHBuild::run()
{
  BVHRange root;

  /* add references */
  add_references(root);

  if (progress.get_cancel()) {
    return nullptr;
  }

  /* init spatial splits */
  if (params.top_level) {
    /* NOTE: Technically it is supported by the builder but it's not really
     * optimized for speed yet and not really clear yet if it has measurable
     * improvement on render time. Needs some extra investigation before
     * enabling spatial split for top level BVH.
     */
    params.use_spatial_split = false;
  }

  if (!params.top_level && params.use_spatial_split && params.use_unaligned_nodes &&
      !references.empty())
  {
    /* Spatial splitting for curve splitting leads to very long build times.
     *
     * There are also some issues (and, possibly, bugs in the split builder w.r.t how the alignment
     * space is interpreted. It would be good to fix those issues, but due to performance, and the
     * BVH becoming more obsolete with time it might not be the most optimal development time
     * investment.
     *
     * The check is a bit implicit here, it relies on the fact that spatial splits are disabled on
     * the top level, and that an object has primitives of the same type. */
    if (references[0].prim_type() & PRIMITIVE_CURVE) {
      params.use_spatial_split = false;
    }
  }

  spatial_min_overlap = root.bounds().safe_area() * params.spatial_split_alpha;
  spatial_free_index = 0;

  need_prim_time = params.use_motion_steps();

  /* init progress updates */
  double build_start_time;
  build_start_time = progress_start_time = time_dt();
  progress_count = 0;
  progress_total = references.size();
  progress_original_total = progress_total;

  prim_type.resize(references.size());
  prim_index.resize(references.size());
  prim_object.resize(references.size());
  if (need_prim_time) {
    prim_time.resize(references.size());
  }
  else {
    prim_time.resize(0);
  }

  /* build recursively */
  unique_ptr<BVHNode> rootnode;

  if (params.use_spatial_split) {
    /* Perform multithreaded spatial split build. */
    BVHSpatialStorage *local_storage = &spatial_storage.local();
    rootnode = build_node(root, references, 0, local_storage);
    task_pool.wait_work();
  }
  else {
    /* Perform multithreaded binning build. */
    const BVHObjectBinning rootbin(root, (!references.empty()) ? references.data() : nullptr);
    rootnode = build_node(rootbin, 0);
    task_pool.wait_work();
  }

  /* clean up temporary memory usage by threads */
  spatial_storage.clear();

  /* delete if we canceled */
  if (rootnode) {
    if (progress.get_cancel()) {
      rootnode.reset();
      LOG_WORK << "BVH build canceled.";
    }
    else {
      /*rotate(rootnode, 4, 5);*/
      rootnode->update_visibility();
      rootnode->update_time();
    }
    if (rootnode != nullptr) {
      LOG_WORK << "BVH build statistics:"
               << "  Build time: " << time_dt() - build_start_time << "\n"
               << "  Total number of nodes: "
               << string_human_readable_number(rootnode->getSubtreeSize(BVH_STAT_NODE_COUNT))
               << "\n"
               << "  Number of inner nodes: "
               << string_human_readable_number(rootnode->getSubtreeSize(BVH_STAT_INNER_COUNT))
               << "\n"
               << "  Number of leaf nodes: "
               << string_human_readable_number(rootnode->getSubtreeSize(BVH_STAT_LEAF_COUNT))
               << "\n"
               << "  Number of unaligned nodes: "
               << string_human_readable_number(rootnode->getSubtreeSize(BVH_STAT_UNALIGNED_COUNT))
               << "\n"
               << "  Allocation slop factor: "
               << ((prim_type.capacity() != 0) ? (float)prim_type.size() / prim_type.capacity() :
                                                 1.0f)
               << "\n"
               << "  Maximum depth: "
               << string_human_readable_number(rootnode->getSubtreeSize(BVH_STAT_DEPTH));
    }
  }

  return rootnode;
}

void BVHBuild::progress_update()
{
  if (time_dt() - progress_start_time < 0.25) {
    return;
  }

  const double progress_start = (double)progress_count / (double)progress_total;
  const double duplicates = (double)(progress_total - progress_original_total) /
                            (double)progress_total;

  const string msg = string_printf(
      "Building BVH %.0f%%, duplicates %.0f%%", progress_start * 100.0, duplicates * 100.0);

  progress.set_substatus(msg);
  progress_start_time = time_dt();
}

void BVHBuild::thread_build_node(InnerNode *inner,
                                 const int child,
                                 const BVHObjectBinning &range,
                                 const int level)
{
  if (progress.get_cancel()) {
    return;
  }

  /* build nodes */
  unique_ptr<BVHNode> node = build_node(range, level);

  /* set child in inner node */
  inner->children[child] = std::move(node);

  /* update progress */
  if (range.size() < THREAD_TASK_SIZE) {
    /*rotate(node, INT_MAX, 5);*/

    const thread_scoped_lock lock(build_mutex);

    progress_count += range.size();
    progress_update();
  }
}

void BVHBuild::thread_build_spatial_split_node(InnerNode *inner,
                                               const int child,
                                               const BVHRange &range,
                                               vector<BVHReference> &references,
                                               const int level)
{
  if (progress.get_cancel()) {
    return;
  }

  /* Get per-thread memory for spatial split. */
  BVHSpatialStorage *local_storage = &spatial_storage.local();

  /* build nodes */
  unique_ptr<BVHNode> node = build_node(range, references, level, local_storage);

  /* set child in inner node */
  inner->children[child] = std::move(node);
}

bool BVHBuild::range_within_max_leaf_size(const BVHRange &range,
                                          const vector<BVHReference> &references) const
{
  const size_t size = range.size();
  const size_t max_leaf_size = max(max(params.max_triangle_leaf_size, params.max_curve_leaf_size),
                                   params.max_point_leaf_size);

  if (size > max_leaf_size) {
    return false;
  }

  size_t num_triangles = 0;
  size_t num_motion_triangles = 0;
  size_t num_curves = 0;
  size_t num_motion_curves = 0;
  size_t num_points = 0;
  size_t num_motion_points = 0;

  for (int i = 0; i < size; i++) {
    const BVHReference &ref = references[range.start() + i];

    if (ref.prim_type() & PRIMITIVE_CURVE) {
      if (ref.prim_type() & PRIMITIVE_MOTION) {
        num_motion_curves++;
      }
      else {
        num_curves++;
      }
    }
    else if (ref.prim_type() & PRIMITIVE_TRIANGLE) {
      if (ref.prim_type() & PRIMITIVE_MOTION) {
        num_motion_triangles++;
      }
      else {
        num_triangles++;
      }
    }
    else if (ref.prim_type() & PRIMITIVE_POINT) {
      if (ref.prim_type() & PRIMITIVE_MOTION) {
        num_motion_points++;
      }
      else {
        num_points++;
      }
    }
  }

  return (num_triangles <= params.max_triangle_leaf_size) &&
         (num_motion_triangles <= params.max_motion_triangle_leaf_size) &&
         (num_curves <= params.max_curve_leaf_size) &&
         (num_motion_curves <= params.max_motion_curve_leaf_size) &&
         (num_points <= params.max_point_leaf_size) &&
         (num_motion_points <= params.max_motion_point_leaf_size);
}

/* multithreaded binning builder */
unique_ptr<BVHNode> BVHBuild::build_node(const BVHObjectBinning &range, const int level)
{
  const size_t size = range.size();
  const float leafSAH = params.sah_primitive_cost * range.leafSAH;
  const float splitSAH = params.sah_node_cost * range.bounds().half_area() +
                         params.sah_primitive_cost * range.splitSAH;

  /* Have at least one inner node on top level, for performance and correct
   * visibility tests, since object instances do not check visibility flag.
   */
  if (!(range.size() > 0 && params.top_level && level == 0)) {
    /* Make leaf node when threshold reached or SAH tells us. */
    if ((params.small_enough_for_leaf(size, level)) ||
        (range_within_max_leaf_size(range, references) && leafSAH < splitSAH))
    {
      return create_leaf_node(range, references);
    }
  }

  BVHObjectBinning unaligned_range;
  float unalignedSplitSAH = FLT_MAX;
  float unalignedLeafSAH = FLT_MAX;
  Transform aligned_space;
  bool do_unalinged_split = false;
  if (params.use_unaligned_nodes && splitSAH > params.unaligned_split_threshold * leafSAH) {
    aligned_space = unaligned_heuristic.compute_aligned_space(range, references.data());
    unaligned_range = BVHObjectBinning(
        range, references.data(), &unaligned_heuristic, &aligned_space);
    unalignedSplitSAH = params.sah_node_cost * unaligned_range.unaligned_bounds().half_area() +
                        params.sah_primitive_cost * unaligned_range.splitSAH;
    unalignedLeafSAH = params.sah_primitive_cost * unaligned_range.leafSAH;
    if (!(range.size() > 0 && params.top_level && level == 0)) {
      if (unalignedLeafSAH < unalignedSplitSAH && unalignedSplitSAH < splitSAH &&
          range_within_max_leaf_size(range, references))
      {
        return create_leaf_node(range, references);
      }
    }
    /* Check whether unaligned split is better than the regular one. */
    if (unalignedSplitSAH < splitSAH) {
      do_unalinged_split = true;
    }
  }

  /* Perform split. */
  BVHObjectBinning left;
  BVHObjectBinning right;
  if (do_unalinged_split) {
    unaligned_range.split(references.data(), left, right);
  }
  else {
    range.split(references.data(), left, right);
  }

  BoundBox bounds;
  if (do_unalinged_split) {
    bounds = unaligned_heuristic.compute_aligned_boundbox(range, references.data(), aligned_space);
  }
  else {
    bounds = range.bounds();
  }

  /* Create inner node. */
  unique_ptr<InnerNode> inner;
  if (range.size() < THREAD_TASK_SIZE) {
    /* local build */
    unique_ptr<BVHNode> leftnode = build_node(left, level + 1);
    unique_ptr<BVHNode> rightnode = build_node(right, level + 1);

    inner = make_unique<InnerNode>(bounds, std::move(leftnode), std::move(rightnode));
  }
  else {
    /* Threaded build */
    inner = make_unique<InnerNode>(bounds);
    InnerNode *inner_ptr = inner.get();

    task_pool.push(
        [this, inner_ptr, left, level] { thread_build_node(inner_ptr, 0, left, level + 1); });
    task_pool.push(
        [this, inner_ptr, right, level] { thread_build_node(inner_ptr, 1, right, level + 1); });
  }

  if (do_unalinged_split) {
    inner->set_aligned_space(aligned_space);
  }

  return inner;
}

/* multithreaded spatial split builder */
unique_ptr<BVHNode> BVHBuild::build_node(const BVHRange &range,
                                         vector<BVHReference> &references,
                                         const int level,
                                         BVHSpatialStorage *storage)
{
  /* Update progress.
   *
   * TODO(sergey): Currently it matches old behavior, but we can move it to the
   * task thread (which will mimic non=split builder) and save some CPU ticks
   * on checking cancel status.
   */
  progress_update();
  if (progress.get_cancel()) {
    return nullptr;
  }

  /* Small enough or too deep => create leaf. */
  if (!(range.size() > 0 && params.top_level && level == 0)) {
    if (params.small_enough_for_leaf(range.size(), level)) {
      progress_count += range.size();
      return create_leaf_node(range, references);
    }
  }

  /* Perform splitting test. */
  BVHMixedSplit split(this, storage, range, references, level);

  if (!(range.size() > 0 && params.top_level && level == 0)) {
    if (split.no_split) {
      progress_count += range.size();
      return create_leaf_node(range, references);
    }
  }
  const float leafSAH = params.sah_primitive_cost * split.leafSAH;
  const float splitSAH = params.sah_node_cost * range.bounds().half_area() +
                         params.sah_primitive_cost * split.nodeSAH;

  BVHMixedSplit unaligned_split;
  float unalignedSplitSAH = FLT_MAX;
  // float unalignedLeafSAH = FLT_MAX;
  Transform aligned_space;
  bool do_unalinged_split = false;
  if (params.use_unaligned_nodes && splitSAH > params.unaligned_split_threshold * leafSAH) {
    aligned_space = unaligned_heuristic.compute_aligned_space(range, &references.at(0));
    unaligned_split = BVHMixedSplit(
        this, storage, range, references, level, &unaligned_heuristic, &aligned_space);
    // unalignedLeafSAH = params.sah_primitive_cost * split.leafSAH;
    unalignedSplitSAH = params.sah_node_cost * unaligned_split.bounds.half_area() +
                        params.sah_primitive_cost * unaligned_split.nodeSAH;
    /* TODO(sergey): Check we can create leaf already. */
    /* Check whether unaligned split is better than the regular one. */
    if (unalignedSplitSAH < splitSAH) {
      do_unalinged_split = true;
    }
  }

  /* Do split. */
  BVHRange left;
  BVHRange right;
  if (do_unalinged_split) {
    unaligned_split.split(this, left, right, range);
  }
  else {
    split.split(this, left, right, range);
  }

  progress_total += left.size() + right.size() - range.size();

  BoundBox bounds;
  if (do_unalinged_split) {
    bounds = unaligned_heuristic.compute_aligned_boundbox(range, &references.at(0), aligned_space);
  }
  else {
    bounds = range.bounds();
  }

  /* Create inner node. */
  unique_ptr<InnerNode> inner;
  if (range.size() < THREAD_TASK_SIZE) {
    /* Local build. */

    /* Build left node. */
    vector<BVHReference> right_references(references.begin() + right.start(),
                                          references.begin() + right.end());
    right.set_start(0);

    unique_ptr<BVHNode> leftnode = build_node(left, references, level + 1, storage);

    /* Build right node. */
    unique_ptr<BVHNode> rightnode = build_node(right, right_references, level + 1, storage);

    inner = make_unique<InnerNode>(bounds, std::move(leftnode), std::move(rightnode));
  }
  else {
    /* Threaded build. */
    inner = make_unique<InnerNode>(bounds);

    vector<BVHReference> left_references(references.begin() + left.start(),
                                         references.begin() + left.end());
    vector<BVHReference> right_references(references.begin() + right.start(),
                                          references.begin() + right.end());
    right.set_start(0);

    InnerNode *inner_ptr = inner.get();

    /* Create tasks for left and right nodes, using copy for most arguments and
     * move for reference to avoid memory copies. */
    task_pool.push([this, inner_ptr, left, level, refs = std::move(left_references)]() mutable {
      thread_build_spatial_split_node(inner_ptr, 0, left, refs, level + 1);
    });
    task_pool.push([this, inner_ptr, right, level, refs = std::move(right_references)]() mutable {
      thread_build_spatial_split_node(inner_ptr, 1, right, refs, level + 1);
    });
  }

  if (do_unalinged_split) {
    inner->set_aligned_space(aligned_space);
  }

  return inner;
}

/* Create Nodes */

unique_ptr<BVHNode> BVHBuild::create_object_leaf_nodes(const BVHReference *ref,
                                                       const int start,
                                                       const int num)
{
  if (num == 0) {
    const BoundBox bounds = BoundBox::empty;
    return make_unique<LeafNode>(bounds, 0, 0, 0);
  }
  if (num == 1) {
    assert(start < prim_type.size());
    prim_type[start] = ref->prim_type();
    prim_index[start] = ref->prim_index();
    prim_object[start] = ref->prim_object();
    if (need_prim_time) {
      prim_time[start] = make_float2(ref->time_from(), ref->time_to());
    }

    const uint visibility = objects[ref->prim_object()]->visibility_for_tracing();
    unique_ptr<BVHNode> leaf_node = make_unique<LeafNode>(
        ref->bounds(), visibility, start, start + 1);
    leaf_node->time_from = ref->time_from();
    leaf_node->time_to = ref->time_to();
    return leaf_node;
  }

  const int mid = num / 2;
  unique_ptr<BVHNode> leaf0 = create_object_leaf_nodes(ref, start, mid);
  unique_ptr<BVHNode> leaf1 = create_object_leaf_nodes(ref + mid, start + mid, num - mid);

  BoundBox bounds = BoundBox::empty;
  bounds.grow(leaf0->bounds);
  bounds.grow(leaf1->bounds);

  const float time_from = min(leaf0->time_from, leaf1->time_from);
  const float time_to = max(leaf0->time_to, leaf1->time_to);

  unique_ptr<BVHNode> inner_node = make_unique<InnerNode>(
      bounds, std::move(leaf0), std::move(leaf1));
  inner_node->time_from = time_from;
  inner_node->time_to = time_to;
  return inner_node;
}

unique_ptr<BVHNode> BVHBuild::create_leaf_node(const BVHRange &range,
                                               const vector<BVHReference> &references)
{
  /* This is a bit over-allocating here (considering leaf size into account),
   * but chunk-based re-allocation in vector makes it difficult to use small
   * size of stack storage here. Some tweaks are possible tho.
   *
   * NOTES:
   *  - If the size is too big, we'll have inefficient stack usage,
   *    and lots of cache misses.
   *  - If the size is too small, then we can run out of memory
   *    allowed to be used by vector.
   *    In practice it wouldn't mean crash, just allocator will fall back
   *    to heap which is slower.
   *  - Optimistic re-allocation in STL could jump us out of stack usage
   *    because re-allocation happens in chunks and size of those chunks we
   *    can not control.
   */
  using LeafStackAllocator = StackAllocator<256, int>;
  using LeafTimeStackAllocator = StackAllocator<256, float2>;
  using LeafReferenceStackAllocator = StackAllocator<256, BVHReference>;

  vector<int, LeafStackAllocator> p_type[PRIMITIVE_NUM];
  vector<int, LeafStackAllocator> p_index[PRIMITIVE_NUM];
  vector<int, LeafStackAllocator> p_object[PRIMITIVE_NUM];
  vector<float2, LeafTimeStackAllocator> p_time[PRIMITIVE_NUM];
  vector<BVHReference, LeafReferenceStackAllocator> p_ref[PRIMITIVE_NUM];

  /* TODO(sergey): In theory we should be able to store references. */
  vector<BVHReference, LeafReferenceStackAllocator> object_references;

  uint visibility[PRIMITIVE_NUM] = {0};
  /* NOTE: Keep initialization in sync with actual number of primitives. */
  BoundBox bounds[PRIMITIVE_NUM] = {
      BoundBox::empty, BoundBox::empty, BoundBox::empty, BoundBox::empty};
  int ob_num = 0;
  int num_new_prims = 0;
  /* Fill in per-type type/index array. */
  for (int i = 0; i < range.size(); i++) {
    const BVHReference &ref = references[range.start() + i];
    if (ref.prim_index() != -1) {
      const uint32_t type_index = PRIMITIVE_INDEX(ref.prim_type() & PRIMITIVE_ALL);
      p_ref[type_index].push_back(ref);
      p_type[type_index].push_back(ref.prim_type());
      p_index[type_index].push_back(ref.prim_index());
      p_object[type_index].push_back(ref.prim_object());
      p_time[type_index].push_back(make_float2(ref.time_from(), ref.time_to()));

      bounds[type_index].grow(ref.bounds());
      visibility[type_index] |= objects[ref.prim_object()]->visibility_for_tracing();
      ++num_new_prims;
    }
    else {
      object_references.push_back(ref);
      ++ob_num;
    }
  }

  /* Create leaf nodes for every existing primitive.
   *
   * Here we write primitive types, indices and objects to a temporary array.
   * This way we keep all the heavy memory allocation code outside of the
   * thread lock in the case of spatial split building.
   *
   * TODO(sergey): With some pointer trickery we can write directly to the
   * destination buffers for the non-spatial split BVH.
   */
  unique_ptr<BVHNode> leaves[PRIMITIVE_NUM + 1];
  int num_leaves = 0;
  size_t start_index = 0;
  vector<int, LeafStackAllocator> local_prim_type;
  vector<int, LeafStackAllocator> local_prim_index;
  vector<int, LeafStackAllocator> local_prim_object;
  vector<float2, LeafTimeStackAllocator> local_prim_time;
  local_prim_type.resize(num_new_prims);
  local_prim_index.resize(num_new_prims);
  local_prim_object.resize(num_new_prims);
  if (need_prim_time) {
    local_prim_time.resize(num_new_prims);
  }
  for (int i = 0; i < PRIMITIVE_NUM; ++i) {
    const int num = (int)p_type[i].size();
    if (num != 0) {
      assert(p_type[i].size() == p_index[i].size());
      assert(p_type[i].size() == p_object[i].size());
      Transform aligned_space;
      bool alignment_found = false;
      for (int j = 0; j < num; ++j) {
        const int index = start_index + j;
        local_prim_type[index] = p_type[i][j];
        local_prim_index[index] = p_index[i][j];
        local_prim_object[index] = p_object[i][j];
        if (need_prim_time) {
          local_prim_time[index] = p_time[i][j];
        }
        if (params.use_unaligned_nodes && !alignment_found) {
          alignment_found = unaligned_heuristic.compute_aligned_space(p_ref[i][j], &aligned_space);
        }
      }
      unique_ptr<LeafNode> leaf_node = make_unique<LeafNode>(
          bounds[i], visibility[i], start_index, start_index + num);
      if (true) {
        float time_from = 1.0f;
        float time_to = 0.0f;
        for (int j = 0; j < num; ++j) {
          const BVHReference &ref = p_ref[i][j];
          time_from = min(time_from, ref.time_from());
          time_to = max(time_to, ref.time_to());
        }
        leaf_node->time_from = time_from;
        leaf_node->time_to = time_to;
      }
      if (alignment_found) {
        /* Need to recalculate leaf bounds with new alignment. */
        leaf_node->bounds = BoundBox::empty;
        for (int j = 0; j < num; ++j) {
          const BVHReference &ref = p_ref[i][j];
          const BoundBox ref_bounds = unaligned_heuristic.compute_aligned_prim_boundbox(
              ref, aligned_space);
          leaf_node->bounds.grow(ref_bounds);
        }
        /* Set alignment space. */
        leaf_node->set_aligned_space(aligned_space);
      }
      leaves[num_leaves++] = std::move(leaf_node);
      start_index += num;
    }
  }
  /* Get size of new data to be copied to the packed arrays. */
  const int num_new_leaf_data = start_index;
  const size_t new_leaf_data_size = sizeof(int) * num_new_leaf_data;
  /* Copy actual data to the packed array. */
  if (params.use_spatial_split) {
    spatial_spin_lock.lock();
    /* We use first free index in the packed arrays and mode pointer to the
     * end of the current range.
     *
     * This doesn't give deterministic packed arrays, but it shouldn't really
     * matter because order of children in BVH is deterministic.
     */
    start_index = spatial_free_index;
    spatial_free_index += range.size();
    /* Extend an array when needed. */
    const size_t range_end = start_index + range.size();
    if (prim_type.size() < range_end) {
      /* Avoid extra re-allocations by pre-allocating bigger array in an
       * advance.
       */
      if (range_end >= prim_type.capacity()) {
        const float progress = (float)progress_count / (float)progress_total;
        const float factor = (1.0f - progress);
        const size_t reserve = (size_t)(range_end + (float)range_end * factor);
        prim_type.reserve(reserve);
        prim_index.reserve(reserve);
        prim_object.reserve(reserve);
        if (need_prim_time) {
          prim_time.reserve(reserve);
        }
      }

      prim_type.resize(range_end);
      prim_index.resize(range_end);
      prim_object.resize(range_end);
      if (need_prim_time) {
        prim_time.resize(range_end);
      }
    }
    /* Perform actual data copy. */
    if (new_leaf_data_size > 0) {
      memcpy(&prim_type[start_index], local_prim_type.data(), new_leaf_data_size);
      memcpy(&prim_index[start_index], local_prim_index.data(), new_leaf_data_size);
      memcpy(&prim_object[start_index], local_prim_object.data(), new_leaf_data_size);
      if (need_prim_time) {
        memcpy(
            &prim_time[start_index], local_prim_time.data(), sizeof(float2) * num_new_leaf_data);
      }
    }
    spatial_spin_lock.unlock();
  }
  else {
    /* For the regular BVH builder we simply copy new data starting at the
     * range start. This is totally thread-safe, all threads are living
     * inside of their own range.
     */
    start_index = range.start();
    if (new_leaf_data_size > 0) {
      memcpy(&prim_type[start_index], local_prim_type.data(), new_leaf_data_size);
      memcpy(&prim_index[start_index], local_prim_index.data(), new_leaf_data_size);
      memcpy(&prim_object[start_index], local_prim_object.data(), new_leaf_data_size);
      if (need_prim_time) {
        memcpy(
            &prim_time[start_index], local_prim_time.data(), sizeof(float2) * num_new_leaf_data);
      }
    }
  }

  /* So far leaves were created with the zero-based index in an arrays,
   * here we modify the indices to correspond to actual packed array start
   * index.
   */
  for (int i = 0; i < num_leaves; ++i) {
    LeafNode *leaf = (LeafNode *)leaves[i].get();
    leaf->lo += start_index;
    leaf->hi += start_index;
  }

  /* Create leaf node for object. */
  if (num_leaves == 0 || ob_num) {
    /* Only create object leaf nodes if there are objects or no other
     * nodes created.
     */
    const BVHReference *ref = (ob_num) ? object_references.data() : nullptr;
    leaves[num_leaves] = create_object_leaf_nodes(ref, start_index + num_new_leaf_data, ob_num);
    ++num_leaves;
  }

  /* TODO(sergey): Need to take care of alignment when number of leaves
   * is more than 1.
   */
  if (num_leaves == 1) {
    /* Simplest case: single leaf, just return it.
     * In all the rest cases we'll be creating intermediate inner node with
     * an appropriate bounding box.
     */
    return std::move(leaves[0]);
  }
  if (num_leaves == 2) {
    return make_unique<InnerNode>(range.bounds(), std::move(leaves[0]), std::move(leaves[1]));
  }
  if (num_leaves == 3) {
    const BoundBox inner_bounds = merge(leaves[1]->bounds, leaves[2]->bounds);
    unique_ptr<BVHNode> inner = make_unique<InnerNode>(
        inner_bounds, std::move(leaves[1]), std::move(leaves[2]));
    return make_unique<InnerNode>(range.bounds(), std::move(leaves[0]), std::move(inner));
  }

  /* Should be doing more branches if more primitive types added. */
  assert(num_leaves <= 5);
  const BoundBox inner_bounds_a = merge(leaves[0]->bounds, leaves[1]->bounds);
  const BoundBox inner_bounds_b = merge(leaves[2]->bounds, leaves[3]->bounds);
  unique_ptr<BVHNode> inner_a = make_unique<InnerNode>(
      inner_bounds_a, std::move(leaves[0]), std::move(leaves[1]));
  unique_ptr<BVHNode> inner_b = make_unique<InnerNode>(
      inner_bounds_b, std::move(leaves[2]), std::move(leaves[3]));
  const BoundBox inner_bounds_c = merge(inner_a->bounds, inner_b->bounds);
  unique_ptr<BVHNode> inner_c = make_unique<InnerNode>(
      inner_bounds_c, std::move(inner_a), std::move(inner_b));
  if (num_leaves == 5) {
    return make_unique<InnerNode>(range.bounds(), std::move(inner_c), std::move(leaves[4]));
  }
  return inner_c;

#undef MAX_ITEMS_PER_LEAF
}

/* Tree Rotations */

void BVHBuild::rotate(BVHNode *node, const int max_depth, const int iterations)
{
  /* In tested scenes, this resulted in slightly slower ray-tracing, so disabled
   * it for now. could be implementation bug, or depend on the scene. */
  if (node) {
    for (int i = 0; i < iterations; i++) {
      rotate(node, max_depth);
    }
  }
}

void BVHBuild::rotate(BVHNode *node, const int max_depth)
{
  /* nothing to rotate if we reached a leaf node. */
  if (node->is_leaf() || max_depth < 0) {
    return;
  }

  InnerNode *parent = (InnerNode *)node;

  /* rotate all children first */
  for (size_t c = 0; c < 2; c++) {
    rotate(parent->children[c].get(), max_depth - 1);
  }

  /* compute current area of all children */
  const BoundBox bounds0 = parent->children[0]->bounds;
  const BoundBox bounds1 = parent->children[1]->bounds;

  const float area0 = bounds0.half_area();
  const float area1 = bounds1.half_area();
  float4 child_area = make_float4(area0, area1, 0.0f, 0.0f);

  /* find best rotation. we pick a target child of a first child, and swap
   * this with an other child. we perform the best such swap. */
  float best_cost = FLT_MAX;
  int best_child = -1;
  int best_target = -1;
  int best_other = -1;

  for (size_t c = 0; c < 2; c++) {
    /* ignore leaf nodes as we cannot descent into */
    if (parent->children[c]->is_leaf()) {
      continue;
    }

    InnerNode *child = (InnerNode *)parent->children[c].get();
    const BoundBox &other = (c == 0) ? bounds1 : bounds0;

    /* transpose child bounds */
    const BoundBox target0 = child->children[0]->bounds;
    const BoundBox target1 = child->children[1]->bounds;

    /* compute cost for both possible swaps */
    const float cost0 = merge(other, target1).half_area() - child_area[c];
    const float cost1 = merge(target0, other).half_area() - child_area[c];

    if (min(cost0, cost1) < best_cost) {
      best_child = (int)c;
      best_other = (int)(1 - c);

      if (cost0 < cost1) {
        best_cost = cost0;
        best_target = 0;
      }
      else {
        best_cost = cost0;
        best_target = 1;
      }
    }
  }

  /* if we did not find a swap that improves the SAH then do nothing */
  if (best_cost >= 0) {
    return;
  }

  assert(best_child == 0 || best_child == 1);
  assert(best_target != -1);

  /* perform the best found tree rotation */
  InnerNode *child = (InnerNode *)parent->children[best_child].get();

  swap(parent->children[best_other], child->children[best_target]);
  child->bounds = merge(child->children[0]->bounds, child->children[1]->bounds);
}

CCL_NAMESPACE_END
