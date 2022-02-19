from nonebot import on_message
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from .data_source import cancel_all_notice, save_data, get_data, set_data_value
from services.log import logger
import time


__zx_plugin_name__ = "群聊最后聊天时间记录 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


last_chat = on_message(priority=1, block=False, permission=GROUP)


@last_chat.handle()
async def _(event: GroupMessageEvent):
    time_data = await get_data()
    set_data_value(event.group_id, time.time())
    if event.group_id in time_data["_group"]:
        time_data["_group"].remove(event.group_id)
        set_data_value("_group", time_data["_group"])
    for key in time_data.keys():
        if key not in ["check_time", "_group"]:
            if key not in time_data["_group"]:
                if time.time() - time_data[key] > 60 * 60 * 36:
                    await cancel_all_notice(key)
                    time_data["_group"].append(key)
                    set_data_value("_group", time_data["_group"])
                    logger.info(f"GROUP {event.group_id} 因群内发言时间大于36小时被取消全部通知")
    if time.time() - time_data["check_time"] > 60 * 60 * 1:
        set_data_value("check_time", time.time())
        save_data()
