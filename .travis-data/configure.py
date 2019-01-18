#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Usage: python configure.py config_input_file config_output_file
"""

import sys
import subprocess


def get_path(codename):
    return subprocess.check_output(
        'which {}'.format(codename), shell=True
    ).decode().strip()


TBMODELS_PATH = get_path('tbmodels')
BANDS_INSPECT_PATH = get_path('bands-inspect')

with open(sys.argv[1], 'r') as f:
    RES = f.read().format(
        tbmodels_path=TBMODELS_PATH, bands_inspect_path=BANDS_INSPECT_PATH
    )
with open(sys.argv[2], 'w') as f:
    f.write(RES)
