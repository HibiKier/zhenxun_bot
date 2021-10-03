from nonebot import on_keyword
from utils.message_builder import record
from configs.path_config import VOICE_PATH
import random
from services.log import logger
from utils.utils import FreqLimiter
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.rule import to_me
import os

__zx_plugin_name__ = "骂我"
__plugin_usage__ = """
usage：
    多骂我一点，球球了
    指令：
        骂老子
""".strip()
__plugin_des__ = "请狠狠的骂我一次！"
__plugin_cmd__ = ["骂老子/骂我"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["骂老子", "骂我"],
}

_flmt = FreqLimiter(3)


dg_voice = on_keyword({"骂"}, rule=to_me(), priority=5, block=True)


@dg_voice.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if len(str((event.get_message()))) == 1:
        return
    if not _flmt.check(event.user_id):
        await dg_voice.finish("就...就算求我骂你也得慢慢来...", at_sender=True)
    _flmt.start_cd(event.user_id)
    voice = random.choice(os.listdir(VOICE_PATH + "dinggong/"))
    result = record(voice, "dinggong")
    await dg_voice.send(result)
    await dg_voice.send(voice.split("_")[1])
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送钉宫骂人:"
        + result
    )
