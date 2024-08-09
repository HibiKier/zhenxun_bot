import asyncio
import random
import re
from datetime import datetime

from nonebot_plugin_alconna import UniMessage
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.models.sign_user import SignUser
from zhenxun.services.log import logger
from zhenxun.utils.image_utils import BuildImage
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.utils import cn2py

from .build_image import draw_card
from .config import *
from .models.open_cases_log import OpenCasesLog
from .models.open_cases_user import OpenCasesUser
from .utils import CaseManager, update_skin_data

RESULT_MESSAGE = {
    "BLUE": ["这样看着才舒服", "是自己人，大伙把刀收好", "非常舒适~"],
    "PURPLE": ["还行吧，勉强接受一下下", "居然不是蓝色，太假了", "运气-1-1-1-1-1..."],
    "PINK": ["开始不适....", "你妈妈买菜必涨价！涨三倍！", "你最近不适合出门，真的"],
    "RED": [
        "已经非常不适",
        "好兄弟你开的什么箱子啊，一般箱子不是只有蓝色的吗",
        "开始拿阳寿开箱子了？",
    ],
    "KNIFE": [
        "你的好运我收到了，你可以去喂鲨鱼了",
        "最近该吃啥就迟点啥吧，哎，好好的一个人怎么就....哎",
        "众所周知，欧皇寿命极短.",
    ],
}

COLOR2NAME = {
    "BLUE": "军规",
    "PURPLE": "受限",
    "PINK": "保密",
    "RED": "隐秘",
    "KNIFE": "罕见",
}

COLOR2CN = {"BLUE": "蓝", "PURPLE": "紫", "PINK": "粉", "RED": "红", "KNIFE": "金"}


def add_count(user: OpenCasesUser, skin: BuffSkin, case_price: float):
    if skin.color == "BLUE":
        if skin.is_stattrak:
            user.blue_st_count += 1
        else:
            user.blue_count += 1
    elif skin.color == "PURPLE":
        if skin.is_stattrak:
            user.purple_st_count += 1
        else:
            user.purple_count += 1
    elif skin.color == "PINK":
        if skin.is_stattrak:
            user.pink_st_count += 1
        else:
            user.pink_count += 1
    elif skin.color == "RED":
        if skin.is_stattrak:
            user.red_st_count += 1
        else:
            user.red_count += 1
    elif skin.color == "KNIFE":
        if skin.is_stattrak:
            user.knife_st_count += 1
        else:
            user.knife_count += 1
    user.make_money += skin.sell_min_price
    user.spend_money += int(17 + case_price)


async def get_user_max_count(user_id: str) -> int:
    """获取用户每日最大开箱次数

    参数:
        user_id: 用户id

    返回:
        int: 最大开箱次数
    """
    user, _ = await SignUser.get_or_create(user_id=user_id)
    impression = int(user.impression)
    initial_open_case_count = Config.get_config("open_cases", "INITIAL_OPEN_CASE_COUNT")
    each_impression_add_count = Config.get_config(
        "open_cases", "EACH_IMPRESSION_ADD_COUNT"
    )
    return int(initial_open_case_count + impression / each_impression_add_count)  # type: ignore


