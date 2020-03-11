# -*- coding: utf-8 -*-
# Author:w k

'''
每次程序启动加载需要的数据。
'''
from .schedule import get_bd_token
import asyncio
from .bilibili.live_subscription import read_subscription_info
from .game.fives import load_title

init_loop = asyncio.get_event_loop().run_until_complete

# 获取百度token
init_loop(get_bd_token())

# 加载B站直播订阅房间信息
init_loop(read_subscription_info())

# 加载5S游戏题库
init_loop(load_title())
