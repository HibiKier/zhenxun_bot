from nonebot import on_request
from nonebot.adapters.cqhttp import Bot, FriendRequestEvent, GroupRequestEvent
from models.friend_user import FriendUser
from datetime import datetime
from configs.config import AUTO_ADD_FRIEND
from nonebot.adapters.cqhttp.exception import ActionFailed
from utils.utils import scheduler

__plugin_name__ = "好友群聊处理请求 [Hidden]"

friend_req = on_request(priority=5)


exists_list = []


@friend_req.handle()
async def _(bot: Bot, event: FriendRequestEvent, state: dict):
    global exists_list
    if f"{event.user_id}" not in exists_list:
        exists_list.append(f"{event.user_id}")
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
    global exists_list
    if event.sub_type == "invite":
        if str(event.user_id) in bot.config.superusers:
            try:
                await bot.set_group_add_request(
                    flag=event.flag, sub_type="invite", approve=True
                )
            except ActionFailed:
                pass
        else:
            if f"{event.user_id}:{event.group_id}" not in exists_list:
                exists_list.append(f"{event.user_id}:{event.group_id}")
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
                    message="想要邀请我偷偷入群嘛~已经提醒真寻的管理员大人了\n"
                    "请确保已经群主或群管理沟通过！\n"
                    "等待管理员处理吧！",
                )


@scheduler.scheduled_job(
    "interval",
    minutes=5,
)
async def _():
    global exists_list
    exists_list = []
