import asyncio
import os
import random
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import List, Optional

import nonebot
from nonebot import Driver
from nonebot.adapters.onebot.v11 import MessageSegment

from configs.config import NICKNAME, Config
from configs.path_config import IMAGE_PATH
from models.group_member_info import GroupInfoUser
from models.sign_group_user import SignGroupUser
from utils.image_utils import BuildImage
from utils.message_builder import image
from utils.utils import get_user_avatar

from .config import (
    SIGN_BACKGROUND_PATH,
    SIGN_BORDER_PATH,
    SIGN_RESOURCE_PATH,
    SIGN_TODAY_CARD_PATH,
    level2attitude,
    lik2level,
    lik2relation,
)

driver: Driver = nonebot.get_driver()


@driver.on_startup
async def init_image():
    SIGN_RESOURCE_PATH.mkdir(parents=True, exist_ok=True)
    SIGN_TODAY_CARD_PATH.mkdir(exist_ok=True, parents=True)
    if not await GroupInfoUser.get_or_none(user_qq=114514):
        await GroupInfoUser.create(
            user_qq=114514,
            group_id=114514,
            user_name="",
            uid=0,
        )
    generate_progress_bar_pic()
    clear_sign_data_pic()


async def get_card(
    user: SignGroupUser,
    nickname: str,
    add_impression: Optional[float],
    gold: Optional[int],
    gift: str,
    is_double: bool = False,
    is_card_view: bool = False,
) -> MessageSegment:
    user_id = user.user_qq
    date = datetime.now().date()
    _type = "view" if is_card_view else "sign"
    card_file = (
        Path(SIGN_TODAY_CARD_PATH) / f"{user_id}_{user.group_id}_{_type}_{date}.png"
    )
    if card_file.exists():
        return image(
            IMAGE_PATH
            / "sign"
            / "today_card"
            / f"{user_id}_{user.group_id}_{_type}_{date}.png"
        )
    else:
        if add_impression == -1:
            card_file = (
                Path(SIGN_TODAY_CARD_PATH)
                / f"{user_id}_{user.group_id}_view_{date}.png"
            )
            if card_file.exists():
                return image(
                    IMAGE_PATH
                    / "sign"
                    / "today_card"
                    / f"{user_id}_{user.group_id}_view_{date}.png"
                )
            is_card_view = True
        ava = BytesIO(await get_user_avatar(user_id))
        uid = await GroupInfoUser.get_group_member_uid(user.user_qq, user.group_id)
        impression_list = None
        if is_card_view:
            _, impression_list, _ = await SignGroupUser.get_all_impression(
                user.group_id
            )
        return await asyncio.get_event_loop().run_in_executor(
            None,
            _generate_card,
            user,
            nickname,
            user_id,
            add_impression,
            gold,
            gift,
            uid,
            ava,
            impression_list,
            is_double,
            is_card_view,
        )


