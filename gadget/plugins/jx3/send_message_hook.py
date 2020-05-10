# -*- coding: utf-8 -*-
# Author:w k
import requests
import time
import random
import redis
import json

client = redis.Redis(db=3)
api_url = 'https://jx3.derzh.com/serendipity/'
message_url = 'https://app.qun.qq.com/cgi-bin/api/hookrobot_send?key=ada830e784b81dbba46a4177774d06d1218552c3'

request_params = {
    'm': 1,
    'test': '1',
    'R': '',
    'S': '',
    't': '',
    's': '',
    'n': '',
    'csrf': '',
}

first_run = True
last_time = 0
while True:
    try:
        token = client.randomkey()
    except:
        client = redis.Redis(db=3)
        continue

    if not token:
        time.sleep(0.5)
        continue
    token = token.decode()
    client.delete(token)
    request_params['r'] = token
    response = requests.get(api_url, params=request_params, verify=False)
    ret = ''
    try:
        response.status_code
        ret = response.json()['result']
    except:
        time.sleep(0.5)
        continue
    if ret:
        if first_run:
            last_time = int(ret[0]['time'])
            first_run = False
            time.sleep(5)
            continue
        new_time = int(ret[0]['time'])
        for item in ret:
            if int(item['time']) > last_time:
                # 发送
                # 处理消息内容
                message = {"content": [
                    {
                        "type": 0,
                        "data": f'来自:天鹅坪\n玩家:梦影大佬nb\n奇遇:红衣歌'
                    }
                ]
                }
                a = requests.post(message_url,data=json.dumps(message))
                print('发送',a.text)

        last_time = new_time

    time.sleep(random.randint(7, 10))
