from nonebot import on_request
from nonebot.adapters.cqhttp import Bot, FriendRequestEvent, GroupRequestEvent
from models.friend_user import FriendUser
from datetime import datetime
from configs.config import AUTO_ADD_FRIEND
from nonebot.adapters.cqhttp.exception import ActionFailed

__plugin_name__ = '处理请求'

friend_req = on_request(priority=5)


@friend_req.handle()
async def _(bot: Bot, event: FriendRequestEvent, state: dict):
    if AUTO_ADD_FRIEND:
        nickname = ''
        for user in await bot.get_friend_list():
            if user['user_id'] == event.user_id:
                nickname = user['nickname']
                await FriendUser.add_friend_info(user['user_id'], user['nickname'])
                break
        await bot.send_private_msg(user_id=int(list(bot.config.superusers)[0]), message=f"{nickname}({event.user_id})"
                                                                                        f" 添加小真寻好友（已自动同意）")
        await bot.set_friend_add_request(flag=event.flag, approve=True)


group_req = on_request(priority=5, block=True)


@group_req.handle()
async def _(bot: Bot, event: GroupRequestEvent, state: dict):
    if event.sub_type == 'invite':
        nickname = await FriendUser.get_user_name(event.user_id)
        if str(event.user_id) in bot.config.superusers:
            try:
                await bot.set_group_add_request(flag=event.flag, sub_type='invite', approve=True)
            except ActionFailed:
                pass
        else:
            await bot.send_private_msg(user_id=int(list(bot.config.superusers)[0]),
                                       message=f"报告..\n{nickname}({event.user_id})"
                                               f" 希望邀请我加入 {event.group_id}\n邀请日期：{str(datetime.now()).split('.')[0]}")
            await bot.send_private_msg(user_id=event.user_id,
                                       message="想要邀请我偷偷入群嘛~~已经提醒管理员了\n等待管理员处理吧~")
