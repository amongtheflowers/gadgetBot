# -*- coding: utf-8 -*-
# Author:w k


import nonebot as rcnb

__plugin_name = 'Game'


game = rcnb.CommandGroup('game', only_to_me=False)

from . import fives
from . import answer