# -*- coding: utf-8 -*-
# Author:w k


from . import Bilibili
import httpx
import nonebot as rcnb
import re


@Bilibili.command('get_cover', aliases=['封面'])
async def crawl(session: rcnb.CommandSession):
    target_av = session.current_arg_text
    if target_av.startswith('av'):
        if target_av[2:].isdigit():
            ret = await get_pic(av=target_av)
            await session.finish(ret)
    await session.finish('格式:封面 av号\n例子:封面 av123456')

async def get_pic(av) -> str:
    TARGET_URL = 'http://www.bilibili.com/video/' + av
    requests = httpx.AsyncClient()
    html = await requests.get(TARGET_URL, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    })
    html = html.text
    await requests.aclose()
    if html.find('视频去哪了呢') != -1:
        # print(html)
        return '视频已经被删除了哟~'
    img_url = re.findall(r'//i[0-9].hdslb.com/bfs/archive/[0-9a-zA-Z\.]+', html)
    if not img_url:
        return '没找到封面哦~'
    pic_url = 'http:' + img_url[0]
    return f'[CQ:image,file={pic_url}]'
