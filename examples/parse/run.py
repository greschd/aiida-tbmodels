#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
"""
Runs a 'tbmodels parse' calculation.
"""

from __future__ import division, print_function, unicode_literals

import os

from aiida.orm import Code
from aiida.orm.querybuilder import QueryBuilder
from aiida.orm.data.folder import FolderData
from aiida.work.launch import run_get_pid

from aiida_tbmodels.calculations.parse import ParseCalculation


def get_input_folder():
    """
    Gets or creates the input folder containing the Wannier90 output.
    """
    folder_description = u'Bi Wannier90 output'
    query_builder = QueryBuilder()
    query_builder.append(
        FolderData, filters={'description': {
            '==': folder_description
        }}
    )
    res = query_builder.all()
    if len(res) == 0:
        # create archive
        res = FolderData()
        input_folder = './reference_input'
        for filename in os.listdir(input_folder):
            res.add_path(
                os.path.abspath(os.path.join(input_folder, filename)), filename
            )
        res.description = folder_description
        res.store()
    elif len(res) > 1:
        raise ValueError(
            'Query returned more than one matching FolderData instance.'
        )
    else:
        res = res[0][0]
    return res


def run_parse():
    """
    Creates and runs the parse calculation.
    """
    builder = ParseCalculation.get_builder()
    builder.code = Code.get_from_string('tbmodels')

    # single-core on local machine
    builder.options = dict(
        resources=dict(num_machines=1, tot_num_mpiprocs=1),
        withmpi=False,
    )

    builder.wannier_folder = get_input_folder()

    result, pid = run_get_pid(builder)
    print('\nRan calculation with PID', pid)
    print('Result:', result)


if __name__ == '__main__':
    run_parse()
