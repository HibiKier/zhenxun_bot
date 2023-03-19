from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP

from models.bag_user import BagUser
from services.log import logger
from utils.message_builder import image

from ._data_source import create_bag_image

__zx_plugin_name__ = "商店 - 我的道具"
__plugin_usage__ = """
usage：
    我的道具
    指令：
        我的道具
""".strip()
__plugin_des__ = "商店 - 我的道具"
__plugin_cmd__ = ["我的道具"]
__plugin_type__ = ("商店",)
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
async def _(event: GroupMessageEvent):
    props = await BagUser.get_property(event.user_id, event.group_id)
    if props:
        await my_props.send(image(b64=await create_bag_image(props)))
        logger.info(f"查看我的道具", "我的道具", event.user_id, event.group_id)
    else:
        await my_props.finish("您的背包里没有任何的道具噢~", at_sender=True)
