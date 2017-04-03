#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from past.builtins import basestring
from aiida.orm import (
    Code, Computer, DataFactory, CalculationFactory, QueryBuilder, Workflow
)
from aiida.common.exceptions import InputValidationError

class TbextractionWorkflow(Workflow):
    """
    This workflow takes a Wannier90 input and a symmetry file as input and returns the symmetrized TBmodels model.
    """
    def __init__(self, **kwargs):
        super(TbextractionWorkflow, self).__init__(**kwargs)

    def validate_input(self):
        """
        Check if all necessary inputs are present
        """
        params = self.get_parameters()
        self.add_attribute('has_slice', 'slice_idx' in params)
        self.add_attribute('has_symmetries', 'symmetries' in params)

        SinglefileData = DataFactory('singlefile')
        ArchiveData = DataFactory('vasp.archive')
        ParameterData = DataFactory('parameter')
        ListData = DataFactory('tbmodels.list')

        param_types = [
            ('wannier_code', basestring),
            ('wannier_data', ArchiveData),
            ('wannier_queue', basestring),
            ('wannier_settings', ParameterData),
            ('tbmodels_code', basestring)
        ]
        extra_steps = ['parse']
        if self.get_attribute('has_slice'):
            param_types += [('slice_idx', ListData)]
            extra_steps += ['slice']
        if self.get_attribute('has_symmetries'):
            param_types += [('symmetries', SinglefileData)]
            extra_steps += ['symmetrize']
        extra_steps += ['finalize']
        self.add_attribute('steps_todo', extra_steps)
        self.add_attribute('steps_done', [])

        for key, valid_type in param_types:
            if key not in params:
                raise InputValidationError('Missing input key {}'.format(key))
            value = params.pop(key)
            if not isinstance(value, valid_type):
                raise InputValidationError(
                    "Input parameter '{key}' is of invalid type '{type}', should be '{valid_type}'.".format(
                        key=key, type=type(value), valid_type=valid_type
                    )
                )
        if params:
            raise InputValidationError('Unrecognized input parameters {}'.format(
                list(params.keys())
            ))
        self.append_to_report("Starting workflow with parameters: {}".format(self.get_parameters()))

    @property
    def previous_step(self):
        return eval('self.' + self.get_attribute('steps_done')[-1])

    def get_next_step(self):
        # This is a bit of a hack -- but it enables chaining the steps without
        # having to write lots of logic to detect which was the previous step
        # For it to work, get_next_step must be used in the self.next call.
        steps_todo = self.get_attribute('steps_todo')
        steps_done = self.get_attribute('steps_done')
        try:
            current_step = self.get_attribute('current_step')
            steps_done += [current_step]
        except ValueError:
            pass

        current_step = steps_todo.pop(0)
        self.add_attribute('current_step', current_step)
        self.add_attribute('steps_todo', steps_todo)
        self.add_attribute('steps_done', steps_done)
        return eval('self.' + current_step)

    def run_wswannier(self):
        input_archive = self.get_parameter('wannier_data')
        calc = CalculationFactory('vasp.wswannier')()
        code = Code.get_from_string(self.get_parameter('wannier_code'))
        calc.use_code(code)
        # No MPI
        calc.set_resources(dict(num_machines=1, tot_num_mpiprocs=1))
        calc.set_computer(code.get_computer())
        calc.set_queue_name(self.get_parameter('wannier_queue'))
        calc.use_data(input_archive)
        # set default for write_tb etc.
        wannier_settings = self.get_parameter('wannier_settings').get_dict()
        wannier_settings.setdefault('write_hr', True)
        # wannier_settings.setdefault('write_xyz', True)
        wannier_settings.setdefault('use_ws_distance', True)
        # TODO: caching!
        calc.use_settings(DataFactory('parameter')(dict=wannier_settings))
        calc.store_all()
        return calc

    @Workflow.step
    def start(self):
        self.validate_input()
        self.append_to_report("Running Wannier90 calculation...")
        self.attach_calculation(self.run_wswannier())
        self.next(self.get_next_step())

    def setup_tbmodels(self, calc):
        code = Code.get_from_string(self.get_parameter('tbmodels_code'))
        calc.use_code(code)
        calc.set_resources({'num_machines': 1})
        calc.set_withmpi(False)
        calc.set_computer(code.get_computer())

    def run_parse(self, wannier_folder):
        calc = CalculationFactory('tbmodels.parse')()
        self.setup_tbmodels(calc)

        calc.use_wannier_folder(wannier_folder)
        calc.store_all()
        return calc

    @Workflow.step
    def parse(self):
        wannier_calc = self.get_step_calculations(self.start)[0]
        wannier_folder = wannier_calc.out.tb_model
        self.append_to_report("Parsing Wannier90 output to tbmodels format...")
        self.attach_calculation(self.run_parse(wannier_folder))
        self.next(self.get_next_step())

    def run_slice(self, tbmodel_file):
        calc = CalculationFactory('tbmodels.slice')()
        self.setup_tbmodels(calc)
        calc.use_tb_model(tbmodel_file)
        calc.use_slice_idx(self.get_parameter("slice_idx"))
        calc.store_all()
        return calc

    @Workflow.step
    def slice(self):
        calc = self.get_step_calculations(self.previous_step)[0]
        tbmodel_file = calc.out.tb_model
        self.append_to_report("Slicing tight-binding model...")
        self.attach_calculation(self.run_slice(tbmodel_file))
        self.next(self.get_next_step())

    def run_symmetrize(self, tbmodel_file):
        calc = CalculationFactory('tbmodels.symmetrize')()
        self.setup_tbmodels(calc)
        calc.use_tb_model(tbmodel_file)
        calc.use_symmetries(self.get_parameter("symmetries"))
        calc.store_all()
        return calc

    @Workflow.step
    def symmetrize(self):
        calc = self.get_step_calculations(self.previous_step)[0]
        tbmodel_file = calc.out.tb_model
        self.append_to_report("Symmetrizing tight-binding model...")
        self.attach_calculation(self.run_symmetrize(tbmodel_file))
        self.next(self.get_next_step())

    @Workflow.step
    def finalize(self):
        calc = self.get_step_calculations(self.previous_step)[0]
        self.add_result('tb_model', calc.out.tb_model)
        self.append_to_report('Added final tb_model to results.')
        self.next(self.exit)
