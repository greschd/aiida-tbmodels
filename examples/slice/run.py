#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from __future__ import division, print_function, unicode_literals

import os
import itertools

from aiida.orm import DataFactory, Code, CalculationFactory, Computer, QueryBuilder

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
    code = Code.get_from_string('tbmodels_dev')
    calc = CalculationFactory('tbmodels.slice')()
    calc.use_code(code)

    calc.use_tb_model(get_singlefile_instance(
        description=u'InSb TB model',
        path='./reference_input/model.hdf5'
    ))

    # single-core on local machine
    calc.set_resources(dict(
        num_machines=1,
        tot_num_mpiprocs=1
    ))
    calc.set_withmpi(False)
    calc.set_computer(Computer.get('localhost'))
    slice_idx = DataFactory('tbmodels.list')()
    slice_idx.value = [0, 3, 2, 1]
    calc.use_slice_idx(slice_idx)
    # calc.use_slice_idx(DataFactory('tbmodels.list')([0, 3, 2, 1]))

    calc.store_all()
    calc.submit()
    print('Submitted calculation', calc.pk)


if __name__ == '__main__':
    run_slice()
