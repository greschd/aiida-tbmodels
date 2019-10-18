#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Tests for the tbmodels.symmetrize calculation.
"""

from __future__ import division, print_function, unicode_literals


def test_symmetrize(
    configure_with_daemon,  # pylint: disable=unused-argument
    sample,
    get_tbmodels_process_builder,
    check_calc_ok
):
    """
    Tests that the 'symmetrize' calculation successfully creates an output.
    """
    from aiida.plugins import DataFactory
    from aiida.engine import run_get_node

    builder = get_tbmodels_process_builder('tbmodels.symmetrize')

    SinglefileData = DataFactory('singlefile')  # pylint: disable=invalid-name

    builder.tb_model = SinglefileData(file=sample('model.hdf5'))

    builder.symmetries = SinglefileData(file=sample('symmetries.hdf5'))

    output, calc = run_get_node(builder)
    check_calc_ok(calc)
    assert isinstance(output['tb_model'], SinglefileData)
