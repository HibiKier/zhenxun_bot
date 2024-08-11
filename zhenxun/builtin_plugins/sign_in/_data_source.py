import random
import secrets
from datetime import datetime
from pathlib import Path

import pytz
from nonebot_plugin_session import EventSession

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
from .utils import get_card

ICON_PATH = IMAGE_PATH / "_icon"

PLATFORM_PATH = {
    "dodo": ICON_PATH / "dodo.png",
    "discord": ICON_PATH / "discord.png",
    "kaiheila": ICON_PATH / "kook.png",
    "qq": ICON_PATH / "qq.png",
}


class SignManage:

    @classmethod
    async def rank(
        cls, user_id: str, num: int, group_id: str | None = None
    ) -> BuildImage:
        """好感度排行

        参数:
            user_id: 用户id
            num: 排行榜数量
            group_id: 群组id

        返回:
            BuildImage: 构造图片
        """
        query = SignUser
        if group_id:
            user_list = await GroupInfoUser.filter(group_id=group_id).values_list(
                "user_id", flat=True
            )
            query = query.filter(user_id__in=user_list)
        all_list = (
            await query.annotate()
            .order_by("-impression")
            .values_list("user_id", flat=True)
        )
        index = all_list.index(user_id) + 1  # type: ignore
        user_list = await query.annotate().order_by("-impression").limit(num).all()
        user_id_list = [u.user_id for u in user_list]
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
                    user.sign_count,
                    (PLATFORM_PATH.get(user.platform), 30, 30),
                ]
            )
        if group_id:
            title = "好感度群组内排行"
            tip = f"你的排名在本群第 {index} 位哦!"
        else:
            title = "好感度全局排行"
            tip = f"你的排名在全局第 {index} 位哦!"
        return await ImageTemplate.table_page(title, tip, column_name, data_list)

    @classmethod
    async def sign(
        cls, session: EventSession, nickname: str, is_card_view: bool = False
    ) -> Path | None:
        """签到

        参数:
            session: Session
            nickname: 用户昵称
            is_card_view: 是否展示卡片

        返回:
            Path: 卡片路径
        """
        if not session.id1:
            return None
        now = datetime.now(pytz.timezone("Asia/Shanghai"))
        user_console = await UserConsole.get_user(session.id1, session.platform)
        user, _ = await SignUser.get_or_create(
            user_id=session.id1,
            defaults={"user_console": user_console, "platform": session.platform},
        )
        new_log = (
            await SignLog.filter(user_id=session.id1).order_by("-create_time").first()
        )
        log_time = None
        if new_log:
            log_time = new_log.create_time.astimezone(
                pytz.timezone("Asia/Shanghai")
            ).date()
        if not is_card_view:
            if not new_log or (log_time and log_time != now.date()):
                return await cls._handle_sign_in(user, nickname, session)
        return await get_card(
            user, nickname, -1, user_console.gold, "", is_card_view=is_card_view
        )

    @classmethod
    async def _handle_sign_in(
        cls,
        user: SignUser,
        nickname: str,
        session: EventSession,
    ) -> Path:
        """签到处理

        参数:
            user: SignUser
            nickname: 用户昵称
            session: Session

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
        )
