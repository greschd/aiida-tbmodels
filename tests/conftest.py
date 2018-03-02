#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from aiida_pytest import *


@pytest.fixture
def get_tbmodels_process_builder(get_process_builder):
    def inner(calculation_string):
        return get_process_builder(
            calculation_string=calculation_string, code_string='tbmodels'
        )

    return inner
