import shutil
from pathlib import Path
from typing import Annotated

import ujson as json
from nonebot import on_command
from nonebot.params import Command
from nonebot.plugin import PluginMetadata
from nonebot_plugin_session import EventSession
from nonebot_plugin_alconna import Text, Image, UniMsg

from zhenxun.services.log import logger
from zhenxun.configs.config import Config
from zhenxun.utils.enum import PluginType
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.configs.path_config import DATA_PATH
from zhenxun.utils.rules import admin_check, ensure_group
from zhenxun.configs.utils import RegisterConfig, PluginExtraData

base_config = Config.get("admin_bot_manage")

__plugin_meta__ = PluginMetadata(
    name="自定义群欢迎消息",
    description="自定义群欢迎消息",
    usage="""
    设置群欢迎消息，当消息中包含 -at 时会at入群用户
    设置欢迎消息 欢迎新人！[图片]
    设置欢迎消息 欢迎你 -at
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.ADMIN,
        admin_level=base_config.get("SET_GROUP_WELCOME_MESSAGE_LEVEL", 2),
        configs=[
            RegisterConfig(
                module="admin_bot_manage",
                key="SET_GROUP_WELCOME_MESSAGE_LEVEL",
                value=2,
                help="设置群欢迎消息所需要的管理员权限等级",
                default_value=2,
            )
        ],
    ).dict(),
)

_matcher = on_command(
    "设置欢迎消息",
    rule=admin_check("admin_bot_manage", "SET_GROUP_WELCOME_MESSAGE_LEVEL")
    & ensure_group,
    priority=5,
    block=True,
)


BASE_PATH = DATA_PATH / "welcome_message"
BASE_PATH.mkdir(parents=True, exist_ok=True)

# 旧数据迁移
old_file = DATA_PATH / "custom_welcome_msg" / "custom_welcome_msg.json"
if old_file.exists():
    try:
        old_data: dict[str, str] = json.load(old_file.open(encoding="utf8"))
        for group_id, message in old_data.items():
            file = BASE_PATH / "qq" / f"{group_id}" / "text.json"
            file.parent.mkdir(parents=True, exist_ok=True)
            json.dump(
                {"at": "[at]" in message, "message": message.replace("[at]", "")},
                file.open("w", encoding="utf8"),
                ensure_ascii=False,
                indent=4,
            )
            logger.debug("群欢迎消息数据迁移", group_id=group_id)
        shutil.rmtree(old_file.parent.absolute())
    except Exception as e:
        logger.error("群欢迎消息数据迁移失败...", e=e)


def get_path(session: EventSession) -> Path:
    """根据Session获取存储路径

    参数:
        session: EventSession:

    返回:
        Path: 存储路径
    """
    path = BASE_PATH / f"{session.platform or session.bot_type}" / f"{session.id2}"
    if session.id3:
        path = (
            BASE_PATH
            / f"{session.platform or session.bot_type}"
            / f"{session.id3}"
            / f"{session.id2}"
        )
    path.mkdir(parents=True, exist_ok=True)
    for f in path.iterdir():
        f.unlink()
    return path


async def save(path: Path, message: UniMsg) -> str:
    """保存群欢迎消息

    参数:
        path: 存储路径
        message: 消息内容

    返回:
        str: 消息内容文本格式
    """
    idx = 0
    text = ""
    file = path / "text.json"
    for msg in message:
        if isinstance(msg, Text):
            text += msg.text
        elif isinstance(msg, Image):
            if msg.url:
                text += f"[image:{idx}]"
                if await AsyncHttpx.download_file(msg.url, path / f"{idx}.png"):
                    idx += 1
            else:
                logger.warning("图片 URL 为空...", "设置欢迎消息")
    json.dump(
        {"at": "-at" in text, "message": text.replace("-at", "", 1)},
        file.open("w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )
    return text


@_matcher.handle()
async def _(
    session: EventSession,
    message: UniMsg,
    command: Annotated[tuple[str, ...], Command()],
):
    path = get_path(session)
    message[0].text = message[0].text.replace(command[0], "").strip()
    text = await save(path, message)
    uni_msg = Text("设置欢迎消息成功: \n") + message
    await uni_msg.send()
    logger.info(f"设置群欢迎消息成功: {text}", command[0], session=session)
