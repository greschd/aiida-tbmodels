#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import numpy as np

def test_bandevaluation(configure_with_daemon, sample, get_tbmodels_process_inputs):
    from aiida.orm import DataFactory
    from aiida.orm.code import Code
    from aiida.work.run import run
    from aiida_tbmodels.work.bandevaluation import BandEvaluation
    from aiida_bands_inspect.io import read_bands

    output = run(
        BandEvaluation,
        tbmodels_code=Code.get_from_string('tbmodels'),
        bands_inspect_code=Code.get_from_string('bands_inspect'),
        tb_model=DataFactory('singlefile')(file=sample('silicon/model.hdf5')),
        reference_bands=read_bands(sample('silicon/bands.hdf5'))
    )
    assert np.isclose(output['difference'].value, 0.)
