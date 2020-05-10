# -*- coding: utf-8 -*-
# Author:w k
import string
import nonebot as nb
import time
from urllib.parse import urlencode
import httpx
import hashlib
from random import randint
import json
import random

class ChatTX(object):
    target_url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
    app_id = nb.get_bot().config.TX_CHAT_APPID
    app_key = nb.get_bot().config.TX_CHAT_APPKEY
    nonce_str_example = 'fa577ce340859f9fe'
    ct = lambda: time.time()
    def get_nonce_str(self):
        nonce_str = ''
        len_str = string.digits + string.ascii_letters
        for i in range(len(self.nonce_str_example)):
            nonce_str += len_str[randint(0, len(len_str) - 1)]
        return nonce_str
    def sign(self, req_data):
        new_list = sorted(req_data.items())
        encode_list = urlencode(new_list)
        req_data = encode_list + "&" + "app_key" + "=" + self.app_key
        md5 = hashlib.md5()
        md5.update(req_data.encode('utf-8'))
        data = md5.hexdigest()
        return data.upper()
    @classmethod
    async def request(self, text):
        req_data = {
            'app_id': self.app_id,
            'time_stamp': int(self.ct()),
            'nonce_str': self.get_nonce_str(),
            'session': 10000,
            'question': text,
        }
        req_data['sign'] = self.sign(req_data)
        req_data = sorted(req_data.items())
        requests = httpx.AsyncClient()
        result = await requests.get(self.target_url, params=req_data)
        await requests.aclose()
        result = result.json()
        if result['ret'] == 0:
            return result['data']['answer']
        return '唔~~等会在跟你说'

class ChatDTP(object):
    api_url = 'http://api.dtp-cloud.cn/query'

    req_data = {
        'agent_id': '5e5a4e0368150d6a7bc6cc8c',
        'type': '1',
        'session_id': 'group',
    }

    @classmethod
    async def request(self, text):
        self.req_data['query'] = text
        clent = httpx.AsyncClient()
        clent.headers.update({'Content-Type': 'application/json'})
        ret = await clent.post(self.api_url, data=json.dumps(self.req_data))
        await clent.aclose()
        try:
            raw = ret.json()['data']['context']
            if '”哦' in raw:
                raw = raw.split('”哦')[0].split('”')[-1]
            return raw
        except:
            return '郭炜炜nb!！我真帅！'

class ChatNvPu(object):
    api_url = 'http://m.mengbaotao.com/api.php?cmd=chatCallback'


    @classmethod
    async def request(self, text):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.10.0',
            'Content-Length': '',
            'Connection': 'Keep-Alive',
            'Host': 'm.mengbaotao.com'
        }
        data = {
            'msg': text,
            'channelid': '2001',
            'channelidModel': random.choice(['2901', '2753']),
            'openid': '359478010543531',
            'token': 'phone_be17865425b3c928b8546b7d947250bd8bf1acc890efd037d600b9c6066d1cff'
        }
        headers['Content-Length'] = str(len(str(urlencode(data))))
        clent = httpx.AsyncClient()
        clent.headers = headers
        ret = await clent.post(self.api_url, data=data,headers=headers)
        await clent.aclose()
        reply = ret['ret_message']
        return reply

