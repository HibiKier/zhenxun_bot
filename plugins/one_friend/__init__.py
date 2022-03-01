from io import BytesIO
from random import choice
from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from utils.utils import get_message_at, get_user_avatar, get_message_text
from utils.message_builder import image
from utils.image_utils import BuildImage
from nonebot.params import RegexGroup
from typing import Tuple, Any

__zx_plugin_name__ = "我有一个朋友"
__plugin_usage__ = """
usage：
    我有一个朋友他...，不知道是不是你
    指令：
        我有一个朋友想问问 [文本] ?[at]: 当at时你的朋友就是艾特对象
""".strip()
__plugin_des__ = "我有一个朋友想问问..."
__plugin_cmd__ = ["我有一个朋友想问问[文本] ?[at]"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["我有一个朋友想问问", "我有一个朋友"],
}

one_friend = on_regex(
    "^我.*?朋友.*?[想问问|说|让我问问|想问|让我问|想知道|让我帮他问问|让我帮他问|让我帮忙问|让我帮忙问问|问](.*)",
    priority=4,
    block=True,
)


@one_friend.handle()
async def _(bot: Bot, event: GroupMessageEvent, reg_group: Tuple[Any, ...] = RegexGroup()):
    qq = get_message_at(event.json())
    if not qq:
        qq = choice(
            [
                x["user_id"]
                for x in await bot.get_group_member_list(
                    group_id=event.group_id
                )
            ]
        )
        user_name = "朋友"
    else:
        qq = qq[0]
        at_user = await bot.get_group_member_info(group_id=event.group_id, user_id=qq)
        user_name = at_user["card"] or at_user["nickname"]
    msg = get_message_text(Message(reg_group[0])).strip()
    if not msg:
        msg = "都不知道问什么"
    msg = msg.replace("他", "我").replace("她", "我").replace("它", "我")
    x = await get_user_avatar(qq)
    if x:
        ava = BuildImage(200, 100, background=BytesIO(x))
    else:
        ava = BuildImage(200, 100, color=(0, 0, 0))
    ava.circle()
    text = BuildImage(400, 30, font_size=30)
    text.text((0, 0), user_name)
    A = BuildImage(700, 150, font_size=25, color="white")
    await A.apaste(ava, (30, 25), True)
    await A.apaste(text, (150, 38))
    await A.atext((150, 85), msg, (125, 125, 125))

    await one_friend.send(image(b64=A.pic2bs4()))
