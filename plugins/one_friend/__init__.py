
import aiohttp
from util.user_agent import get_user_agent
from io import BytesIO
from random import choice
from nonebot import on_regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from util.utils import get_message_text, get_local_proxy, get_message_at
from util.init_result import image
import re
from util.img_utils import CreateImg

__plugin_name__ = '我有一个朋友'

__plugin_usage__ = '用法：我有一个朋友说/问 [消息] [at](不艾特则群员随机)'

one_friend = on_regex('^我.*?朋友.*?(想问问|说|让我问问|想问|让我问|想知道|让我帮他问问|让我'
                      '帮他问|让我帮忙问|让我帮忙问问|问).*', priority=5, block=True)


async def get_pic(qq):
    url = f'http://q1.qlogo.cn/g?b=qq&nk={qq}&s=100'
    async with aiohttp.ClientSession(headers=get_user_agent()) as session:
        async with session.get(url, proxy=get_local_proxy(), timeout=5) as response:
            return await response.read()


@one_friend.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = get_message_text(event.json())
    qq = get_message_at(event.json())
    if not qq:
        qq = choice([x['user_id'] for x in
                     await bot.get_group_member_list(self_id=event.self_id, group_id=event.group_id)])
    else:
        qq = qq[0]
    msg = re.search(r'^我.*?朋友.*?'
                    r'(想问问|说|让我问问|想问|让我问|想知道|让我帮他问问|让我帮他问|让我帮忙问|让我帮忙问问|问)(.*)',
                    msg)
    msg = msg.group(2)
    if not msg:
        msg = '都不知道问什么'
    msg = msg.replace('他', '我').replace('她', '我').replace('它', '我')
    ava = CreateImg(100, 100, background=BytesIO(await get_pic(qq)))
    ava.circle()
    text = CreateImg(60, 30, font_size=30)
    text.text((0, 0), '朋友')
    # text.show()
    A = CreateImg(700, 150, font_size=25, color='white')
    A.paste(ava, (30, 25), True)
    A.paste(text, (150, 40))
    A.text((150, 85), msg, (125, 125, 125))

    await one_friend.send(image(b64=A.pic2bs4()))
