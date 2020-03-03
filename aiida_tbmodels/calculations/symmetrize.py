# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the tbmodels.symmetrize calculation.
"""

from aiida.orm import SinglefileData

from ._base import ModelInputBase, ModelOutputBase


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
            'ERROR_OUTPUT_MODEL_FILE',
            message='The output model HDF5 file was not found.'
        )

    def prepare_for_submission(self, tempfolder):
        calcinfo, codeinfo = super(SymmetrizeCalculation,
                                   self).prepare_for_submission(tempfolder)

        symmetries_file = self.inputs.symmetries

        # add symmetries to the files to be copied
        calcinfo.local_copy_list += [
            (
                symmetries_file.uuid, symmetries_file.filename,
                'symmetries.hdf5'
            ),
        ]
        codeinfo.cmdline_params = [
            'symmetrize', '-o',
            self.node.get_option('output_filename')
        ]

        return calcinfo
