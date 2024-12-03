import os
import random

from nonebot import on_message
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_session import EventSession

from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils
from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.ban_console import BanConsole
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.models.group_console import GroupConsole

__plugin_meta__ = PluginMetadata(
    name="笨蛋检测",
    description="功能名称当命令检测",
    usage="""被动""".strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.DEPENDANT,
        menu_type="其他",
    ).dict(),
)

_matcher = on_message(rule=to_me(), priority=996, block=False)


_path = IMAGE_PATH / "_base" / "laugh"


@_matcher.handle()
async def _(matcher: Matcher, message: UniMsg, session: EventSession):
    gid = session.id3 or session.id2
    if await BanConsole.is_ban(session.id1, gid):
        return
    if gid:
        if await BanConsole.is_ban(None, gid):
            return
        if g := await GroupConsole.get_group(gid):
            if g.level < 0:
                return
    if text := message.extract_plain_text().strip():
        if plugin := await PluginInfo.get_or_none(
            name=text, load_status=True, plugin_type=PluginType.NORMAL
        ):
            image = None
            if _path.exists():
                if files := os.listdir(_path):
                    image = _path / random.choice(files)
            message_list = []
            if image:
                message_list.append(image)
            message_list.append(
                "桀桀桀，预判到会有 '笨蛋' 把功能名称当命令用，特地前来嘲笑！"
                f"但还是好心来帮帮你啦！\n请at我发送 '帮助{plugin.name}' 或者"
                f" '帮助{plugin.id}' 来获取该功能帮助！"
            )
            logger.info(
                "检测到功能名称当命令使用，已发送帮助信息", "功能帮助", session=session
            )
            await MessageUtils.build_message(message_list).send(reply_to=True)
            matcher.stop_propagation()
