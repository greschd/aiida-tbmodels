#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Tests for the tbmodels.symmetrize calculation.
"""

from aiida import orm
from aiida.engine import run_get_node


def test_symmetrize(
    configure_with_daemon,  # pylint: disable=unused-argument
    sample,
    get_tbmodels_process_builder,
    check_calc_ok
):
    """
    Tests that the 'symmetrize' calculation successfully creates an output.
    """

    builder = get_tbmodels_process_builder('tbmodels.symmetrize')

    builder.tb_model = orm.SinglefileData(file=sample('model.hdf5'))

    builder.symmetries = orm.SinglefileData(file=sample('symmetries.hdf5'))

    output, calc = run_get_node(builder)
    check_calc_ok(calc)
    assert isinstance(output['tb_model'], orm.SinglefileData)
