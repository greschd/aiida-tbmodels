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

class TbmodelsBase(JobCalculation):
    def _init_internal_params(self):
        super(TbmodelsBase, self)._init_internal_params()

        self._OUTPUT_FILE_NAME = 'model_out.hdf5'
        self._default_parser = 'tbmodels.model'

    def _prepare_for_submission(self, tempfolder, inputdict):
        try:
            code = inputdict.pop(self.get_linkname('code'))
        except KeyError:
            raise InputValidationError('No code specified for this calculation.')
        if inputdict:
            raise ValidationError('Cannot add other nodes')

        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = [self._OUTPUT_FILE_NAME]

        codeinfo = CodeInfo()
        codeinfo.code_uuid = code.uuid
        calcinfo.codes_info = [codeinfo]

        return calcinfo, codeinfo
