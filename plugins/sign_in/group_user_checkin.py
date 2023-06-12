import asyncio
import math
import os
import random
import secrets
from datetime import datetime, timedelta
from io import BytesIO
from typing import Optional

from nonebot.adapters.onebot.v11 import MessageSegment

from configs.config import NICKNAME
from models.bag_user import BagUser
from models.group_member_info import GroupInfoUser
from models.sign_group_user import SignGroupUser
from services.log import logger
from utils.data_utils import init_rank
from utils.image_utils import BuildImage, BuildMat
from utils.utils import get_user_avatar

from .random_event import random_event
from .utils import SIGN_TODAY_CARD_PATH, get_card


async def group_user_check_in(
    nickname: str, user_id: int, group: int
) -> MessageSegment:
    "Returns string describing the result of checking in"
    present = datetime.now()
    # 取得相应用户
    user, is_create = await SignGroupUser.get_or_create(
        user_id=str(user_id), group_id=str(group)
    )
    # 如果同一天签到过，特殊处理
    if not is_create and (
        user.checkin_time_last.date() >= present.date()
        or f"{user}_{group}_sign_{datetime.now().date()}"
        in os.listdir(SIGN_TODAY_CARD_PATH)
    ):
        gold = await BagUser.get_gold(user_id, group)
        return await get_card(user, nickname, -1, gold, "")
    return await _handle_check_in(nickname, user_id, group, present)  # ok


async def check_in_all(nickname: str, user_id: str):
    """
    说明:
        签到所有群
    参数:
        :param nickname: 昵称
        :param user_id: 用户id
    """
    present = datetime.now()
    for u in await SignGroupUser.filter(user_id=user_id).all():
        group = u.group_id
        if not (
            u.checkin_time_last.date() >= present.date()
            or f"{u}_{group}_sign_{datetime.now().date()}"
            in os.listdir(SIGN_TODAY_CARD_PATH)
        ):
            await _handle_check_in(nickname, user_id, group, present)


async def _handle_check_in(
    nickname: str, user_id: str, group: str, present: datetime
) -> MessageSegment:
    user, _ = await SignGroupUser.get_or_create(user_id=user_id, group_id=group)
    impression_added = (secrets.randbelow(99) + 1) / 100
    critx2 = random.random()
    add_probability = float(user.add_probability)
    specify_probability = user.specify_probability
    if critx2 + add_probability > 0.97:
        impression_added *= 2
    elif critx2 < specify_probability:
        impression_added *= 2
    await SignGroupUser.sign(user, impression_added)
    gold = random.randint(1, 100)
    gift, gift_type = random_event(float(user.impression))
    if gift_type == "gold":
        await BagUser.add_gold(user_id, group, gold + gift)
        gift = f"额外金币 + {gift}"
    else:
        await BagUser.add_gold(user_id, group, gold)
        await BagUser.add_property(user_id, group, gift)
        gift += " + 1"

    logger.info(
        f"(USER {user.user_id}, GROUP {user.group_id})"
        f" CHECKED IN successfully. score: {user.impression:.2f} "
        f"(+{impression_added:.2f}).获取金币：{gold + gift if gift == 'gold' else gold}"
    )
    if critx2 + add_probability > 0.97 or critx2 < specify_probability:
        return await get_card(user, nickname, impression_added, gold, gift, True)
    else:
        return await get_card(user, nickname, impression_added, gold, gift)


async def group_user_check(nickname: str, user_id: str, group: str) -> MessageSegment:
    # heuristic: if users find they have never checked in they are probable to check in
    user, _ = await SignGroupUser.get_or_create(
        user_id=str(user_id), group_id=str(group)
    )
    gold = await BagUser.get_gold(user_id, group)
    return await get_card(user, nickname, None, gold, "", is_card_view=True)


async def group_impression_rank(group: int, num: int) -> Optional[BuildMat]:
    user_qq_list, impression_list, _ = await SignGroupUser.get_all_impression(group)
    return await init_rank("好感度排行榜", user_qq_list, impression_list, group, num)


async def random_gold(user_id, group_id, impression):
    if impression < 1:
        impression = 1
    gold = random.randint(1, 100) + random.randint(1, int(impression))
    if await BagUser.add_gold(user_id, group_id, gold):
        return gold
    else:
        return 0


# 签到总榜
async def impression_rank(group_id: int, data: dict):
    user_qq_list, impression_list, group_list = await SignGroupUser.get_all_impression(
        group_id
    )
    users, impressions, groups = [], [], []
    num = 0
    for i in range(105 if len(user_qq_list) > 105 else len(user_qq_list)):
        impression = max(impression_list)
        index = impression_list.index(impression)
        user = user_qq_list[index]
        group = group_list[index]
        user_qq_list.pop(index)
        impression_list.pop(index)
        group_list.pop(index)
        if user not in users and impression < 100000:
            if user not in data["0"]:
                users.append(user)
                impressions.append(impression)
                groups.append(group)
            else:
                num += 1
    for i in range(num):
        impression = max(impression_list)
        index = impression_list.index(impression)
        user = user_qq_list[index]
        group = group_list[index]
        user_qq_list.pop(index)
        impression_list.pop(index)
        group_list.pop(index)
        if user not in users and impression < 100000:
            users.append(user)
            impressions.append(impression)
            groups.append(group)
    return (await asyncio.gather(*[_pst(users, impressions, groups)]))[0]


async def _pst(users: list, impressions: list, groups: list):
    lens = len(users)
    count = math.ceil(lens / 33)
    width = 10
    idx = 0
    A = BuildImage(1740, 3300, color="#FFE4C4")
    for _ in range(count):
        col_img = BuildImage(550, 3300, 550, 100, color="#FFE4C4")
        for _ in range(33 if int(lens / 33) >= 1 else lens % 33 - 1):
            idx += 1
            if idx > 100:
                break
            impression = max(impressions)
            index = impressions.index(impression)
            user = users[index]
            group = groups[index]
            impressions.pop(index)
            users.pop(index)
            groups.pop(index)
            if user_ := await GroupInfoUser.get_or_none(
                user_id=str(user), group_id=str(group)
            ):
                user_name = user_.user_name
            else:
                user_name = f"我名字呢？"
            user_name = user_name if len(user_name) < 11 else user_name[:10] + "..."
            ava = await get_user_avatar(user)
            if ava:
                ava = BuildImage(50, 50, background=BytesIO(ava))
            else:
                ava = BuildImage(50, 50, color="white")
            ava.circle()
            bk = BuildImage(550, 100, color="#FFE4C4", font_size=30)
            font_w, font_h = bk.getsize(f"{idx}")
            bk.text((5, int((100 - font_h) / 2)), f"{idx}.")
            bk.paste(ava, (55, int((100 - 50) / 2)), True)
            bk.text((120, int((100 - font_h) / 2)), f"{user_name}")
            bk.text((460, int((100 - font_h) / 2)), f"[{impression:.2f}]")
            col_img.paste(bk)
        A.paste(col_img, (width, 0))
        lens -= 33
        width += 580
    W = BuildImage(1740, 3700, color="#FFE4C4", font_size=130)
    W.paste(A, (0, 260))
    font_w, font_h = W.getsize(f"{NICKNAME}的好感度总榜")
    W.text((int((1740 - font_w) / 2), int((260 - font_h) / 2)), f"{NICKNAME}的好感度总榜")
    return W.pic2bs4()
