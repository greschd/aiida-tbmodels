#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals


def test_symmetrize(
    configure_with_daemon, sample, get_tbmodels_process_inputs
):
    from aiida.orm import DataFactory
    from aiida.work.run import run

    process, inputs = get_tbmodels_process_inputs('tbmodels.symmetrize')

    SinglefileData = DataFactory('singlefile')

    input_model = SinglefileData()
    input_model.add_path(sample('model.hdf5'))
    inputs.tb_model = input_model

    input_symmetries = SinglefileData()
    input_symmetries.add_path(sample('symmetries.hdf5'))
    inputs.symmetries = input_symmetries

    output = run(process, **inputs)
    assert isinstance(output['tb_model'], SinglefileData)
