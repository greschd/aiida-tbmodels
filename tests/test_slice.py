#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines tests for the tbmodels.slice calculation.
"""

from __future__ import division, unicode_literals


def test_slice(
    configure_with_daemon,  # pylint: disable=unused-argument
    sample,
    get_tbmodels_process_builder
):
    """
    Run the tbmodels.slice calculation and check that it outputs
    a tight-binding model.
    """
    from aiida.plugins import DataFactory
    from aiida.orm import List
    from aiida.engine import run

    builder = get_tbmodels_process_builder('tbmodels.slice')

    SinglefileData = DataFactory('singlefile')  # pylint: disable=invalid-name
    input_model = SinglefileData()
    input_model.add_path(sample('model.hdf5'))
    builder.tb_model = input_model

    slice_idx = List()
    slice_idx.extend([0, 3, 2, 1])
    builder.slice_idx = slice_idx

    output = run(builder)
    assert isinstance(output['tb_model'], SinglefileData)
