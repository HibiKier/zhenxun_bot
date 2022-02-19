from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from services.log import logger
from .data_source import query_role_data
from .._models import Genshin
from utils.utils import is_number
from nonebot.params import CommandArg


__zx_plugin_name__ = "原神玩家查询"
__plugin_usage__ = """
usage：
    通过uid查询原神玩家信息
    指令：
        原神玩家查询/ys ?[uid]
        示例：原神玩家查询 92342233
""".strip()
__plugin_des__ = "请问你们有几个肝？"
__plugin_cmd__ = ["原神玩家查询/ys"]
__plugin_type__ = ("原神相关",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["原神玩家查询"],
}
__plugin_block_limit__ = {}


query_role_info_matcher = on_command("原神玩家查询", aliases={"原神玩家查找", "ys"}, priority=5, block=True)


@query_role_info_matcher.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if msg:
        if not is_number(msg):
            await query_role_info_matcher.finish("查询uid必须为数字！")
        msg = int(msg)
    if not msg:
        uid = await Genshin.get_user_uid(event.user_id)
    else:
        uid = msg
    if not uid:  # or not await Genshin.get_user_cookie(uid):
        await query_role_info_matcher.finish("请先绑定uid和cookie！")
    nickname = event.sender.card or event.sender.nickname
    mys_id = await Genshin.get_user_mys_id(uid)
    data = await query_role_data(event.user_id, uid, mys_id, nickname)
    if data:
        await query_role_info_matcher.send(data)
        logger.info(
            f"(USER {event.user_id}, "
            f"GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 使用原神玩家查询 uid：{uid}"
        )
    else:
        await query_role_info_matcher.send("查询失败..")




