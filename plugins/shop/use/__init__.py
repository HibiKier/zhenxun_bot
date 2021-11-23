from nonebot import on_command
from services.log import logger
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.typing import T_State
from utils.utils import is_number, get_message_text
from models.bag_user import BagUser
from nonebot.adapters.cqhttp.permission import GROUP
from services.db_context import db
from .data_source import effect


__zx_plugin_name__ = "商店 - 使用道具"
__plugin_usage__ = """
usage：
    普通的使用道具
    指令：
        使用道具 [序号或道具名称]
    * 序号以 ”我的道具“ 为准 *
""".strip()
__plugin_des__ = "商店 - 使用道具"
__plugin_cmd__ = ["使用道具 [序号或道具名称]"]
__plugin_type__ = ('商店',)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["商店", "使用道具"],
}

use_props = on_command("使用道具", priority=5, block=True, permission=GROUP)


@use_props.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if msg in ["", "帮助"]:
        await use_props.finish(__plugin_usage__)
    props = await BagUser.get_props(event.user_id, event.group_id)
    if props:
        async with db.transaction():
            pname_list = []
            props = props[:-1].split(",")
            for p in props:
                if p != "":
                    if p not in pname_list:
                        pname_list.append(p)
            if is_number(msg):
                if 0 < int(msg) <= len(pname_list):
                    name = pname_list[int(msg) - 1]
                else:
                    await use_props.finish("仔细看看自己的道具仓库有没有这个道具？", at_sender=True)
            else:
                if msg not in pname_list:
                    await use_props.finish("道具名称错误！", at_sender=True)
                name = msg
            if await BagUser.del_props(
                event.user_id, event.group_id, name
            ) and await effect(event.user_id, event.group_id, name):
                await use_props.send(f"使用道具 {name} 成功！", at_sender=True)
                logger.info(
                    f"USER {event.user_id} GROUP {event.group_id} 使用道具 {name} 成功"
                )
            else:
                await use_props.send(f"使用道具 {name} 失败！", at_sender=True)
                logger.info(
                    f"USER {event.user_id} GROUP {event.group_id} 使用道具 {name} 失败"
                )
    else:
        await use_props.send("您的背包里没有任何的道具噢~", at_sender=True)
