# SPDX-FileCopyrightText: 2010-2022 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later


_data = []


def update(*args):
    _data[:] = args


def info():
    return tuple(_data)
