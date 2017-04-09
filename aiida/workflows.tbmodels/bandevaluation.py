#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from past.builtins import basestring
from aiida_tools.validate_input import validate_input, parameter
from aiida.orm import (
    Code, Computer, DataFactory, CalculationFactory, QueryBuilder, Workflow
)

@validate_input
@parameter('tb_model', DataFactory('singlefile'))
@parameter('reference_bands', DataFactory('array.bands'))
@parameter('bandstructure_utils_code', basestring)
@parameter('tbmodels_code', basestring)
class BandevaluationWorkflow(Workflow):
    """
    This workflow evaluates the difference between a reference bandstructure and the bandstructure of a given tight-binding model.
    """
    def __init__(self, **kwargs):
        super(BandevaluationWorkflow, self).__init__(**kwargs)

    def setup_calc(self, calc_string, code_param):
        calc = CalculationFactory(calc_string)()
        code = Code.get_from_string(self.get_parameter(code_param))
        calc.use_code(code)
        calc.set_resources({'num_machines': 1})
        calc.set_withmpi(False)
        calc.set_computer(code.get_computer())
        return calc

    @Workflow.step
    def start(self):
        self.append_to_report("Starting workflow with parameters: {}".format(self.get_parameters()))
        self.next(self.eigenvals)

    @Workflow.step
    def eigenvals(self):
        calc = self.setup_calc('tbmodels.eigenvals', 'tbmodels_code')
        calc.use_tb_model(self.get_parameter('tb_model'))
        calc.use_kpoints(self.get_parameter('reference_bands'))
        calc.store_all()
        self.attach_calculation(calc)
        self.append_to_report("Running TBmodels eigenvals calculation...")
        self.next(self.difference)

    @Workflow.step
    def difference(self):
        calc = self.setup_calc('bandstructure_utils.difference', 'bandstructure_utils_code')
        calc.use_bands1(self.get_parameter('reference_bands'))
        ev_calc = self.get_step_calculations(self.eigenvals)[0]
        calc.use_bands2(ev_calc.out.bands)
        calc.store_all()
        self.attach_calculation(calc)
        self.append_to_report("Running bandstructure_utils difference calculation...")
        self.next(self.finalize)

    @Workflow.step
    def finalize(self):
        calc = self.get_step_calculations(self.difference)[0]
        self.add_result('difference', calc.res.diff)
        self.next(self.exit)
