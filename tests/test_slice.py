#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals

import numpy as np

def test_slice(configure, sample):
    from aiida.orm.code import Code
    from aiida.orm import DataFactory, CalculationFactory
    from aiida.work.run import run

    SliceCalculation = CalculationFactory('tbmodels.slice')
    process = SliceCalculation.process()
    inputs = process.get_inputs_template()
    inputs.code = Code.get_from_string('tbmodels')

    SinglefileData = DataFactory('singlefile')
    input_model = SinglefileData()
    input_model.add_path(sample('model.hdf5'))
    inputs.tb_model = input_model

    # single-core on local machine
    inputs._options.resources = {'num_machines': 1, 'tot_num_mpiprocs': 1}
    inputs._options.withmpi = False

    slice_idx = DataFactory('tbmodels.list')()
    slice_idx.value = [0, 3, 2, 1]
    inputs.slice_idx = slice_idx

    output = run(process, **inputs)
    assert isinstance(output['tb_model'], SinglefileData)
