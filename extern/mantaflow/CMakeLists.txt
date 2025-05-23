# SPDX-FileCopyrightText: 2016 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

set(MANTAVERSION "0.13")

add_definitions(-DWITH_FLUID=1)

# Compile Mantaflow dependencies too (e.g. `cnpy` for NUMPY file IO).
# Make sure that dependencies exist before enabling this option
# by updating the source files in `extern/`.
set(WITH_MANTA_DEPENDENCIES 0)

# Enable Mantaflow NUMPY support.
set(WITH_MANTA_NUMPY 0)

if(NOT WITH_MANTA_DEPENDENCIES)
  add_definitions(-DNO_CNPY=1)
endif()

set(MANTA_HLP
  helper
)
set(MANTA_PP
  preprocessed
)
if(WITH_MANTA_DEPENDENCIES)
  set(MANTA_DEP
    dependencies
  )
endif()

if(WITH_TBB)
  add_definitions(-DTBB=1)
endif()

if(WITH_OPENVDB)
  add_definitions(-DOPENVDB=1)
  # OpenVDB headers use deprecated TBB headers, silence warning.
  add_definitions(-DTBB_SUPPRESS_DEPRECATED_MESSAGES=1)
endif()

if(WITH_OPENVDB_BLOSC)
  add_definitions(-DOPENVDB_BLOSC=1)
endif()

if(WIN32)
  add_definitions(-D_USE_MATH_DEFINES)
endif()

if(WITH_MANTA_NUMPY AND WITH_PYTHON_NUMPY)
  add_definitions(-DNUMPY=1)
endif()

set(INC
  ${MANTA_PP}
  ${MANTA_PP}/fileio
  ${MANTA_PP}/python
  ${MANTA_PP}/plugin
  ${MANTA_HLP}/pwrapper
  ${MANTA_HLP}/util
)

if(WITH_MANTA_DEPENDENCIES)
  list(APPEND INC
    ${MANTA_DEP}/cnpy
  )
endif()

set(INC_SYS
  ${PYTHON_INCLUDE_DIRS}
  ${ZLIB_INCLUDE_DIRS}
)

if(WITH_MANTA_NUMPY AND WITH_PYTHON_NUMPY)
  list(APPEND INC_SYS
    ${PYTHON_NUMPY_INCLUDE_DIRS}
  )
endif()

if(WITH_OPENVDB)
  list(APPEND INC_SYS
    ${OPENVDB_INCLUDE_DIRS}
  )
  list(APPEND LIB
    ${OPENVDB_LIBRARIES}
  )
  if(WIN32)
    # OpenVDB emits lots of these, they should be suppressed through other
    # means but MSVC 16.8/16.9 has broken this functionality, so C4251 is
    # suppressed here explicitly. See
    # https://developercommunity.visualstudio.com/content/problem/1167590/bug.html
    # for details.
    string(APPEND CMAKE_CXX_FLAGS " /wd4251")
  endif()

  # This works around the issue described in #120317 and https://github.com/AcademySoftwareFoundation/openvdb/pull/1786
  if(MSVC_CLANG)
    set_source_files_properties(${MANTA_PP}/fileio/iovdb.cpp PROPERTIES COMPILE_FLAGS -fno-delayed-template-parsing)
  endif()
endif()

