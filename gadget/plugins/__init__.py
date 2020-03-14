# -*- coding: utf-8 -*-
# Author:w k

'''
每次程序启动加载需要的数据。
'''
from .schedule import get_bd_token
import asyncio
from .bilibili.live_subscription import read_subscription_info
from .game.fives import load_title
from .game.answer import load_answer
# from .jx3.serendipity import get_serendipity

init_loop = asyncio.get_event_loop().run_until_complete

# 获取百度token
init_loop(get_bd_token())

# 加载B站直播订阅房间信息
init_loop(read_subscription_info())

# 加载5S游戏题库
init_loop(load_title())


#加载答案之书题库
init_loop(load_answer())

# 初始化奇遇获取和发送
# init_loop(get_serendipity(True))


