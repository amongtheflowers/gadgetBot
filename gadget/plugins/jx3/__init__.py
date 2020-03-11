# -*- coding: utf-8 -*-
# Author:w k

import nonebot as rcnb

__plugin_name = 'Jx3'

jx3 = rcnb.CommandGroup('jx3', only_to_me=False)
from . import exam
from . import goldprice
