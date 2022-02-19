from typing import Optional, Union
from nonebot.adapters.onebot.v11 import MessageSegment
from configs.config import Config
from asyncio.exceptions import TimeoutError
from services.log import logger
from configs.path_config import IMAGE_PATH
from utils.image_utils import BuildImage
from utils.http_utils import AsyncHttpx
from utils.utils import get_user_avatar
from utils.message_builder import image
from .._utils import get_ds
from .._models import Genshin
from io import BytesIO
from nonebot import Driver
import asyncio
import nonebot


driver: Driver = nonebot.get_driver()


memo_path = IMAGE_PATH / "genshin" / "genshin_memo"
memo_path.mkdir(exist_ok=True, parents=True)


@driver.on_startup
async def _():
    for name, url in zip(
        ["resin.png", "task.png", "resin_discount.png"],
        [
            "https://upload-bbs.mihoyo.com/upload/2021/09/29/8819732/54266243c7d15ba31690c8f5d63cc3c6_71491376413333325"
            "20.png?x-oss-process=image//resize,s_600/quality,q_80/auto-orient,0/interlace,1/format,png",
            "https://patchwiki.biligame.com/images/ys/thumb/c/cc/6k6kuj1kte6m1n7hexqfrn92z6h4yhh.png/60px-委托任务logo.png",
            "https://patchwiki.biligame.com/images/ys/d/d9/t1hv6wpucbwucgkhjntmzroh90nmcdv.png",
        ],
    ):
        file = memo_path / name
        if not file.exists():
            await AsyncHttpx.download_file(url, file)
            logger.info(f"已下载原神便签资源 -> {file}...")


async def get_user_memo(user_id: int, uid: int, uname: str) -> Optional[Union[str, MessageSegment]]:
    uid = str(uid)
    if uid[0] in ["1", "2"]:
        server_id = "cn_gf01"
    elif uid[0] == "5":
        server_id = "cn_qd01"
    else:
        return None
    return await parse_data_and_draw(user_id, uid, server_id, uname)


async def get_memo(uid: str, server_id: str) -> "Union[str, dict], int":
    try:
        req = await AsyncHttpx.get(
            url=f"https://api-takumi-record.mihoyo.com/game_record/app/genshin/api/dailyNote?server={server_id}&role_id={uid}",
            headers={
                "DS": get_ds(f"role_id={uid}&server={server_id}"),
                "x-rpc-app_version": Config.get_config("genshin", "mhyVersion"),
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.11.1",
                "x-rpc-client_type": Config.get_config("genshin", "client_type"),
                "Referer": "https://webstatic.mihoyo.com/",
                "Cookie": await Genshin.get_user_cookie(int(uid))
            },
        )
        data = req.json()
        if data["message"] == "OK":
            return data["data"], 200
        return data["message"], 999
    except TimeoutError:
        return "访问超时，请稍后再试", 997
    except Exception as e:
        logger.error(f"便签查询获取失败未知错误 {e}：{e}")
        return "发生了一些错误，请稍后再试", 998


def create_border(
    image_name: str, content: str, notice_text: str, value: str
) -> BuildImage:
    border = BuildImage(500, 100, color="#E0D9D1", font="HYWenHei-85W.ttf", font_size=20)
    text_bk = BuildImage(350, 96, color="#F5F1EB", font_size=23, font="HYWenHei-85W.ttf")
    _x = 70 if image_name == "resin.png" else 50
    _px = 10 if image_name == "resin.png" else 20
    text_bk.paste(
        BuildImage(_x, _x, background=memo_path / image_name),
        (_px, 0),
        True,
        center_type="by_height",
    )
    text_bk.text((87, 20), content)
    text_bk.paste(
        BuildImage(
            0,
            0,
            plain_text=notice_text,
            font_color=(203, 189, 175),
            font="HYWenHei-85W.ttf",
            font_size=17,
        ),
        (87, 50),
        True,
    )
    font_width, _ = border.getsize(value)
    border.text((350 + 76 - int(font_width / 2), 0), value, center_type="by_height")
    border.paste(text_bk, (2, 0), center_type="by_height")
    return border


async def parse_data_and_draw(
    user_id: int, uid: str, server_id: str, uname: str
) -> Union[str, MessageSegment]:
    data, code = await get_memo(uid, server_id)
    if code != 200:
        return data
    user_avatar = BytesIO(await get_user_avatar(user_id))
    for x in data["expeditions"]:
        file_name = x["avatar_side_icon"].split("_")[-1]
        role_avatar = memo_path / "role_avatar" / file_name
        if not role_avatar.exists():
            await AsyncHttpx.download_file(x["avatar_side_icon"], role_avatar)
    return await asyncio.get_event_loop().run_in_executor(
        None, _parse_data_and_draw, data, user_avatar, uid, uname
    )


