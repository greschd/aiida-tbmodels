# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the tbmodels.slice calculation.
"""

from aiida.orm import List

from ._base import ModelInputBase, ModelOutputBase

__all__ = ('SliceCalculation', )


class SliceCalculation(ModelInputBase, ModelOutputBase):
    """
    Calculation plugin for the 'tbmodels slice' command, which re-orders or slices orbitals of a tight-binding model.
    """
    _CMD_NAME = 'slice'

    @classmethod
    def define(cls, spec):
        super(SliceCalculation, cls).define(spec)

        spec.input(
            'slice_idx',
            valid_type=List,
            help="Indices of the orbitals which are sliced from the model."
        )

    def prepare_for_submission(self, tempfolder):
        calcinfo, codeinfo = super().prepare_for_submission(tempfolder)

        codeinfo.cmdline_params += [str(x) for x in self.inputs.slice_idx]

        return calcinfo
