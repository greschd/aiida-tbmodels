#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

# from aiida.work.run import submit
from aiida.orm.data.base import Str
from aiida.work.workchain import WorkChain, ToContext
from aiida.orm import Code, Computer, DataFactory, CalculationFactory

class BandEvaluation(WorkChain):
    @classmethod
    def define(cls, spec):
        super(BandEvaluation, cls).define(spec)

        spec.input('tb_model', valid_type=DataFactory('singlefile'))
        spec.input('reference_bands', valid_type=DataFactory('array.bands'))
        spec.input('bandstructure_utils_code', valid_type=Str)
        spec.input('tbmodels_code', valid_type=Str)

        spec.outline(
            cls.calculate_bands, cls.calculate_difference, cls.finalize
        )

    def setup_calc(self, calc_string, code_param):
        process = CalculationFactory(calc_string).process()
        inputs = process.get_inputs_template()
        inputs.code = Code.get_from_string(self.inputs[code_param].value)
        inputs._options.resources = {'num_machines': 1}
        inputs._options.withmpi = False
        return process, inputs

    def calculate_bands(self):
        process, inputs = self.setup_calc('tbmodels.eigenvals', 'tbmodels_code')
        inputs.tb_model = self.inputs.tb_model
        inputs.kpoints = self.inputs.reference_bands
        pid = self.submit(process, inputs).pid
        return ToContext(calculated_bands=pid)

    def calculate_difference(self):
        calc = self.setup_calc('bandstructure_utils.difference', 'bandstructure_utils_code')
        calc.use_bands1(self.inputs.reference_bands)
        ev_calc = self.ctx.calculated_bands
        calc.use_bands2(ev_calc.out.bands)
        calc.store_all()
        pid = self.submit(calc)
        return ToContext(difference=pid)

    def finalize(self):
        self.out("result", self.ctx.difference.res.diff)
