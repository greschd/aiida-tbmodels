# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the base classes for tbmodels calculations.
"""

from aiida import orm
from aiida.engine import CalcJob
from aiida.common import CalcInfo, CodeInfo

__all__ = (
    'TbmodelsBase', 'ResultFileMixin', 'ModelOutputBase', 'ModelInputBase'
)


class TbmodelsBase(CalcJob):
    """
    General base class for calculations which run the tbmodels code.
    """

    _CMD_NAME: str

    @classmethod
    def define(cls, spec):
        super().define(spec)

        spec.input(
            'metadata.options.output_filename',
            valid_type=str,
            default='aiida.out'
        )
        spec.input(
            'metadata.options.error_filename',
            valid_type=str,
            default='aiida.err'
        )
        spec.inputs['metadata']['options']['resources'].default = lambda: {
            'num_machines': 1
        }
        spec.exit_code(
            301,
            'UNKNOWN_ERROR',
            message=
            'The standard error file contains an unknown TBmodels exception.'
        )

    def prepare_for_submission(self, tempfolder):  # pylint: disable=unused-argument,arguments-differ
        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.remote_copy_list = []

        codeinfo = CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid
        calcinfo.codes_info = [codeinfo]
        codeinfo.cmdline_params = self._get_cmdline_params()
        codeinfo.stdout_name = self.metadata.options.output_filename
        codeinfo.stderr_name = self.metadata.options.error_filename

        calcinfo.retrieve_list = [
            self.metadata.options.output_filename,
            self.metadata.options.error_filename,
        ]

        return calcinfo, codeinfo

    def _get_cmdline_params(self):
        return [self._CMD_NAME]


class ResultFileMixin:
    """Mixin class to add the 'result_filename' option, and add the
    result file to the list of files to retrieve.
    """
    _RESULT_FILENAME: str

    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.input(
            'metadata.options.result_filename',
            valid_type=str,
            default=cls._RESULT_FILENAME
        )

    def prepare_for_submission(self, tempfolder):
        calcinfo, codeinfo = super().prepare_for_submission(tempfolder)
        calcinfo.retrieve_list += [self.metadata.options.result_filename]
        return calcinfo, codeinfo

    def _get_cmdline_params(self):
        return super()._get_cmdline_params() + [
            '-o', self.metadata.options.result_filename
        ]


class ModelOutputBase(ResultFileMixin, TbmodelsBase):
    """
    Base class for calculations which have a model (in HDF5 form) as output.
    """

    _RESULT_FILENAME = 'model_out.hdf5'

    @classmethod
    def define(cls, spec):
        super().define(spec)

        spec.input(
            'metadata.options.parser_name',
            valid_type=str,
            default='tbmodels.model'
        )
        spec.input(
            'sparsity',
            valid_type=orm.Str,
            required=False,
            help=
            'Set the sparsity of the output model. Requires TBmodels version >=1.4.',
            validator=cls._sparsity_validator
        )

        spec.output(
            'tb_model',
            valid_type=orm.SinglefileData,
            help="Output model in TBmodels HDF5 format."
        )

        spec.exit_code(
            300,
            'ERROR_RESULT_FILE',
            message='The output model HDF5 file was not found.'
        )

    @staticmethod
    def _sparsity_validator(value, port):  # pylint: disable=unused-argument
        """
        Helper function to validate the 'sparsity' input.
        """
        if value:
            sparsity_value = value.value
            allowed_values = ['as_input', 'sparse', 'dense']
            if sparsity_value not in allowed_values:
                return f"Invalid sparsity value '{sparsity_value}', must be one of {allowed_values}"
        return None

    def _get_cmdline_params(self):
        cmdline_params = super()._get_cmdline_params()
        if 'sparsity' in self.inputs:
            cmdline_params.extend(['--sparsity', self.inputs.sparsity.value])
        return cmdline_params


class ModelInputBase(TbmodelsBase):
    """
    Base class for calculations which take a model (in HDF5 form) as input.
    """
    @classmethod
    def define(cls, spec):
        super().define(spec)

        spec.input(
            'tb_model',
            valid_type=orm.SinglefileData,
            help="Input model in TBmodels HDF5 format."
        )

    def prepare_for_submission(self, tempfolder):
        super().prepare_for_submission(tempfolder)

        model_file = self.inputs.tb_model

        calcinfo, codeinfo = super().prepare_for_submission(tempfolder)
        calcinfo.local_copy_list = [
            (model_file.uuid, model_file.filename, 'model.hdf5')
        ]

        return calcinfo, codeinfo
