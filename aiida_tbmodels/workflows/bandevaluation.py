#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from past.builtins import basestring
# from aiida_tools.validate_input import validate_input, parameter
# from aiida.orm import (
#     Code, Computer, DataFactory, CalculationFactory, Workflow
# )
from aiida.work.workchain import WorkChain

class BandEvaluation(WorkChain):
    @classmethod
    def define(cls, spec):
