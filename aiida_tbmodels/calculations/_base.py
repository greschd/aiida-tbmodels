# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the base classes for tbmodels calculations.
"""

# pylint: disable=abstract-method

from aiida.orm import JobCalculation
from aiida.common.utils import classproperty
from aiida.orm.data.singlefile import SinglefileData
from aiida.common.exceptions import InputValidationError, ValidationError
from aiida.common.datastructures import CalcInfo, CodeInfo


class TbmodelsBase(JobCalculation):
    """
    General base class for calculations which run the tbmodels code.
    """

    def _prepare_for_submission(self, tempfolder, inputdict):
        try:
            code = inputdict.pop(self.get_linkname('code'))
        except KeyError:
            raise InputValidationError(
                'No code specified for this calculation.'
            )
        if inputdict:
            raise ValidationError(
                'Cannot add other nodes. Remaining input: {}'.
                format(inputdict)
            )

        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.remote_copy_list = []

        codeinfo = CodeInfo()
        codeinfo.code_uuid = code.uuid
        calcinfo.codes_info = [codeinfo]

        return calcinfo, codeinfo


class ModelOutputBase(TbmodelsBase):
    """
    Base class for calculations which have a model (in HDF5 form) as output.
    """

    def _init_internal_params(self):
        super(ModelOutputBase, self)._init_internal_params()

        self._OUTPUT_FILE_NAME = 'model_out.hdf5'
        self._default_parser = 'tbmodels.model'

    def _prepare_for_submission(self, tempfolder, inputdict):
        calcinfo, codeinfo = super(ModelOutputBase,
                                   self)._prepare_for_submission(
                                       tempfolder, inputdict
                                   )
        calcinfo.retrieve_list = [self._OUTPUT_FILE_NAME]
        return calcinfo, codeinfo


class ModelInputBase(TbmodelsBase):
    """
    Base class for calculations which take a model (in HDF5 form) as input.
    """

    @classproperty
    def _use_methods(cls):  # pylint: disable=no-self-argument
        retdict = super(ModelInputBase, cls)._use_methods
        retdict.update(  # pylint: disable=no-member
            dict(
                tb_model=dict(
                    valid_types=SinglefileData,
                    additional_parameter=None,
                    linkname='tb_model',
                    docstring="Input model in TBmodels HDF5 format."
                )
            )
        )
        return retdict

    def _prepare_for_submission(self, tempfolder, inputdict):
        try:
            model_file = inputdict.pop(self.get_linkname('tb_model'))
        except KeyError:
            raise InputValidationError(
                "No tight-binding model 'tb_model' specified for this calculation."
            )

        calcinfo, codeinfo = super(ModelInputBase,
                                   self)._prepare_for_submission(
                                       tempfolder, inputdict
                                   )
        calcinfo.local_copy_list = [
            (model_file.get_file_abs_path(), 'model.hdf5')
        ]

        return calcinfo, codeinfo
