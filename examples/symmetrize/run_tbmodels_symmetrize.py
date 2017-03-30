#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from __future__ import division, print_function, unicode_literals

import os
import itertools

from aiida.orm import Code, CalculationFactory, Computer, QueryBuilder
from aiida.orm.data.singlefile import SinglefileData

def get_singlefile_instance(description, path):
    qb = QueryBuilder()
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

def run_symmetrize():
    code = Code.get_from_string('tbmodels_dev')
    calc = CalculationFactory('tbmodels.symmetrize')()
    calc.use_code(code)
    # single-core on local machine
    calc.set_resources(dict(
        num_machines=1,
        tot_num_mpiprocs=1
    ))
    calc.set_withmpi(False)
    calc.set_computer(Computer.get('localhost'))
    calc.use_tb_model(get_singlefile_instance(
        description=u'InAs unsymmetrized TB model',
        path='./reference_input/model_nosym.hdf5'
    ))
    calc.use_symmetries(get_singlefile_instance(
        description=u'InAs symmetries',
        path='./reference_input/symmetries.hdf5'
    ))
    calc.store_all()
    calc.submit()
    print('Submitted calculation', calc.pk)


if __name__ == '__main__':
    run_symmetrize()
