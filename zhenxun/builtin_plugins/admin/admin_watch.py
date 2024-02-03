from nonebot import on_notice
from nonebot.adapters.onebot.v11 import GroupAdminNoticeEvent
from nonebot.plugin import PluginMetadata

from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.group_member_info import GroupInfoUser
from zhenxun.models.level_user import LevelUser
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType

__zx_plugin_name__ = "群管理员变动监测 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


__plugin_meta__ = PluginMetadata(
    name="群管理员变动监测",
    description="检测群管理员变动, 添加与删除管理员默认权限, 当配置项 ADMIN_DEFAULT_AUTH 为空时, 不会添加管理员权限",
    usage="",
    extra=PluginExtraData(
        author="HibiKier", version="0.1", plugin_type=PluginType.HIDDEN
    ).dict(),
)


admin_notice = on_notice(priority=5)

base_config = Config.get("admin_bot_manage")


@admin_notice.handle()
async def _(event: GroupAdminNoticeEvent):
    nickname = event.user_id
    if user := await GroupInfoUser.get_or_none(
        user_id=str(event.user_id), group_id=str(event.group_id)
    ):
        nickname = user.user_name
    if event.sub_type == "set":
        admin_default_auth = base_config.get("ADMIN_DEFAULT_AUTH")
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
        logger.info("撤销群管理员, 取消权限等级", "群管理员变动监测", event.user_id, event.group_id)
