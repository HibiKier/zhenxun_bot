from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna
from nonebot_plugin_htmlrender import template_to_pic
from nonebot_plugin_session import EventSession
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import PokeNotifyEvent

from zhenxun.configs.path_config import TEMPLATE_PATH
from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.rules import notice_rule

from .data_source import get_status_info

__plugin_meta__ = PluginMetadata(
    name="服务器自我检查",
    description="查看服务器当前状态",
    usage="""
    查看服务器当前状态
    指令:
        自检
        戳一戳BOT
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier", version="0.1", plugin_type=PluginType.SUPERUSER
    ).dict(),
)


async def handle_self_check():
    try:
        logger.info("触发自检")
        data = await get_status_info()
        image = await template_to_pic(
            template_path=str((TEMPLATE_PATH / "check").absolute()),
            template_name="main.html",
            templates={"data": data},
            pages={
                "viewport": {"width": 195, "height": 750},
                "base_url": f"file://{TEMPLATE_PATH}",
            },
            wait=2,
        )
        await MessageUtils.build_message(image).send()
        logger.info("自检成功")
    except Exception as e:
        await MessageUtils.build_message(f"自检失败: {e}").send()
        logger.error("自检失败", e=e)

#word
_self_check_matcher = on_alconna(
    Alconna("自检"), rule=to_me(), permission=SUPERUSER, block=True, priority=1
)

@_self_check_matcher.handle()
async def _():
    await handle_self_check()

#poke
_self_check_poke_matcher = on_notice(priority=5, block=False, rule=notice_rule(PokeNotifyEvent) & to_me())

@_self_check_poke_matcher.handle()
async def _(event: PokeNotifyEvent):
    await handle_self_check()

