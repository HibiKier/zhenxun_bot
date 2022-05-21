from nonebot.adapters.onebot.v11 import Bot
from utils.image_utils import BuildImage, text2image
from services.log import logger
from typing import Optional
from datetime import datetime
from .model import BlackWord
from .utils import _get_punish, Config


async def show_black_text_image(
    bot: Bot,
    user: Optional[int],
    group_id: Optional[int],
    date: Optional[datetime],
    data_type: str = "=",
) -> BuildImage:
    """
    展示记录名单
    :param bot: bot
    :param user: 用户qq
    :param group_id: 群聊
    :param date: 日期
    :param data_type: 日期搜索类型
    :return:
    """
    data = await BlackWord.get_black_data(user, group_id, date, data_type)
    A = BuildImage(0, 0, color="#f9f6f2", font_size=20)
    image_list = []
    friend_str = await bot.get_friend_list()
    id_str = ""
    uname_str = ""
    uid_str = ""
    gid_str = ""
    plant_text_str = ""
    black_word_str = ""
    punish_str = ""
    punish_level_str = ""
    create_time_str = ""
    for i, x in enumerate(data):
        try:
            if x.group_id:
                user_name = (
                    await bot.get_group_member_info(
                        group_id=x.group_id, user_id=x.user_qq
                    )
                )["card"]
            else:
                user_name = [
                    u["nickname"] for u in friend_str if u["user_id"] == x.user_qq
                ][0]
        except Exception as e:
            logger.warning(
                f"show_black_text_image 获取 USER {x.user_qq} user_name 失败 {type(e)}：{e}"
            )
            user_name = x.user_qq
        id_str += f"{i}\n"
        uname_str += f"{user_name}\n"
        uid_str += f"{x.user_qq}\n"
        gid_str += f"{x.group_id}\n"
        plant_text = " ".join(x.plant_text.split("\n"))
        if A.getsize(plant_text)[0] > 200:
            plant_text = plant_text[:20] + "..."
        plant_text_str += f"{plant_text}\n"
        black_word_str += f"{x.black_word}\n"
        punish_str += f"{x.punish}\n"
        punish_level_str += f"{x.punish_level}\n"
        create_time_str += f"{x.create_time.replace(microsecond=0)}\n"
    _tmp_img = BuildImage(0, 0, font_size=35, font="CJGaoDeGuo.otf")
    for s, type_ in [
        (id_str, "Id"),
        (uname_str, "昵称"),
        (uid_str, "UID"),
        (gid_str, "GID"),
        (plant_text_str, "文本"),
        (black_word_str, "检测"),
        (punish_str, "惩罚"),
        (punish_level_str, "等级"),
        (create_time_str, "记录日期"),
    ]:
        img = await text2image(s, color="#f9f6f2", _add_height=2.1)
        w = _tmp_img.getsize(type_)[0] if _tmp_img.getsize(type_)[0] > img.w else img.w
        A = BuildImage(w + 11, img.h + 50, color="#f9f6f2", font_size=35, font="CJGaoDeGuo.otf")
        await A.atext((10, 10), type_)
        await A.apaste(img, (0, 50))
        image_list.append(A)
    horizontal_line = []
    w, h = 0, 0
    for img in image_list:
        w += img.w + 20
        h = img.h if img.h > h else h
        horizontal_line.append(img.w)
    A = BuildImage(w, h, color="#f9f6f2")
    current_w = 0
    for img in image_list:
        await A.apaste(img, (current_w, 0))
        current_w += img.w + 20
    return A


async def set_user_punish(user_id: int, id_: int, punish_level: int) -> str:
    """
    设置惩罚
    :param user_id: 用户id
    :param id_: 记录下标
    :param punish_level: 惩罚等级
    """
    result = await _get_punish(punish_level, user_id)
    punish = {
        1: "永久ban",
        2: "删除好友",
        3: f"ban {result} 天",
        4: f"ban {result} 分钟",
        5: "口头警告"
    }
    if await BlackWord.set_user_punish(user_id, punish[punish_level], id_=id_):
        return f"已对 USER {user_id} 进行 {punish[punish_level]} 处罚。"
    else:
        return "操作失败，可能未找到用户，id或敏感词"
