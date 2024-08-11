import os
import random

from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import Alconna, Arparma, UniMessage, Voice, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.path_config import RECORD_PATH
from zhenxun.configs.utils import PluginCdBlock, PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

__plugin_meta__ = PluginMetadata(
    name="钉宫骂我",
    description="请狠狠的骂我一次！",
    usage="""
    多骂我一点，球球了
    指令：
        骂老子
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        limits=[PluginCdBlock(cd=3, result="就...就算求我骂你也得慢慢来...")],
    ).dict(),
)

_matcher = on_alconna(Alconna("ma-wo"), rule=to_me(), priority=5, block=True)

_matcher.shortcut(
    r".*?骂.*?我.*?",
    command="ma-wo",
    arguments=[],
    prefix=True,
)

path = RECORD_PATH / "dinggong"


@_matcher.handle()
async def _(session: EventSession, arparma: Arparma):
    if not path.exists():
        await MessageUtils.build_message("钉宫语音文件夹不存在...").finish()
    files = os.listdir(path)
    if not files:
        await MessageUtils.build_message("钉宫语音文件夹为空...").finish()
    voice = random.choice(files)
    await UniMessage([Voice(path=path / voice)]).send()
    await MessageUtils.build_message(voice.split("_")[1]).send()
    logger.info(f"发送钉宫骂人: {voice}", arparma.header_result, session=session)
