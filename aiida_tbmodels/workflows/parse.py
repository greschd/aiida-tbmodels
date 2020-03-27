# -*- coding: utf-8 -*-
"""
Defines a restart workchain for the ParseCalculation.
"""

from aiida import orm
from aiida.common import AttributeDict
from aiida.engine import (
    BaseRestartWorkChain, while_, process_handler, ProcessHandlerReport
)

from ..calculations.parse import ParseCalculation


class ParseWorkChain(BaseRestartWorkChain):
    """
    Workchain for the 'tbmodels parse' command that handles basic
    failures. If `pos_kind = 'nearest_atom'` is specified as input
    and fails due to ambiguous positions, the model is instead
    parsed with `pos_kind = 'wannier'`.
    """
    _process_class = ParseCalculation

    @classmethod
    def define(cls, spec):
        super().define(spec)

        spec.expose_inputs(ParseCalculation, namespace='parse')
        spec.expose_outputs(ParseCalculation)

        spec.outline(
            cls.setup,
            while_(cls.should_run_process)(
                cls.run_process,
                cls.inspect_process,
            ), cls.results
        )

    def setup(self):
        super().setup()
        self.ctx.inputs = AttributeDict(
            self.exposed_inputs(ParseCalculation, 'parse')
        )

    @process_handler(
        priority=100,
        exit_codes=ParseCalculation.exit_codes.AMBIGUOUS_NEAREST_ATOM_POSITIONS  # pylint: disable=no-member
    )
    def handle_ambiguous_positions_error(self, node):  # pylint: disable=unused-argument
        """
        If the 'ambiguous nearest position' error occurs, switch to
        `pos_kind = 'wannier'` parsing.
        """
        self.logger.warning(
            "Cannot parse the model with 'nearest_atom' positions, using 'wannier' instead."
        )
        self.ctx.inputs['pos_kind'] = orm.Str('wannier')
        return ProcessHandlerReport(do_break=True)
