#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals

import numpy as np

def test_slice(configure, sample, get_tbmodels_process_inputs):
    from aiida.orm import DataFactory
    from aiida.work.run import run

    process, inputs = get_tbmodels_process_inputs('tbmodels.slice')

    SinglefileData = DataFactory('singlefile')
    input_model = SinglefileData()
    input_model.add_path(sample('model.hdf5'))
    inputs.tb_model = input_model

    slice_idx = DataFactory('tbmodels.list')()
    slice_idx.value = [0, 3, 2, 1]
    inputs.slice_idx = slice_idx

    output = run(process, **inputs)
    assert isinstance(output['tb_model'], SinglefileData)
