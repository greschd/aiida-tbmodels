#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import os
import sys
import argparse
import itertools

import numpy as np
from aiida.orm import QueryBuilder
from aiida.tools.codespecific.bandstructure_utils.io import read_bands

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

def get_bandsdata():
    qb = QueryBuilder()
    BandsData = DataFactory('array.bands')
    description = 'Silicon bands from TB model.'
    qb.append(
        BandsData,
        filters={'description': {'==': description}}
    )
    res = qb.all()
    if len(res) == 0:
        res = read_bands('input/silicon_bands.hdf5')
        res.store()
    elif len(res) > 1:
        raise ValueError('Query returned more than one matching SinglefileData instance.')
    else:
        res = res[0][0]
    return res

def run():
    params = dict()

    params['tbmodels_code'] = 'tbmodels_dev'
    params['bandstructure_utils_code'] = 'bandstructure_utils_dev'
    params['tb_model'] = get_singlefile_instance('Silicon TB model', 'input/silicon_model.hdf5')
    params['reference_bands'] = get_bandsdata()

    wfobj = WorkflowFactory('tbmodels.bandevaluation')(params=params)
    wfobj.store()
    wfobj.start()
    print('Submitted workflow {}'.format(wfobj.pk))

if __name__ == '__main__':
    run()
