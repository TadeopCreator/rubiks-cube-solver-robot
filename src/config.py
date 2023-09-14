#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et

import os
import json

class Config:

    def __init__(self):
        x = '{"locale": "es", "cube_palette": {"red": [86, 87, 200], "orange": [65, 123, 213], "blue": [170, 101, 73], "green": [83, 130, 53], "white": [160, 166, 164], "yellow": [56, 175, 183]}}'
        #self.config_dir = os.path.expanduser('G:\.shortcut-targets-by-id\1-01mM6c8vbmV3TV0V2PYZ0laF8YcgKIN\Materias\Taller de Proyecto I\Código\rubiks-cube-solver-robot\src')
        #self.settings_file = os.path.join('G:\.shortcut-targets-by-id\1-01mM6c8vbmV3TV0V2PYZ0laF8YcgKIN\Materias\Taller de Proyecto I\Código\rubiks-cube-solver-robot\src', 'settings.json')

        #try:
            #self.settings = json.loads(open(self.settings_file, 'r').read())
        #except Exception:
        self.settings = json.loads(x)

        #if not os.path.exists(self.config_dir):
            #os.mkdir(self.config_dir)

    def get_setting(self, key, default_value=None):
        """Get a specific key from the settings."""
        if key in self.settings:
            return self.settings[key]
        if default_value is not None:
            return default_value
        return None

    def set_setting(self, key, value):
        """Set a specific setting and save it."""
        self.settings[key] = value
        #with open(self.settings_file, 'w') as f:
            #json.dump(self.settings, f)
            #f.close()

config = Config()
