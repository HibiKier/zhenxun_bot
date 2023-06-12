from nonebot import on_notice
from nonebot.adapters.onebot.v11 import GroupAdminNoticeEvent

from configs.config import Config
from models.group_member_info import GroupInfoUser
from models.level_user import LevelUser
from services.log import logger

__zx_plugin_name__ = "群管理员变动监测 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


admin_notice = on_notice(priority=5)


@admin_notice.handle()
async def _(event: GroupAdminNoticeEvent):
    if user := await GroupInfoUser.get_or_none(
        user_id=str(event.user_id), group_id=str(event.group_id)
    ):
        nickname = user.user_name
    else:
        nickname = event.user_id
    if event.sub_type == "set":
        admin_default_auth = Config.get_config("admin_bot_manage", "ADMIN_DEFAULT_AUTH")
        if admin_default_auth is not None:
            await LevelUser.set_level(
                event.user_id,
                event.group_id,
                admin_default_auth,
            )
            logger.info(
                f"成为管理员，添加权限: {admin_default_auth}",
                "群管理员变动监测",
                event.user_id,
                event.group_id,
            )
        else:
            logger.warning(
                f"配置项 MODULE: [<u><y>admin_bot_manage</y></u>] | KEY: [<u><y>ADMIN_DEFAULT_AUTH</y></u>] 为空"
            )
    elif event.sub_type == "unset":
        await LevelUser.delete_level(event.user_id, event.group_id)
        logger.info("撤销管理员,，取消权限等级", "群管理员变动监测", event.user_id, event.group_id)
