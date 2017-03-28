#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import os
import itertools

import numpy as np
from aiida.orm import QueryBuilder

def get_input_folder():
    folder_description = u'InAs Wannier90 input from HF VASP calculation'
    qb = QueryBuilder()
    FolderData = DataFactory('folder')
    qb.append(
        FolderData,
        filters={'description': {'==': folder_description}}
    )
    res = qb.all()
    if len(res) == 0:
        # create archive
        res = FolderData()
        input_folder = './reference_input/wannier_folder'
        for fn in os.listdir(input_folder):
            res.add_path(os.path.abspath(os.path.join(input_folder, fn)), fn)
        res.description = folder_description
        res.store()
    elif len(res) > 1:
        raise ValueError('Query returned more than one matching FolderData instance.')
    else:
        res = res[0][0]
    return res

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

def run_symmetricextraction():
    params = dict()
    params['wannier_data'] = get_input_folder()

    # wannier code and queue settings
    params['wannier_queue'] = 'dphys_compute'
    params['wannier_code'] = 'Wannier90_2.1.0'
    k_values = [x if x <= 0.5 else -1 + x for x in np.linspace(0, 1, 6, endpoint=False)]
    k_points = [list(reversed(k)) for k in itertools.product(k_values, repeat=3)]
    params['wannier_settings'] = DataFactory('parameter')(
        dict=dict(
            num_wann=36,
            use_bloch_phases=True,
            spinors=True,
            unit_cell_cart=[
                [0, 3.2395, 3.2395],
                [3.2395, 0, 3.2395],
                [3.2395, 3.2395, 0]
            ],
            atoms_cart=[
                ['In       0.0000000     0.0000000     0.0000000'],
                ['Sb       1.6197500     1.6197500     1.6197500']
            ],
            mp_grid='6 6 6',
            kpoints=k_points
        )
    )
    params['symmetries'] = get_singlefile_instance(u'Symmetries for InAs', 'reference_input/symmetries.hdf5')
    wfobj = WorkflowFactory('symmetrictbextraction')(params=params)
    wfobj.store()
    wfobj.start()


if __name__ == '__main__':
    run_symmetricextraction()
print(get_input_folder())
