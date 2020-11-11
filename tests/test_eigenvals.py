#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Tests for the tbmodels.eigenvals calculation.
"""

from aiida.engine import run
from aiida.plugins import DataFactory, CalculationFactory


def test_eigenvals(
    configure_with_daemon,  # pylint: disable=unused-argument
    sample,
    get_tbmodels_process_builder
):
    """
    Test that the eigenvals calculation creates a bands output.
    """
    builder = get_tbmodels_process_builder('tbmodels.eigenvals')

    builder.tb_model = DataFactory('singlefile')(file=sample('model.hdf5'))

    k_mesh = DataFactory('array.kpoints')()
    k_mesh.set_kpoints_mesh([4, 4, 4], offset=[0, 0, 0])
    builder.kpoints = k_mesh

    output = run(builder)
    assert isinstance(output['bands'], DataFactory('array.bands'))


def test_eigenvals_calcfunction(
    configure,  # pylint: disable=unused-argument
    sample,
):
    """
    Test that the eigenvals calcfunction creates a bands output.
    """
    eigenvals_calcfunction = CalculationFactory(
        'tbmodels.calcfunctions.eigenvals'
    )
    tb_model = DataFactory('singlefile')(file=sample('model.hdf5'))

    k_mesh = DataFactory('array.kpoints')()
    k_mesh.set_kpoints_mesh([4, 4, 4], offset=[0, 0, 0])

    res = eigenvals_calcfunction(tb_model=tb_model, kpoints=k_mesh)
    assert isinstance(res, DataFactory('array.bands'))
    assert res.get_array('bands').shape == (64, 14)
