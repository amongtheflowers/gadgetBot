# -*- coding: utf-8 -*-
# Author:w k

import nonebot as rcnb
from nonebot.typing import Context_T
from nonebot.helpers import context_id
from collections import deque, namedtuple
from datetime import datetime as dt

rcnbot = rcnb.get_bot()
msg_queue_item = namedtuple('msg_queue_item', ['ctx_id', 'time'])
msg_queue = deque()


@rcnbot.on_message('group')
async def group_msg(ctx: Context_T):
    ctx_id = context_id(ctx)

    msg_queue.append(msg_queue_item(ctx_id, ctx['time']))

    now_ts = int(dt.now().timestamp())

    while msg_queue and (now_ts - msg_queue[0].time) >= rcnbot.config.REMOVE_DELAY:
        # 如果数据大于5s则移除
        msg_queue.popleft()
    count = 0
    for item in msg_queue:
        if item.ctx_id != ctx_id:
            continue
        count += 1
    if count > rcnbot.config.MAX_COUNT:
        await rcnbot.set_group_ban(**ctx, duration=60)
