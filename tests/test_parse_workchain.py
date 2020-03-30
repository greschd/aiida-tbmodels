#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Tests for the tbmodels.parse workchain.
"""

# pylint: disable=no-member

import pytest

from aiida import orm
from aiida.engine import run_get_node

from aiida_tbmodels.workflows.parse import ParseWorkChain


@pytest.mark.parametrize('pos_kind', [None, 'wannier', 'nearest_atom'])
def test_parse(
    configure,  # pylint: disable=unused-argument
    assert_finished,
    pos_kind,
    get_folderdata_from_directory,
):
    """
    Test the parse calculation when launched with 'run_get_node'.
    """
    builder = ParseWorkChain.get_builder()

    builder.calc.wannier_folder = get_folderdata_from_directory(
        dirname='silicon'
    )
    if pos_kind is not None:
        builder.calc.pos_kind = orm.Str(pos_kind)
    builder.calc.code = orm.Code.get(label='tbmodels')
    output, node = run_get_node(builder)

    assert_finished(node.pk)

    assert isinstance(output['tb_model'], orm.SinglefileData)
