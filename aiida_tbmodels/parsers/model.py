# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the parser for tight-binding models in TBmodels HDF5 format.
"""

from aiida.plugins import DataFactory

from ._base import ParserBase

__all__ = ('ModelParser', )


class ModelParser(ParserBase):
    """
    Parse TBmodels output to a SinglefileData containing the model file.
    """
    def parse(self, **kwargs):  # pylint: disable=inconsistent-return-statements
        exit_code = super().parse(**kwargs)
        if exit_code is not None and exit_code.status != 0:
            return exit_code

        try:
            out_folder = self.retrieved
        except KeyError as err:
            self.logger.error("No retrieved folder found")
            raise err

        try:
            with out_folder.open(
                self.node.get_option('result_filename'), 'rb'
            ) as result_file:
                model_node = DataFactory('singlefile')(file=result_file)
        except IOError:
            return self.exit_codes.ERROR_RESULT_FILE

        self.out('tb_model', model_node)
