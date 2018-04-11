#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import os


def test_parse(configure_with_daemon, sample, get_tbmodels_process_builder):
    from aiida.orm.data.folder import FolderData
    from aiida.orm import DataFactory, load_node
    from aiida.work.launch import run_get_node

    builder = get_tbmodels_process_builder('tbmodels.parse')

    input_path = sample('bi_wannier_output')
    input_folder = FolderData()
    for fn in os.listdir(input_path):
        input_folder.add_path(os.path.join(input_path, fn), fn)
    builder.wannier_folder = input_folder

    output, calc = run_get_node(builder)

    assert isinstance(output['tb_model'], DataFactory('singlefile'))
    assert calc.get_hash() == calc.get_extra('_aiida_hash')
