from nonebot import on_command
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters.cqhttp.message import Message
from utils.utils import get_message_text, is_number
from utils.message_builder import image
from services.log import logger
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State
from .data_source import get_image
from models.pixiv import Pixiv
import random


pix = on_command("pix", aliases={"PIX"}, priority=5, block=True)


@pix.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    num = 1
    keyword = get_message_text(event.json())
    if is_number(keyword):
        all_image = await Pixiv.query_images(uid=int(keyword))
    elif keyword.lower().startswith("pid"):
        pid = keyword.replace("pid", "").replace(":", "")
        if not is_number(pid):
            await pix.finish("PID必须是数字...", at_sender=True)
        all_image = await Pixiv.query_images(pid=int(pid))
    else:
        x = keyword.split()
        if len(x) > 1:
            if is_number(x[-1]):
                num = int(x[-1])
                if num > 11:
                    num = random.randint(1, 10)
                    await pix.send(f"太贪心了，就给你发 {num}张 好了")
                x = x[:-1]
                keyword = " ".join(x)
        all_image = await Pixiv.query_images(x)
    if not all_image:
        await pix.finish(f"未在图库中找到与 {keyword} 相关Tag/UID/PID的图片...", at_sender=True)
    for _ in range(num):
        if not all_image:
            await pix.finish("坏了...发完了，没图了...")
        img = random.choice(all_image)
        all_image.remove(img)
        img_url = img.img_url
        pid = img.pid
        title = img.title
        author = img.author
        uid = img.uid
        # tags = img.tags
        await pix.send(
            Message(
                f"title：{title}\n"
                f"author：{author}\n"
                f"PID：{pid}\nUID：{uid}\n"
                f"{image(await get_image(img_url, event.user_id), 'temp')}"
            )
        )
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 查看PIX图库PID: {pid}"
        )
