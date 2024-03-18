from datetime import datetime

from nonebot.adapters import Bot

from zhenxun.models.friend_user import FriendUser
from zhenxun.models.group_member_info import GroupInfoUser
from zhenxun.utils.image_utils import BuildImage, ImageTemplate

from .model import BlackWord
from .utils import Config, _get_punish


async def show_black_text_image(
    user_id: str | None,
    group_id: str | None,
    date: datetime | None,
    data_type: str = "=",
) -> BuildImage:
    """展示记录名单

    参数:
        bot: bot
        user: 用户id
        group_id: 群组id
        date: 日期
        data_type: 日期搜索类型

    返回:
        BuildImage: 数据图片
    """
    data_list = await BlackWord.get_black_data(user_id, group_id, date, data_type)
    column_name = [
        "ID",
        "昵称",
        "UID",
        "GID",
        "文本",
        "检测内容",
        "检测等级",
        "惩罚",
        "平台",
        "记录日期",
    ]
    column_list = []
    uid_list = [u for u in data_list]
    uid2name = {
        u.user_id: u.user_name for u in await FriendUser.filter(user_id__in=uid_list)
    }
    for i, data in enumerate(data_list):
        uname = uid2name.get(data.user_id)
        if not uname:
            if u := await GroupInfoUser.get_or_none(
                user_id=data.user_id, group_id=data.group_id
            ):
                uname = u.user_name
        if len(data.plant_text) > 30:
            data.plant_text = data.plant_text[:30] + "..."
        column_list.append(
            [
                i,
                uname or data.user_id,
                data.user_id,
                data.group_id,
                data.plant_text,
                data.black_word,
                data.punish_level,
                data.punish,
                data.platform,
                data.create_time,
            ]
        )
    A = await ImageTemplate.table_page(
        "记录名单", "一个都不放过!", column_name, column_list
    )
    return A


async def set_user_punish(
    bot: Bot, user_id: str, group_id: str | None, id_: int, punish_level: int
) -> str:
    """设置惩罚

    参数:
        user_id: 用户id
        group_id: 群组id或频道id
        id_: 记录下标
        punish_level: 惩罚等级

    返回:
        str: 结果
    """
    result = await _get_punish(bot, punish_level, user_id, group_id)
    punish = {
        1: "永久ban",
        2: "删除好友",
        3: f"ban {result} 天",
        4: f"ban {result} 分钟",
        5: "口头警告",
    }
    if await BlackWord.set_user_punish(user_id, punish[punish_level], id_=id_):
        return f"已对 USER {user_id} 进行 {punish[punish_level]} 处罚。"
    else:
        return "操作失败，可能未找到用户，id或敏感词"
