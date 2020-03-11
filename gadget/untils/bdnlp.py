# -*- coding: utf-8 -*-
# Author:w k

import httpx
import nonebot as rcnb
import json



async def nlp(text):
    api_url = f'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer?access_token={rcnb.get_bot().config.BD_TOKEN}'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    data = {
        'text': text
    }
    data = json.dumps(data).encode('GBK')
    requests = httpx.AsyncClient()
    ret = await requests.post(api_url, headers=headers, data=data)
    ret = ret.json()
    await requests.aclose()
    if ret.get('items',None):
        return ret['items']
    return None