async def open_case(
    user_id: str, group_id: str, case_name: str | None, session: EventSession
) -> UniMessage:
    """开箱

    参数:
        user_id: 用户id
        group_id : 群号
        case_name: 武器箱名称. Defaults to "狂牙大行动".
        session: EventSession

    返回:
        Union[str, Message]: 回复消息
    """
    user_id = str(user_id)
    group_id = str(group_id)
    if not CaseManager.CURRENT_CASES:
        return MessageUtils.build_message("未收录任何武器箱")
    if not case_name:
        case_name = random.choice(CaseManager.CURRENT_CASES)  # type: ignore
    if case_name not in CaseManager.CURRENT_CASES:
        return "武器箱未收录, 当前可用武器箱:\n" + ", ".join(CaseManager.CURRENT_CASES)  # type: ignore
    logger.debug(
        f"尝试开启武器箱: {case_name}", "开箱", session=user_id, group_id=group_id
    )
    case = cn2py(case_name)  # type: ignore
    user = await OpenCasesUser.get_or_none(user_id=user_id, group_id=group_id)
    if not user:
        user = await OpenCasesUser.create(
            user_id=user_id, group_id=group_id, open_cases_time_last=datetime.now()
        )
    max_count = await get_user_max_count(user_id)
    # 一天次数上限
    if user.today_open_total >= max_count:
        return MessageUtils.build_message(
            f"今天已达开箱上限了喔，明天再来吧\n(提升好感度可以增加每日开箱数 #疯狂暗示)"
        )
    skin_list = await random_skin(1, case_name)  # type: ignore
    if not skin_list:
        return MessageUtils.build_message("未抽取到任何皮肤")
    skin, rand = skin_list[0]
    rand = str(rand)[:11]
    case_price = 0
    if case_skin := await BuffSkin.get_or_none(case_name=case_name, color="CASE"):
        case_price = case_skin.sell_min_price
    user.today_open_total += 1
    user.total_count += 1
    user.open_cases_time_last = datetime.now()
    await user.save(
        update_fields=["today_open_total", "total_count", "open_cases_time_last"]
    )
    add_count(user, skin, case_price)
    ridicule_result = random.choice(RESULT_MESSAGE[skin.color])
    price_result = skin.sell_min_price
    name = skin.name + "-" + skin.skin_name + "-" + skin.abrasion
    img_path = IMAGE_PATH / "csgo_cases" / case / f"{cn2py(name)}.jpg"
    logger.info(
        f"开启{case_name}武器箱获得 {skin.name}{'（StatTrak™）' if skin.is_stattrak else ''} | {skin.skin_name} ({skin.abrasion}) 磨损: [{rand}] 价格: {skin.sell_min_price}",
        "开箱",
        session=session,
    )
    await user.save()
    await OpenCasesLog.create(
        user_id=user_id,
        group_id=group_id,
        case_name=case_name,
        name=skin.name,
        skin_name=skin.skin_name,
        is_stattrak=skin.is_stattrak,
        abrasion=skin.abrasion,
        color=skin.color,
        price=skin.sell_min_price,
        abrasion_value=rand,
        create_time=datetime.now(),
    )
    logger.debug(f"添加 1 条开箱日志", "开箱", session=session)
    over_count = max_count - user.today_open_total
    img = await draw_card(skin, rand)
    return MessageUtils.build_message(
        [
            f"开启{case_name}武器箱.\n剩余开箱次数:{over_count}.\n",
            img,
            f"\n箱子单价:{case_price}\n花费:{17 + case_price:.2f}\n:{ridicule_result}",
        ]
    )


