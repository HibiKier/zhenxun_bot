from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me

from models.friend_user import FriendUser
from models.group_info import GroupInfo
from services.log import logger

__zx_plugin_name__ = "更新群/好友信息 [Superuser]"
__plugin_usage__ = """
usage：
    更新群/好友信息
    指令：
        更新群信息
        更新好友信息
""".strip()
__plugin_des__ = "更新群/好友信息"
__plugin_cmd__ = [
    "更新群信息",
    "更新好友信息",
]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"

update_group_info = on_command(
    "更新群信息", rule=to_me(), permission=SUPERUSER, priority=1, block=True
)
update_friend_info = on_command(
    "更新好友信息", rule=to_me(), permission=SUPERUSER, priority=1, block=True
)


@update_group_info.handle()
async def _(bot: Bot, event: MessageEvent):
    gl = await bot.get_group_list()
    gl = [g["group_id"] for g in gl]
    num = 0
    for g in gl:
        try:
            group_info = await bot.get_group_info(group_id=g)
            await GroupInfo.update_or_create(
                group_id=str(group_info["group_id"]),
                defaults={
                    "group_name": group_info["group_name"],
                    "max_member_count": group_info["max_member_count"],
                    "member_count": group_info["member_count"],
                },
            )
            num += 1
            logger.debug(
                "群聊信息更新成功", "更新群信息", event.user_id, target=group_info["group_id"]
            )
        except Exception as e:
            logger.error(f"更新群聊信息失败", "更新群信息", event.user_id, target=g, e=e)
    await update_group_info.send(f"成功更新了 {len(gl)} 个群的信息")
    logger.info(f"更新群聊信息完成，共更新了 {len(gl)} 个群的信息", "更新群信息", event.user_id)


@update_friend_info.handle()
async def _(bot: Bot, event: MessageEvent):
    num = 0
    error_list = []
    fl = await bot.get_friend_list()
    for f in fl:
        try:
            await FriendUser.update_or_create(
                user_id=str(f["user_id"]), defaults={"nickname": f["nickname"]}
            )
            logger.debug(f"更新好友信息成功", "更新好友信息", event.user_id, target=f["user_id"])
            num += 1
        except Exception as e:
            logger.error(f"更新好友信息失败", "更新好友信息", event.user_id, target=f["user_id"], e=e)
    await update_friend_info.send(f"成功更新了 {num} 个好友的信息")
    if error_list:
        await update_friend_info.send(f"以下好友更新失败:\n" + "\n".join(error_list))
    logger.info(f"更新好友信息完成，共更新了 {num} 个群的信息", "更新好友信息", event.user_id)
