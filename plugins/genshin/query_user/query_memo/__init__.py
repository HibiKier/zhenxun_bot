from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent

from services.log import logger

from .._models import Genshin
from .data_source import get_memo, get_user_memo

__zx_plugin_name__ = "原神便笺查询"
__plugin_usage__ = """
usage：
    通过指定cookie和uid查询事实数据
    指令：
        原神便笺查询/yss
        示例：原神便笺查询 92342233
""".strip()
__plugin_des__ = "不能浪费丝毫体力"
__plugin_cmd__ = ["原神便笺查询/yss"]
__plugin_type__ = ("原神相关",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["原神便笺查询"],
}
__plugin_block_limit__ = {}


query_memo_matcher = on_command(
    "原神便签查询", aliases={"原神便笺查询", "yss"}, priority=5, block=True
)


@query_memo_matcher.handle()
async def _(event: MessageEvent):
    user = await Genshin.get_or_none(user_qq=event.user_id)
    if not user or not user.uid or not user.cookie:
        await query_memo_matcher.finish("请先绑定uid和cookie！")
    if isinstance(event, GroupMessageEvent):
        uname = event.sender.card or event.sender.nickname
    else:
        uname = event.sender.nickname
    data = await get_user_memo(event.user_id, user.uid, uname)
    if data:
        await query_memo_matcher.send(data)
        logger.info(
            f"(USER {event.user_id}, "
            f"GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) "
            f"使用原神便笺查询 uid：{user.uid}"
        )
    else:
        await query_memo_matcher.send("未查询到数据...")
