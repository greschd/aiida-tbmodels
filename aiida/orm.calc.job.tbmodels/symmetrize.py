# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import os
import json

from aiida.orm.data.singlefile import SinglefileData
from aiida.common.utils import classproperty
from aiida.common.exceptions import InputValidationError, ValidationError

from ._base import SingleModelInputBase

class SymmetrizeCalculation(SingleModelInputBase):
    @classproperty
    def _use_methods(cls):
        retdict = super(SymmetrizeCalculation, cls)._use_methods
        retdict.update(
            symmetries=dict(
                valid_types=SinglefileData,
                additional_parameter=None,
                linkname='symmetries',
                docstring="File containing the symmetries in HDF5 format."
            )
        )
        return retdict

    def _prepare_for_submission(self, tempfolder, inputdict):
        try:
            symmetries_file = inputdict.pop(self.get_linkname('symmetries'))
        except KeyError:
            raise InputValidationError("No symmetries specified for this calculation.")

        model_file, calcinfo, codeinfo = super(SymmetrizeCalculation, self)._prepare_for_submission(tempfolder, inputdict)

        # add symmetries to the files to be copied
        calcinfo.local_copy_list += [
            (symmetries_file.get_file_abs_path(), 'symmetries.hdf5'),
        ]
        codeinfo.cmdline_params = ['symmetrize', '-o', self._OUTPUT_FILE_NAME]

        return calcinfo