async def open_multiple_case(
    user_id: str,
    group_id: str,
    case_name: str | None,
    num: int = 10,
    session: EventSession | None = None,
) -> UniMessage:
    """多连开箱

    参数:
        user_id (int): 用户id
        group_id (int): 群号
        case_name (str): 箱子名称
        num (int, optional): 数量. Defaults to 10.
        session: EventSession

    返回:
        _type_: _description_
    """
    user_id = str(user_id)
    group_id = str(group_id)
    if not CaseManager.CURRENT_CASES:
        return MessageUtils.build_message("未收录任何武器箱")
    if not case_name:
        case_name = random.choice(CaseManager.CURRENT_CASES)  # type: ignore
    if case_name not in CaseManager.CURRENT_CASES:
        return MessageUtils.build_message(
            "武器箱未收录, 当前可用武器箱:\n" + ", ".join(CaseManager.CURRENT_CASES)
        )
    user, _ = await OpenCasesUser.get_or_create(
        user_id=user_id,
        group_id=group_id,
        defaults={"open_cases_time_last": datetime.now()},
    )
    max_count = await get_user_max_count(user_id)
    if user.today_open_total >= max_count:
        return MessageUtils.build_message(
            f"今天已达开箱上限了喔，明天再来吧\n(提升好感度可以增加每日开箱数 #疯狂暗示)"
        )
    if max_count - user.today_open_total < num:
        return MessageUtils.build_message(
            f"今天开箱次数不足{num}次噢，请单抽试试看（也许单抽运气更好？）"
            f"\n剩余开箱次数:{max_count - user.today_open_total}"
        )
    logger.debug(f"尝试开启武器箱: {case_name}", "开箱", session=session)
    case = cn2py(case_name)  # type: ignore
    skin_count = {}
    img_list = []
    skin_list = await random_skin(num, case_name)  # type: ignore
    if not skin_list:
        return MessageUtils.build_message("未抽取到任何皮肤...")
    total_price = 0
    log_list = []
    now = datetime.now()
    user.today_open_total += num
    user.total_count += num
    user.open_cases_time_last = datetime.now()
    await user.save(
        update_fields=["today_open_total", "total_count", "open_cases_time_last"]
    )
    case_price = 0
    if case_skin := await BuffSkin.get_or_none(case_name=case_name, color="CASE"):
        case_price = case_skin.sell_min_price
    img_w, img_h = 0, 0
    for skin, rand in skin_list:
        img = await draw_card(skin, str(rand)[:11])
        img_w, img_h = img.size
        total_price += skin.sell_min_price
        color_name = COLOR2CN[skin.color]
        if not skin_count.get(color_name):
            skin_count[color_name] = 0
        skin_count[color_name] += 1
        add_count(user, skin, case_price)
        img_list.append(img)
        logger.info(
            f"开启{case_name}武器箱获得 {skin.name}{'（StatTrak™）' if skin.is_stattrak else ''} | {skin.skin_name} ({skin.abrasion}) 磨损: [{rand:.11f}] 价格: {skin.sell_min_price}",
            "开箱",
            session=session,
        )
        log_list.append(
            OpenCasesLog(
                user_id=user_id,
                group_id=group_id,
                case_name=case_name,
                name=skin.name,
                skin_name=skin.skin_name,
                is_stattrak=skin.is_stattrak,
                abrasion=skin.abrasion,
                color=skin.color,
                price=skin.sell_min_price,
                abrasion_value=rand,
                create_time=now,
            )
        )
    await user.save()
    if log_list:
        await OpenCasesLog.bulk_create(log_list, 10)
        logger.debug(f"添加 {len(log_list)} 条开箱日志", "开箱", session=session)
    img_w += 10
    img_h += 10
    w = img_w * 5
    if num < 5:
        h = img_h - 10
        w = img_w * num
    elif not num % 5:
        h = img_h * int(num / 5)
    else:
        h = img_h * int(num / 5) + img_h
    mark_image = BuildImage(w - 10, h - 10, color=(255, 255, 255))
    mark_image = await mark_image.auto_paste(img_list, 5, padding=20)
    over_count = max_count - user.today_open_total
    result = ""
    for color_name in skin_count:
        result += f"[{color_name}:{skin_count[color_name]}] "
    return MessageUtils.build_message(
        [
            f"开启{case_name}武器箱\n剩余开箱次数：{over_count}\n",
            mark_image,
            f"\n{result[:-1]}\n箱子单价：{case_price}\n总获取金额：{total_price:.2f}\n总花费：{(17 + case_price) * num:.2f}",
        ]
    )


async def total_open_statistics(user_id: str, group_id: str) -> str:
    user, _ = await OpenCasesUser.get_or_create(user_id=user_id, group_id=group_id)
    return (
        f"开箱总数：{user.total_count}\n"
        f"今日开箱：{user.today_open_total}\n"
        f"蓝色军规：{user.blue_count}\n"
        f"蓝色暗金：{user.blue_st_count}\n"
        f"紫色受限：{user.purple_count}\n"
        f"紫色暗金：{user.purple_st_count}\n"
        f"粉色保密：{user.pink_count}\n"
        f"粉色暗金：{user.pink_st_count}\n"
        f"红色隐秘：{user.red_count}\n"
        f"红色暗金：{user.red_st_count}\n"
        f"金色罕见：{user.knife_count}\n"
        f"金色暗金：{user.knife_st_count}\n"
        f"花费金额：{user.spend_money}\n"
        f"获取金额：{user.make_money:.2f}\n"
        f"最后开箱日期：{user.open_cases_time_last.date()}"
    )


async def group_statistics(group_id: str):
    user_list = await OpenCasesUser.filter(group_id=str(group_id)).all()
    #          lan   zi   fen   hong   jin  pricei
    uplist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0]
    for user in user_list:
        uplist[0] += user.blue_count
        uplist[1] += user.blue_st_count
        uplist[2] += user.purple_count
        uplist[3] += user.purple_st_count
        uplist[4] += user.pink_count
        uplist[5] += user.pink_st_count
        uplist[6] += user.red_count
        uplist[7] += user.red_st_count
        uplist[8] += user.knife_count
        uplist[9] += user.knife_st_count
        uplist[10] += user.make_money
        uplist[11] += user.total_count
        uplist[12] += user.today_open_total
    return (
        f"群开箱总数：{uplist[11]}\n"
        f"群今日开箱：{uplist[12]}\n"
        f"蓝色军规：{uplist[0]}\n"
        f"蓝色暗金：{uplist[1]}\n"
        f"紫色受限：{uplist[2]}\n"
        f"紫色暗金：{uplist[3]}\n"
        f"粉色保密：{uplist[4]}\n"
        f"粉色暗金：{uplist[5]}\n"
        f"红色隐秘：{uplist[6]}\n"
        f"红色暗金：{uplist[7]}\n"
        f"金色罕见：{uplist[8]}\n"
        f"金色暗金：{uplist[9]}\n"
        f"花费金额：{uplist[11] * 17}\n"
        f"获取金额：{uplist[10]:.2f}"
    )