def _generate_card(
    user: "SignGroupUser",
    nickname: str,
    user_id: int,
    impression: Optional[float],
    gold: Optional[int],
    gift: str,
    uid: str,
    ava_bytes: BytesIO,
    impression_list: List[float],
    is_double: bool = False,
    is_card_view: bool = False,
) -> MessageSegment:
    ava_bk = BuildImage(140, 140, is_alpha=True)
    ava_border = BuildImage(
        140,
        140,
        background=SIGN_BORDER_PATH / "ava_border_01.png",
    )
    ava = BuildImage(102, 102, background=ava_bytes)
    ava.circle()
    ava_bk.paste(ava, center_type="center")
    ava_bk.paste(ava_border, alpha=True, center_type="center")
    add_impression = impression
    impression = float(user.impression)
    info_img = BuildImage(250, 150, color=(255, 255, 255, 0), font_size=15)
    level, next_impression, previous_impression = get_level_and_next_impression(
        impression
    )
    interpolation = next_impression - impression
    if level == "9":
        level = "8"
        interpolation = 0
    info_img.text((0, 0), f"· 好感度等级：{level} [{lik2relation[level]}]")
    info_img.text((0, 20), f"· {NICKNAME}对你的态度：{level2attitude[level]}")
    info_img.text((0, 40), f"· 距离升级还差 {interpolation:.2f} 好感度")

    bar_bk = BuildImage(220, 20, background=SIGN_RESOURCE_PATH / "bar_white.png")
    bar = BuildImage(220, 20, background=SIGN_RESOURCE_PATH / "bar.png")
    ratio = 1 - (next_impression - user.impression) / (
        next_impression - previous_impression
    )
    bar.resize(w=int(bar.w * ratio) or 1, h=bar.h)
    bar_bk.paste(
        bar,
        alpha=True,
    )
    font_size = 30
    if "好感度双倍加持卡" in gift:
        font_size = 20
    gift_border = BuildImage(
        270,
        100,
        background=SIGN_BORDER_PATH / "gift_border_02.png",
        font_size=font_size,
    )
    gift_border.text((0, 0), gift, center_type="center")

    bk = BuildImage(
        876,
        424,
        background=SIGN_BACKGROUND_PATH
        / random.choice(os.listdir(SIGN_BACKGROUND_PATH)),
        font_size=25,
    )
    A = BuildImage(876, 274, background=SIGN_RESOURCE_PATH / "white.png")
    line = BuildImage(2, 180, color="black")
    A.transparent(2)
    A.paste(ava_bk, (25, 80), True)
    A.paste(line, (200, 70))

    nickname_img = BuildImage(
        0,
        0,
        plain_text=nickname,
        color=(255, 255, 255, 0),
        font_size=50,
        font_color=(255, 255, 255),
    )
    if uid:
        uid = f"{uid}".rjust(12, "0")
        uid = uid[:4] + " " + uid[4:8] + " " + uid[8:]
    else:
        uid = "XXXX XXXX XXXX"
    uid_img = BuildImage(
        0,
        0,
        plain_text=f"UID: {uid}",
        color=(255, 255, 255, 0),
        font_size=30,
        font_color=(255, 255, 255),
    )
    sign_day_img = BuildImage(
        0,
        0,
        plain_text=f"{user.checkin_count}",
        color=(255, 255, 255, 0),
        font_size=40,
        font_color=(211, 64, 33),
    )
    lik_text1_img = BuildImage(
        0, 0, plain_text="当前", color=(255, 255, 255, 0), font_size=20
    )
    lik_text2_img = BuildImage(
        0,
        0,
        plain_text=f"好感度：{user.impression:.2f}",
        color=(255, 255, 255, 0),
        font_size=30,
    )
    watermark = BuildImage(
        0,
        0,
        plain_text=f"{NICKNAME}@{datetime.now().year}",
        color=(255, 255, 255, 0),
        font_size=15,
        font_color=(155, 155, 155),
    )
    today_data = BuildImage(300, 300, color=(255, 255, 255, 0), font_size=20)
    if is_card_view:
        today_sign_text_img = BuildImage(
            0, 0, plain_text="", color=(255, 255, 255, 0), font_size=30
        )
        if impression_list:
            impression_list.sort(reverse=True)
            index = impression_list.index(impression)
            rank_img = BuildImage(
                0,
                0,
                plain_text=f"* 此群好感排名第 {index + 1} 位",
                color=(255, 255, 255, 0),
                font_size=30,
            )
            A.paste(rank_img, ((A.w - rank_img.w - 10), 20), True)
        today_data.text(
            (0, 0),
            f"上次签到日期：{'从未' if user.checkin_time_last == datetime.min else user.checkin_time_last.date()}",
        )
        today_data.text((0, 25), f"总金币：{gold}")
        default_setu_prob = (
            Config.get_config("send_setu", "INITIAL_SETU_PROBABILITY") * 100  # type: ignore
        )
        today_data.text(
            (0, 50),
            f"色图概率：{(default_setu_prob + float(user.impression) if user.impression < 100 else 100):.2f}%",
        )
        today_data.text((0, 75), f"开箱次数：{(20 + int(user.impression / 3))}")
        _type = "view"
    else:
        A.paste(gift_border, (570, 140), True)
        today_sign_text_img = BuildImage(
            0, 0, plain_text="今日签到", color=(255, 255, 255, 0), font_size=30
        )
        if is_double:
            today_data.text((0, 0), f"好感度 + {add_impression / 2:.2f} × 2")
        else:
            today_data.text((0, 0), f"好感度 + {add_impression:.2f}")
        today_data.text((0, 25), f"金币 + {gold}")
        _type = "sign"
    current_date = datetime.now()
    current_datetime_str = current_date.strftime("%Y-%m-%d %a %H:%M:%S")
    data = current_date.date()
    data_img = BuildImage(
        0,
        0,
        plain_text=f"时间：{current_datetime_str}",
        color=(255, 255, 255, 0),
        font_size=20,
    )
    bk.paste(nickname_img, (30, 15), True)
    bk.paste(uid_img, (30, 85), True)
    bk.paste(A, (0, 150), alpha=True)
    bk.text((30, 167), "Accumulative check-in for")
    _x = bk.getsize("Accumulative check-in for")[0] + sign_day_img.w + 45
    bk.paste(sign_day_img, (346, 158), True)
    bk.text((_x, 167), "days")
    bk.paste(data_img, (220, 370), True)
    bk.paste(lik_text1_img, (220, 240), True)
    bk.paste(lik_text2_img, (262, 234), True)
    bk.paste(bar_bk, (225, 275), True)
    bk.paste(info_img, (220, 305), True)
    bk.paste(today_sign_text_img, (550, 180), True)
    bk.paste(today_data, (580, 220), True)
    bk.paste(watermark, (15, 400), True)
    bk.save(SIGN_TODAY_CARD_PATH / f"{user_id}_{user.group_id}_{_type}_{data}.png")
    return image(
        IMAGE_PATH
        / "sign"
        / "today_card"
        / f"{user_id}_{user.group_id}_{_type}_{data}.png"
    )


