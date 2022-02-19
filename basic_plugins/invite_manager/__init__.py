from nonebot import on_request, on_message
from nonebot.adapters.onebot.v11 import (
    Bot,
    FriendRequestEvent,
    GroupRequestEvent,
    MessageEvent,
)
from models.friend_user import FriendUser
from datetime import datetime
from configs.config import NICKNAME, Config
from nonebot.adapters.onebot.v11.exception import ActionFailed
from utils.manager import requests_manager
from models.group_info import GroupInfo
from utils.utils import scheduler
import asyncio
import time
import re

__zx_plugin_name__ = "好友群聊处理请求 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_configs__ = {
    "AUTO_ADD_FRIEND": {"value": False, "help": "是否自动同意好友添加", "default_value": False}
}

friend_req = on_request(priority=5, block=True)
group_req = on_request(priority=5, block=True)
x = on_message(priority=9, block=False)

exists_data = {"private": {}, "group": {}}


@friend_req.handle()
async def _(bot: Bot, event: FriendRequestEvent):
    global exists_data
    if exists_data["private"].get(event.user_id):
        if time.time() - exists_data["private"][event.user_id] < 60 * 5:
            return
    exists_data["private"][event.user_id] = time.time()
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
        await bot.set_friend_add_request(flag=event.flag, approve=True)
        await FriendUser.add_friend_info(user["user_id"], user["nickname"])
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


@group_req.handle()
async def _(bot: Bot, event: GroupRequestEvent):
    global exists_data
    if event.sub_type == "invite":
        if str(event.user_id) in bot.config.superusers:
            try:
                if await GroupInfo.get_group_info(event.group_id):
                    await GroupInfo.set_group_flag(event.group_id, 1)
                else:
                    group_info = await bot.get_group_info(group_id=event.group_id)
                    await GroupInfo.add_group_info(
                        group_info["group_id"],
                        group_info["group_name"],
                        group_info["max_member_count"],
                        group_info["member_count"],
                        1,
                    )
                await bot.set_group_add_request(
                    flag=event.flag, sub_type="invite", approve=True
                )
            except ActionFailed:
                pass
        else:
            user = await bot.get_stranger_info(user_id=event.user_id)
            sex = user["sex"]
            age = str(user["age"])
            if exists_data["group"].get(f"{event.user_id}:{event.group_id}"):
                if (
                    time.time()
                    - exists_data["group"][f"{event.user_id}:{event.group_id}"]
                    < 60 * 5
                ):
                    return
            exists_data["group"][f"{event.user_id}:{event.group_id}"] = time.time()
            nickname = await FriendUser.get_user_name(event.user_id)
            await bot.send_private_msg(
                user_id=int(list(bot.config.superusers)[0]),
                message=f"*****一份入群申请*****\n"
                f"申请人：{nickname}({event.user_id})\n"
                f"群聊：{event.group_id}\n"
                f"邀请日期：{str(datetime.now()).split('.')[0]}",
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
    global exists_data
    exists_data = {"private": {}, "group": {}}
