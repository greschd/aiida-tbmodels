#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from aiida_pytest import *


@pytest.fixture
def get_tbmodels_process_inputs(get_process_inputs):
    def inner(calculation_string):
        return get_process_inputs(
            calculation_string=calculation_string, code_string='tbmodels'
        )

    return inner
