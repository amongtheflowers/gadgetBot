# -*- coding: utf-8 -*-
# Author:w k

import nonebot as rcnb
import asyncio
import httpx

RCNBOT = rcnb.get_bot()


### 百度

# 获取百度语音合成的token
@rcnb.scheduler.scheduled_job('interval', days=10)
async def get_bd_token():
    token_url = 'https://aip.baidubce.com/oauth/2.0/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': RCNBOT.config.BD_CLIENT_ID,
        'client_secret': RCNBOT.config.BD_CLIENT_SECRET,
    }
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    requests = httpx.AsyncClient()
    response = await requests.post(token_url, data=data, headers=headers)
    response = response.json()
    await requests.aclose()
    print(response)
    key = response['access_token']
    if key:
        RCNBOT.config.BD_TOKEN = key
    else:
        await asyncio.sleep(60)
        return await get_bd_token()


### B站
LIVE_OPEN = []
SEND_QUEUE = []


async def get_live_status(room):
    requests = httpx.AsyncClient()
    status = await requests.get(f'http://api.live.bilibili.com/room/v1/Room/room_init?id={room}')
    await requests.aclose()
    status = status.json()
    if status['msg'] == '房间不存在':
        return '房间不存在'
    return status['data']['live_status']


# 延迟发送开播信息
@rcnb.scheduler.scheduled_job('interval', seconds=3)
async def send_message():
    if not len(SEND_QUEUE):
        return
    item = SEND_QUEUE.pop(0)
    msg = f'你订阅的 {item["roomid"]}号房间开播啦~'
    for cid in item['userset']:
        ''.split()
        target_type = cid.split('/')[1]
        target_id = cid.split('/')[2]
        if target_type == 'group':
            await RCNBOT.send_msg(message_type='group', group_id=target_id, message=msg)
        else:
            await RCNBOT.send_msg(message_type='private', user_id=target_id, message=msg)
        await asyncio.sleep(0.1)

# B站直播状态
@rcnb.scheduler.scheduled_job('interval', seconds=RCNBOT.config.CHECK_OPEN_STATUS)
async def live_status_open():
    for item in RCNBOT.config.BILIBILI_SUBSCRIPTION_INFO:
        if item['roomid'] not in LIVE_OPEN:
            status = await get_live_status(item['roomid'])
            if status == 1:
                LIVE_OPEN.append(item['roomid'])
                SEND_QUEUE.append(item)
            await asyncio.sleep(0.2)


#@rcnb.scheduler.scheduled_job('interval', minutes=RCNBOT.config.CHECK_CLOSE_STATUS)
@rcnb.scheduler.scheduled_job('interval', seconds=30)
async def live_status_close():
    for item in RCNBOT.config.BILIBILI_SUBSCRIPTION_INFO:
        if item['roomid'] in LIVE_OPEN:
            status = await get_live_status(item['roomid'])
            if status != 1 and len(LIVE_OPEN) > 0:
                LIVE_OPEN.remove(item['roomid'])
