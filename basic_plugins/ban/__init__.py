from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent, MessageEvent, Message, Bot
from nonebot.params import CommandArg, Command
from nonebot import on_command
from models.ban_user import BanUser
from models.level_user import LevelUser
from typing import Tuple
from utils.utils import get_message_at, is_number
from configs.config import NICKNAME, Config
from nonebot.permission import SUPERUSER
from .data_source import parse_ban_time, a_ban
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
    b了=屏蔽用户消息，相当于最上级.ban
    跨群ban以及跨群b了
    指令：
        b了 [at/qq]
        .ban [user_id] ?[小时] ?[分钟]
        示例：b了 @user
        示例：b了 1234567
        示例：.ban 12345567
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
async def _(bot: Bot, event: GroupMessageEvent, cmd: Tuple[str, ...] = Command(),  arg: Message = CommandArg()):
    cmd = cmd[0]
    result = ""
    qq = get_message_at(event.json())
    if qq:
        qq = qq[0]
        user_name = await bot.get_group_member_info(group_id=event.group_id, user_id=qq)
        user_name = user_name['card'] or user_name['nickname']
        msg = arg.extract_plain_text().strip()
        time = parse_ban_time(msg)
        if isinstance(time, str):
            await ban.finish(time, at_sender=True)
        if cmd in [".ban", "/ban"]:
            if (
                await LevelUser.get_user_level(event.user_id, event.group_id)
                <= await LevelUser.get_user_level(qq, event.group_id)
                and str(event.user_id) not in bot.config.superusers
            ):
                await ban.finish(
                    f"您的权限等级比对方低或相等, {NICKNAME}不能为您使用此功能!",
                    at_sender=True,
                )
            result = await a_ban(qq, time, user_name, event)
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
    await ban.send(result, at_sender=True)


@ban.handle()
async def _(bot: Bot, event: PrivateMessageEvent, cmd: Tuple[str, ...] = Command(),  arg: Message = CommandArg()):
    cmd = cmd[0]
    msg = arg.extract_plain_text().strip()
    if msg:
        if str(event.user_id) in bot.config.superusers:
            if is_number(arg.extract_plain_text().strip().split()[0]):
                qq = int(msg[0])
                msg = msg[1:]
                if cmd in [".ban", "/ban"]:
                    time = parse_ban_time(msg)
                    if isinstance(time, str):
                        await ban.finish(time)
                    result = await a_ban(qq, time, str(qq), event, 9)
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
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    if isinstance(event, GroupMessageEvent):
        qq = get_message_at(event.json())
    else:
        qq = arg.extract_plain_text().strip()
        if not is_number(qq):
            await super_ban.finish("对象qq必须为纯数字...")
        qq = [qq]
    if qq:
        qq = qq[0]
        user = await bot.get_group_member_info(group_id=event.group_id, user_id=qq)
        user_name = user['card'] or user['nickname']
        if not await BanUser.ban(qq, 10, 99999999):
            await BanUser.unban(qq)
            await BanUser.ban(qq, 10, 99999999)
        await ban.send(f"已将 {user_name} 拉入黑名单！")
    else:
        await super_ban.send('需要添加被super ban的对象，可以使用at或者指定qq..')

