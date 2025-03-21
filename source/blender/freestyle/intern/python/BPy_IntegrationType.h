/* SPDX-FileCopyrightText: 2023 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

/** \file
 * \ingroup freestyle
 */

#pragma once

extern "C" {
#include <Python.h>
}

#include "../view_map/Interface1D.h"

///////////////////////////////////////////////////////////////////////////////////////////

extern PyTypeObject IntegrationType_Type;

#define BPy_IntegrationType_Check(v) \
  (PyObject_IsInstance((PyObject *)v, (PyObject *)&IntegrationType_Type))

/*---------------------------Python BPy_IntegrationType visible prototypes-----------*/

int IntegrationType_Init(PyObject *module);

///////////////////////////////////////////////////////////////////////////////////////////
