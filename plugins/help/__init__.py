from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, PrivateMessageEvent
from nonebot.typing import T_State
from nonebot.rule import to_me
from configs.path_config import DATA_PATH
from utils.message_builder import image
import os
from .data_source import create_help_img, create_group_help_img, get_plugin_help
from utils.utils import get_message_text


__plugin_name__ = "帮助"


if not os.path.exists(DATA_PATH + "group_help/"):
    os.mkdir(DATA_PATH + "group_help/")
create_help_img()
for file in os.listdir(DATA_PATH + "group_help/"):
    os.remove(DATA_PATH + "group_help/" + file)

_help = on_command("功能", rule=to_me(), aliases={"help", "帮助"}, priority=1, block=True)


@_help.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if not msg:
        if not os.path.exists(DATA_PATH + f"group_help/{event.group_id}.png"):
            create_group_help_img(event.group_id)
        await _help.finish(
            image(abspath=DATA_PATH + f"group_help/{event.group_id}.png")
        )
    else:
        await _help.finish(get_plugin_help(msg))


@_help.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if not msg:
        await _help.finish(image("help.png"))
    else:
        await _help.finish(get_plugin_help(msg))
