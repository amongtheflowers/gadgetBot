# -*- coding: utf-8 -*-
# Author:w k


from gadget.untils.fs import get_data_folder
import nonebot as rcnb
from random import choice
import asyncio
from gadget.untils.gametts import game_voice_tts


rcnbot = rcnb.get_bot()

answer_list = []
answer_filter = []

async def load_answer():
    filename = get_data_folder('Game', '答案之书.txt')
    with open(filename, 'r', encoding='gbk') as f:
        answers = f.read().split('\n')
    for i in answers:
        answer_list.append(i.strip())


async def send_answer(bot, ctx, user_id, use_tts=False, mode=False):
    answer = choice(answer_list)
    await asyncio.sleep(6)
    if use_tts:
        reply = await game_voice_tts(answer, mode)
        answer = reply if reply else answer
    if ctx.get('group_id'):
        # 艾特他
        answer = f'[CQ:at,qq={user_id}] ' + answer
    await bot.send(ctx, message=answer)
    answer_filter.remove(user_id)
    return

@rcnb.on_command('get_answer', aliases=['我的答案', '答案', '解答'], only_to_me=False)
async def get_answer(session: rcnb.CommandSession):
    # 设定5秒后回复
    user_id = session.ctx.get('user_id')
    if user_id in answer_filter:
        return
    use_tts = False
    mode = False
    args = session.ctx['raw_message'].split(' ')
    if len(args) > 1:
        use_tts = True
        mode = args[1]

    answer_filter.append(user_id)
    asyncio.create_task(send_answer(session.bot, session.ctx, user_id, use_tts, mode))
    await session.finish('想出你的问题,5秒后为你解答！')


