# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import os
import json

from aiida.common.utils import classproperty
from aiida.common.exceptions import InputValidationError, ValidationError

from ._base import SingleModelInputBase

class SliceCalculation(SingleModelInputBase):
    @classproperty
    def _use_methods(cls):
        retdict = super(SymmetrizeCalculation, cls)._use_methods
        retdict.update(
            slice_idx=dict(
                valid_types=list,
                additional_parameter=None,
                linkname='slice_idx',
                docstring="Indices of the orbitals which are sliced from the model."
            )
        )
        return retdict

    def _prepare_for_submission(self, tempfolder, inputdict):
        try:
            slice_idx = inputdict.pop(self.get_linkname('slice_idx'))
        except KeyError:
            raise InputValidationError('No slice_idx specified for this calculation.')

        model_file, calcinfo, codeinfo = super(SliceCalculation, self)._prepare_for_submission(tempfolder, inputdict)

        codeinfo.cmdline_params = ['slice', '-o', self._OUTPUT_FILE_NAME] + [str(x) for x in slice_idx]

        return calcinfo
