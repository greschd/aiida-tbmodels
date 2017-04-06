#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from aiida.orm import DataFactory
from aiida.common.utils import classproperty
from aiida.common.exceptions import InputValidationError, ValidationError
from aiida.tools.codespecific.bandstructure_utils.io import write_kpoints

from ._base import ModelInputBase

class BandsCalculation(ModelInputBase):
    @classproperty
    def _use_methods(cls):
        retdict = super(BandsCalculation, cls)._use_methods
        retdict.update(
            kpoints=dict(
                valid_types=DataFactory('kpoints'),
                additional_parameter=None,
                linkname='kpoints',
                docstring="Kpoints for which the eigenvalues are calculated."
            )
        )
        return retdict

    def _prepare_for_submission(self, tempfolder, inputdict):
        calcinfo, codeinfo = super(BandsCalculation, self)._prepare_for_submission(tempfolder, inputdict)

        kpoints_file = tempfolder.get_abs_path('kpoints.hdf5')
        write_kpoints(inputdict.pop('kpoints'), kpoints_file)

        codeinfo.cmdline_params = ['bands', '-k', 'kpoints.hdf5']
