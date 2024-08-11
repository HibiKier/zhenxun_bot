import time
from typing import Tuple

from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.path_config import TEMP_PATH
from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.withdraw_manage import WithdrawManager

__plugin_meta__ = PluginMetadata(
    name="coser",
    description="三次元也不戳，嘿嘿嘿",
    usage="""
    ?N连cos/coser
    示例: cos
    示例: 5连cos （单次请求张数小于9）
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        configs=[
            RegisterConfig(
                key="WITHDRAW_COS_MESSAGE",
                value=(0, 1),
                help="自动撤回，参1：延迟撤回色图时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
                default_value=(0, 1),
                type=Tuple[int, int],
            ),
        ],
    ).dict(),
)

_matcher = on_alconna(Alconna("get-cos", Args["num", int, 1]), priority=5, block=True)

_matcher.shortcut(
    r"cos",
    command="get-cos",
    arguments=["1"],
    prefix=True,
)

_matcher.shortcut(
    r"(?P<num>\d)(张|个|条|连)cos",
    command="get-cos",
    arguments=["{num}"],
    prefix=True,
)


# 纯cos，较慢:https://picture.yinux.workers.dev
# 比较杂，有福利姬，较快:https://api.jrsgslb.cn/cos/url.php?return=img
url = "https://picture.yinux.workers.dev"


@_matcher.handle()
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    num: int,
):
    withdraw_time = Config.get_config("coser", "WITHDRAW_COS_MESSAGE")
    for _ in range(num):
        path = TEMP_PATH / f"cos_cc{int(time.time())}.jpeg"
        try:
            await AsyncHttpx.download_file(url, path)
            receipt = await MessageUtils.build_message(path).send()
            message_id = receipt.msg_ids[0]["message_id"]
            if message_id and WithdrawManager.check(session, withdraw_time):
                WithdrawManager.append(
                    bot,
                    message_id,
                    withdraw_time[0],
                )
            logger.info(f"发送cos", arparma.header_result, session=session)
        except Exception as e:
            await MessageUtils.build_message("你cos给我看！").send()
            logger.error(
                f"cos错误",
                arparma.header_result,
                session=session,
                e=e,
            )
