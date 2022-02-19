from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.typing import T_State
import re


__zx_plugin_name__ = "消息撤回 [Admin]"
__plugin_usage__ = """
usage：
    简易的消息撤回机制
    指令：
        [回复]撤回
""".strip()
__plugin_des__ = "消息撤回机制"
__plugin_cmd__ = ["[回复]撤回"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "admin_level": 0,
}


withdraw_msg = on_command("撤回", priority=5, block=True)


@withdraw_msg.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    r = re.search(r"\[CQ:reply,id=(-?\d*)]", event.raw_message)
    if r:
        await bot.delete_msg(message_id=int(r.group(1)))
