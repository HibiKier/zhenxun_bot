from PIL import ImageFont, ImageDraw, Image
import textwrap
from configs.path_config import IMAGE_PATH, TTF_PATH
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent
from utils.init_result import image
from services.log import logger
from utils.utils import UserExistLimiter, get_message_text
from utils.img_utils import pic2b64

__plugin_name__ = '鲁迅说'

__plugin_usage__ = '用法：鲁迅说 [消息]'

_ulmt = UserExistLimiter()


luxun = on_command("鲁迅说过", aliases={"鲁迅说"}, priority=5, block=True)


@luxun.handle()
async def handle(bot: Bot, event: MessageEvent, state: T_State):
    if _ulmt.check(event.user_id):
        await luxun.finish('你的鲁迅正在说，等会', at_sender=True)
    args = get_message_text(event.json())
    if args:
        state["content"] = args if args else '烦了，不说了'


@luxun.got("content", prompt="你让鲁迅说点啥?")
async def handle_event(bot: Bot, event: MessageEvent, state: T_State):
    filename = str(event.user_id) + "_.jpg"
    content = state["content"].strip()
    if content.startswith(',') or content.startswith('，'):
        content = content[1:]
    _ulmt.set_True(event.user_id)
    if len(content) > 20:
        _ulmt.set_False(event.user_id)
        await luxun.finish("太长了, 鲁迅说不完!", at_sender=True)
    else:
        if len(content) >= 12:
            content = content[:12] + '\n' + content[12:]
        img = image(b64=process_pic(content, filename))
        logger.info(f"USER {event.user_id} GROUP "
                    f"{event.group_id if event.message_type != 'private' else 'private'} 鲁迅说过 {content}")
        await luxun.send(img)
        _ulmt.set_False(event.user_id)


def process_pic(content, filename) -> str:
    text = content
    para = textwrap.wrap(text, width=15)
    MAX_W, MAX_H = 480, 280
    bk_img = Image.open(IMAGE_PATH + "other/luxun.jpg")
    font_path = TTF_PATH + "/msyh.ttf"
    font = ImageFont.truetype(font_path, 37)
    font2 = ImageFont.truetype(font_path, 30)
    draw = ImageDraw.Draw(bk_img)
    current_h, pad = 300, 10
    for line in para:
        w, h = draw.textsize(line, font=font)
        draw.text(((MAX_W - w) / 2, current_h), line, font=font)
        current_h += h + pad
    draw.text((320, 400), "——鲁迅", font=font2, fill=(255, 255, 255))
    return pic2b64(bk_img)


