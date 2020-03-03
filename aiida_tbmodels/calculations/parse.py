# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the tbmodels.parse calculation.
"""

from aiida.orm import Str
from aiida.orm.nodes.data.folder import FolderData
from aiida.common import InputValidationError

from ._base import ModelOutputBase


class ParseCalculation(ModelOutputBase):
    """
    Calculation plugin for the 'tbmodels parse' command, which creates a TBmodels tight-binding model from the Wannier90 output.
    """
    _CMD_NAME = 'parse'

    @classmethod
    def define(cls, spec):
        super(ParseCalculation, cls).define(spec)

        spec.input(
            'wannier_folder',
            valid_type=FolderData,
            help="Folder containing the Wannier90 output data."
        )
        spec.exit_code(
            300,
            'ERROR_OUTPUT_MODEL_FILE',
            message='The output model HDF5 file was not found.'
        )
        spec.input(
            'pos_kind',
            valid_type=Str,
            default=lambda: Str('wannier'),
            help='Determines how the orbital positions are parsed.'
        )

    def prepare_for_submission(self, tempfolder):
        wannier_folder = self.inputs.wannier_folder
        pos_kind = self.inputs.pos_kind.value

        # get the prefix from the *_hr.dat file
        for filename in wannier_folder.list_object_names():
            if filename.endswith('_hr.dat'):
                prefix = filename.rsplit('_hr.dat', 1)[0]
                break
        else:
            raise InputValidationError(
                "'wannier_folder' does not contain a *_hr.dat file."
            )

        calcinfo, codeinfo = super(ParseCalculation,
                                   self).prepare_for_submission(tempfolder)

        # add Wannier90 output files to local_copy_list
        calcinfo.local_copy_list = [
            (wannier_folder.uuid, filename, filename)
            for filename in wannier_folder.list_object_names()
        ]
        codeinfo.cmdline_params += [
            '-p',
            prefix,
            '--pos-kind',
            pos_kind,
        ]

        return calcinfo
