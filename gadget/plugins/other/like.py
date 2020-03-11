# -*- coding: utf-8 -*-
# Author:w k


# 点赞 需要pro

from . import other
import nonebot as rcnb
from collections import deque

IS_LIKE = deque()


@other.command('send_like', aliases=['点赞', '赞我'])
async def _(session: rcnb.CommandSession):
    session.ctx['times'] = 10
    await session.bot.send_like(**session.ctx)
    msg = f'[CQ:at,qq={session.ctx["user_id"]}]已经给你赞了10次了,记得回赞哦。'
    if session.ctx["user_id"] in IS_LIKE:
        msg = f'[CQ:at,qq={session.ctx["user_id"]}]今天已经赞过你啦！'
    IS_LIKE.append(session.ctx["user_id"])
    await session.finish(msg)
