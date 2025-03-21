# SPDX-FileCopyrightText: 2017-2022 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

# ############################################################
# Importing - Same For All Render Layer Tests
# ############################################################

import unittest

from view_layer_common import (
    ViewLayerTesting,
    get_layers,
    get_scene_collections,
    setup_extra_arguments,
)


# ############################################################
# Testing
# ############################################################

class UnitTesting(ViewLayerTesting):
    def test_scene_layers_link(self):
        """
        See if scene copying 'LINK_OBJECTS' is working for scene layers
        """
        import os
        ROOT = self.get_root()

        filepath_layers_json_copy = os.path.join(ROOT, 'layers_copy_link.json')
        self.do_scene_copy(
            filepath_layers_json_copy,
            'LINK_OBJECTS',
            (get_scene_collections, get_layers))


# ############################################################
# Main - Same For All Render Layer Tests
# ############################################################

if __name__ == '__main__':
    UnitTesting._extra_arguments = setup_extra_arguments(__file__)
    unittest.main()
