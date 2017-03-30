#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import copy

from aiida.orm.data import Data

class ListData(Data):
    def __init__(self, value=[]):
        self.value = value

    @property
    def value(self):
        self.get_attr('list')

    @value.setter
    def value(self, value):
        self._set_attr('list', list(copy.deepcopy(value)))
