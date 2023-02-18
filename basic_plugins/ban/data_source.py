from typing import Optional, Union

from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent

from configs.config import NICKNAME
from models.ban_user import BanUser
from models.level_user import LevelUser
from services.log import logger
from utils.utils import is_number


def parse_ban_time(msg: str) -> Union[int, str]:
    """
    解析ban时长
    :param msg: 文本消息
    """
    try:
        if not msg:
            return -1
        msg_split = msg.split()
        if len(msg_split) == 1:
            if not is_number(msg_split[0].strip()):
                return "参数必须是数字！"
            return int(msg_split[0]) * 60 * 60
        else:
            if not is_number(msg_split[0].strip()) or not is_number(
                msg_split[1].strip()
            ):
                return "参数必须是数字！"
            return int(msg_split[0]) * 60 * 60 + int(msg_split[1]) * 60
    except ValueError as e:
        logger.error("解析ban时长错误", ".ban", e=e)
        return "时长不可以带小数点！"


async def a_ban(
    qq: int,
    time: int,
    user_name: str,
    event: MessageEvent,
    ban_level: Optional[int] = None,
) -> str:
    """
    ban
    :param qq: qq
    :param time: ban时长
    :param user_name: ban用户昵称
    :param event: event
    :param ban_level: ban级别
    """
    group_id = None
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
        ban_level = await LevelUser.get_user_level(event.user_id, event.group_id)
    if not ban_level:
        return "未查询到ban级用户权限"
    if await BanUser.ban(qq, ban_level, time):
        logger.info(
            f"将 [Target]({qq})封禁 时长 {time / 60} 分钟", ".ban", event.user_id, group_id
        )
        result = f"已经将 {user_name} 加入{NICKNAME}的黑名单了！"
        if time != -1:
            result += f"将在 {time / 60} 分钟后解封"
        else:
            result += f"将在 ∞ 分钟后解封"
    else:
        ban_time = await BanUser.check_ban_time(qq)
        if isinstance(ban_time, int):
            ban_time = abs(float(ban_time))
            if ban_time < 60:
                ban_time = str(ban_time) + " 秒"
            else:
                ban_time = str(int(ban_time / 60)) + " 分钟"
        else:
            ban_time += " 分钟"
        result = f"{user_name} 已在黑名单！预计 {ban_time}后解封"
    return result
