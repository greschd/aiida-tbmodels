#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import os

from aiida.orm import QueryBuilder

def get_input_folder():
    folder_description = u'InAs Wannier90 input from HF VASP'
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

print(get_input_folder())
