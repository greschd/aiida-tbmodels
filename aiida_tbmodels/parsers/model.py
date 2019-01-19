# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the parser for tight-binding models in TBmodels HDF5 format.
"""

from aiida.orm import DataFactory
from aiida.parsers.parser import Parser


class ModelParser(Parser):
    """
    Parse TBmodels output to a SinglefileData containing the model file.
    """

    def parse_with_retrieved(self, retrieved):
        try:
            out_folder = retrieved[self._calc._get_linkname_retrieved()]
        except KeyError as err:
            self.logger.error("No retrieved folder found")
            raise err

        model_file = out_folder.get_abs_path(self._calc._OUTPUT_FILE_NAME)  # pylint: disable=protected-access
        model_node = DataFactory('singlefile')()
        model_node.add_path(model_file)
        new_nodes_list = [('tb_model', model_node)]

        return True, new_nodes_list
