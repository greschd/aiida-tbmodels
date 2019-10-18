#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Tests for the tbmodels.parse calculation.
"""

from __future__ import division, print_function, unicode_literals

import os

import pytest


@pytest.fixture
def get_tbmodels_parse_builder(sample, get_tbmodels_process_builder):
    """
    Fixture which creates a builder for the tbmodels.parse
    calculation.
    """
    from aiida.orm.nodes.data.folder import FolderData

    builder = get_tbmodels_process_builder('tbmodels.parse')

    input_path = sample('bi_wannier_output')
    input_folder = FolderData()
    for filename in os.listdir(input_path):
        input_folder.put_object_from_file(
            os.path.join(input_path, filename), filename
        )
    builder.wannier_folder = input_folder

    return builder


def test_parse(
    configure,  # pylint: disable=unused-argument
    assert_finished,
    get_tbmodels_parse_builder  # pylint: disable=redefined-outer-name
):
    """
    Test the parse calculation when launched with 'run_get_node'.
    """
    from aiida.orm import SinglefileData
    from aiida.engine.launch import run_get_node

    builder = get_tbmodels_parse_builder
    output, calc = run_get_node(builder)

    assert_finished(calc.pk)
    assert isinstance(output['tb_model'], SinglefileData)
    assert calc.get_hash() == calc.get_extra('_aiida_hash')


def test_parse_submit(
    configure_with_daemon,  # pylint: disable=unused-argument
    assert_finished,
    wait_for,
    get_tbmodels_parse_builder  # pylint: disable=redefined-outer-name
):
    """
    Test the parse calculation when submitted to the daemon.
    """
    from aiida.orm import SinglefileData
    from aiida.engine.launch import submit

    builder = get_tbmodels_parse_builder
    calc = submit(builder)
    wait_for(calc.pk)
    assert_finished(calc.pk)

    assert isinstance(calc.outputs.tb_model, SinglefileData)
    assert calc.get_hash() == calc.get_extra('_aiida_hash')
