# -*- coding: utf-8 -*-
# Author:w k

from . import jx3
import httpx
import nonebot as rcnb


@jx3.command('exam', aliases=('科举',))
async def _(session: rcnb.CommandSession):
    # 使用茗衣题库
    # url  https://jx3.derzh.com/exam/?m=1&q=%E9%9D%92%E5%B2%A9&csrf=
    # methon get
    # params m=1&q=问题&csrf=
    args = session.current_arg_text.strip().split(' ')
    if len(args) != 1:
        await session.finish('科举使用方式:\n科举+空格+问题关键字\n科举 青岩')
        return
    question = args[0]
    requests = httpx.AsyncClient(verify=False)
    result = await requests.get(f'https://jx3.derzh.com/exam/?m=1&q={question}&csrf=')
    await requests.aclose()
    result  = result.json()
    report_msg = ''
    for item in result['result']:
        ques = item['ques'].replace('單選題:', '').replace('单选题：','').replace('單選題：', '').replace('单选题:','').strip()
        ans = item['answ'].strip()
        report_msg += '问题:' + ques + '\n答案:' + ans + '\n'
    await session.finish(report_msg.strip())
    return
