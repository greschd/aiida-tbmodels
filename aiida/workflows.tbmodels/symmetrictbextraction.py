#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from aiida.orm import (
    Code, Computer, DataFactory, CalculationFactory, QueryBuilder, Workflow
)
from aiida.common.exceptions import InputValidationError

class SymmetrictbextractionWorkflow(Workflow):
    """
    This workflow takes a Wannier90 input and a symmetry file as input and returns the symmetrized TBmodels model.
    """
    def __init__(self, **kwargs):
        super(SymmetrictbextractionWorkflow, self).__init__(**kwargs)

    # def validate_input(self):
    #     """
    #     Check if all necessary inputs are present
    #     """
    #     params = self.get_parameters()
    #     for key in ['wannier_data', 'wannier_settings', 'symmetries']:
    #         if key not in params:
    #             raise InputValidationError('Missing input key {}'.format(key))

    def run_wswannier(self):
        # self.validate_input()
        input_archive = self.get_parameter('wannier_data')
        calc = CalculationFactory('vasp.wswannier')()
        code = Code.get_from_string(self._wannier_code)
        calc.use_code(self.get_parameter('wannier_code'))
        # No MPI
        calc.set_resources(dict(num_machines=1, tot_num_mpiprocs=1))
        calc.set_computer(code.get_computer())
        calc.set_queue_name(self.get_parameter('wannier_queue'))
        calc.use_data(input_archive)
        # set default for write_tb etc.
        wannier_settings = self.get_parameter('wannier_settings').get_dict()
        wannier_settings.setdefault('write_hr', True)
        wannier_settings.setdefault('write_xyz', True)
        wannier_settings.setdefault('use_ws_distance', True)
        # TODO: caching!
        calc.use_settings(DataFactory('parameter')(dict=wannier_settings))
        calc.store_all()
        return calc

    @Workflow.step
    def start(self):
        ...
