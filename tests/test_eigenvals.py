#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test_eigenvals(
    configure_with_daemon, sample, get_tbmodels_process_builder
):
    from aiida.orm import DataFactory
    from aiida.work.run import run

    builder = get_tbmodels_process_builder('tbmodels.eigenvals')

    input_model = DataFactory('singlefile')()
    input_model.add_path(sample('model.hdf5'))
    builder.tb_model = input_model

    k_mesh = DataFactory('array.kpoints')()
    k_mesh.set_kpoints_mesh([4, 4, 4], offset=[0, 0, 0])
    builder.kpoints = k_mesh

    output = run(builder)
    assert isinstance(output['bands'], DataFactory('array.bands'))
