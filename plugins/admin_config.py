from nonebot import on_notice
from services.log import logger
from nonebot.adapters.cqhttp import Bot, GroupAdminNoticeEvent
from nonebot.typing import T_State
from models.level_user import LevelUser
from models.group_member_info import GroupInfoUser
from configs.config import ADMIN_DEFAULT_AUTH


admin_notice = on_notice(priority=5)


@admin_notice.handle()
async def _(bot: Bot, event: GroupAdminNoticeEvent, state: T_State):
    try:
        nickname = (await GroupInfoUser.select_member_info(event.user_id, event.group_id)).user_name
    except AttributeError:
        nickname = event.user_id
    if event.sub_type == 'set':
        await LevelUser.set_level(event.user_id, event.group_id, ADMIN_DEFAULT_AUTH)
        logger.info(f'为新晋管理员 {nickname}({event.user_id}) 添加权限等级：{ADMIN_DEFAULT_AUTH}')
    if event.sub_type == 'unset':
        await LevelUser.delete_level(event.user_id, event.group_id)
        logger.info(f'将非管理员 {nickname}({event.user_id}) 取消权限等级')



