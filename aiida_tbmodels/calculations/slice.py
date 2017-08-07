# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import os
import json

from aiida.orm import DataFactory
from aiida.orm.data.base import List
from aiida.common.utils import classproperty
from aiida.common.exceptions import InputValidationError, ValidationError

from ._base import ModelInputBase, ModelOutputBase

class SliceCalculation(ModelInputBase, ModelOutputBase):
    @classproperty
    def _use_methods(cls):
        retdict = super(SliceCalculation, cls)._use_methods
        retdict.update(
            slice_idx=dict(
                valid_types=List,
                additional_parameter=None,
                linkname='slice_idx',
                docstring="Indices of the orbitals which are sliced from the model."
            )
        )
        return retdict

    def _prepare_for_submission(self, tempfolder, inputdict):
        try:
            slice_idx = inputdict.pop(self.get_linkname('slice_idx')).value
        except KeyError:
            raise InputValidationError('No slice_idx specified for this calculation.')

        calcinfo, codeinfo = super(SliceCalculation, self)._prepare_for_submission(tempfolder, inputdict)

        codeinfo.cmdline_params = ['slice', '-o', self._OUTPUT_FILE_NAME] + [str(x) for x in slice_idx]

        return calcinfo
