#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_eigenvals(configure, sample, get_tbmodels_process_inputs):
    from aiida.orm import DataFactory
    from aiida.work.run import run

    process, inputs = get_tbmodels_process_inputs('tbmodels.eigenvals')

    input_model = DataFactory('singlefile')()
    input_model.add_path(sample('model.hdf5'))
    inputs.tb_model = input_model

    k_mesh = DataFactory('array.kpoints')()
    k_mesh.set_kpoints_mesh([4, 4, 4], offset=[0, 0, 0])
    inputs.kpoints = k_mesh

    output = run(process, **inputs)
    assert isinstance(output['bands'], DataFactory('array.bands'))
