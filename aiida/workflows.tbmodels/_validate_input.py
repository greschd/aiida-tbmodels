#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from aiida.common.exceptions import InputValidationError

def validate_input(params, param_types):
    for key, valid_type in param_types:
        if key not in params:
            raise InputValidationError('Missing input key {}'.format(key))
        value = params.pop(key)
        if not isinstance(value, valid_type):
            raise InputValidationError(
                "Input parameter '{key}' is of invalid type '{type}', should be '{valid_type}'.".format(
                    key=key, type=type(value), valid_type=valid_type
                )
            )
    if params:
        raise InputValidationError('Unrecognized input parameters {}'.format(
            list(params.keys())
        ))
