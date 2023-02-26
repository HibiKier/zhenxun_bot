from typing import List

from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

from configs.config import NICKNAME, Config
from models.ban_user import BanUser
from models.level_user import LevelUser
from services.log import logger
from utils.depends import AtList, OneCommand
from utils.utils import is_number

from .data_source import a_ban, parse_ban_time

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
__plugin_des__ = "你被逮捕了！丢进小黑屋！"
__plugin_cmd__ = [".ban [at] ?[小时] ?[分钟]", ".unban [at]", "b了 [at] [_superuser]"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "admin_level": Config.get_config("ban", "BAN_LEVEL"),
    "cmd": [".ban", ".unban", "ban", "unban"],
}
__plugin_configs__ = {
    "BAN_LEVEL [LEVEL]": {
        "value": 5,
        "help": "ban/unban所需要的管理员权限等级",
        "default_value": 5,
        "type": int
    }
}


ban = on_command(
    ".ban",
    aliases={".unban", "/ban", "/unban"},
    priority=5,
    block=True,
)

super_ban = on_command("b了", permission=SUPERUSER, priority=5, block=True)


@ban.handle()
async def _(
    bot: Bot,
    event: GroupMessageEvent,
    cmd: str = OneCommand(),
    arg: Message = CommandArg(),
    at_list: List[int] = AtList(),
):
    result = ""
    if at_list:
        qq = at_list[0]
        user = await bot.get_group_member_info(group_id=event.group_id, user_id=qq)
        user_name = user["card"] or user["nickname"]
        msg = arg.extract_plain_text().strip()
        time = parse_ban_time(msg)
        if isinstance(time, str):
            await ban.finish(time, at_sender=True)
        user_level = await LevelUser.get_user_level(event.user_id, event.group_id)
        is_not_superuser = str(event.user_id) not in bot.config.superusers
        if cmd in [".ban", "/ban"]:
            at_user_level = await LevelUser.get_user_level(qq, event.group_id)
            if user_level <= at_user_level and is_not_superuser:
                await ban.finish(
                    f"您的权限等级比对方低或相等, {NICKNAME}不能为您使用此功能!",
                    at_sender=True,
                )
            logger.info(f"用户封禁 时长: {time}", cmd, event.user_id, event.group_id, qq)
            result = await a_ban(qq, time, user_name, event)
        else:
            if await BanUser.check_ban_level(qq, user_level) and is_not_superuser:
                await ban.finish(
                    f"ban掉 {user_name} 的管理员权限比您高，无法进行unban", at_sender=True
                )
            if await BanUser.unban(qq):
                logger.info(f"解除用户封禁", cmd, event.user_id, event.group_id, qq)
                result = f"已经将 {user_name} 从黑名单中删除了！"
            else:
                result = f"{user_name} 不在黑名单！"
    else:
        await ban.finish("艾特人了吗？？", at_sender=True)
    await ban.send(result, at_sender=True)


@ban.handle()
async def _(
    bot: Bot,
    event: PrivateMessageEvent,
    cmd: str = OneCommand(),
    arg: Message = CommandArg(),
):
    msg = arg.extract_plain_text().strip()
    if msg and str(event.user_id) in bot.config.superusers:
        msg_split = msg.split()
        if msg_split and is_number(msg_split[0]):
            qq = int(msg_split[0])
            param = msg_split[1:]
            if cmd in [".ban", "/ban"]:
                time = parse_ban_time(" ".join(param))
                if isinstance(time, str):
                    logger.info(time, cmd, event.user_id, target=qq)
                    await ban.finish(time)
                result = await a_ban(qq, time, str(qq), event, 9)
            else:
                if await BanUser.unban(qq):
                    result = f"已经把 {qq} 从黑名单中删除了！"
                else:
                    result = f"{qq} 不在黑名单！"
            await ban.send(result)
            logger.info(result, cmd, event.user_id, target=qq)
        else:
            await ban.send("参数不正确！\n格式：.ban [qq] [hour]? [minute]?", at_sender=True)


@super_ban.handle()
async def _(
    bot: Bot,
    event: MessageEvent,
    cmd: str = OneCommand(),
    arg: Message = CommandArg(),
    at_list: List[int] = AtList(),
):
    user_name = ""
    qq = None
    if isinstance(event, GroupMessageEvent):
        if at_list:
            qq = at_list[0]
            user = await bot.get_group_member_info(group_id=event.group_id, user_id=qq)
            user_name = user["card"] or user["nickname"]
    else:
        msg = arg.extract_plain_text().strip()
        if not is_number(msg):
            await super_ban.finish("对象qq必须为纯数字...")
        qq = int(msg)
        user_name = msg
    if qq:
        await BanUser.ban(qq, 10, 99999999)
        await ban.send(f"已将 {user_name} 拉入黑名单！")
        logger.info(
            f"已将 {user_name} 拉入黑名单！",
            cmd,
            event.user_id,
            event.group_id if isinstance(event, GroupMessageEvent) else None,
            qq,
        )
    else:
        await super_ban.send("需要提供被super ban的对象，可以使用at或者指定qq...")
