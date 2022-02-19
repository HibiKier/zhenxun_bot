from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from utils.utils import get_bot
from services.log import logger
from models.group_info import GroupInfo
from models.friend_user import FriendUser


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
async def _():
    bot = get_bot()
    gl = await bot.get_group_list()
    gl = [g["group_id"] for g in gl]
    num = 0
    rst = ""
    for g in gl:
        group_info = await bot.get_group_info(group_id=g)
        if await GroupInfo.add_group_info(
            group_info["group_id"],
            group_info["group_name"],
            group_info["max_member_count"],
            group_info["member_count"],
        ):
            num += 1
            logger.info(f"自动更新群组 {g} 信息成功")
        else:
            logger.info(f"自动更新群组 {g} 信息失败")
            rst += f"{g} 更新失败\n"
    await update_group_info.send(f"成功更新了 {num} 个群的信息\n{rst[:-1]}")


@update_friend_info.handle()
async def _():
    num = 0
    rst = ""
    fl = await get_bot().get_friend_list()
    for f in fl:
        if await FriendUser.add_friend_info(f["user_id"], f["nickname"]):
            logger.info(f'自动更新好友 {f["user_id"]} 信息成功')
            num += 1
        else:
            logger.warning(f'自动更新好友 {f["user_id"]} 信息失败')
            rst += f'{f["user_id"]} 更新失败\n'
    await update_friend_info.send(f"成功更新了 {num} 个好友的信息\n{rst[:-1]}")
