#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from __future__ import division, unicode_literals

import numpy as np


def test_slice(configure_with_daemon, sample, get_tbmodels_process_builder):
    from aiida.orm import DataFactory
    from aiida.orm.data.base import List
    from aiida.work.run import run

    builder = get_tbmodels_process_builder('tbmodels.slice')

    SinglefileData = DataFactory('singlefile')
    input_model = SinglefileData()
    input_model.add_path(sample('model.hdf5'))
    builder.tb_model = input_model

    slice_idx = List()
    slice_idx.extend([0, 3, 2, 1])
    builder.slice_idx = slice_idx

    output = run(builder)
    assert isinstance(output['tb_model'], SinglefileData)
