# -*- coding: utf-8 -*-
# Author:w k

from . import game
from gadget.untils.fs import get_data_folder
import nonebot as rcnb
from collections import namedtuple, deque, OrderedDict
from nonebot.typing import Context_T
import configparser
import re
import asyncio
from random import choice

rcnbot = rcnb.get_bot()
# ===题库
title_list = deque()
ans = namedtuple('ans', ['类型', '题目', '答案'])  # 答题类型
all_ans = namedtuple('all_ans', ['类型', '题目'])  # 回复类型
make = namedtuple('make', ['类型', '题目', 'long', 'size', 'text1', 'text2'])  # 文本类型
# ===

# ===随机语句
congratulations = deque(['恭喜', '很高兴', '我宣布', '告诉大家一个好消息'])
pass_ = deque(['的回答被认可！ ', '通过本关！ ', '保持存活！ ', '晋级下一轮！', '的答案校验正确！', '的回答近乎完美！', '的答案简直无可挑剔！'])
lose = deque(['很遗憾', '非常抱歉', 'so~sorry~'])
out = deque(['已出局！', '回答错误！', '无法继续参与！ ', '不能继续陪大家了！'])
finish = deque(['抱歉，所有玩家均已出局。', '战败乃兵家常事！', '稳住，下次能赢！', '很遗憾，全员挑战失败！', '想我泱泱大群，竟无一人解得此题！'])
speed = deque(['SPEED UP！', '加速！加速！', '全员加速中！', '→→→→', '自由选择！前进四！', '》》》》'])
calm = deque(['稳住！', '保持冷静！', '别慌！', '准备好了吗,'])
timeout = deque(['因超时和大家再见了~', '没有赶上列车~', '回答的太慢啦~'])
# ===

# ===群记录
game_status = OrderedDict()
msg_keep = set()

# ===笨方法过滤标点符号
str_replace = ['＂', '＃', '＄', '％', '＆', '＇', '（', '）', '＊', '＋', '，', '－', '／', '：', '；', '＜', '＝', '＞', '＠', '［', '＼',
               '］', '＾', '＿', '｀', '｛', '｜', '｝', '～', '｟', '｠', '｢', '｣', '､', '\u3000', '、', '〃', '〈', '〉', '《', '》',
               '「', '」', '『', '』', '【', '】', '〔', '〕', '〖', '〗', '〘', '〙', '〚', '〛', '〜', '〝', '〞', '〟', '〰', '〾', '〿',
               '–', '—', '‘', '’', '‛', '“', '”', '„', '‟', '…', '‧', '﹏', '﹑', '﹔', '·', '！', '？', '｡', '。', '!', '"',
               '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[',
               '\\', ']', '^', '_', '`', '{', '|', '}', '~']


async def load_title():
    filename = get_data_folder('Game', '题库.ini')
    config = configparser.ConfigParser()
    config.sections()
    config.read(filename, encoding='utf-8')
    for title in config.sections():
        if config[title]['类型'] == '7':

            title_list.append(ans('7', config[title]['题目'], config[title]['答案']))

        elif config[title]['类型'] == '2':

            title_list.append(all_ans('2', config[title]['题目']))

        elif config[title]['类型'] == '3':

            title_list.append(all_ans('3', config[title]['题目']))

        elif config[title]['类型'] == '1':
            title_list.append(all_ans('1', config[title]['题目']))

        elif config[title]['类型'] == '4':
            text1 = ''
            text2 = ''
            if config[title].get('type1'):
                text1 = config[title]['text1']
            if config[title].get('type2'):
                text2 = config[title]['text2']
            title_list.append(
                make('4', config[title]['题目'], config[title]['long'], config[title]['size'], text1, text2))

        elif config[title]['类型'] == '6':
            title_list.append(all_ans('6', config[title]['题目']))

        elif config[title]['类型'] == '7':
            title_list.append(ans('7', config[title]['题目'], config[title]['答案']))


