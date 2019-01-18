#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Runs a 'tbmodels slice' calculation.
"""

from __future__ import division, print_function, unicode_literals

import os

from aiida.orm import Code
from aiida.orm.data.base import List
from aiida.orm.data.singlefile import SinglefileData
from aiida.orm.querybuilder import QueryBuilder
from aiida.work.launch import run_get_pid

from aiida_tbmodels.calculations.slice import SliceCalculation


def get_singlefile_instance(description, path):
    """
    Retrieve an instance of SinglefileData with the given description, loading it from ``path`` if it does not exist.
    """
    query_builder = QueryBuilder()
    query_builder.append(
        SinglefileData, filters={'description': {
            '==': description
        }}
    )
    res = query_builder.all()
    if len(res) == 0:
        # create archive
        res = SinglefileData()
        res.add_path(os.path.abspath(path))
        res.description = description
        res.store()
    elif len(res) > 1:
        raise ValueError(
            'Query returned more than one matching SinglefileData instance.'
        )
    else:
        res = res[0][0]
    return res


def run_slice():
    """
    Creates and runs the slice calculation.
    """
    builder = SliceCalculation.get_builder()
    builder.code = Code.get_from_string('tbmodels')

    builder.tb_model = get_singlefile_instance(
        description=u'InSb TB model', path='./reference_input/model.hdf5'
    )

    # single-core on local machine
    builder.options = dict(
        resources=dict(num_machines=1, tot_num_mpiprocs=1), withmpi=False
    )

    builder.slice_idx = List(list=[0, 3, 2, 1])

    result, pid = run_get_pid(builder)
    print('\nRan calculation with PID', pid)
    print('Result:\n', result)


if __name__ == '__main__':
    run_slice()
