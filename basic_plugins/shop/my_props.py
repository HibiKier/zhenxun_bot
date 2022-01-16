from nonebot import on_command
from services.log import logger
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.typing import T_State
from models.bag_user import BagUser
from nonebot.adapters.cqhttp.permission import GROUP


__zx_plugin_name__ = "商店 - 我的道具"
__plugin_usage__ = """
usage：
    我的道具
    指令：
        我的道具
""".strip()
__plugin_des__ = "商店 - 我的道具"
__plugin_cmd__ = ["我的道具"]
__plugin_type__ = ('商店',)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["商店", "我的道具"],
}


my_props = on_command("我的道具", priority=5, block=True, permission=GROUP)


@my_props.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    props = await BagUser.get_property(event.user_id, event.group_id)
    if props:
        rst = ""
        for i, p in enumerate(props.keys()):
            rst += f"{i+1}.{p}\t×{props[p]}\n"
        await my_props.send("\n" + rst[:-1], at_sender=True)
        logger.info(f"USER {event.user_id} GROUP {event.group_id} 查看我的道具")
    else:
        await my_props.finish("您的背包里没有任何的道具噢~", at_sender=True)
