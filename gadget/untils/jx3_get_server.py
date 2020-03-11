# -*- coding: utf-8 -*-
# Author:w k

from .fs import get_data_folder


# 大区 0
# 名字 1
# ip 3
# port 4
# 主服务器 10

def get_server(server, need_ip=None):
    filename = get_data_folder('Jx3', 'serverlist.ini')
    f = open(filename)
    for info in f.readlines():
        if server in info:
            info = info.split('\t')
            if need_ip:
                return info[0], info[10], info[3], info[4]
            return info[0], info[10]
    return None

