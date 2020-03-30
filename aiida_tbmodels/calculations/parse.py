# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the tbmodels.parse calculation.
"""

from tbmodels.exceptions import ParseExceptionMarker

from aiida import orm
from aiida.orm.nodes.data.folder import FolderData
from aiida.common import InputValidationError

from ._base import ModelOutputBase

__all__ = ('ParseCalculation', )


class ParseCalculation(ModelOutputBase):
    """
    Calculation plugin for the 'tbmodels parse' command, which creates a
    TBmodels tight-binding model from the Wannier90 output.
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
            'ERROR_RESULT_FILE',
            message='The output model HDF5 file was not found.'
        )
        spec.exit_code(
            301,
            ParseExceptionMarker.INCOMPLETE_WSVEC_FILE.name,
            message=ParseExceptionMarker.INCOMPLETE_WSVEC_FILE.value
        )
        spec.exit_code(
            401,
            ParseExceptionMarker.AMBIGUOUS_NEAREST_ATOM_POSITIONS.name,
            message=ParseExceptionMarker.AMBIGUOUS_NEAREST_ATOM_POSITIONS.value
        )
        spec.input(
            'pos_kind',
            valid_type=orm.Str,
            default=lambda: orm.Str('wannier'),
            help='Determines how the orbital positions are parsed.'
        )
        spec.input(
            'distance_ratio_threshold',
            valid_type=orm.Float,
            required=False,
            help="Determines the minimum ratio between nearest and "
            "next-nearest atom when parsing with 'nearest_atom' mode."
        )
        spec.inputs.validator = cls._validate_inputs

    @staticmethod
    def _validate_inputs(inputs, ctx=None):  # pylint: disable=unused-argument
        """Validate the inputs of the entire input namespace."""

        if 'distance_ratio_threshold' in inputs:
            if inputs['pos_kind'].value != 'nearest_atom':
                return "Can only set 'distance_ratio_threshold' when 'pos_kind' is 'nearest_atom'."
            if inputs['distance_ratio_threshold'] < 1:
                return "The 'distance_ratio_threshold' value must be at least one."

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

        calcinfo, codeinfo = super().prepare_for_submission(tempfolder)

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
        if 'distance_ratio_threshold' in self.inputs:
            codeinfo.cmdline_params += [
                '--distance-ratio-threshold',
                str(self.inputs.distance_ratio_threshold.value)
            ]

        return calcinfo
