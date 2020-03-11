# -*- coding: utf-8 -*-
# Author:w k


from . import other
from gadget.untils.chat_txai import Chat
import nonebot as rcnb


@other.command('chat')
async def _(session: rcnb.CommandSession):
    msg = session.get_optional('msg')
    report = await Chat.request(msg)
    await session.finish(report)
    return


@rcnb.on_natural_language()
async def _(session: rcnb.NLPSession):
    return rcnb.IntentCommand(60.0, ('other', 'chat'), {'msg': session.msg_text})
