#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Tests for the tbmodels.eigenvals calculation.
"""


def test_eigenvals(
    configure_with_daemon,  # pylint: disable=unused-argument
    sample,
    get_tbmodels_process_builder
):
    """
    Test that the eigenvals calculation creates a bands output.
    """
    from aiida.plugins import DataFactory
    from aiida.engine import run

    builder = get_tbmodels_process_builder('tbmodels.eigenvals')

    input_model = DataFactory('singlefile')()
    input_model.add_path(sample('model.hdf5'))
    builder.tb_model = input_model

    k_mesh = DataFactory('array.kpoints')()
    k_mesh.set_kpoints_mesh([4, 4, 4], offset=[0, 0, 0])
    builder.kpoints = k_mesh

    output = run(builder)
    assert isinstance(output['bands'], DataFactory('array.bands'))
