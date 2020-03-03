# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the tbmodels.eigenvals calculation.
"""

from aiida.plugins import DataFactory
from aiida_bands_inspect.io import write_kpoints

from ._base import ModelInputBase


class EigenvalsCalculation(ModelInputBase):
    """
    Calculation class for the 'tbmodels eigenvals' command, which computes the eigenvalues from a given tight-binding model.
    """

    _CMD_NAME = 'eigenvals'
    _DEFAULT_OUTPUT_FILE = 'eigenvals.hdf5'

    @classmethod
    def define(cls, spec):
        super(EigenvalsCalculation, cls).define(spec)

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
        # spec.exit_code(
        #     300,
        #     'ERROR_OUTPUT_FILE',
        #     message='The output HDF5 file was not found.'
        # )
        spec.output(
            'bands',
            valid_type=DataFactory('array.bands'),
            help="The calculated eigenvalues of the model at given k-points."
        )

    def prepare_for_submission(self, tempfolder):
        with tempfolder.open('kpoints.hdf5', 'w+b') as kpoints_file:
            write_kpoints(self.inputs.kpoints, kpoints_file)

        calcinfo, codeinfo = super(EigenvalsCalculation,
                                   self).prepare_for_submission(tempfolder)
        calcinfo.retrieve_list = [self.inputs.metadata.options.output_filename]

        codeinfo.cmdline_params += ['-k', 'kpoints.hdf5']
        return calcinfo
