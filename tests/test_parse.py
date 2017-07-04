#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import os

def test_parse(configure, sample):
    from aiida.orm.code import Code
    from aiida.orm.data.folder import FolderData
    from aiida.orm import CalculationFactory, DataFactory
    from aiida.work.run import run

    process = CalculationFactory('tbmodels.parse').process()
    inputs = process.get_inputs_template()

    inputs.code = Code.get_from_string('tbmodels')

    # single-core on local machine
    inputs._options.resources = {'num_machines': 1, 'tot_num_mpiprocs': 1}
    inputs._options.withmpi = False

    input_path = sample('bi_wannier_output')
    input_folder = FolderData()
    for fn in os.listdir(input_path):
        input_folder.add_path(os.path.join(input_path, fn), fn)
    inputs.wannier_folder = input_folder

    output = run(process, **inputs)
    assert isinstance(output['tb_model'], DataFactory('singlefile'))
