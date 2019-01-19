# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the tbmodels.symmetrize calculation.
"""

from aiida.orm.data.singlefile import SinglefileData
from aiida.common.utils import classproperty
from aiida.common.exceptions import InputValidationError

from ._base import ModelInputBase, ModelOutputBase


class SymmetrizeCalculation(ModelInputBase, ModelOutputBase):
    """
    Calculation class for the 'tbmodels symmetrize' command, which creates a symmetrized tight-binding model from a tight-binding model and symmetry representations.
    """

    @classproperty
    def _use_methods(cls):  # pylint: disable=no-self-argument
        retdict = super(SymmetrizeCalculation, cls)._use_methods
        retdict.update(  # pylint: disable=no-member
            symmetries=dict(
                valid_types=SinglefileData,
                additional_parameter=None,
                linkname='symmetries',
                docstring="File containing the symmetries in HDF5 format."
            )
        )
        return retdict

    def _prepare_for_submission(self, tempfolder, inputdict):
        try:
            symmetries_file = inputdict.pop(self.get_linkname('symmetries'))
        except KeyError:
            raise InputValidationError(
                "No symmetries specified for this calculation."
            )

        calcinfo, codeinfo = super(SymmetrizeCalculation,
                                   self)._prepare_for_submission(
                                       tempfolder, inputdict
                                   )

        # add symmetries to the files to be copied
        calcinfo.local_copy_list += [
            (symmetries_file.get_file_abs_path(), 'symmetries.hdf5'),
        ]
        codeinfo.cmdline_params = ['symmetrize', '-o', self._OUTPUT_FILE_NAME]

        return calcinfo
