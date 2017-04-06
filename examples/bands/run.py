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

def run_bands():
    code = Code.get_from_string('tbmodels_dev')
    calc = CalculationFactory('tbmodels.bands')()
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

    k_mesh = DataFactory('kpoints')()
    k_mesh.set_kpoints_mesh([4, 4, 4], offset=[0, 0, 0])
    calc.use_kpoints(k_mesh)

    calc.store_all()
    calc.submit()
    print('Submitted calculation', calc.pk)


if __name__ == '__main__':
    run_bands()
