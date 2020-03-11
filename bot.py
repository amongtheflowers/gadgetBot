# -*- coding: utf-8 -*-
# Author:w k


import nonebot as nb
import config
import os
from nonebot import logger

logger.name = 'rcnb'

if __name__ == '__main__':
    nb.init(config)
    nb.load_plugins(os.path.join(os.path.dirname(__file__), 'gadget\plugins'), 'gadget.plugins')
    # 如果是docker使用要用容器ip
    nb.run(host='127.0.0.1', port=8083)
