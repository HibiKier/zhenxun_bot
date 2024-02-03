import shutil
from typing import Dict

import ujson as json
from arclet.alconna import Args, Option
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Alconna,
    AlconnaMatch,
    Arparma,
    Match,
    on_alconna,
    store_true,
)
from nonebot_plugin_alconna.matcher import AlconnaMatcher
from nonebot_plugin_saa import Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.path_config import DATA_PATH
from zhenxun.configs.utils import PluginCdBlock, PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.rules import admin_check, ensure_group

base_config = Config.get("admin_bot_manage")

__plugin_meta__ = PluginMetadata(
    name="自定义群欢迎消息",
    description="自定义群欢迎消息",
    usage="""
    设置欢迎消息 欢迎新人！
    设置欢迎消息 欢迎你 -at
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.ADMIN,
        admin_level=base_config.get("SET_GROUP_WELCOME_MESSAGE_LEVEL", 2),
        configs=[
            RegisterConfig(
                key="SET_GROUP_WELCOME_MESSAGE_LEVEL",
                value=2,
                help="设置群欢迎消息所需要的管理员权限等级",
                default_value=2,
            )
        ],
    ).dict(),
)

_matcher = on_alconna(
    Alconna(
        "设置欢迎消息",
        Args["message", str],
        Option("-at", action=store_true, help_text="是否at新入群用户"),
    ),
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
        old_data: Dict[str, str] = json.load(old_file.open(encoding="utf8"))
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
        pass


@_matcher.handle()
async def _(
    session: EventSession,
    matcher: AlconnaMatcher,
    arparma: Arparma,
    message: str,
):
    file = (
        BASE_PATH
        / f"{session.platform or session.bot_type}"
        / f"{session.id2}"
        / "text.json"
    )
    if session.id3:
        file = (
            BASE_PATH
            / f"{session.platform or session.bot_type}"
            / f"{session.id3}"
            / f"{session.id2}"
            / "text.json"
        )
    if not file.exists():
        file.parent.mkdir(exist_ok=True, parents=True)
    json.dump(
        {"at": arparma.find("at"), "message": message},
        file.open("w"),
        ensure_ascii=False,
        indent=4,
    )
    logger.info(f"设置群欢迎消息成功: {message}", arparma.header_result, session=session)
    await Text(f"设置欢迎消息成功: \n{message}").send()
