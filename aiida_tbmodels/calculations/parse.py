# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import os
import json

from aiida.orm.data.folder import FolderData
from aiida.common.utils import classproperty
from aiida.common.exceptions import InputValidationError, ValidationError

from ._base import ModelOutputBase


class ParseCalculation(ModelOutputBase):
    @classproperty
    def _use_methods(cls):
        retdict = super(ParseCalculation, cls)._use_methods
        retdict.update(
            dict(
                wannier_folder=dict(
                    valid_types=FolderData,
                    additional_parameter=None,
                    linkname='wannier_folder',
                    docstring=
                    "Folder containing the Wannier90 output data, with prefix 'wannier90'."
                )
            )
        )
        return retdict

    def _prepare_for_submission(self, tempfolder, inputdict):
        try:
            wannier_folder = inputdict.pop(self.get_linkname('wannier_folder'))
        except KeyError:
            raise InputValidationError(
                'No wannier_folder specified for this calculation'
            )

        # get the prefix from the *_hr.dat file
        for filename in wannier_folder.get_folder_list():
            if filename.endswith('_hr.dat'):
                prefix = filename.rsplit('_hr.dat', 1)[0]
                break
        else:
            raise InputValidationError(
                "'wannier_folder' does not contain a *_hr.dat file."
            )

        calcinfo, codeinfo = super(ParseCalculation,
                                   self)._prepare_for_submission(
                                       tempfolder, inputdict
                                   )

        # add Wannier90 output files to local_copy_list
        wannier_folder_abspath = wannier_folder.get_abs_path()
        calcinfo.local_copy_list = [
            (os.path.join(wannier_folder_abspath, 'path', filename), filename)
            for filename in wannier_folder.get_folder_list()
        ]
        codeinfo.cmdline_params = [
            'parse', '-p', prefix, '-o', self._OUTPUT_FILE_NAME
        ]

        return calcinfo
