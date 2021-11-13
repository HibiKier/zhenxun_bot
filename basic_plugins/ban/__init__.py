from nonebot import on_command
from models.ban_user import BanUser
from models.level_user import LevelUser
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot
from nonebot.adapters.cqhttp import GroupMessageEvent, PrivateMessageEvent
from utils.utils import get_message_at, get_message_text, is_number
from configs.config import NICKNAME, Config
from nonebot.permission import SUPERUSER
from services.log import logger


__zx_plugin_name__ = "封禁Ban用户 [Admin]"
__plugin_usage__ = """
usage：
    将用户拉入或拉出黑名单
    指令:
        .ban [at] ?[小时] ?[分钟]
        .unban 
        示例：.ban @user
        示例：.ban @user 6
        示例：.ban @user 3 10
        示例：.unban @user
""".strip()
__plugin_superuser_usage__ = """
usage：
    屏蔽用户消息，相当于最上级.ban
    指令：
        b了 [at]
        示例：b了 @user
""".strip()
__plugin_des__ = '你被逮捕了！丢进小黑屋！'
__plugin_cmd__ = ['.ban [at] ?[小时] ?[分钟]', '.unban [at]', 'b了 [at] [_superuser]']
__plugin_version__ = 0.1
__plugin_author__ = 'HibiKier'
__plugin_settings__ = {
    "admin_level": Config.get_config("ban", "BAN_LEVEL"),
    "cmd": ['.ban', '.unban', 'ban', 'unban']
}
__plugin_configs__ = {
    "BAN_LEVEL [LEVEL]": {
        "value": 5,
        "help": "ban/unban所需要的管理员权限等级",
        "default_value": 5
    }
}


ban = on_command(
    ".ban",
    aliases={".unban", "/ban", "/unban"},
    priority=5,
    block=True,
)

super_ban = on_command('b了', permission=SUPERUSER, priority=5, block=True)


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
                    f"您的权限等级比对方低或相等, {NICKNAME}不能为您使用此功能!",
                    at_sender=True,
                )
            if await BanUser.ban(
                    qq, await LevelUser.get_user_level(event.user_id, event.group_id), time
            ):
                logger.info(
                    f"USER {event.user_id} GROUP {event.group_id} 将 USER {qq} 封禁 时长 {time/60} 分钟"
                )
                result = f"已经将 {user_name} 加入{NICKNAME}的黑名单了！"
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


@ban.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    if str(event.user_id) in bot.config.superusers:
        msg = get_message_text(event.json())
        msg = msg.split()
        if is_number(msg[0]):
            qq = int(msg[0])
            if state["_prefix"]["raw_command"] in [".ban", "/ban"]:
                hour = 0
                minute = 0
                if len(msg) > 1 and is_number(msg[1]):
                    hour = int(msg[1])
                if len(msg) > 2 and is_number(msg[2]):
                    minute = int(msg[2])
                time = hour * 60 * 60 + minute * 60
                time = time if time else -1
                if await BanUser.ban(
                    qq, 9, time
                ):
                    logger.info(
                        f"USER {event.user_id} 将 USER {qq} 封禁 时长 {time/60} 分钟"
                    )
                    result = f"已经将 {qq} 加入{NICKNAME}的黑名单了！"
                    if time != -1:
                        result += f"将在 {time/60} 分钟后解封"
                    else:
                        result += f"将在 ∞ 分钟后解封"
                    await ban.send(result)
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
                    await ban.send(f"{qq} 已在黑名单！预计 {time}后解封")
            else:
                if await BanUser.unban(qq):
                    logger.info(
                        f"USER {event.user_id} 将 USER {qq} 解禁"
                    )
                    result = f"已经把 {qq} 从黑名单中删除了！"
                else:
                    result = f"{qq} 不在黑名单！"
                await ban.send(result)
        else:
            await ban.finish('qq号必须是数字！\n格式：.ban [qq] [hour]? [minute]?', at_sender=True)


@super_ban.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    qq = get_message_at(event.json())
    if qq:
        qq = qq[0]
        user = await bot.get_group_member_info(group_id=event.group_id, user_id=qq)
        user_name = user['card'] if user['card'] else user['nickname']
        if not await BanUser.ban(qq, 10, 99999999):
            await BanUser.unban(qq)
            await BanUser.ban(qq, 10, 99999999)
        await ban.send(f"已将 {user_name} 拉入黑名单！")
    else:
        await super_ban.send('需要艾特被super ban的对象..')

