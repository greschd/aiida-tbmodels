# -*- coding: utf-8 -*-
"""Defines a calcfunction to compute eigenvalues."""

import tbmodels
import bands_inspect as bi

from aiida import orm
from aiida.engine import calcfunction

from aiida_bands_inspect.convert import to_bands_inspect, from_bands_inspect


@calcfunction
def eigenvals(
    tb_model: orm.SinglefileData, kpoints: orm.KpointsData
) -> orm.BandsData:
    """Calculate the eigenvalues of a model at given k-points.

    Parameters
    ----------
    tb_model :
        The tight-binding model.
    kpoints :
        The k-points at which the eigenvalues should be evaluated.

    Returns
    -------
    orm.BandsData :
        The computed eigenvalues.
    """
    with tb_model.open(mode='rb') as in_f:
        model = tbmodels.io.load(in_f)

    bands = bi.eigenvals.EigenvalsData.from_eigenval_function(
        eigenval_function=model.eigenval,
        kpoints=to_bands_inspect(kpoints),
        listable=True
    )
    return from_bands_inspect(bands)