def _parse_data_and_draw(
    data: dict, user_avatar: BytesIO, uid: int, uname: str
) -> Union[str, MessageSegment]:
    current_resin = data["current_resin"]  # 当前树脂
    max_resin = data["max_resin"]  # 最大树脂
    resin_recovery_time = data["resin_recovery_time"]  # 树脂全部回复时间
    finished_task_num = data["finished_task_num"]  # 完成的每日任务
    total_task_num = data["total_task_num"]  # 每日任务总数
    remain_resin_discount_num = data["remain_resin_discount_num"]  # 值得铭记的强敌总数
    resin_discount_num_limit = data["resin_discount_num_limit"]  # 剩余值得铭记的强敌
    current_expedition_num = data["current_expedition_num"]  # 当前挖矿人数
    max_expedition_num = data["max_expedition_num"]  # 每日挖矿最大人数
    expeditions = data["expeditions"]  # 挖矿详情

    minute, second = divmod(int(resin_recovery_time), 60)
    hour, minute = divmod(minute, 60)

    A = BuildImage(1030, 520, color="#f1e9e1", font_size=15, font="HYWenHei-85W.ttf")
    A.text((10, 15), "原神便笺 | Create By ZhenXun", (198, 186, 177))
    ava = BuildImage(100, 100, background=user_avatar)
    ava.circle()
    A.paste(ava, (40, 40), True)
    A.paste(
        BuildImage(0, 0, plain_text=uname, font_size=20, font="HYWenHei-85W.ttf"),
        (160, 62),
        True,
    )
    A.paste(
        BuildImage(
            0,
            0,
            plain_text=f"UID：{uid}",
            font_size=15,
            font="HYWenHei-85W.ttf",
            font_color=(21, 167, 89),
        ),
        (160, 92),
        True,
    )
    border = create_border(
        "resin.png",
        "原粹树脂",
        "将在{:0>2d}:{:0>2d}:{:0>2d}秒后全部恢复".format(hour, minute, second),
        f"{current_resin}/{max_resin}",
    )

    A.paste(border, (10, 155))
    border = create_border(
        "task.png",
        "每日委托",
        "今日委托已全部完成" if finished_task_num == total_task_num else "今日委托完成数量不足",
        f"{finished_task_num}/{total_task_num}",
    )
    A.paste(border, (10, 265))
    border = create_border(
        "resin_discount.png",
        "值得铭记的强敌",
        "本周剩余消耗减半次数",
        f"{remain_resin_discount_num}/{resin_discount_num_limit}",
    )
    A.paste(border, (10, 375))
    expeditions_border = BuildImage(
        470, 430, color="#E0D9D1", font="HYWenHei-85W.ttf", font_size=20
    )
    expeditions_text = BuildImage(
        466, 426, color="#F5F1EB", font_size=23, font="HYWenHei-85W.ttf"
    )
    expeditions_text.text(
        (5, 5), f"探索派遣限制{current_expedition_num}/{max_expedition_num}", (100, 100, 98)
    )
    h = 45
    for x in expeditions:
        _bk = BuildImage(400, 66, color="#ECE3D8", font="HYWenHei-85W.ttf", font_size=21)
        file_name = x["avatar_side_icon"].split("_")[-1]
        role_avatar = memo_path / "role_avatar" / file_name
        _ava_img = BuildImage(75, 75, background=role_avatar)
        _ava_img.circle()
        if x["status"] == "Finished":
            msg = "探索完成"
            font_color = (146, 188, 63)
            _circle_color = (146, 188, 63)
        else:
            minute, second = divmod(int(x["remained_time"]), 60)
            hour, minute = divmod(minute, 60)
            font_color = (193, 180, 167)
            msg = "还剩{:0>2d}小时{:0>2d}分钟{:0>2d}秒".format(hour, minute, second)
            _circle_color = "#DE9C58"

        _circle_bk = BuildImage(60, 60)
        _circle_bk.circle()
        a_circle = BuildImage(55, 55, color=_circle_color)
        a_circle.circle()
        b_circle = BuildImage(47, 47)
        b_circle.circle()
        a_circle.paste(b_circle, (4, 4), alpha=True)
        _circle_bk.paste(a_circle, (4, 4), alpha=True)

        _bk.paste(_circle_bk, (25, 0), True, center_type="by_height")
        _bk.paste(_ava_img, (19, -13), True)
        _bk.text((100, 0), msg, font_color, "by_height")
        _bk.circle_corner(20)

        expeditions_text.paste(_bk, (25, h), True)
        h += 75

    expeditions_border.paste(expeditions_text, center_type="center")

    A.paste(expeditions_border, (550, 45))

    return image(b64=A.pic2bs4())
