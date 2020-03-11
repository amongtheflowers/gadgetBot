# -*- coding: utf-8 -*-
# Author:w k


'''
基于百度语音合成所以需要获取一个toekn(会过期),所以每天请求一次。也可以请求时加上是否token过期

'''
from . import other
import nonebot as rcnb
from gadget.untils.bdtts import tts
import time
import hashlib


@other.command('speak')
async def say(session: rcnb.CommandSession):
    text = session.get_optional('text')
    s_type = session.get_optional('type')
    report = await tts(text, s_type)
    if report:
        await session.finish(f'[CQ:record,file=base64://{report}]')
    return


@rcnb.on_natural_language(['说'], only_to_me=False)
async def _(session: rcnb.NLPSession):
    if session.msg_text.startswith('说'):
        msg_filter = session.msg_text.split(' ')
        if len(msg_filter) > 1 and msg_filter[1] in ['男', '女']:
            speak_type = msg_filter[1]
        else:
            speak_type = None
        return rcnb.IntentCommand(90.0, ('other', 'speak'), {'text': msg_filter[0][1:], 'type': speak_type})

