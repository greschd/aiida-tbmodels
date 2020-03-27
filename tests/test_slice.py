#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines tests for the tbmodels.slice calculation.
"""

from aiida import orm
from aiida.engine import run_get_node


def test_slice(
    configure_with_daemon,  # pylint: disable=unused-argument
    sample,
    get_tbmodels_process_builder,
    check_calc_ok
):
    """
    Run the tbmodels.slice calculation and check that it outputs
    a tight-binding model.
    """

    builder = get_tbmodels_process_builder('tbmodels.slice')

    builder.tb_model = orm.SinglefileData(file=sample('model.hdf5'))
    builder.slice_idx = orm.List(list=[0, 3, 2, 1])

    output, calc = run_get_node(builder)
    check_calc_ok(calc)
    assert isinstance(output['tb_model'], orm.SinglefileData)
