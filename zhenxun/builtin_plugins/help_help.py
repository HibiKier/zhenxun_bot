import os
import random

from nonebot import on_message
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import Image, UniMessage, UniMsg
from nonebot_plugin_session import EventSession

from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType

__plugin_meta__ = PluginMetadata(
    name="功能名称当命令检测",
    description="功能名称当命令检测",
    usage=f"""被动""".strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.HIDDEN,
    ).dict(),
)


_matcher = on_message(rule=to_me(), priority=996, block=False)


_path = IMAGE_PATH / "_base" / "laugh"


@_matcher.handle()
async def _(matcher: Matcher, message: UniMsg, session: EventSession):
    if text := message.extract_plain_text().strip():
        if plugin := await PluginInfo.get_or_none(
            name=text, load_status=True, plugin_type=PluginType.NORMAL
        ):
            image = None
            if _path.exists():
                if files := os.listdir(_path):
                    image = Image(path=_path / random.choice(files))
            message_list = []
            if image:
                message_list.append(image)
            message_list.append(
                f"桀桀桀，预判到会有 '笨蛋' 把功能名称当命令用，特地前来嘲笑！但还是好心来帮帮你啦！\n请at我发送 '帮助{plugin.name}' 或者 '帮助{plugin.id}' 来获取该功能帮助！"
            )
            logger.info(
                f"检测到功能名称当命令使用，已发送帮助信息", "功能帮助", session=session
            )
            await UniMessage(message_list).send(reply_to=True)
            matcher.stop_propagation()
