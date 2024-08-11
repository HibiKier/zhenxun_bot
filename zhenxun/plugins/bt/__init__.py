from asyncio.exceptions import TimeoutError

from httpx import ConnectTimeout
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.rules import ensure_private

from .data_source import get_bt_info

__plugin_meta__ = PluginMetadata(
    name="磁力搜索",
    description="bt(磁力搜索)[仅支持私聊，懂的都懂]",
    usage="""
    * 拒绝反冲斗士！ *
    指令:
        bt [关键词] ?[页数]
        示例: bt 钢铁侠
        示例: bt 钢铁侠 3
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        configs=[
            RegisterConfig(
                key="BT_MAX_NUM",
                value=10,
                help="单次BT搜索返回最大消息数量",
                default_value=10,
                type=int,
            ),
        ],
    ).dict(),
)


_matcher = on_alconna(
    Alconna("bt", Args["keyword", str]["page?", int]),
    rule=ensure_private,
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(
    session: EventSession,
    arparma: Arparma,
    keyword: str,
    page: Match[int],
):
    send_flag = False
    try:
        async for title, type_, create_time, file_size, link in get_bt_info(
            keyword, page.result if page.available else 1
        ):
            await MessageUtils.build_message(
                f"标题：{title}\n"
                f"类型：{type_}\n"
                f"创建时间：{create_time}\n"
                f"文件大小：{file_size}\n"
                f"种子：{link}"
            ).send()
            send_flag = True
    except (TimeoutError, ConnectTimeout):
        await MessageUtils.build_message(f"搜索 {keyword} 超时...").finish()
    except Exception as e:
        logger.error(f"bt 错误", arparma.header_result, session=session, e=e)
        await MessageUtils.build_message(f"bt 其他未知错误..").finish()
    if not send_flag:
        await MessageUtils.build_message(f"{keyword} 未搜索到...").send()
    logger.info(
        f"BT搜索 {keyword} 第 {page} 页", arparma.header_result, session=session
    )
