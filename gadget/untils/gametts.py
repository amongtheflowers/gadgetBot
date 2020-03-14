# -*- coding: utf-8 -*-
# Author:w k

import nonebot as rcnb
import httpx
import json
import time
import random
import hmac, hashlib
import binascii
import base64
import nonebot as rcnb

rcnbot = rcnb.get_bot()

api_url = "https://openai.qq.com/api/json/ai/GetMultiAI"



def gen_sign(appid, secret_key):
    if not appid or not secret_key:
        return -1
    expired = 0
    now = int(time.time())
    rdm = random.randint(0, 999999999)
    plain_text = 'a=' + str(appid) + '&e=' + str(expired) + '&t=' + str(now) + '&r=' + str(rdm)
    bin = hmac.new(secret_key.encode(), plain_text.encode(), hashlib.sha1)
    s = bin.hexdigest()
    s = binascii.unhexlify(s)
    s = s + plain_text.encode('ascii')
    signature = base64.b64encode(s).rstrip()
    return signature



async def game_voice_tts(text, mode, speed='normal'):
    '''
    :param text: 转换文本
    :param mode: 发音人
    modes = {
        '妲己': 'Daji',
        '吕布': 'Lvbu',
        '孙尚香': 'Sunshangxiang',
    }
    :param speed: 发音速度
    :return:
    '''
    headers = {
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'Referer': 'https://servicewechat.com/wxfe46e0ba015739e7/9/page-frame.html',
        'Host': 'openai.qq.com',
        'Connection': 'keep-alive'
    }
    modes = {
        '妲己': 'Daji',
        '吕布': 'Lvbu',
        '孙尚香': 'Sunshangxiang',
    }
    appid = rcnbot.config.GAME_APPID
    secret_key = rcnbot.config.GAME_SECRET_KEY
    sign = gen_sign(appid, secret_key).decode()
    data = {
        'base':
            {
                'appid': appid,
                'auth_key': sign,
                'cmds': 'NlpTts'
            },
        'media': text,
        'params':
            {
                'NlpTts': {'mode': modes[mode], 'speed': speed}
            }
    }
    client = httpx.AsyncClient()
    response = await client.post(api_url, headers=headers, data=json.dumps(data))
    await client.aclose()
    if response.status_code == 200:
        ret = response.json()
        if ret['base']['ret'] == 0:
            voice_url = ret['cmd_rsps']['NlpTts']['data']['voice_url']
            return '[CQ:record,file=%s]' % voice_url
    return False
