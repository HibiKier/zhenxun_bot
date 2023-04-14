import asyncio
import re
import time
from datetime import datetime

from nonebot import on_message, on_request
from nonebot.adapters.onebot.v11 import (
    ActionFailed,
    Bot,
    FriendRequestEvent,
    GroupRequestEvent,
    MessageEvent,
)

from configs.config import NICKNAME, Config
from models.friend_user import FriendUser
from models.group_info import GroupInfo
from services.log import logger
from utils.manager import requests_manager
from utils.utils import scheduler

from .utils import time_manager

__zx_plugin_name__ = "好友群聊处理请求 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_configs__ = {
    "AUTO_ADD_FRIEND": {
        "value": False,
        "help": "是否自动同意好友添加",
        "default_value": False,
        "type": bool,
    }
}

friend_req = on_request(priority=5, block=True)
group_req = on_request(priority=5, block=True)
x = on_message(priority=999, block=False, rule=lambda: False)


@friend_req.handle()
async def _(bot: Bot, event: FriendRequestEvent):
    if time_manager.add_user_request(event.user_id):
        logger.debug(f"收录好友请求...", "好友请求", target=event.user_id)
        user = await bot.get_stranger_info(user_id=event.user_id)
        nickname = user["nickname"]
        sex = user["sex"]
        age = str(user["age"])
        comment = event.comment
        await bot.send_private_msg(
            user_id=int(list(bot.config.superusers)[0]),
            message=f"*****一份好友申请*****\n"
            f"昵称：{nickname}({event.user_id})\n"
            f"自动同意：{'√' if Config.get_config('invite_manager', 'AUTO_ADD_FRIEND') else '×'}\n"
            f"日期：{str(datetime.now()).split('.')[0]}\n"
            f"备注：{event.comment}",
        )
        if Config.get_config("invite_manager", "AUTO_ADD_FRIEND"):
            logger.debug(f"已开启好友请求自动同意，成功通过该请求", "好友请求", target=event.user_id)
            await bot.set_friend_add_request(flag=event.flag, approve=True)
            await FriendUser.create(user_id=str(user["user_id"]), user_name=user["nickname"])
        else:
            requests_manager.add_request(
                event.user_id,
                "private",
                event.flag,
                nickname=nickname,
                sex=sex,
                age=age,
                comment=comment,
            )
    else:
        logger.debug(f"好友请求五分钟内重复, 已忽略", "好友请求", target=event.user_id)


@group_req.handle()
async def _(bot: Bot, event: GroupRequestEvent):
    # 邀请
    if event.sub_type == "invite":
        if str(event.user_id) in bot.config.superusers:
            try:
                logger.debug(
                    f"超级用户自动同意加入群聊", "群聊请求", event.user_id, target=event.group_id
                )
                await bot.set_group_add_request(
                    flag=event.flag, sub_type="invite", approve=True
                )
                group_info = await bot.get_group_info(group_id=event.group_id)
                await GroupInfo.update_or_create(
                    group_id=str(group_info["group_id"]),
                    defaults={
                        "group_name": group_info["group_name"],
                        "max_member_count": group_info["max_member_count"],
                        "member_count": group_info["member_count"],
                        "group_flag": 1,
                    },
                )
            except ActionFailed as e:
                logger.error(
                    "超级用户自动同意加入群聊发生错误",
                    "群聊请求",
                    event.user_id,
                    target=event.group_id,
                    e=e,
                )
        else:
            if time_manager.add_group_request(event.user_id, event.group_id):
                logger.debug(
                    f"收录 用户[{event.user_id}] 群聊[{event.group_id}] 群聊请求", "群聊请求"
                )
                user = await bot.get_stranger_info(user_id=event.user_id)
                sex = user["sex"]
                age = str(user["age"])
                nickname = await FriendUser.get_user_name(event.user_id)
                await bot.send_private_msg(
                    user_id=int(list(bot.config.superusers)[0]),
                    message=f"*****一份入群申请*****\n"
                    f"申请人：{nickname}({event.user_id})\n"
                    f"群聊：{event.group_id}\n"
                    f"邀请日期：{datetime.now().replace(microsecond=0)}",
                )
                await bot.send_private_msg(
                    user_id=event.user_id,
                    message=f"想要邀请我偷偷入群嘛~已经提醒{NICKNAME}的管理员大人了\n"
                    "请确保已经群主或群管理沟通过！\n"
                    "等待管理员处理吧！",
                )
                requests_manager.add_request(
                    event.user_id,
                    "group",
                    event.flag,
                    invite_group=event.group_id,
                    nickname=nickname,
                    sex=sex,
                    age=age,
                )
            else:
                logger.debug(
                    f"群聊请求五分钟内重复, 已忽略",
                    "群聊请求",
                    target=f"{event.user_id}:{event.group_id}",
                )


@x.handle()
async def _(event: MessageEvent):
    await asyncio.sleep(0.1)
    r = re.search(r'groupcode="(.*?)"', str(event.get_message()))
    if r:
        group_id = int(r.group(1))
    else:
        return
    r = re.search(r'groupname="(.*?)"', str(event.get_message()))
    if r:
        group_name = r.group(1)
    else:
        group_name = "None"
    requests_manager.set_group_name(group_name, group_id)


@scheduler.scheduled_job(
    "interval",
    minutes=5,
)
async def _():
    time_manager.clear()
