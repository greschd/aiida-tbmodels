# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import os
import json

from aiida.orm import JobCalculation
from aiida.orm.data.folder import FolderData
from aiida.common.utils import classproperty
from aiida.common.exceptions import InputValidationError, ValidationError
from aiida.common.datastructures import CalcInfo, CodeInfo

class ParseCalculation(JobCalculation):
    def _init_internal_params(self):
        super(ParseCalculation, self)._init_internal_params()

        self._OUTPUT_FILE_NAME = 'model_out.hdf5'
        self._default_parser = 'tbmodels.model'

    @classproperty
    def _use_methods(cls):
        retdict = super(ParseCalculation, cls)._use_methods
        retdict.update(dict(
            wannier_folder=dict(
                valid_types=FolderData,
                additional_parameter=None,
                linkname='wannier_folder',
                docstring="Folder containing the Wannier90 output data, with prefix 'wannier90'."
            )
        ))
        return retdict

    def _prepare_for_submission(self, tempfolder, inputdict):
        try:
            wannier_folder = inputdict.pop(self.get_linkname('wannier_folder'))
        except KeyError:
            raise InputValidationError('No wannier_folder specified for this calculation')
        try:
            code = inputdict.pop(self.get_linkname('code'))
        except KeyError:
            raise InputValidationError('No code specified for this calculation.')
        if inputdict:
            raise ValidationError('Cannot add other nodes')

        # get the prefix from the *_hr.dat file
        for filename in wannier_folder.get_folder_list():
            if filename.endswith('_hr.dat'):
                prefix = filename.rsplit('_hr.dat', 1)[0]
                break
        else:
            raise InputValidationError("'wannier_folder' does not contain a *_hr.dat file.")

        # add Wannier90 output files to local_copy_list
        wannier_folder_abspath = wannier_folder.get_abs_path()
        local_copy_list = [
            (os.path.join(wannier_folder_abspath, 'path', filename), filename)
            for filename in wannier_folder.get_folder_list()
        ]

        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.local_copy_list = local_copy_list
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = [self._OUTPUT_FILE_NAME]

        codeinfo = CodeInfo()
        codeinfo.cmdline_params = ['parse', '-p', prefix, '-o', self._OUTPUT_FILE_NAME]
        codeinfo.code_uuid = code.uuid
        calcinfo.codes_info = [codeinfo]

        return calcinfo
