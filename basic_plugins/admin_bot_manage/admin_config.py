from nonebot import on_notice
from services.log import logger
from nonebot.adapters.onebot.v11 import GroupAdminNoticeEvent
from models.level_user import LevelUser
from models.group_member_info import GroupInfoUser
from configs.config import Config


__zx_plugin_name__ = "群管理员变动监测 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


admin_notice = on_notice(priority=5)


@admin_notice.handle()
async def _(event: GroupAdminNoticeEvent):
    try:
        nickname = (
            await GroupInfoUser.get_member_info(event.user_id, event.group_id)
        ).user_name
    except AttributeError:
        nickname = event.user_id
    if event.sub_type == "set":
        await LevelUser.set_level(
            event.user_id,
            event.group_id,
            Config.get_config("admin_bot_manage", "ADMIN_DEFAULT_AUTH"),
        )
        logger.info(
            f"为新晋管理员 {nickname}({event.user_id}) "
            f"添加权限等级：{Config.get_config('admin_bot_manage', 'ADMIN_DEFAULT_AUTH')}"
        )
    elif event.sub_type == "unset":
        await LevelUser.delete_level(event.user_id, event.group_id)
        logger.info(f"将非管理员 {nickname}({event.user_id}) 取消权限等级")
