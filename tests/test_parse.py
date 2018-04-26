#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import os

import pytest


@pytest.fixture
def get_tbmodels_parse_builder(sample, get_tbmodels_process_builder):
    from aiida.orm.data.folder import FolderData

    builder = get_tbmodels_process_builder('tbmodels.parse')

    input_path = sample('bi_wannier_output')
    input_folder = FolderData()
    for fn in os.listdir(input_path):
        input_folder.add_path(os.path.join(input_path, fn), fn)
    builder.wannier_folder = input_folder

    return builder


def test_parse(configure, assert_finished, get_tbmodels_parse_builder):
    from aiida.orm.data.singlefile import SinglefileData
    from aiida.work.launch import run_get_node

    builder = get_tbmodels_parse_builder
    output, calc = run_get_node(builder)

    assert_finished(calc.pk)
    assert isinstance(output['tb_model'], SinglefileData)
    assert calc.get_hash() == calc.get_extra('_aiida_hash')


def test_parse_submit(
    configure_with_daemon, assert_finished, wait_for,
    get_tbmodels_parse_builder
):
    from aiida.orm.data.singlefile import SinglefileData
    from aiida.work.launch import submit

    builder = get_tbmodels_parse_builder
    calc = submit(builder)
    wait_for(calc.pk)
    assert_finished(calc.pk)
    output = calc.get_outputs_dict()

    assert isinstance(output['tb_model'], SinglefileData)
    assert calc.get_hash() == calc.get_extra('_aiida_hash')
