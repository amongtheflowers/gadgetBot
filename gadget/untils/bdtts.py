# -*- coding: utf-8 -*-
# Author:w k


import nonebot as rcnb
import httpx
from urllib.parse import quote_plus
import random
from base64 import b64encode


async def tts(text: str, s_type=None):
    target_url = 'http://tsn.baidu.com/text2audio'
    data = {
        'tex': quote_plus(text),
        'tok': rcnb.get_bot().config.BD_TOKEN,
        'cuid': 'JX3BOTVOICE',
        'ctp': 1,
        'spd': 4,
        'lan': 'zh',
    }
    if s_type:
        if s_type == '男':
            data['per'] = 3
        else:
            data['per'] = 4
    else:
        data['per'] = random.choice([3, 4])
    # 可调节音调语素音量等等。。以后更新
    requests = httpx.AsyncClient()
    response = await requests.post(target_url, data=data)
    await requests.aclose()
    try:
        mp3 = b64encode(response.content)
        return str(mp3, encoding='utf-8')
    except:
        return None


