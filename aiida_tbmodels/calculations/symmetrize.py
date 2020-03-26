# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the tbmodels.symmetrize calculation.
"""

from tbmodels.exceptions import SymmetrizeExceptionMarker

from aiida.orm import SinglefileData

from ._base import ModelInputBase, ModelOutputBase

__all__ = ('SymmetrizeCalculation', )


class SymmetrizeCalculation(ModelInputBase, ModelOutputBase):
    """
    Calculation class for the 'tbmodels symmetrize' command, which creates a symmetrized tight-binding model from a tight-binding model and symmetry representations.
    """
    _CMD_NAME = 'symmetrize'

    @classmethod
    def define(cls, spec):
        super(SymmetrizeCalculation, cls).define(spec)

        spec.input(
            'symmetries',
            valid_type=SinglefileData,
            help="File containing the symmetries in HDF5 format."
        )
        spec.exit_code(
            300,
            'ERROR_RESULT_FILE',
            message='The output model HDF5 file was not found.'
        )
        spec.exit_code(
            301,
            SymmetrizeExceptionMarker.INVALID_SYMMETRY_TYPE.name,
            message=SymmetrizeExceptionMarker.INVALID_SYMMETRY_TYPE.value
        )

    def prepare_for_submission(self, tempfolder):
        calcinfo, _ = super().prepare_for_submission(tempfolder)

        symmetries_file = self.inputs.symmetries

        # add symmetries to the files to be copied
        calcinfo.local_copy_list += [
            (
                symmetries_file.uuid, symmetries_file.filename,
                'symmetries.hdf5'
            ),
        ]

        return calcinfo
