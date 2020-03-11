# -*- coding: utf-8 -*-
# Author:w k

import nonebot as rcnb
import os


def get_data_folder(sub_folder: str = '', filename=None) -> str:
    data_folder = rcnb.get_bot().config.DATA_FOLDER
    if sub_folder:
        data_folder = os.path.join(data_folder, sub_folder)
    os.makedirs(data_folder, mode=0o755, exist_ok=True)
    if filename:
        data_folder = os.path.join(data_folder, filename)
        open(data_folder, 'a').close()
    return data_folder
