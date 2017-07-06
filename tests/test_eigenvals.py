#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_eigenvals(configure, sample, get_tbmodels_process_inputs):
    from aiida.orm import DataFactory, CalculationFactory

    process, inputs = get_tbmodels_process_inputs('tbmodels.eigenvals')

    input_model = DataFactory('singlefile')()
    input_model.add_path(sample('model.hdf5'))

    inputs.tb_model = input_model
