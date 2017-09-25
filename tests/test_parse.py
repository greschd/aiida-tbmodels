#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import os


def test_parse(configure_with_daemon, sample, get_tbmodels_process_inputs):
    from aiida.orm.data.folder import FolderData
    from aiida.orm import DataFactory
    from aiida.work.run import run

    process, inputs = get_tbmodels_process_inputs('tbmodels.parse')

    input_path = sample('bi_wannier_output')
    input_folder = FolderData()
    for fn in os.listdir(input_path):
        input_folder.add_path(os.path.join(input_path, fn), fn)
    inputs.wannier_folder = input_folder

    output = run(process, **inputs)
    assert isinstance(output['tb_model'], DataFactory('singlefile'))
