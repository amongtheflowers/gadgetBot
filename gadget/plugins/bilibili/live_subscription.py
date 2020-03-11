# -*- coding: utf-8 -*-
# Author:w k


from . import Bilibili
import nonebot as rcnb
from nonebot import permission
from gadget.untils.fs import get_data_folder
import pickle
from gadget.plugins.schedule import get_live_status
from nonebot.helpers import context_id as rcnbid

rcnbot = rcnb.get_bot().config


@Bilibili.command('check_info', aliases=['订阅查询'])
async def check(session: rcnb.CommandSession):
    report = await read_subscription_info(session.ctx['user_id'])
    if report:
        msg = '你订阅的房间有->' + ','.join(report)
        await session.finish(msg)


@Bilibili.command('del_info')
async def del_info(session: rcnb.CommandSession):
    user = session.get_optional('user')
    roomid = session.get_optional('roomid')
    if await del_subscription_info(user=user, roomid=roomid):
        await session.finish(f'取消订阅{roomid}号房间成功')
    else:
        await session.finish(f'你好像没订阅{roomid}号房间哦')


@rcnb.on_natural_language('取消订阅', only_to_me=False)
async def _(session: rcnb.NLPSession):
    if session.msg_text.startswith('取消订阅') and session.msg_text[4:].isdigit():
        return rcnb.IntentCommand(90.0, ('Bilibili', 'del_info'), {
            'user': session.ctx['user_id'],
            'roomid': session.msg_text[4:],
        })


@Bilibili.command('subscription')
async def _(session: rcnb.CommandSession):
    room = session.get_optional('roomid')
    cid = rcnbid(session.ctx)
    if await get_live_status(room) == '房间不存在':
        await session.finish(f'你订阅的房间{room}是不存在的哦！')
        return
    await save_subscription_info(room, cid)
    await session.finish(f'订阅 {room}号房间成功~')


@rcnb.on_natural_language('开播订阅', permission=permission.PRIVATE | permission.GROUP_ADMIN, only_to_me=False)
async def _(session: rcnb.NLPSession):
    target = ''
    if session.msg_text.startswith('开播订阅') and session.msg_text[4:].isdigit():
        if session.ctx['message_type'] == 'group':
            target = session.ctx['group_id']
        else:
            target = session.ctx['user_id']
        return rcnb.IntentCommand(100.0, ('Bilibili', 'subscription'),
                                  {'type': session.ctx['message_type'], 'target': target,
                                   'roomid': session.msg_text[4:],
                                   'user': session.ctx['user_id']})


async def save_subscription_info(roomid, cid):
    filename = get_data_folder('Bilibili', 'subscription.pkl')
    for item in rcnbot.BILIBILI_SUBSCRIPTION_INFO:
        if item['roomid'] == roomid:
            item['userset'].add(cid)
            pickle.dump(rcnbot.BILIBILI_SUBSCRIPTION_INFO, open(filename, 'wb'), pickle.HIGHEST_PROTOCOL)
            return
    rcnbot.BILIBILI_SUBSCRIPTION_INFO.append(
        {'roomid': roomid, 'userset': {cid}})
    pickle.dump(rcnbot.BILIBILI_SUBSCRIPTION_INFO, open(filename, 'wb'), pickle.HIGHEST_PROTOCOL)


async def read_subscription_info(user=None):
    filename = get_data_folder('Bilibili', 'subscription.pkl')
    try:
        all_info = pickle.load(open(filename, 'rb'), encoding='utf-8')
    except:
        # 首次运行读取没数据会报错
        all_info = []
    rcnbot.BILIBILI_SUBSCRIPTION_INFO = all_info
    if user:
        tmp_list = []
        for item in all_info:
            for u in item['userset']:
                if str(user) in u:
                    tmp_list.append(item['roomid'])
        return tmp_list


async def del_subscription_info(roomid, user):
    filename = get_data_folder('Bilibili', 'subscription.pkl')
    for item in rcnbot.BILIBILI_SUBSCRIPTION_INFO:
        for u in item['userset']:
            if str(user) in u and roomid == item['roomid']:
                item['userset'].remove(u)
                pickle.dump(rcnbot.BILIBILI_SUBSCRIPTION_INFO, open(filename, 'wb'), pickle.HIGHEST_PROTOCOL)
                return roomid
    return None