async def get_my_knifes(user_id: str, group_id: str) -> UniMessage:
    """获取我的金色

    参数:
        user_id (str): 用户id
        group_id (str): 群号

    返回:
        MessageFactory: 回复消息或图片
    """
    data_list = await get_old_knife(str(user_id), str(group_id))
    data_list += await OpenCasesLog.filter(
        user_id=user_id, group_id=group_id, color="KNIFE"
    ).all()
    if not data_list:
        return MessageUtils.build_message("您木有开出金色级别的皮肤喔...")
    length = len(data_list)
    if length < 5:
        h = 600
        w = length * 540
    elif length % 5 == 0:
        h = 600 * int(length / 5)
        w = 540 * 5
    else:
        h = 600 * int(length / 5) + 600
        w = 540 * 5
    A = BuildImage(w, h)
    image_list = []
    for skin in data_list:
        name = skin.name + "-" + skin.skin_name + "-" + skin.abrasion
        img_path = (
            IMAGE_PATH / "csgo_cases" / cn2py(skin.case_name) / f"{cn2py(name)}.jpg"
        )
        knife_img = BuildImage(470, 600, font_size=20)
        await knife_img.paste(
            BuildImage(470, 470, background=img_path if img_path.exists() else None),
            (0, 0),
        )
        await knife_img.text(
            (5, 500), f"\t{skin.name}|{skin.skin_name}({skin.abrasion})"
        )
        await knife_img.text((5, 530), f"\t磨损：{skin.abrasion_value}")
        await knife_img.text((5, 560), f"\t价格：{skin.price}")
        image_list.append(knife_img)
    A = await A.auto_paste(image_list, 5)
    return MessageUtils.build_message(A)


async def get_old_knife(user_id: str, group_id: str) -> list[OpenCasesLog]:
    """获取旧数据字段

    参数:
        user_id (str): 用户id
        group_id (str): 群号

    返回:
        list[OpenCasesLog]: 旧数据兼容
    """
    user, _ = await OpenCasesUser.get_or_create(user_id=user_id, group_id=group_id)
    knifes_name = user.knifes_name
    data_list = []
    if knifes_name:
        knifes_list = knifes_name[:-1].split(",")
        for knife in knifes_list:
            try:
                if r := re.search(
                    "(.*)\|\|(.*) \| (.*)\((.*)\) 磨损：(.*)， 价格：(.*)", knife
                ):
                    case_name_py = r.group(1)
                    name = r.group(2)
                    skin_name = r.group(3)
                    abrasion = r.group(4)
                    abrasion_value = r.group(5)
                    price = r.group(6)
                    name = name.replace("（StatTrak™）", "")
                    data_list.append(
                        OpenCasesLog(
                            user_id=user_id,
                            group_id=group_id,
                            name=name.strip(),
                            case_name=case_name_py.strip(),
                            skin_name=skin_name.strip(),
                            abrasion=abrasion.strip(),
                            abrasion_value=abrasion_value,
                            price=price,
                        )
                    )
            except Exception as e:
                logger.error(
                    f"获取兼容旧数据错误: {knife}",
                    "我的金色",
                    session=user_id,
                    group_id=group_id,
                    e=e,
                )
    return data_list


async def auto_update():
    """自动更新武器箱"""
    if case_list := Config.get_config("open_cases", "DAILY_UPDATE"):
        logger.debug("尝试自动更新武器箱", "更新武器箱")
        if "ALL" in case_list:
            case_list = CASE2ID.keys()
        logger.debug(f"预计自动更新武器箱 {len(case_list)} 个", "更新武器箱")
        for case_name in case_list:
            logger.debug(f"开始自动更新武器箱: {case_name}", "更新武器箱")
            try:
                await update_skin_data(case_name)
                rand = random.randint(300, 500)
                logger.info(
                    f"成功自动更新武器箱: {case_name}, 将在 {rand} 秒后再次更新下一武器箱",
                    "更新武器箱",
                )
                await asyncio.sleep(rand)
            except Exception as e:
                logger.error(f"自动更新武器箱: {case_name}", e=e)
