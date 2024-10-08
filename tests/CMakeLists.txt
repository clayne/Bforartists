# SPDX-FileCopyrightText: 2014-2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

# Always run tests from install path, so all required scripts and libraries
# are available and we are testing the actual installation layout.
#
# Getting the install path of the executable is somewhat involved, as there are
# no direct CMake generator expressions to get the install paths of executables.
set(TEST_INSTALL_DIR ${CMAKE_INSTALL_PREFIX_WITH_CONFIG})

# Path to Blender and Python executables for all platforms.
if(MSVC)
  set(TEST_BLENDER_EXE ${TEST_INSTALL_DIR}/bforartists.exe)
elseif(APPLE)
  set(TEST_BLENDER_EXE ${TEST_INSTALL_DIR}/Bforartists.app/Contents/MacOS/Bforartists)
else()
  if(WITH_INSTALL_PORTABLE)
    set(TEST_BLENDER_EXE ${TEST_INSTALL_DIR}/bforartists)
  else()
    set(TEST_BLENDER_EXE ${TEST_INSTALL_DIR}/bin/bforartists)
  endif()
endif()

# The installation directory's Python is the best one to use. However, it can only be there
# after the install step, # which means that Python will never be there on a fresh system.
# To suit different needs, the user can pass `-DTEST_PYTHON_EXE=/path/to/python` to CMake.
if(NOT TEST_PYTHON_EXE)
  set(TEST_PYTHON_EXE ${PYTHON_EXECUTABLE})
  if(FIRST_RUN)
    message(STATUS "Tests: Using Python executable: ${TEST_PYTHON_EXE}")
  endif()
elseif(NOT EXISTS ${TEST_PYTHON_EXE})
  message(FATAL_ERROR "Tests: TEST_PYTHON_EXE ${TEST_PYTHON_EXE} does not exist")
endif()


# Include these arguments before all others, they must not interfere with Python execution.
set(TEST_PYTHON_EXE_EXTRA_ARGS "")

# Check if this a Blender managed Python installation, if so, don't add `*.pyc` files.
if(DEFINED LIBDIR)
  path_is_prefix(LIBDIR TEST_PYTHON_EXE _is_prefix)
  if(_is_prefix)
    # Keep the Python in Blender's SVN LIBDIR pristine, to avoid conflicts on updating.
    set(TEST_PYTHON_EXE_EXTRA_ARGS "-B")
  endif()
  unset(_is_prefix)
endif()

# For testing with Valgrind
# set(TEST_BLENDER_EXE valgrind --track-origins=yes --error-limit=no ${TEST_BLENDER_EXE})

# Standard Blender arguments for running tests.
# Specify exit code so that if a Python script error happens, the test fails.
set(TEST_BLENDER_EXE_PARAMS
  --background --factory-startup --debug-memory --debug-exit-on-error --python-exit-code 1
)

# Python CTests
if(WITH_BLENDER AND WITH_PYTHON AND NOT WITH_PYTHON_MODULE)
  add_subdirectory(python)
endif()

# Blender as python module tests.
if(WITH_PYTHON_MODULE)
  add_subdirectory(blender_as_python_module)
endif()

# GTest
add_subdirectory(gtests)

if(WITH_COMPILER_CODE_COVERAGE)
  set(COVERAGE_SCRIPT_PATH ${CMAKE_CURRENT_SOURCE_DIR}/coverage/coverage.py)

  add_custom_target(coverage-report
    ${PYTHON_EXECUTABLE} ${COVERAGE_SCRIPT_PATH} report --build-directory ${CMAKE_BINARY_DIR}
    USES_TERMINAL
  )

  add_custom_target(coverage-reset
    ${PYTHON_EXECUTABLE} ${COVERAGE_SCRIPT_PATH} reset --build-directory ${CMAKE_BINARY_DIR}
    USES_TERMINAL
  )
endif()
