import os
import random
import secrets
from datetime import datetime
from pathlib import Path

import pytz
from nonebot_plugin_session import EventSession
from tortoise.functions import Count

from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.models.friend_user import FriendUser
from zhenxun.models.group_member_info import GroupInfoUser
from zhenxun.models.sign_log import SignLog
from zhenxun.models.sign_user import SignUser
from zhenxun.models.user_console import UserConsole
from zhenxun.services.log import logger
from zhenxun.utils.image_utils import BuildImage, ImageTemplate
from zhenxun.utils.utils import get_user_avatar

from ._random_event import random_event
from .utils import SIGN_TODAY_CARD_PATH, get_card

ICON_PATH = IMAGE_PATH / "_icon"

PLATFORM_PATH = {
    "dodo": ICON_PATH / "dodo.png",
    "discord": ICON_PATH / "discord.png",
    "kaiheila": ICON_PATH / "kook.png",
    "qq": ICON_PATH / "qq.png",
}


class SignManage:

    @classmethod
    async def rank(cls, user_id: str, num: int) -> BuildImage:
        all_list = (
            await SignUser.annotate()
            .order_by("impression")
            .values_list("user_id", flat=True)
        )
        index = all_list.index(user_id) + 1  # type: ignore
        user_list = await SignUser.annotate().order_by("impression").limit(num).all()
        user_id_list = [u.user_id for u in user_list]
        log_list = (
            await SignLog.filter(user_id__in=user_id_list)
            .annotate(count=Count("id"))
            .group_by("user_id")
            .values_list("user_id", "count")
        )
        uid2cnt = {l[0]: l[1] for l in log_list}
        column_name = ["排名", "-", "名称", "好感度", "签到次数", "平台"]
        friend_list = await FriendUser.filter(user_id__in=user_id_list).values_list(
            "user_id", "user_name"
        )
        uid2name = {f[0]: f[1] for f in friend_list}
        group_member_list = await GroupInfoUser.filter(
            user_id__in=user_id_list
        ).values_list("user_id", "user_name")
        for gm in group_member_list:
            uid2name[gm[0]] = gm[1]
        data_list = []
        for i, user in enumerate(user_list):
            bytes = await get_user_avatar(user.user_id)
            data_list.append(
                [
                    f"{i+1}",
                    (bytes, 30, 30) if user.platform == "qq" else "",
                    uid2name.get(user.user_id),
                    user.impression,
                    uid2cnt.get(user.user_id) or 0,
                    (PLATFORM_PATH.get(user.platform), 30, 30),
                ]
            )
        return await ImageTemplate.table_page(
            "好感度排行", f"你的排名在第 {index} 位哦!", column_name, data_list
        )

    @classmethod
    async def sign(
        cls, session: EventSession, nickname: str, is_view_card: bool = False
    ) -> Path | None:
        """签到

        参数:
            session: Session
            nickname: 用户昵称
            is_view_card: 是否展示卡片

        返回:
            Path: 卡片路径
        """
        if not session.id1:
            return None
        now = datetime.now(pytz.timezone("Asia/Shanghai"))
        user_console, _ = await UserConsole.get_or_create(
            user_id=session.id1,
            defaults={
                "uid": await UserConsole.get_new_uid(),
                "platform": session.platform,
            },
        )
        user, _ = await SignUser.get_or_create(
            user_id=session.id1,
            defaults={"user_console": user_console, "platform": session.platform},
        )
        new_log = await SignLog.filter(user_id=session.id1).first()
        file_name = f"{user}_sign_{datetime.now().date()}.png"
        if (
            user.sign_count != 0
            or (new_log and now > new_log.create_time)
            or file_name in os.listdir(SIGN_TODAY_CARD_PATH)
        ):
            user_console, _ = await UserConsole.get_or_create(user_id=session.id1)
            path = await get_card(user, nickname, -1, user_console.gold, "")
        else:
            path = await cls._handle_sign_in(user, nickname, session, is_view_card)
        return path

    @classmethod
    async def _handle_sign_in(
        cls,
        user: SignUser,
        nickname: str,
        session: EventSession,
        is_view_card: bool,
    ) -> Path:
        """签到处理

        参数:
            user: SignUser
            nickname: 用户昵称
            session: Session
            is_view_card: 是否展示卡片

        返回:
            Path: 卡片路径
        """
        impression_added = (secrets.randbelow(99) + 1) / 100
        rand = random.random()
        add_probability = float(user.add_probability)
        specify_probability = user.specify_probability
        if rand + add_probability > 0.97:
            impression_added *= 2
        elif rand < specify_probability:
            impression_added *= 2
        await SignUser.sign(user, impression_added, session.bot_id, session.platform)
        gold = random.randint(1, 100)
        gift = random_event(float(user.impression))
        if isinstance(gift, int):
            gold += gift
            await UserConsole.add_gold(
                user.user_id, gold + gift, "sign_in", session.platform
            )
            gift = f"额外金币 +{gift}"
        else:
            await UserConsole.add_gold(user.user_id, gold, "sign_in", session.platform)
            await UserConsole.add_props(user.user_id, gift, 1, session.platform)
            gift += " + 1"
        logger.info(
            f"签到成功. score: {user.impression:.2f} "
            f"(+{impression_added:.2f}).获取金币/道具: {gold}",
            "签到",
            session=session,
        )
        return await get_card(
            user,
            nickname,
            impression_added,
            gold,
            gift,
            rand + add_probability > 0.97 or rand < specify_probability,
            is_view_card,
        )
