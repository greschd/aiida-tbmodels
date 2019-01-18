#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from __future__ import division, print_function, unicode_literals


def test_symmetrize(
    configure_with_daemon, sample, get_tbmodels_process_builder
):
    from aiida.orm import DataFactory
    from aiida.work.run import run

    builder = get_tbmodels_process_builder('tbmodels.symmetrize')

    SinglefileData = DataFactory('singlefile')

    input_model = SinglefileData()
    input_model.add_path(sample('model.hdf5'))
    builder.tb_model = input_model

    input_symmetries = SinglefileData()
    input_symmetries.add_path(sample('symmetries.hdf5'))
    builder.symmetries = input_symmetries

    output = run(builder)
    assert isinstance(output['tb_model'], SinglefileData)
