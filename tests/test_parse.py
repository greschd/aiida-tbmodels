#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Tests for the tbmodels.parse calculation.
"""

import os

import pytest

from aiida import orm
from aiida.engine import run_get_node, submit


@pytest.fixture(params=[None, 'as_input', 'dense', 'sparse'])
def sparsity(request):
    """
    Fixture to define the 'sparsity' input.
    """
    sparsity_val = request.param
    if sparsity_val is None:
        return {}
    return {'sparsity': orm.Str(sparsity_val)}


@pytest.fixture
def get_tbmodels_parse_builder(sample, get_tbmodels_process_builder):
    """
    Fixture which creates a builder for the tbmodels.parse
    calculation.
    """
    def _get_tbmodels_parse_builder(dirname='bi_wannier_output'):
        builder = get_tbmodels_process_builder('tbmodels.parse')

        input_path = sample(dirname)
        input_folder = orm.FolderData()
        for filename in os.listdir(input_path):
            input_folder.put_object_from_file(
                os.path.join(input_path, filename), filename
            )
        builder.wannier_folder = input_folder

        return builder

    return _get_tbmodels_parse_builder


def test_parse(
    configure,  # pylint: disable=unused-argument
    assert_finished,
    get_tbmodels_parse_builder,  # pylint: disable=redefined-outer-name
    check_calc_ok,
    sparsity  # pylint: disable=redefined-outer-name
):
    """
    Test the parse calculation when launched with 'run_get_node'.
    """
    builder = get_tbmodels_parse_builder()
    output, calc = run_get_node(builder, **sparsity)

    assert_finished(calc.pk)
    check_calc_ok(calc)
    assert isinstance(output['tb_model'], orm.SinglefileData)
    assert calc.get_hash() == calc.get_extra('_aiida_hash')


def test_parse_submit(
    configure_with_daemon,  # pylint: disable=unused-argument
    assert_finished,
    wait_for,
    get_tbmodels_parse_builder,  # pylint: disable=redefined-outer-name
    check_calc_ok
):
    """
    Test the parse calculation when submitted to the daemon.
    """
    builder = get_tbmodels_parse_builder()
    calc = submit(builder)
    wait_for(calc.pk)
    assert_finished(calc.pk)
    check_calc_ok(calc)

    assert isinstance(calc.outputs.tb_model, orm.SinglefileData)
    assert calc.get_hash() == calc.get_extra('_aiida_hash')


def test_parse_error(
    configure_with_daemon,  # pylint: disable=unused-argument
    get_tbmodels_parse_builder  # pylint: disable=redefined-outer-name
):
    """
    Test that the error which is raised when the nearest atom parsing
    is ambiguous is correctly parsed.
    """
    builder = get_tbmodels_parse_builder(dirname='silicon')

    builder.pos_kind = orm.Str('nearest_atom')
    _, node = run_get_node(builder)
    assert node.is_finished
    assert node.is_failed
    assert node.exit_status == 401
