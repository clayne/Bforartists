#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

################## BFORARTISTS ########################
# To do changes to the default theme, you have to recompile them to the repository. The theming is not stored in the startup.blend. But needs to be recreated.
#
#	1. Save the theme to disk from the theme Editor in the User Preferences. The Add Preset button does this then saves it in to the user preferences folder.
#	2. Grab the *.xml from the appdata folder, and replace the one in the \scripts\presets\interface_theme with the new one.
#	3. To change the factory presests you need to save a userpref.blend, throw it into \tools\utils
#	4. Then open the blender_theme_as_c.py file, and follow the instructions there.
#		This script recreates the userdef_default_theme.c in the \release\datafiles\userdef then.
#		a. Run Script
#			Open console, and navigate to the utils folder.
#			- windows does not auto detect the required python version. So with windows the useage in the console is as follow:
#				py -3 blender_theme_as_c.py userpref.blend
#			or if you just have python 3 installed
#				python blender_theme_as_c.py userpref.blend

"""
Generates 'userdef_default_theme.c' from a 'userpref.blend' file.

Pass your user preferences blend file to this script to update the C source file.

eg:

    ./tools/utils/blender_theme_as_c.py ~/.config/blender/2.80/config/userpref.blend

.. or find the latest:

    ./tools/utils/blender_theme_as_c.py $(find ~/.config/blender -name "userpref.blend" | sort | tail -1)
"""
__all__ = (
    "main",
)


C_SOURCE_HEADER = r'''/* SPDX-FileCopyrightText: 2018 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

/**
 * Generated by 'tools/utils/blender_theme_as_c.py'
 *
 * Do not hand edit this file!
 */

#include "DNA_userdef_types.h"

#include "BLO_userdef_default.h"

/* clang-format off */

/* NOTE: this is endianness-sensitive. */
#define RGBA(c) {((c) >> 24) & 0xff, ((c) >> 16) & 0xff, ((c) >> 8) & 0xff, (c) & 0xff}
#define RGB(c)  {((c) >> 16) & 0xff, ((c) >> 8) & 0xff, (c) & 0xff}

'''


def round_float_32(f):
    from struct import pack, unpack
    return unpack("f", pack("f", f))[0]


def repr_f32(f):
    f_round = round_float_32(f)
    f_str = repr(f)
    f_str_frac = f_str.partition(".")[2]
    if not f_str_frac:
        return f_str
    for i in range(1, len(f_str_frac)):
        f_test = round(f, i)
        f_test_round = round_float_32(f_test)
        if f_test_round == f_round:
            return "{:.{:d}f}".format(f_test, i)
    return f_str


import os

# Avoid maintaining multiple blendfile modules
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "modules"))
del sys

source_dst = os.path.join(
    os.path.dirname(__file__),
    "..", "..",
    "release", "datafiles", "userdef", "userdef_default_theme.c",
)

dna_rename_defs_h = os.path.join(
    os.path.dirname(__file__),
    "..", "..",
    "source", "blender", "makesdna", "intern", "dna_rename_defs.h",
)


def dna_rename_defs(blend):
    """
    """
    from blendfile import DNAName
    import re
    re_dna_struct_rename = re.compile(
        r'DNA_STRUCT_RENAME+\('
        r'([a-zA-Z0-9_]+)' r',\s*'
        r'([a-zA-Z0-9_]+)' r'\)',
    )

    re_dna_struct_rename_elem = re.compile(
        r'DNA_STRUCT_RENAME_MEMBER+\('
        r'([a-zA-Z0-9_]+)' r',\s*'
        r'([a-zA-Z0-9_]+)' r',\s*'
        r'([a-zA-Z0-9_]+)' r'\)',
    )
    with open(dna_rename_defs_h, 'r', encoding='utf-8') as fh:
        data = fh.read()

    struct_runtime_to_storage_map = {}
    member_runtime_to_storage_map = {}

    for line in data.split('\n'):
        m = re_dna_struct_rename.match(line)
        if m is not None:
            struct_storage, struct_runtime = m.groups()
            struct_runtime_to_storage_map[struct_runtime] = struct_storage
            continue

        m = re_dna_struct_rename_elem.match(line)
        if m is not None:
            struct_name_runtime, member_storage, member_runtime = m.groups()
            if struct_name_runtime not in member_runtime_to_storage_map:
                member_runtime_to_storage_map[struct_name_runtime] = []
            member_runtime_to_storage_map[struct_name_runtime].append((member_storage, member_runtime))
            continue

    for struct_name_runtime, members in member_runtime_to_storage_map.items():
        if len(members) > 1:
            # Order renames that are themselves destinations to go first, so that the item is not removed.
            # Needed e.g.
            # `DNA_STRUCT_RENAME_ELEM(Light, energy_new, energy);`
            # `DNA_STRUCT_RENAME_ELEM(Light, energy, energy_deprecated)`
            # ... in this case the order matters.
            member_runtime_set = set(member_runtime for (_member_storage, member_runtime) in members)
            members_ordered = ([], [])
            for (member_storage, member_runtime) in members:
                members_ordered[member_storage not in member_runtime_set].append((member_storage, member_runtime))
            members = members_ordered[0] + members_ordered[1]
            del member_runtime_set, members_ordered

        for (member_storage, member_runtime) in members:
            struct_name_storage = struct_runtime_to_storage_map.get(struct_name_runtime, struct_name_runtime)
            struct_name_storage = struct_name_storage.encode('utf-8')
            # The struct itself may have been renamed.
            member_storage = member_storage.encode('utf-8')
            member_runtime = member_runtime.encode('utf-8')
            dna_struct = blend.structs[blend.sdna_index_from_id[struct_name_storage]]
            for field in dna_struct.fields:
                dna_name = field.dna_name
                if member_storage == dna_name.name_only:
                    field.dna_name = dna_name = DNAName(dna_name.name_full)
                    del dna_struct.field_from_name[dna_name.name_only]
                    dna_name.name_full = dna_name.name_full.replace(member_storage, member_runtime)
                    dna_name.name_only = member_runtime
                    dna_struct.field_from_name[dna_name.name_only] = field


