from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent
from configs.config import NICKNAME
from models.level_user import LevelUser
from utils.utils import is_number
from models.ban_user import BanUser
from services.log import logger
from typing import Union


def parse_ban_time(msg: str) -> Union[int, str]:
    """
    解析ban时长
    :param msg: 文本消息
    """
    if not msg:
        return -1
    msg = msg.split()
    if len(msg) == 1:
        if not is_number(msg[0].strip()):
            return "参数必须是数字！"
        return int(msg[0]) * 60 * 60
    else:
        if not is_number(msg[0].strip()) or not is_number(msg[1].strip()):
            return "参数必须是数字！"
        return int(msg[0]) * 60 * 60 + int(msg[1]) * 60


async def a_ban(
    qq: int, time: int, user_name: str, event: MessageEvent, ban_level: int = None
) -> str:
    """
    ban
    :param qq: qq
    :param time: ban时长
    :param user_name: ban用户昵称
    :param event: event
    :param ban_level: ban级别
    """
    if isinstance(event, GroupMessageEvent):
        ban_level = await LevelUser.get_user_level(event.user_id, event.group_id)
    if await BanUser.ban(qq, ban_level, time):
        logger.info(
            f"USER {event.user_id} GROUP"
            f" {event.group_id if isinstance(event, GroupMessageEvent) else ''} 将 USER {qq} 封禁 时长 {time / 60} 分钟"
        )
        result = f"已经将 {user_name} 加入{NICKNAME}的黑名单了！"
        if time != -1:
            result += f"将在 {time / 60} 分钟后解封"
        else:
            result += f"将在 ∞ 分钟后解封"
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
    return result