def generate_progress_bar_pic():
    bg_2 = (254, 1, 254)
    bg_1 = (0, 245, 246)

    bk = BuildImage(1000, 50, is_alpha=True)
    img_x = BuildImage(50, 50, color=bg_2)
    img_x.circle()
    img_x.crop((25, 0, 50, 50))
    img_y = BuildImage(50, 50, color=bg_1)
    img_y.circle()
    img_y.crop((0, 0, 25, 50))
    A = BuildImage(950, 50)
    width, height = A.size

    step_r = (bg_2[0] - bg_1[0]) / width
    step_g = (bg_2[1] - bg_1[1]) / width
    step_b = (bg_2[2] - bg_1[2]) / width

    for y in range(0, width):
        bg_r = round(bg_1[0] + step_r * y)
        bg_g = round(bg_1[1] + step_g * y)
        bg_b = round(bg_1[2] + step_b * y)
        for x in range(0, height):
            A.point((y, x), fill=(bg_r, bg_g, bg_b))
    bk.paste(img_y, (0, 0), True)
    bk.paste(A, (25, 0))
    bk.paste(img_x, (975, 0), True)
    bk.save(SIGN_RESOURCE_PATH / "bar.png")

    A = BuildImage(950, 50)
    bk = BuildImage(1000, 50, is_alpha=True)
    img_x = BuildImage(50, 50)
    img_x.circle()
    img_x.crop((25, 0, 50, 50))
    img_y = BuildImage(50, 50)
    img_y.circle()
    img_y.crop((0, 0, 25, 50))
    bk.paste(img_y, (0, 0), True)
    bk.paste(A, (25, 0))
    bk.paste(img_x, (975, 0), True)
    bk.save(SIGN_RESOURCE_PATH / "bar_white.png")


def get_level_and_next_impression(impression: float):
    if impression == 0:
        return lik2level[10], 10, 0
    keys = list(lik2level.keys())
    for i in range(len(keys)):
        if impression > keys[i]:
            return lik2level[keys[i]], keys[i - 1], keys[i]
    return lik2level[10], 10, 0


def clear_sign_data_pic():
    date = datetime.now().date()
    for file in os.listdir(SIGN_TODAY_CARD_PATH):
        if str(date) not in file:
            os.remove(SIGN_TODAY_CARD_PATH / file)
