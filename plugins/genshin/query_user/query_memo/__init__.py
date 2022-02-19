from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent
from services.log import logger
from .data_source import get_user_memo, get_memo
from .._models import Genshin
from nonebot.plugin import export


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


export = export()

export.get_memo = get_memo

query_memo_matcher = on_command("原神便签查询", aliases={"原神便笺查询", "yss"}, priority=5, block=True)


@query_memo_matcher.handle()
async def _(event: MessageEvent):
    uid = await Genshin.get_user_uid(event.user_id)
    if not uid or not await Genshin.get_user_cookie(uid, True):
        await query_memo_matcher.finish("请先绑定uid和cookie！")
    if isinstance(event, GroupMessageEvent):
        uname = event.sender.card or event.sender.nickname
    else:
        uname = event.sender.nickname
    data = await get_user_memo(event.user_id, uid, uname)
    if data:
        await query_memo_matcher.send(data)
        logger.info(
            f"(USER {event.user_id}, "
            f"GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) "
            f"使用原神便笺查询 uid：{uid}"
        )
    else:
        await query_memo_matcher.send("未查询到数据...")





