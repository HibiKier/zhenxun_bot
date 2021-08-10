from nonebot import on_command
from models.ban_user import BanUser
from models.level_user import LevelUser
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot
from nonebot.adapters.cqhttp import GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP
from utils.utils import get_message_at, get_message_text, is_number
from services.log import logger


__plugin_name__ = "Ban/unBan"
__plugin_usage__ = (
    "用法：\n"
    "（不是禁言！是针对真寻是否处理封禁用户消息）\n"
    "封禁/解封用户 [小时] [分钟]\n"
    "示例：.ban @djdsk\n"
    "示例：.ban @djdsk 0 30\n"
    "示例：.ban @sdasf 4\n"
    "示例：.unban @sdasf"
)


ban = on_command(
    ".ban",
    aliases={".unban", "/ban", "/unban"},
    priority=5,
    permission=GROUP,
    block=True,
)


@ban.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    result = ""
    qq = get_message_at(event.json())
    if qq:
        qq = qq[0]
        user_name = await bot.get_group_member_info(group_id=event.group_id, user_id=qq)
        user_name = user_name['card'] if user_name['card'] else user_name['nickname']
        msg = get_message_text(event.json())
        if msg:
            msg = msg.split()
            if len(msg) == 2:
                if not is_number(msg[0].strip()) or not is_number(msg[1].strip()):
                    await ban.finish("参数必须是数字！", at_sender=True)
                time = int(msg[0]) * 60 * 60 + int(msg[1]) * 60
            else:
                if not is_number(msg[0].strip()):
                    await ban.finish("参数必须是数字！", at_sender=True)
                time = int(msg[0]) * 60 * 60
        else:
            time = -1
        if state["_prefix"]["raw_command"] in [".ban", "/ban"]:
            if (
                    await LevelUser.get_user_level(event.user_id, event.group_id)
                    <= await LevelUser.get_user_level(qq, event.group_id)
                    and str(event.user_id) not in bot.config.superusers
            ):
                await ban.finish(
                    f"您的权限等级比对方低或相等, {list(bot.config.nickname)[0]}不能为您使用此功能!",
                    at_sender=True,
                )
            if await BanUser.ban(
                    qq, await LevelUser.get_user_level(event.user_id, event.group_id), time
            ):
                logger.info(
                    f"USER {event.user_id} GROUP {event.group_id} 将 USER {qq} 封禁 时长 {time/60} 分钟"
                )
                result = f"已经将 {user_name} 加入{list(bot.config.nickname)[0]}的黑名单了！"
                if time != -1:
                    result += f"将在 {time/60} 分钟后解封"
            else:
                time = await BanUser.check_ban_time(qq)
                if is_number(time):
                    time = abs(int(time))
                    if time < 60:
                        time = str(time) + " 秒"
                    else:
                        time = str(int(time / 60)) + " 分钟"
                else:
                    time += " 分钟"
                result = f"{user_name} 已在黑名单！预计 {time}后解封"
        else:
            if (
                    await BanUser.check_ban_level(
                        qq, await LevelUser.get_user_level(event.user_id, event.group_id)
                    )
                    and str(event.user_id) not in bot.config.superusers
            ):
                await ban.finish(
                    f"ban掉 {user_name} 的管理员权限比您高，无法进行unban", at_sender=True
                )
            if await BanUser.unban(qq):
                logger.info(
                    f"USER {event.user_id} GROUP {event.group_id} 将 USER {qq} 解禁"
                )
                result = f"已经把 {user_name} 从黑名单中删除了！"
            else:
                result = f"{user_name} 不在黑名单！"
    else:
        await ban.finish("艾特人了吗？？", at_sender=True)
    await ban.finish(result, at_sender=True)

        


