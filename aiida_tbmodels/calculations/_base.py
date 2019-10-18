# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the base classes for tbmodels calculations.
"""

import six

from aiida.orm import SinglefileData
from aiida.engine import CalcJob
from aiida.common import CalcInfo, CodeInfo


class TbmodelsBase(CalcJob):
    """
    General base class for calculations which run the tbmodels code.
    """
    @classmethod
    def define(cls, spec):
        super(TbmodelsBase, cls).define(spec)

        spec.input(
            'metadata.options.output_filename',
            valid_type=six.string_types,
            default=cls._DEFAULT_OUTPUT_FILE
        )

    def prepare_for_submission(self, tempfolder):  # pylint: disable=unused-argument,arguments-differ
        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.remote_copy_list = []

        codeinfo = CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid
        calcinfo.codes_info = [codeinfo]

        return calcinfo, codeinfo


class ModelOutputBase(TbmodelsBase):
    """
    Base class for calculations which have a model (in HDF5 form) as output.
    """

    _DEFAULT_OUTPUT_FILE = 'model_out.hdf5'

    @classmethod
    def define(cls, spec):
        super(ModelOutputBase, cls).define(spec)

        spec.input(
            'metadata.options.parser_name',
            valid_type=six.string_types,
            default='tbmodels.model'
        )

        spec.output(
            'tb_model',
            valid_type=SinglefileData,
            help="Output model in TBmodels HDF5 format."
        )

    def prepare_for_submission(self, tempfolder):
        calcinfo, codeinfo = super(ModelOutputBase,
                                   self).prepare_for_submission(tempfolder)
        calcinfo.retrieve_list = [self.inputs.metadata.options.output_filename]
        return calcinfo, codeinfo


class ModelInputBase(TbmodelsBase):
    """
    Base class for calculations which take a model (in HDF5 form) as input.
    """
    @classmethod
    def define(cls, spec):
        super(ModelInputBase, cls).define(spec)

        spec.input(
            'tb_model',
            valid_type=SinglefileData,
            help="Input model in TBmodels HDF5 format."
        )

    def prepare_for_submission(self, tempfolder):
        super(ModelInputBase, self).prepare_for_submission(tempfolder)

        model_file = self.inputs.tb_model

        calcinfo, codeinfo = super(ModelInputBase,
                                   self).prepare_for_submission(tempfolder)
        calcinfo.local_copy_list = [
            (model_file.uuid, model_file.filename, 'model.hdf5')
        ]

        return calcinfo, codeinfo