set(SRC
  ${MANTA_PP}/commonkernels.h
  ${MANTA_PP}/commonkernels.h.reg.cpp
  ${MANTA_PP}/conjugategrad.cpp
  ${MANTA_PP}/conjugategrad.h
  ${MANTA_PP}/conjugategrad.h.reg.cpp
  ${MANTA_PP}/edgecollapse.cpp
  ${MANTA_PP}/edgecollapse.h
  ${MANTA_PP}/edgecollapse.h.reg.cpp
  ${MANTA_PP}/fastmarch.cpp
  ${MANTA_PP}/fastmarch.h
  ${MANTA_PP}/fastmarch.h.reg.cpp
  ${MANTA_PP}/fileio/iogrids.cpp
  ${MANTA_PP}/fileio/iomeshes.cpp
  ${MANTA_PP}/fileio/ioparticles.cpp
  ${MANTA_PP}/fileio/ioutil.cpp
  ${MANTA_PP}/fileio/iovdb.cpp
  ${MANTA_PP}/fileio/mantaio.cpp
  ${MANTA_PP}/fileio/mantaio.h
  ${MANTA_PP}/fileio/mantaio.h.reg.cpp
  ${MANTA_PP}/fluidsolver.cpp
  ${MANTA_PP}/fluidsolver.h
  ${MANTA_PP}/fluidsolver.h.reg.cpp
  ${MANTA_PP}/general.cpp
  ${MANTA_PP}/general.h
  ${MANTA_PP}/general.h.reg.cpp
  ${MANTA_PP}/gitinfo.h
  ${MANTA_PP}/grid.cpp
  ${MANTA_PP}/grid.h
  ${MANTA_PP}/grid.h.reg.cpp
  ${MANTA_PP}/grid4d.cpp
  ${MANTA_PP}/grid4d.h
  ${MANTA_PP}/grid4d.h.reg.cpp
  ${MANTA_PP}/kernel.cpp
  ${MANTA_PP}/kernel.h
  ${MANTA_PP}/kernel.h.reg.cpp
  ${MANTA_PP}/levelset.cpp
  ${MANTA_PP}/levelset.h
  ${MANTA_PP}/levelset.h.reg.cpp
  ${MANTA_PP}/mesh.cpp
  ${MANTA_PP}/mesh.h
  ${MANTA_PP}/mesh.h.reg.cpp
  ${MANTA_PP}/movingobs.cpp
  ${MANTA_PP}/movingobs.h
  ${MANTA_PP}/movingobs.h.reg.cpp
  ${MANTA_PP}/multigrid.cpp
  ${MANTA_PP}/multigrid.h
  ${MANTA_PP}/multigrid.h.reg.cpp
  ${MANTA_PP}/noisefield.cpp
  ${MANTA_PP}/noisefield.h
  ${MANTA_PP}/noisefield.h.reg.cpp
  ${MANTA_PP}/particle.cpp
  ${MANTA_PP}/particle.h
  ${MANTA_PP}/particle.h.reg.cpp
  ${MANTA_PP}/plugin/advection.cpp
  ${MANTA_PP}/plugin/apic.cpp
  ${MANTA_PP}/plugin/extforces.cpp
  ${MANTA_PP}/plugin/fire.cpp
  ${MANTA_PP}/plugin/flip.cpp
  ${MANTA_PP}/plugin/fluidguiding.cpp
  ${MANTA_PP}/plugin/initplugins.cpp
  ${MANTA_PP}/plugin/kepsilon.cpp
  ${MANTA_PP}/plugin/meshplugins.cpp
  ${MANTA_PP}/plugin/pressure.cpp
  ${MANTA_PP}/plugin/ptsplugins.cpp
  ${MANTA_PP}/plugin/secondaryparticles.cpp
  ${MANTA_PP}/plugin/surfaceturbulence.cpp
  ${MANTA_PP}/plugin/viscosity.cpp
  ${MANTA_PP}/plugin/vortexplugins.cpp
  ${MANTA_PP}/plugin/waveletturbulence.cpp
  ${MANTA_PP}/plugin/waves.cpp
  ${MANTA_PP}/python/defines.py
  ${MANTA_PP}/python/defines.py.reg.cpp
  ${MANTA_PP}/registration.cpp
  ${MANTA_PP}/shapes.cpp
  ${MANTA_PP}/shapes.h
  ${MANTA_PP}/shapes.h.reg.cpp
  ${MANTA_PP}/test.cpp
  ${MANTA_PP}/timing.cpp
  ${MANTA_PP}/timing.h
  ${MANTA_PP}/timing.h.reg.cpp
  ${MANTA_PP}/turbulencepart.cpp
  ${MANTA_PP}/turbulencepart.h
  ${MANTA_PP}/turbulencepart.h.reg.cpp
  ${MANTA_PP}/vortexpart.cpp
  ${MANTA_PP}/vortexpart.h
  ${MANTA_PP}/vortexpart.h.reg.cpp
  ${MANTA_PP}/vortexsheet.cpp
  ${MANTA_PP}/vortexsheet.h
  ${MANTA_PP}/vortexsheet.h.reg.cpp

  ${MANTA_HLP}/pwrapper/manta.h
  ${MANTA_HLP}/pwrapper/pclass.cpp
  ${MANTA_HLP}/pwrapper/pclass.h
  ${MANTA_HLP}/pwrapper/pconvert.cpp
  ${MANTA_HLP}/pwrapper/pconvert.h
  ${MANTA_HLP}/pwrapper/pvec3.cpp
  ${MANTA_HLP}/pwrapper/pythonInclude.h
  ${MANTA_HLP}/pwrapper/registry.cpp
  ${MANTA_HLP}/pwrapper/registry.h
  ${MANTA_HLP}/util/integrator.h
  ${MANTA_HLP}/util/interpol.h
  ${MANTA_HLP}/util/interpolHigh.h
  ${MANTA_HLP}/util/matrixbase.h
  ${MANTA_HLP}/util/mcubes.h
  ${MANTA_HLP}/util/quaternion.h
  ${MANTA_HLP}/util/randomstream.h
  ${MANTA_HLP}/util/rcmatrix.h
  ${MANTA_HLP}/util/simpleimage.cpp
  ${MANTA_HLP}/util/simpleimage.h
  ${MANTA_HLP}/util/solvana.h
  ${MANTA_HLP}/util/vector4d.cpp
  ${MANTA_HLP}/util/vector4d.h
  ${MANTA_HLP}/util/vectorbase.cpp
  ${MANTA_HLP}/util/vectorbase.h
)

if(WITH_MANTA_DEPENDENCIES)
  list(APPEND SRC
    ${MANTA_DEP}/cnpy/cnpy.cpp
    ${MANTA_DEP}/cnpy/cnpy.h
  )
endif()
if(WITH_MANTA_NUMPY AND WITH_PYTHON_NUMPY)
  list(APPEND SRC
    ${MANTA_PP}/plugin/numpyconvert.cpp
    ${MANTA_PP}/plugin/tfplugins.cpp
    ${MANTA_HLP}/pwrapper/numpyWrap.cpp
    ${MANTA_HLP}/pwrapper/numpyWrap.h
  )
endif()

set(LIB
  PRIVATE bf::dependencies::optional::tbb
  ${PYTHON_LINKFLAGS}
  ${PYTHON_LIBRARIES}
)

blender_add_lib(extern_mantaflow "${SRC}" "${INC}" "${INC_SYS}" "${LIB}")

if(WITH_OPENVDB)
  # The VDB libs above are only added to as INTERFACE libs by blender_add_lib,
  # meaning extern_mantaflow itself actually does not have a dependency on the
  # OpenVDB libraries, and CMAKE is free to link the VDB libraries before
  # extern_mantaflow causing linker errors on linux. By explicitly declaring
  # a dependency here, CMAKE will do the right thing.
  target_link_libraries(extern_mantaflow PRIVATE ${OPENVDB_LIBRARIES})
endif()
