#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import abspath, join

import pytest

from aiida_pytest.configure import *
from aiida_pytest.process import *

@pytest.fixture
def sample():
    def inner(name):
        return join(abspath('./samples'), name)
    return inner

@pytest.fixture
def get_tbmodels_process_inputs(get_process_inputs):
    def inner(calculation_string):
        return get_process_inputs(
            calculation_string=calculation_string,
            code_string='tbmodels'
        )
    return inner
