from nonebot import on_message
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData, RegisterConfig, Task
from zhenxun.models.group_console import GroupConsole
from zhenxun.models.task_info import TaskInfo
from zhenxun.services.log import logger

from .data_source import Parser

__plugin_meta__ = PluginMetadata(
    name="B站转发解析",
    description="B站转发解析",
    usage="""
    usage：
        B站转发解析，解析b站分享信息，支持bv，bilibili链接，b站手机端转发卡片，cv，b23.tv，且30秒内内不解析相同url
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        menu_type="其他",
        configs=[
            RegisterConfig(
                module="_task",
                key="DEFAULT_BILIBILI_PARSE",
                value=True,
                default_value=True,
                help="被动 B站转发解析 进群默认开关状态",
                type=bool,
            )
        ],
        tasks=[Task(module="bilibili_parse", name="b站转发解析")],
    ).dict(),
)


async def _rule(session: EventSession) -> bool:
    task = await TaskInfo.get_or_none(module="bilibili_parse")
    if not task or not task.status:
        logger.debug("b站转发解析被动全局关闭，已跳过...")
        return False
    if gid := session.id3 or session.id2:
        return not await GroupConsole.is_block_task(gid, "bilibili_parse")
    return False


_matcher = on_message(priority=1, block=False, rule=_rule)


@_matcher.handle()
async def _(session: EventSession, message: UniMsg):
    data = message[0]
    if result := await Parser.parse(data, message.extract_plain_text().strip()):
        await result.send()
        logger.info(f"b站转发解析: {result}", "BILIBILI_PARSE", session=session)
