#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from __future__ import division, print_function, unicode_literals

import os
import itertools

from aiida.orm import Code, CalculationFactory, Computer, QueryBuilder
from aiida.orm.data.folder import FolderData

def get_input_folder():
    folder_description = u'Bi Wannier90 output'
    qb = QueryBuilder()
    qb.append(
        FolderData,
        filters={'description': {'==': folder_description}}
    )
    res = qb.all()
    if len(res) == 0:
        # create archive
        res = FolderData()
        input_folder = './reference_input'
        for fn in os.listdir(input_folder):
            res.add_path(os.path.abspath(os.path.join(input_folder, fn)), fn)
        res.description = folder_description
        res.store()
    elif len(res) > 1:
        raise ValueError('Query returned more than one matching FolderData instance.')
    else:
        res = res[0][0]
    return res

def run_parse():
    code = Code.get_from_string('tbmodels_dev')
    calc = CalculationFactory('tbmodels.parse')()
    calc.use_code(code)
    # single-core on local machine
    calc.set_resources(dict(
        num_machines=1,
        tot_num_mpiprocs=1
    ))
    calc.set_withmpi(False)
    calc.set_computer(Computer.get('localhost'))
    calc.use_wannier_folder(get_input_folder())

    calc.store_all()
    calc.submit()
    print('Submitted calculation', calc.pk)


if __name__ == '__main__':
    run_parse()
