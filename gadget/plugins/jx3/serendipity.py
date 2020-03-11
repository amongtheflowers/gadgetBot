# -*- coding: utf-8 -*-
# Author:w k

import nonebot as rcnb
import httpx
import aioredis
import asyncio
from nonebot.permission import SUPERUSER



api_url = 'https://jx3.derzh.com/serendipity/'
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

last_time = 0
serendipity_list = []
serendipity_status = False
serendipity_send_group = [1078637663]


@rcnb.scheduler.scheduled_job('interval', seconds=8, max_instances=100)
async def get_serendipity(first_run=False):
    global last_time
    global serendipity_status
    redis = await aioredis.create_redis_pool(
        'redis://127.0.0.1', db=3)
    token = await redis.randomkey()
    token = token.decode()
    await redis.delete(token)
    redis.close()
    await redis.wait_closed()
    request_params['r'] = token
    client = httpx.AsyncClient(verify=False)
    response = await client.get(api_url, params=request_params)
    await client.aclose()
    response = response.json()['result']
    if first_run:
        last_time = int(response[0]['time'])
        print(last_time)
        # 修改最后奇遇时间
        return
    if not serendipity_status:
        serendipity_status = True
        asyncio.create_task(send_serendipity_loop())
    new_time = int(response[0]['time'])
    for item in response:
        if int(item['time']) > last_time:
            serendipity_list.append(item)
        else:  # 大于上次时间的都推送
            break
    last_time = new_time  # 更新最后时间






async def send_serendipity_loop():
    bot = rcnb.get_bot()
    print('载入自动发送')
    while True:
        if serendipity_list:
            item = serendipity_list.pop(0)
            msg = '==奇遇播报==\n'
            msg += f'来自:{item["server"]}\n玩家:{item["name"]}\n奇遇:{item["serendipity"]}'
            for g in serendipity_send_group:
                await bot.send_group_msg(group_id=g, message=msg)
        await asyncio.sleep(0.5)  # 0.5s处理一次


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(get_serendipity(True))
