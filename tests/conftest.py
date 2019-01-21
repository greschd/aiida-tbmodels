#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Test setup for aiida-tbmodels tests.
"""

import pytest

from aiida_pytest import *  # pylint: disable=unused-wildcard-import,redefined-builtin


@pytest.fixture
def get_tbmodels_process_builder(get_process_builder):  # pylint: disable=redefined-outer-name
    """
    Fixture that creates a Builder for tbmodels calculations.
    """

    def inner(calculation_string):
        return get_process_builder(
            calculation_string=calculation_string, code_string='tbmodels'
        )

    return inner
