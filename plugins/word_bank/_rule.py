import re
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Event
from utils.utils import get_message_img_file
from .model import WordBank


async def check(event: Event) -> bool:
    if isinstance(event, GroupMessageEvent):
        msg = event.raw_message
        list_img = get_message_img_file(event.json())
        if list_img:
            for img_file in list_img:
                strinfo = re.compile(f"{img_file},.*?]")
                msg = strinfo.sub(f'{img_file}]', msg)
        strinfo_face = re.compile(f",type=sticker]")
        msg = strinfo_face.sub(f']', msg)
        return bool(await WordBank.check(event.group_id, msg,))
    return False