def theme_data(userpref_filename):
    import blendfile
    blend = blendfile.open_blend(userpref_filename)
    dna_rename_defs(blend)
    u = next((c for c in blend.blocks if c.code == b'USER'), None)
    # theme_type = b.sdna_index_from_id[b'bTheme']
    t = u.get_pointer((b'themes', b'first'))
    t.refine_type(b'bTheme')
    return blend, t


def is_ignore_dna_name(name):
    if name.startswith(b'_'):
        return True
    elif name in {
            b'active_theme_area',
    }:
        return True
    else:
        return False


def write_member(fw, indent, _blend, _theme, ls):
    path_old = ()

    for key, value in ls:
        key = key if type(key) is tuple else (key,)
        path_new = key[:-1]

        if tuple(path_new) != tuple(path_old):
            if path_old:
                p = len(path_old) - 1
                while p >= 0 and (p >= len(path_new) or path_new[p] != path_old[p]):
                    indent = p + 1
                    fw('\t' * indent)
                    fw('},\n')
                    p -= 1
                del p

            p = 0
            for p in range(min(len(path_old), len(path_new))):
                if path_old[p] != key[p]:
                    break
                else:
                    p = p + 1

            for i, c in enumerate(path_new[p:]):
                indent = p + i + 1
                fw('\t' * indent)
                if type(c) is bytes:
                    attr = c.decode('ascii')
                    fw(f'.{attr} = ')
                fw('{\n')

        if not is_ignore_dna_name(key[-1]):
            indent = '\t' * (len(path_new) + 1)
            attr = key[-1].decode('ascii')
            if isinstance(value, float):
                if value != 0.0:
                    value_repr = repr_f32(value)
                    fw(f'{indent}.{attr} = {value_repr}f,\n')
            elif isinstance(value, int):
                if value != 0:
                    fw(f'{indent}.{attr} = {value},\n')
            elif isinstance(value, bytes):
                if set(value) != {0}:
                    if len(value) == 3:
                        value_repr = "".join(f'{ub:02x}' for ub in value)
                        fw(f'{indent}.{attr} = RGB(0x{value_repr}),\n')
                    elif len(value) == 4:
                        value_repr = "".join(f'{ub:02x}' for ub in value)
                        fw(f'{indent}.{attr} = RGBA(0x{value_repr}),\n')
                    else:
                        value = value.rstrip(b'\x00')
                        is_ascii = True
                        for ub in value:
                            if not (ub >= 32 and ub < 127):
                                is_ascii = False
                                break
                        if is_ascii:
                            value_repr = value.decode('ascii')
                            fw(f'{indent}.{attr} = "{value_repr}",\n')
                        else:
                            value_repr = "".join(f'{ub:02x}' for ub in value)
                            fw(f'{indent}.{attr} = {{{value_repr}}},\n')
            else:
                fw(f'{indent}.{attr} = {value},\n')
        path_old = path_new


def convert_data(blend, theme, f):
    fw = f.write
    fw(C_SOURCE_HEADER)
    fw('const bTheme U_theme_default = {\n')
    ls = list(theme.items_recursive_iter(use_nil=False))
    write_member(fw, 1, blend, theme, ls)

    fw('};\n')
    fw('\n')
    fw('/* clang-format on */\n')


def file_remove_empty_braces(source_dst):
    with open(source_dst, 'r', encoding='utf-8') as fh:
        data = fh.read()
    # Remove:
    #     .foo = { }
    import re

    def key_replace(match):
        del match
        return ""
    data_prev = None
    # Braces may become empty by removing nested
    while data != data_prev:
        data_prev = data
        data = re.sub(
            r'\s+\.[a-zA-Z_0-9]+\s+=\s+\{\s*\},',
            key_replace, data, re.MULTILINE,
        )

    # Use two spaces instead of tabs.
    data = data.replace('\t', '  ')

    with open(source_dst, 'w', encoding='utf-8') as fh:
        fh.write(data)


def main():
    import sys
    blend, theme = theme_data(sys.argv[-1])
    with open(source_dst, 'w', encoding='utf-8') as fh:
        convert_data(blend, theme, fh)

    # Microsoft Visual Studio doesn't support empty braces.
    file_remove_empty_braces(source_dst)


if __name__ == "__main__":
    main()
