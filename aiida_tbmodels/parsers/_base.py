# -*- coding: utf-8 -*-
"""
Defines a base parser class for all aiida-tbmodels parsers.
"""

import re

from aiida.parsers.parser import Parser

__all__ = ('ParserBase', )


class ParserBase(Parser):
    """
    Base class for TBmodels parsers. Checks for errors defined as
    TBmodels ExceptionMarker, and emits the corresponding exit code.

    Note that child classes must manually call super().parse, and
    act upon its return value.
    """
    def parse(self, **kwargs):  # pylint: disable=inconsistent-return-statements
        with self.retrieved.open(
            self.node.get_option('error_filename'), 'r'
        ) as err_file:
            stderr = err_file.read()
        error_matches = re.findall(
            r'Error: \[([a-zA-Z|_][a-zA-Z\d|_]+)\]', stderr
        )
        if error_matches:
            for match in error_matches:
                if match in self.exit_codes:
                    return self.exit_codes[match]
            return self.exit_codes.UNKNOWN_ERROR
