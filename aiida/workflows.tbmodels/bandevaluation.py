#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from past.builtins import basestring
from aiida.orm import (
    Code, Computer, DataFactory, CalculationFactory, QueryBuilder, Workflow
)
from ._validate_input import validate_input

class BandevaluationWorkflow(Workflow):
    """
    This workflow evaluates the difference between a reference bandstructure and the bandstructure of a given tight-binding model.
    """
    def __init__(self, **kwargs):
        super(BandevaluationWorkflow, self).__init__(**kwargs)

    def validate_input(self):
        """
        Check if all necessary inputs are present
        """
        params = self.get_parameters()

        BandsData = DataFactory('array.bands')
        SinglefileData = DataFactory('singlefile')

        param_types = [
            ('tb_model', ParameterData),
            ('reference_bands', BandsData),
            ('bandstructure_utils_code', basestring),
            ('tbmodels_code', basestring)
        ]
        validate_input(params, param_types)
        self.append_to_report("Starting workflow with parameters: {}".format(self.get_parameters()))

    # @Workflow.step
    # def start(self):
    #     self.validate_input()
    #     self.append_to_report("Running Wannier90 calculation...")
    #     self.attach_calculation(self.run_wswannier())
    #     self.next(self.get_next_step())

    # def setup_tbmodels(self, calc):
    #     code = Code.get_from_string(self.get_parameter('tbmodels_code'))
    #     calc.use_code(code)
    #     calc.set_resources({'num_machines': 1})
    #     calc.set_withmpi(False)
    #     calc.set_computer(code.get_computer())

    # def run_parse(self, wannier_folder):
    #     calc = CalculationFactory('tbmodels.parse')()
    #     self.setup_tbmodels(calc)
    #
    #     calc.use_wannier_folder(wannier_folder)
    #     calc.store_all()
    #     return calc
    #
    # @Workflow.step
    # def parse(self):
    #     wannier_calc = self.get_step_calculations(self.start)[0]
    #     wannier_folder = wannier_calc.out.tb_model
    #     self.append_to_report("Parsing Wannier90 output to tbmodels format...")
    #     self.attach_calculation(self.run_parse(wannier_folder))
    #     self.next(self.get_next_step())
    #
    # def run_slice(self, tbmodel_file):
    #     calc = CalculationFactory('tbmodels.slice')()
    #     self.setup_tbmodels(calc)
    #     calc.use_tb_model(tbmodel_file)
    #     calc.use_slice_idx(self.get_parameter("slice_idx"))
    #     calc.store_all()
    #     return calc
    #
    # @Workflow.step
    # def slice(self):
    #     calc = self.get_step_calculations(self.previous_step)[0]
    #     tbmodel_file = calc.out.tb_model
    #     self.append_to_report("Slicing tight-binding model...")
    #     self.attach_calculation(self.run_slice(tbmodel_file))
    #     self.next(self.get_next_step())
    #
    # def run_symmetrize(self, tbmodel_file):
    #     calc = CalculationFactory('tbmodels.symmetrize')()
    #     self.setup_tbmodels(calc)
    #     calc.use_tb_model(tbmodel_file)
    #     calc.use_symmetries(self.get_parameter("symmetries"))
    #     calc.store_all()
    #     return calc
    #
    # @Workflow.step
    # def symmetrize(self):
    #     calc = self.get_step_calculations(self.previous_step)[0]
    #     tbmodel_file = calc.out.tb_model
    #     self.append_to_report("Symmetrizing tight-binding model...")
    #     self.attach_calculation(self.run_symmetrize(tbmodel_file))
    #     self.next(self.get_next_step())
    #
    # @Workflow.step
    # def finalize(self):
    #     calc = self.get_step_calculations(self.previous_step)[0]
    #     self.add_result('tb_model', calc.out.tb_model)
    #     self.append_to_report('Added final tb_model to results.')
    #     self.next(self.exit)
