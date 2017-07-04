#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from __future__ import division, print_function, unicode_literals

import os
import itertools

from aiida.orm.code import Code
from aiida.orm import DataFactory, CalculationFactory
from aiida.orm.querybuilder import QueryBuilder
from aiida.work.run import run

def get_singlefile_instance(description, path):
    qb = QueryBuilder()
    SinglefileData = DataFactory('singlefile')
    qb.append(
        SinglefileData,
        filters={'description': {'==': description}}
    )
    res = qb.all()
    if len(res) == 0:
        # create archive
        res = SinglefileData()
        res.add_path(os.path.abspath(path))
        res.description = description
        res.store()
    elif len(res) > 1:
        raise ValueError('Query returned more than one matching SinglefileData instance.')
    else:
        res = res[0][0]
    return res

def run_slice():
    SliceCalculation = CalculationFactory('tbmodels.slice')
    process = SliceCalculation.process()
    inputs = process.get_inputs_template()
    inputs.code = Code.get_from_string('tbmodels_dev')
    inputs.tb_model = get_singlefile_instance(
        description='InSb TB model',
        path='./reference_input/model.hdf5'
    )

    # single-core on local machine
    inputs._options.resources = {'num_machines': 1, 'tot_num_mpiprocs': 1}
    inputs._options.withmpi = False

    slice_idx = DataFactory('tbmodels.list')()
    slice_idx.value = [0, 3, 2, 1]
    inputs.slice_idx = slice_idx

    output = run(process, **inputs)
    print(output['tb_model'])

if __name__ == '__main__':
    run_slice()
