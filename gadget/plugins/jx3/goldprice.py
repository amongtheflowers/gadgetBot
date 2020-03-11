# -*- coding: utf-8 -*-
# Author:w k


from . import jx3
import nonebot as rcnb
from gadget.untils.jx3_get_server import get_server
from gadget.untils.bdnlp import nlp
faces_data = None

@jx3.command('gold')
async def gold(session: rcnb.CommandSession):
    text = session.get_optional('text')
    report = await nlp(text.strip())
    if not report:
        await session.finish(f'产能不足了,等会再试吧!')
    for item in report:
        if item['ne'] == 'TIME' or item['item'] == '金价':
            continue
        if len(item['item']) < 2:
            continue
        server = get_server(item['item'])
        if server:
            await session.send(f'好的呢,正在寻找【{server[0]}】--【{server[1]}】的金价')
            #调用金价函数
            return
    await session.finish('?没有服务器哦')


@rcnb.on_natural_language(['金价'], only_to_me=False)
async def _(session: rcnb.NLPSession):
    text = session.msg_text.strip()
    return rcnb.IntentCommand(100.0, ('jx3', 'gold'), {'text': text})
