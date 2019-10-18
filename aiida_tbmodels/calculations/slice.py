# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the tbmodels.slice calculation.
"""

from aiida.orm import List

from ._base import ModelInputBase, ModelOutputBase


class SliceCalculation(ModelInputBase, ModelOutputBase):
    """
    Calculation plugin for the 'tbmodels slice' command, which re-orders or slices orbitals of a tight-binding model.
    """
    @classmethod
    def define(cls, spec):
        super(SliceCalculation, cls).define(spec)

        spec.input(
            'slice_idx',
            valid_type=List,
            help="Indices of the orbitals which are sliced from the model."
        )
        spec.exit_code(
            300,
            'ERROR_OUTPUT_MODEL_FILE',
            message='The output model HDF5 file was not found.'
        )

    def prepare_for_submission(self, tempfolder):
        calcinfo, codeinfo = super(SliceCalculation,
                                   self).prepare_for_submission(tempfolder)

        codeinfo.cmdline_params = [
            'slice', '-o', self.inputs.metadata.options.output_filename
        ] + [str(x) for x in self.inputs.slice_idx]

        return calcinfo
