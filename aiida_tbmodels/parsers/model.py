# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the parser for tight-binding models in TBmodels HDF5 format.
"""

from aiida.plugins import DataFactory
from aiida.parsers.parser import Parser


class ModelParser(Parser):
    """
    Parse TBmodels output to a SinglefileData containing the model file.
    """
    def parse(self, **kwargs):  # pylint: disable=inconsistent-return-statements
        try:
            out_folder = self.retrieved
        except KeyError as err:
            self.logger.error("No retrieved folder found")
            raise err

        try:
            with out_folder.open(
                self.node.get_option('output_filename'), 'rb'
            ) as output_file:
                model_node = DataFactory('singlefile')(file=output_file)
        except IOError:
            return self.exit_codes.ERROR_OUTPUT_MODEL_FILE

        self.out('tb_model', model_node)
