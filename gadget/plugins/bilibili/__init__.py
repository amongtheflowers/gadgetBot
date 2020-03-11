# -*- coding: utf-8 -*-
# Author:w k


import nonebot as rcnb

__plugin_name = 'Bilibili'

Bilibili = rcnb.CommandGroup('Bilibili', only_to_me=False)

from . import get_cover
from . import live_subscription
