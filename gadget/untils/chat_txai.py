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

class ChatTX(object):
    target_url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
    app_id = nb.get_bot().config.TX_CHAT_APPID
    app_key = nb.get_bot().config.TX_CHAT_APPKEY
    nonce_str_example = 'fa577ce340859f9fe'
    ct = lambda: time.time()

    @classmethod
    def get_nonce_str(self):
        nonce_str = ''
        len_str = string.digits + string.ascii_letters
        for i in range(len(self.nonce_str_example)):
            nonce_str += len_str[randint(0, len(len_str) - 1)]
        return nonce_str

    @classmethod
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

class Chat(object):
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

