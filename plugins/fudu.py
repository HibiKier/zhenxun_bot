from nonebot.adapters.cqhttp.permission import GROUP
from configs.path_config import IMAGE_PATH
from util.img_utils import get_img_hash
import random
from util.init_result import image
from nonebot import on_message
from util.utils import get_message_text, get_message_imgs, get_local_proxy
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
import aiohttp
import aiofiles
from collections import defaultdict
from configs.config import FUDU_PROBABILITY


class Fudu:
    def __init__(self):
        self.mlist = defaultdict(list)

    def append(self, key, content):
        self.mlist[key].append(content)

    def clear(self, key):
        self.mlist[key] = []

    def size(self, key) -> int:
        return len(self.mlist[key])

    def check(self, key, content) -> bool:
        return self.mlist[key][0] == content

    def get(self, key):
        return self.mlist[key][0]


_fudulist = Fudu()


fudu = on_message(permission=GROUP, priority=9)


@fudu.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if event.is_tome() or state["_prefix"]["raw_command"]:
        return
    if get_message_text(event.json()):
        if get_message_text(event.json()).find('@可爱的小真寻') != -1:
            await fudu.finish('复制粘贴的虚空艾特？', at_sender=True)
    imgs = get_message_imgs(event.json())
    msg = get_message_text(event.json())
    if not imgs and not msg:
        return
    if imgs:
        img_hash = await get_fudu_img_hash(imgs[0], event.group_id)
    else:
        img_hash = ''
    add_msg = msg + '|-|' + img_hash
    if _fudulist.size(event.group_id) == 0:
        _fudulist.append(event.group_id, add_msg)
    elif _fudulist.check(event.group_id, add_msg):
        _fudulist.append(event.group_id, add_msg)
    else:
        _fudulist.clear(event.group_id)
        _fudulist.append(event.group_id, add_msg)
    if _fudulist.size(event.group_id) > 2:
        if random.random() < FUDU_PROBABILITY:
            if random.random() < 0.2:
                await fudu.finish("打断施法！")
            if imgs and msg:
                rst = msg + image(f'compare_{event.group_id}_img.jpg', 'temp')
            elif imgs:
                rst = image(f'compare_{event.group_id}_img.jpg', 'temp')
            elif msg:
                rst = msg
            else:
                rst = ''
            if rst:
                await fudu.send(rst)
            _fudulist.clear(event.group_id)


async def get_fudu_img_hash(url, group_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=get_local_proxy(), timeout=5) as response:
            async with aiofiles.open(IMAGE_PATH + f"temp/compare_{group_id}_img.jpg", 'wb') as f:
                await f.write(await response.read())
    img_hash = get_img_hash(IMAGE_PATH + f"temp/compare_{group_id}_img.jpg")
    return str(img_hash)