@rcnbot.on_message('group')
async def rcnb_msg(ctx: Context_T):
    group_id = str(ctx['group_id'])
    if group_id not in game_status.keys():
        game_status.setdefault(group_id, OrderedDict())
    if game_status[group_id].get('status') == 2:
        if ctx['user_id'] in game_status[group_id]['alldeath']:
            return
        else:
            game_status[group_id]['allsurvival'].add(ctx['user_id'])
        msg_keep.add(ctx['user_id'])
        if str(ctx['user_id']) not in game_status[group_id]['answercount'].keys():
            game_status[group_id]['answercount'][str(ctx['user_id'])] = 0
        topic_type = game_status[group_id]['题目'].类型
        if topic_type == '1':
            game_status[group_id]['answercount'][str(ctx['user_id'])] += 1
            game_status[group_id]['survival'].append(ctx['user_id'])
        elif topic_type == '2':
            if '[CQ:face' not in ctx['raw_message']:  # 不是
                game_status[group_id]['death'].append(ctx['user_id'])
                return
            else:
                game_status[group_id]['answercount'][str(ctx['user_id'])] += 1
                game_status[group_id]['survival'].append(ctx['user_id'])
                return
        elif topic_type == '3':
            if '[CQ:image' in ctx['raw_message'] or '[CQ:bface' in ctx['raw_message']:  # 不是
                game_status[group_id]['answercount'][str(ctx['user_id'])] += 1
                game_status[group_id]['survival'].append(ctx['user_id'])
                return
            else:
                game_status[group_id]['death'].append(ctx['user_id'])
                return

        elif topic_type == '4':
            flag = 0
            text1 = game_status[group_id]['题目'].text1
            text2 = game_status[group_id]['题目'].text2
            if text1:
                if text1 not in ctx['raw_message']:
                    flag = 1
            if text2:
                if text2 not in ctx['raw_message']:
                    flag = 1
            if text2 and text1:
                if text2 in ctx['raw_message'] and text1 in ctx['raw_message']:
                    flag = 1
            msg = ctx['raw_message']
            for i in str_replace:
                msg = msg.replace(i, '')
            msg_size = len(msg)
            long = int(game_status[group_id]['题目'].long)
            size = int(game_status[group_id]['题目'].size)
            if long == 1:
                if msg_size < size:
                    flag = 1
            if long == 2:
                if msg_size != size:
                    flag = 1
            if long == 3:
                if msg_size > size:
                    flag = 1
            if long == 4:
                if msg_size == size:
                    flag = 1
            if flag != 1:
                game_status[group_id]['answercount'][str(ctx['user_id'])] += 1
                game_status[group_id]['survival'].append(ctx['user_id'])
                return
            game_status[group_id]['death'].append(ctx['user_id'])
            return
        elif topic_type == '6':
            if '[CQ:at' not in ctx['raw_message']:
                game_status[group_id]['death'].append(ctx['user_id'])
                return
            game_status[group_id]['answercount'][str(ctx['user_id'])] += 1
            game_status[group_id]['survival'].append(ctx['user_id'])
            return
        elif topic_type == '7':
            a = game_status[group_id]['题目'].答案
            if ctx['raw_message'] == a:
                game_status[group_id]['answercount'][str(ctx['user_id'])] += 1
                game_status[group_id]['survival'].append(ctx['user_id'])
                return
            game_status[group_id]['death'].append(ctx['user_id'])
            return
    if game_status[group_id].get('status') == 3:
        return
    if game_status[group_id].get('status') == 1:
        return
    if ctx['raw_message'].startswith('5s') and len(title_list) and len(ctx['raw_message']) == 2:
        game_status[group_id]['status'] = 1
        game_status[group_id]['death'] = deque()
        game_status[group_id]['survival'] = deque()
        game_status[group_id]['alldeath'] = set()
        game_status[group_id]['allsurvival'] = set()
        game_status[group_id]['answercount'] = OrderedDict()
        await game_deatil(ctx.copy())

async def game_deatil(ctx):
    count = 1
    group_id = str(ctx['group_id'])
    st = await delay_time(count)
    ctx['message'] = f'还存活的玩家，请在9秒内..'
    await rcnbot.send_group_msg(**ctx)
    game_status[group_id]['status'] = 2
    titile = await get_question(group_id)
    ctx['message'] = titile
    await rcnbot.send_group_msg(**ctx)
    await asyncio.sleep(st)
    ctx = await personnel_handling(ctx)
    msg_keep.clear()
    game_status[group_id]['status'] = 1
    while len(game_status[group_id]['allsurvival']):
        count += 1
        a = st
        st = await delay_time(count)
        if a == st:
            ctx['message'] = ctx['message'] + '\n' + f'{random_msg(8)} 请在{st}秒内。。'

        else:
            ctx['message'] = ctx['message'] + '\n' + f'{random_msg(6)}{random_msg(8)}请在{st}秒内。。'
        await rcnbot.send_group_msg(**ctx)
        titile = await get_question(group_id)
        ctx['message'] = titile
        await rcnbot.send_group_msg(**ctx)
        game_status[group_id]['status'] = 2
        await asyncio.sleep(st)
        ctx = await personnel_handling(ctx)
        msg_keep.clear()
        game_status[group_id]['status'] = 1
    game_status[group_id]['status'] = 3

    u = sorted(game_status[group_id]['answercount'].items(), key=lambda x: x[1], reverse=True)
    msg = '所有玩家都已经出局.榜单:\n'
    for i, info in enumerate(u):
        msg += f'#{i+1} [CQ:at,qq={info[0]}]-分数:{info[1]}\n'
    ctx['message'] = msg.strip()
    await rcnbot.send_group_msg(**ctx)
    game_status[group_id]['status'] = 0


async def delay_time(count):
    if count <= 1:
        return 8
    if count <= 2:
        return 7
    if count <= 3:
        return 6
    if count <= 5:
        return 5
    if count <= 8:
        return 4
    if count <= 12:
        return 3
    if count <= 18:
        return 2
    return 1


async def get_question(group_id):
    # 出题
    title = choice(title_list)
    game_status[group_id]['题目'] = title
    return title.题目


def random_msg(t):
    if t == 1:
        return choice(congratulations)
    if t == 2:
        return choice(pass_)
    if t == 3:
        return choice(lose)
    if t == 4:
        return choice(out)
    if t == 5:
        return choice(finish)
    if t == 6:
        return choice(speed)
    if t == 7:
        return choice(timeout)
    if t == 8:
        return choice(calm)


async def personnel_handling(ctx):
    group_id = str(ctx['group_id'])
    msg = ''
    survival = game_status[group_id]['survival'].copy()
    game_status[group_id]['death'] = list(game_status[group_id]['allsurvival'] - msg_keep)
    death = game_status[group_id]['death'].copy()
    if len(survival):
        for user in survival:
            msg += f'[CQ:at,qq={user}]'
        msg = random_msg(1) + msg + random_msg(2)
        game_status[group_id]['allsurvival'].update(survival)
        game_status[group_id]['survival'].clear()
    if len(death):
        msg = msg.strip() + random_msg(3)
        for user in death:
            msg += f'[CQ:at,qq={user}]'
        msg = msg + random_msg(4)
        game_status[group_id]['alldeath'].update(death)
        game_status[group_id]['death'].clear()
    if not msg:
        ctx['message'] = ' '
    ctx['message'] = msg

    game_status[group_id]['allsurvival'] = game_status[group_id]['allsurvival'] - game_status[group_id]['alldeath']
    if not survival:
        game_status[group_id]['allsurvival'] = set()

    return ctx
