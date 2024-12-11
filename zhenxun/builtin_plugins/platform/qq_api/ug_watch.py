from nonebot.message import run_preprocessor
from nonebot_plugin_uninfo import Uninfo

from zhenxun.models.friend_user import FriendUser
from zhenxun.models.group_console import GroupConsole
from zhenxun.models.group_member_info import GroupInfoUser
from zhenxun.services.log import logger
from zhenxun.utils.platform import PlatformUtils


@run_preprocessor
async def do_something(session: Uninfo):
    platform = PlatformUtils.get_platform(session)
    if session.group:
        if not await GroupConsole.exists(group_id=session.group.id):
            await GroupConsole.create(group_id=session.group.id)
            logger.info("添加当前群组ID信息" "", session=session)

        if not await GroupInfoUser.exists(
            user_id=session.user.id, group_id=session.group.id
        ):
            await GroupInfoUser.create(
                user_id=session.user.id, group_id=session.group.id, platform=platform
            )
            logger.info("添加当前用户群组ID信息", "", session=session)
    elif not await FriendUser.exists(user_id=session.user.id, platform=platform):
        try:
            await FriendUser.create(user_id=session.user.id, platform=platform)
            logger.info("添加当前好友用户信息", "", session=session)
        except Exception as e:
            logger.error("添加当前好友用户信息失败", session=session, e=e)
