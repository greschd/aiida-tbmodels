#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from __future__ import division, print_function, unicode_literals

import os
import itertools

from aiida.orm.data import Data
from aiida.orm import Code, CalculationFactory, Computer, QueryBuilder

def run_slice():
    code = Code.get_from_string('tbmodels_dev')
    calc = CalculationFactory('tbmodels.slice')()
    calc.use_code(code)
    # single-core on local machine
    calc.set_resources(dict(
        num_machines=1,
        tot_num_mpiprocs=1
    ))
    calc.set_withmpi(False)
    calc.set_computer(Computer.get('localhost'))
    slice_idx = Data()
    slice_idx.value = [0, 3, 2, 1]
    calc.use_slice_idx(slice_idx)

    calc.store_all()
    calc.submit()
    print('Submitted calculation', calc.pk)


if __name__ == '__main__':
    run_slice()
