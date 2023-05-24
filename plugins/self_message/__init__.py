from datetime import datetime

from nonebot import on
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    GroupMessageEvent,
    PrivateMessageEvent,
)
from nonebot.message import handle_event

from configs.config import Config

from ._rule import rule

__zx_plugin_name__ = "自身消息触发 [Hidden]"
__plugin_version__ = 0.1

Config.add_plugin_config(
    "self_message",
    "STATUS",
    False,
    help_="允许真寻自身触发命令，需要在go-cqhttp配置文件中report-self-message修改为true，触发命令时需前缀cmd且受权限影响，例如：cmd签到",
    default_value=False,
    type=bool,
)

message_sent = on(
    type="message_sent",
    priority=999,
    block=False,
    rule=rule(),
)


@message_sent.handle()
async def handle_message_sent(bot: Bot, event: Event):
    msg = str(getattr(event, "message", ""))
    self_id = event.self_id
    user_id = getattr(event, "user_id", -1)
    msg_id = getattr(event, "message_id", -1)
    msg_type = getattr(event, "message_type")
    if (
        str(user_id) not in bot.config.superusers and self_id != user_id
    ) or not msg.lower().startswith("cmd"):
        return
    msg = msg[3:]
    if msg_type == "group":
        new_event = GroupMessageEvent.parse_obj(
            {
                "time": getattr(event, "time", int(datetime.now().timestamp())),
                "self_id": self_id,
                "user_id": user_id,
                "message": msg,
                "raw_message": getattr(event, "raw_message", ""),
                "post_type": "message",
                "sub_type": getattr(event, "sub_type", "normal"),
                "group_id": getattr(event, "group_id", -1),
                "message_type": getattr(event, "message_type", "group"),
                "message_id": msg_id,
                "font": getattr(event, "font", 0),
                "sender": getattr(event, "sender", {"user_id": user_id}),
                "to_me": True,
            }
        )
        # await _check_reply(bot, new_event)
        # _check_at_me(bot, new_event)
        # _check_nickname(bot, new_event)
        await handle_event(bot=bot, event=new_event)
    elif msg_type == "private":
        target_id = getattr(event, "target_id")
        if target_id == user_id:
            new_event = PrivateMessageEvent.parse_obj(
                {
                    "time": getattr(event, "time", int(datetime.now().timestamp())),
                    "self_id": self_id,
                    "user_id": user_id,
                    "message": getattr(event, "message", ""),
                    "raw_message": getattr(event, "raw_message", ""),
                    "post_type": "message",
                    "sub_type": getattr(event, "sub_type"),
                    "message_type": msg_type,
                    "message_id": msg_id,
                    "font": getattr(event, "font", 0),
                    "sender": getattr(event, "sender"),
                    "to_me": True,
                    "target_id": target_id,
                }
            )
            await handle_event(bot=bot, event=new_event)
