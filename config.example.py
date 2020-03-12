# -*- coding: utf-8 -*-
# Author:w k

from nonebot.default_config import *
from os import path

COMMAND_START = {''}
DEBUG = True
SUPERUSERS = {}
NICKNAME = {'!', '花'}

# 数据存储文件
DATA_FOLDER = path.join(path.dirname(__file__), 'data')

# B站订阅的列表
BILIBILI_SUBSCRIPTION_INFO = []

# B站直播订阅时间（防止过快封IP,需要自己看着设置吧 0 0）
CHECK_OPEN_STATUS = 10  # 单位是秒
CHECK_CLOSE_STATUS = 10  # 单位是分钟

###CHAT SETTING
TX_CHAT_APPID = ''
TX_CHAT_APPKEY = ''
###

###BD SPEAK
BD_CLIENT_ID = 'Xkrek8ZsR8Bvupw1UGGhUcmZ'
BD_CLIENT_SECRET = 'xI1PnxwVdKtsY29XaO795ZKuFQd8oj5R'
BD_TOKEN = ''
###


###刷屏禁言
REMOVE_DELAY = 5
MAX_COUNT = 7
