import re

import ujson as json
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.path_config import DATA_PATH
from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.rules import ensure_group

__plugin_meta__ = PluginMetadata(
    name="查看群欢迎消息",
    description="查看群欢迎消息",
    usage="""
    usage：
        查看群欢迎消息
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        menu_type="其他",
    ).dict(),
)

_matcher = on_alconna(Alconna("群欢迎消息"), rule=ensure_group, priority=5, block=True)


BASE_PATH = DATA_PATH / "welcome_message"


@_matcher.handle()
async def _(
    session: EventSession,
    arparma: Arparma,
):
    path = BASE_PATH / f"{session.platform or session.bot_type}" / f"{session.id2}"
    if session.id3:
        path = (
            BASE_PATH
            / f"{session.platform or session.bot_type}"
            / f"{session.id3}"
            / f"{session.id2}"
        )
    file = path / "text.json"
    if not file.exists():
        await MessageUtils.build_message("未设置群欢迎消息...").finish(reply_to=True)
    message = json.load(open(file, encoding="utf8"))["message"]
    message_split = re.split(r"\[image:\d+\]", message)
    if len(message_split) == 1:
        await MessageUtils.build_message(message_split[0]).finish(reply_to=True)
    idx = 0
    data_list = []
    for msg in message_split[:-1]:
        data_list.append(msg)
        data_list.append(path / f"{idx}.png")
        idx += 1
    data_list.append(message_split[-1])
    await MessageUtils.build_message(data_list).send(reply_to=True)
    logger.info("查看群欢迎消息", arparma.header_result, session=session)
