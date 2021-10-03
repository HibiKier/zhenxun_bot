from nonebot import on_request
from nonebot.adapters.cqhttp import Bot, FriendRequestEvent, GroupRequestEvent
from models.friend_user import FriendUser
from datetime import datetime
from configs.config import AUTO_ADD_FRIEND, NICKNAME
from nonebot.adapters.cqhttp.exception import ActionFailed
from utils.utils import scheduler
import time

__zx_plugin_name__ = "好友群聊处理请求 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = 'HibiKier'

friend_req = on_request(priority=5)


exists_data = {"private": {}, "group": {}}


@friend_req.handle()
async def _(bot: Bot, event: FriendRequestEvent, state: dict):
    global exists_data
    if exists_data["private"].get(event.user_id):
        if time.time() - exists_data["private"][event.user_id] < 60 * 5:
            return
    exists_data["private"][event.user_id] = time.time()
    user = await bot.get_stranger_info(user_id=event.user_id)
    nickname = user["nickname"]
    await bot.send_private_msg(
        user_id=int(list(bot.config.superusers)[0]),
        message=f"*****一份好友申请*****\n"
        f"昵称：{nickname}({event.user_id})\n"
        f"自动同意：{'√' if AUTO_ADD_FRIEND else '×'}\n"
        f"日期：{str(datetime.now()).split('.')[0]}\n"
        f"备注：{event.comment}",
    )
    if AUTO_ADD_FRIEND:
        await bot.set_friend_add_request(flag=event.flag, approve=True)
        await FriendUser.add_friend_info(user["user_id"], user["nickname"])


group_req = on_request(priority=5, block=True)


@group_req.handle()
async def _(bot: Bot, event: GroupRequestEvent, state: dict):
    global exists_data
    if event.sub_type == "invite":
        if str(event.user_id) in bot.config.superusers:
            try:
                await bot.set_group_add_request(
                    flag=event.flag, sub_type="invite", approve=True
                )
            except ActionFailed:
                pass
        else:
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


@scheduler.scheduled_job(
    "interval",
    minutes=5,
)
async def _():
    global exists_data
    exists_data = {"private": {}, "group": {}}
