# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the tbmodels.eigenvals calculation.
"""

from aiida.plugins import DataFactory
from aiida_bands_inspect.io import write

from ._base import ModelInputBase, ResultFileMixin

__all__ = ('EigenvalsCalculation', )


class EigenvalsCalculation(ResultFileMixin, ModelInputBase):
    """
    Calculation class for the 'tbmodels eigenvals' command, which computes the eigenvalues from a given tight-binding model.
    """

    _CMD_NAME = 'eigenvals'
    _RESULT_FILENAME = 'eigenvals.hdf5'

    @classmethod
    def define(cls, spec):
        super().define(spec)

        spec.input(
            'metadata.options.parser_name',
            valid_type=str,
            default='bands_inspect.bands'
        )
        spec.input(
            'kpoints',
            valid_type=DataFactory('array.kpoints'),
            help="Kpoints for which the eigenvalues are calculated."
        )
        spec.exit_code(
            300,
            'ERROR_RESULT_FILE',
            message='The result HDF5 file was not found.'
        )
        spec.output(
            'bands',
            valid_type=DataFactory('array.bands'),
            help="The calculated eigenvalues of the model at given k-points."
        )

    def prepare_for_submission(self, tempfolder):
        with tempfolder.open('kpoints.hdf5', 'w+b') as kpoints_file:
            write(self.inputs.kpoints, kpoints_file)

        calcinfo, _ = super().prepare_for_submission(tempfolder)
        return calcinfo

    def _get_cmdline_params(self):
        return super()._get_cmdline_params() + ['-k', 'kpoints.hdf5']
