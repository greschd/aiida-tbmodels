#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import os
import itertools

import numpy as np
from aiida.orm import QueryBuilder

def get_input_archive():
    archive_description = u'InSb Wannier90 input from HF VASP calculation'
    qb = QueryBuilder()
    ArchiveData = DataFactory('vasp.archive')
    qb.append(
        ArchiveData,
        filters={'description': {'==': archive_description}}
    )
    res = qb.all()
    if len(res) == 0:
        # create archive
        res = ArchiveData()
        input_archive = './reference_input/wannier_archive'
        for fn in os.listdir(input_archive):
            res.add_file(os.path.abspath(os.path.join(input_archive, fn)), fn)
        res.description = archive_description
        res.store()
    elif len(res) > 1:
        raise ValueError('Query returned more than one matching ArchiveData instance.')
    else:
        res = res[0][0]
    return res

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

def run_symmetricextraction():
    params = dict()
    params['wannier_data'] = get_input_archive()

    # wannier code and queue settings
    params['wannier_queue'] = 'dphys_compute'
    params['wannier_code'] = 'Wannier90_2.1.0'
    params['tbmodels_code'] = 'tbmodels_dev'
    k_values = [x if x <= 0.5 else -1 + x for x in np.linspace(0, 1, 6, endpoint=False)]
    k_points = [list(reversed(k)) for k in itertools.product(k_values, repeat=3)]
    wannier_settings = DataFactory('parameter')(
        dict=dict(
            num_wann=14,
            num_bands=36,
            dis_num_iter=1000,
            num_iter=0,
            dis_win_min=-4.5,
            dis_win_max=16.,
            dis_froz_min=-4.,
            dis_froz_max=6.5,
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
    wannier_settings.store()
    params['wannier_settings'] = wannier_settings
    params['symmetries'] = get_singlefile_instance(u'Symmetries for InAs', 'reference_input/symmetries.hdf5')
    slice_idx = DataFactory('tbmodels.list')()
    slice_idx.value = [0, 2, 3, 1, 5, 6, 4, 7, 9, 10, 8, 12, 13, 11]
    slice_idx.store()
    params['slice_idx'] = slice_idx
    wfobj = WorkflowFactory('tbmodels.symmetrictbextraction')(params=params)
    wfobj.store()
    wfobj.start()
    print('Submitted workflow {}'.format(wfobj.pk))

if __name__ == '__main__':
    run_symmetricextraction()
