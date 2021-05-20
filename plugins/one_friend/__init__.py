import json
import os
import aiohttp
from util.user_agent import get_user_agent
from io import BytesIO
from random import choice
from PIL import Image, ImageDraw, ImageFont
from nonebot import on_regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from util.utils import get_message_text, get_local_proxy
from util.img_utils import pic2b64
from configs.path_config import TTF_PATH
import re
from nonebot.adapters.cqhttp import MessageSegment

one_friend = on_regex('^我.*?朋友.*?(想问问|说|让我问问|想问|让我问|想知道|让我帮他问问|让我'
                      '帮他问|让我帮忙问|让我帮忙问问|问).*', priority=5, block=True)


async def get_pic(qq):
    url = f'http://q1.qlogo.cn/g?b=qq&nk={qq}&s=100'
    async with aiohttp.ClientSession(headers=get_user_agent()) as session:
        async with session.get(url, proxy=get_local_proxy(), timeout=5) as response:
            return await response.read()


@one_friend.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    arr = []
    member_list = await bot.get_group_member_list(self_id=event.self_id, group_id=event.group_id)
    for member in member_list:
        arr.append(member['user_id'])
    msg = get_message_text(event.json())
    msg = re.search(r'^我.*?朋友.*?'
                    r'(想问问|说|让我问问|想问|让我问|想知道|让我帮他问问|让我帮他问|让我帮忙问|让我帮忙问问|问)(.*)',
                    msg)
    msg = msg.group(2)
    if not msg:
        msg = '都不知道问什么'
    msg = msg.replace('他', '我').replace('她', '我')
    image = Image.open(BytesIO(await get_pic(choice(arr))))
    img_origin = Image.new('RGBA', (100, 100), (255, 255, 255))
    scale = 3
    # 使用新的半径构建alpha层
    r = 100 * scale
    alpha_layer = Image.new('L', (r, r), 0)
    draw = ImageDraw.Draw(alpha_layer)
    draw.ellipse((0, 0, r, r), fill=255)
    # 使用ANTIALIAS采样器缩小图像
    alpha_layer = alpha_layer.resize((100, 100), Image.ANTIALIAS)
    img_origin.paste(image, (0, 0), alpha_layer)

    # 创建Font对象:
    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), TTF_PATH + 'yz.ttf'), 30)
    font2 = ImageFont.truetype(os.path.join(os.path.dirname(__file__), TTF_PATH + 'yz.ttf'), 25)

    # 创建Draw对象:
    image_text = Image.new('RGB', (450, 150), (255, 255, 255))
    draw = ImageDraw.Draw(image_text)
    draw.text((0, 0), '朋友', fill=(0, 0, 0), font=font)
    draw.text((0, 40), msg, fill=(125, 125, 125), font=font2)

    image_back = Image.new('RGB', (700, 150), (255, 255, 255))
    image_back.paste(img_origin, (25, 25))
    image_back.paste(image_text, (150, 40))

    await one_friend.send(MessageSegment.image(pic2b64(image_back)))
