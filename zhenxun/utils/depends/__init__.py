from nonebot.internal.params import Depends
from nonebot.params import Command
from nonebot_plugin_userinfo import EventUserInfo, UserInfo


def OneCommand():
    """
    获取单个命令Command
    """

    async def dependency(
        cmd: tuple[str, ...] = Command(),
    ):
        return cmd[0] if cmd else None

    return Depends(dependency)


def UserName():
    """
    用户名称
    """

    async def dependency(user_info: UserInfo = EventUserInfo()):
        return (
            user_info.user_displayname or user_info.user_remark or user_info.user_name
        )

    return Depends(dependency)
