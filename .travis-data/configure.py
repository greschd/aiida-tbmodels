#!/usr/bin/env python
"""
Usage: python configure.py config_input_file config_output_file
"""

import sys
import subprocess
from os.path import join


def get_path(codename):
    return subprocess.check_output(
        'which {}'.format(codename), shell=True
    ).decode().strip()


tbmodels_path = get_path('tbmodels')
bands_inspect_path = get_path('bands-inspect')

with open(sys.argv[1], 'r') as f:
    res = f.read().format(
        tbmodels_path=tbmodels_path, bands_inspect_path=bands_inspect_path
    )
with open(sys.argv[2], 'w') as f:
    f.write(res)
