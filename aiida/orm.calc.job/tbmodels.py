# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import json

from aiida.orm import JobCalculation
from aiida.orm.data.folder import FolderData
from aiida.common.utils import classproperty
from aiida.common.exceptions import InputValidationError, ValidationError
from aiida.common.datastructures import CalcInfo, CodeInfo

class TbmodelsCalculation(JobCalculation):
    def _init_internal_params(self):
        super(SumCalculation, self)._init_internal_params()
        
        self._OUTPUT_FILE_NAME = 'model.hdf5'
        self._default_parser = 'tbmodels'
        
    @classproperty
    def _use_methods(cls):
        retdict = super(SumCalculation, cls)._use_methods
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
            
        # input_json = parameters.get_dict()
        
        input_filename = tempfolder.get_abs_path(self._INPUT_FILE_NAME)
        # with open(input_filename, 'w') as infile:
        #     json.dump(input_json, infile)
            
        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.local_copy_list = []
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = [self._OUTPUT_FILE_NAME]
        
        codeinfo = CodeInfo()
        codeinfo.cmdline_params = [self._INPUT_FILE_NAME, self._OUTPUT_FILE_NAME]
        codeinfo.code_uuid = code.uuid
        calcinfo.codes_info = [codeinfo]
        
        return calcinfo
