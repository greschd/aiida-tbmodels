# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import os
import json

from aiida.orm import JobCalculation
from aiida.orm.data.singlefile import SinglefileData
from aiida.common.utils import classproperty
from aiida.common.exceptions import InputValidationError, ValidationError
from aiida.common.datastructures import CalcInfo, CodeInfo

class SymmetrizeCalculation(JobCalculation):
    def _init_internal_params(self):
        super(SymmetrizeCalculation, self)._init_internal_params()

        self._OUTPUT_FILE_NAME = 'model_out.hdf5'
        self._default_parser = 'tbmodels.model'

    @classproperty
    def _use_methods(cls):
        retdict = super(SymmetrizeCalculation, cls)._use_methods
        retdict.update(dict(
            tb_model=dict(
                valid_types=SinglefileData,
                additional_parameter=None,
                linkname='tb_model',
                docstring="Input model in TBmodels HDF5 format."
            ),
            symmetries=dict(
                valid_types=SinglefileData,
                additional_parameter=None,
                linkname='symmetries',
                docstring="File containing the symmetries in HDF5 format."
            )
        ))
        return retdict

    def _prepare_for_submission(self, tempfolder, inputdict):
        try:
            model_file = inputdict.pop(self.get_linkname('tb_model'))
        except KeyError:
            raise InputValidationError("No tight-binding model 'tb_model' specified for this calculation.")
        try:
            symmetries_file = inputdict.pop(self.get_linkname('symmetries'))
        except KeyError:
            raise InputValidationError("No symmetries specified for this calculation.")
        try:
            code = inputdict.pop(self.get_linkname('code'))
        except KeyError:
            raise InputValidationError('No code specified for this calculation.')
        if inputdict:
            raise ValidationError('Cannot add other nodes')

        # add input model and symmetries to the files to be copied
        local_copy_list = [
            (model_file.get_file_abs_path(), 'model.hdf5'),
            (symmetries_file.get_file_abs_path(), 'symmetries.hdf5'),
        ]

        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.local_copy_list = local_copy_list
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = [self._OUTPUT_FILE_NAME]

        codeinfo = CodeInfo()
        codeinfo.cmdline_params = ['symmetrize', '-o', self._OUTPUT_FILE_NAME]
        codeinfo.code_uuid = code.uuid
        calcinfo.codes_info = [codeinfo]

        return calcinfo
