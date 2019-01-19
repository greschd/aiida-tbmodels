# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the tbmodels.slice calculation.
"""

from aiida.orm.data.base import List
from aiida.common.utils import classproperty
from aiida.common.exceptions import InputValidationError

from ._base import ModelInputBase, ModelOutputBase


class SliceCalculation(ModelInputBase, ModelOutputBase):
    """
    Calculation plugin for the 'tbmodels slice' command, which re-orders or slices orbitals of a tight-binding model.
    """

    @classproperty
    def _use_methods(cls):  # pylint: disable=no-self-argument
        retdict = super(SliceCalculation, cls)._use_methods
        retdict.update(  # pylint: disable=no-member
            slice_idx=dict(
                valid_types=List,
                additional_parameter=None,
                linkname='slice_idx',
                docstring=
                "Indices of the orbitals which are sliced from the model."
            )
        )
        return retdict

    def _prepare_for_submission(self, tempfolder, inputdict):
        try:
            slice_idx = inputdict.pop(self.get_linkname('slice_idx'))
        except KeyError:
            raise InputValidationError(
                'No slice_idx specified for this calculation.'
            )

        calcinfo, codeinfo = super(SliceCalculation,
                                   self)._prepare_for_submission(
                                       tempfolder, inputdict
                                   )

        codeinfo.cmdline_params = ['slice', '-o', self._OUTPUT_FILE_NAME
                                   ] + [str(x) for x in slice_idx]

        return calcinfo
