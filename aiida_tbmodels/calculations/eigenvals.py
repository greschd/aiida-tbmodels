# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the tbmodels.eigenvals calculation.
"""

from aiida.orm import DataFactory
from aiida.common.utils import classproperty
from aiida_bands_inspect.io import write_kpoints

from ._base import ModelInputBase


class EigenvalsCalculation(ModelInputBase):
    """
    Calculation class for the 'tbmodels eigenvals' command, which computes the eigenvalues from a given tight-binding model.
    """

    def _init_internal_params(self):
        super(EigenvalsCalculation, self)._init_internal_params()

        self._OUTPUT_FILE_NAME = 'eigenvals.hdf5'
        self._default_parser = 'bands_inspect.bands'

    @classproperty
    def _use_methods(cls):  # pylint: disable=no-self-argument
        retdict = super(EigenvalsCalculation, cls)._use_methods
        retdict.update(  # pylint: disable=no-member
            kpoints=dict(
                valid_types=DataFactory('array.kpoints'),
                additional_parameter=None,
                linkname='kpoints',
                docstring="Kpoints for which the eigenvalues are calculated."
            )
        )
        return retdict

    def _prepare_for_submission(self, tempfolder, inputdict):
        kpoints_file = tempfolder.get_abs_path('kpoints.hdf5')
        write_kpoints(inputdict.pop('kpoints'), kpoints_file)

        calcinfo, codeinfo = super(EigenvalsCalculation,
                                   self)._prepare_for_submission(
                                       tempfolder, inputdict
                                   )
        calcinfo.retrieve_list = [self._OUTPUT_FILE_NAME]

        codeinfo.cmdline_params = ['eigenvals', '-k', 'kpoints.hdf5']
        return calcinfo
