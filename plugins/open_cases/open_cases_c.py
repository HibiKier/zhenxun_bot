from datetime import datetime, timedelta
from .config import *
from services.log import logger
from services.db_context import db
from .models.open_cases_user import OpenCasesUser
from models.sign_group_user import SignGroupUser
from utils.message_builder import image
import pypinyin
import random
from .utils import get_price
from .models.buff_prices import BuffPrice
from PIL import Image
from utils.image_utils import alpha2white_pil, BuildImage
from configs.path_config import IMAGE_PATH
import asyncio
from utils.utils import cn2py
from configs.config import Config


async def open_case(user_qq: int, group: int, case_name: str = "狂牙大行动") -> str:
    if case_name not in ["狂牙大行动", "突围大行动", "命悬一线", "裂空", "光谱"]:
        return "武器箱未收录"
    knifes_flag = False
    #          lan   zi   fen   hong   jin  price
    uplist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0]
    case = ""
    for i in pypinyin.pinyin(case_name, style=pypinyin.NORMAL):
        case += "".join(i)
    impression = (await SignGroupUser.ensure(user_qq, group)).impression
    rand = random.random()
    async with db.transaction():
        user = await OpenCasesUser.ensure(user_qq, group, for_update=True)
        # 一天次数上限
        if user.today_open_total == int(
            Config.get_config("open_cases", "INITIAL_OPEN_CASE_COUNT")
            + int(impression)
            / Config.get_config("open_cases", "EACH_IMPRESSION_ADD_COUNT")
        ):
            return _handle_is_MAX_COUNT()
        skin, mosun = get_color_quality(rand, case_name)
        # 调侃
        if skin[:2] == "军规":
            if skin.find("StatTrak") == -1:
                uplist[0] = 1
            else:
                uplist[1] = 1
            ridicule_result = random.choice(["这样看着才舒服", "是自己人，大伙把刀收好", "非常舒适~"])
        if skin[:2] == "受限":
            if skin.find("StatTrak") == -1:
                uplist[2] = 1
            else:
                uplist[3] = 1
            ridicule_result = random.choice(
                ["还行吧，勉强接受一下下", "居然不是蓝色，太假了", "运气-1-1-1-1-1..."]
            )
        if skin[:2] == "保密":
            if skin.find("StatTrak") == -1:
                uplist[4] = 1
            else:
                uplist[5] = 1
            ridicule_result = random.choice(
                ["开始不适....", "你妈妈买菜必涨价！涨三倍！", "你最近不适合出门，真的"]
            )
        if skin[:2] == "隐秘":
            if skin.find("StatTrak") == -1:
                uplist[6] = 1
            else:
                uplist[7] = 1
            ridicule_result = random.choice(
                ["已经非常不适", "好兄弟你开的什么箱子啊，一般箱子不是只有蓝色的吗", "开始拿阳寿开箱子了？"]
            )
        if skin[:2] == "罕见":
            knifes_flag = True
            if skin.find("StatTrak") == -1:
                uplist[8] = 1
            else:
                uplist[9] = 1
            ridicule_result = random.choice(
                ["你的好运我收到了，你可以去喂鲨鱼了", "最近该吃啥就迟点啥吧，哎，好好的一个人怎么就....哎", "众所周知，欧皇寿命极短."]
            )
        if skin.find("（") != -1:
            cskin = skin.split("（")
            skin = cskin[0].strip() + "（" + cskin[1].strip()
        skin = skin.split("|")[0].strip() + " | " + skin.split("|")[1].strip()
        # 价格
        if skin.find("无涂装") == -1:
            dbprice = await BuffPrice.ensure(skin[9:])
        else:
            dbprice = await BuffPrice.ensure(skin[9 : skin.rfind("(")].strip())
        if dbprice.skin_price != 0:
            price_result = dbprice.skin_price
            logger.info("数据库查询到价格: ", dbprice.skin_price)
            uplist[10] = dbprice.skin_price
        else:
            price = -1
            price_result = "未查询到"
            price_list, status = await get_price(skin[9:])
            if price_list not in ["访问超时! 请重试或稍后再试!", "访问失败！"]:
                for price_l in price_list[1:]:
                    pcp = price_l.split(":")
                    if pcp[0] == skin[9:]:
                        price = float(pcp[1].strip())
                        break
                if price != -1:
                    logger.info("存储入数据库---->", price)
                    uplist[10] = price
                    price_result = str(price)
                    await dbprice.update(
                        skin_price=price,
                        update_date=datetime.now(),
                    ).apply()
        # sp = skin.split("|")
        # cskin_word = sp[1][:sp[1].find("(") - 1].strip()
        if knifes_flag:
            await user.update(
                knifes_name=user.knifes_name
                + f"{case}||{skin.split(':')[1].strip()} 磨损：{str(mosun)[:11]}， 价格：{uplist[10]},"
            ).apply()
        cskin_word = skin.split(":")[1].replace("|", "-").replace("（StatTrak™）", "")
        cskin_word = cskin_word[: cskin_word.rfind("(")].strip()
        skin_name = cn2py(
            cskin_word.replace("|", "-").replace("（StatTrak™）", "").strip()
        )
        img = image(f"{skin_name}.png", "cases/" + case)
        #        if knifes_flag:
        #            await user.update(
        #                knifes_name=user.knifes_name + f"{skin} 磨损：{mosun}， 价格：{uplist[10]}"
        #            ).apply()
        if await update_user_total(user, uplist):
            logger.info(
                f"qq:{user_qq} 群:{group} 开启{case_name}武器箱 获得 {skin} 磨损：{mosun}， 价格：{uplist[10]}， 数据更新成功"
            )
        else:
            logger.warning(
                f"qq:{user_qq} 群:{group} 开启{case_name}武器箱 获得 {skin} 磨损：{mosun}， 价格：{uplist[10]}， 数据更新失败"
            )
        user = await OpenCasesUser.ensure(user_qq, group, for_update=True)
        over_count = int(
            Config.get_config("open_cases", "INITIAL_OPEN_CASE_COUNT")
            + int(impression)
            / Config.get_config("open_cases", "EACH_IMPRESSION_ADD_COUNT")
        ) - user.today_open_total
        return (
            f"开启{case_name}武器箱.\n剩余开箱次数：{over_count}.\n" + img + "\n" + f"皮肤:{skin}\n"
            f"磨损:{mosun:.9f}\n"
            f"价格:{price_result}\n"
            f"{ridicule_result}"
        )


async def open_shilian_case(user_qq: int, group: int, case_name: str, num: int = 10):
    user = await OpenCasesUser.ensure(user_qq, group, for_update=True)
    impression = (await SignGroupUser.ensure(user_qq, group)).impression
    max_count = int(
        Config.get_config("open_cases", "INITIAL_OPEN_CASE_COUNT")
        + int(impression) / Config.get_config("open_cases", "EACH_IMPRESSION_ADD_COUNT")
    )
    if user.today_open_total == max_count:
        return _handle_is_MAX_COUNT()
    if max_count - user.today_open_total < num:
        return (
            f"今天开箱次数不足{num}次噢，请单抽试试看（也许单抽运气更好？）"
            f"\n剩余开箱次数：{max_count - user.today_open_total}"
        )
    await user.update(
        total_count=user.total_count + num,
        spend_money=user.spend_money + 17 * num,
        today_open_total=user.today_open_total + num,
    ).apply()
    if num < 5:
        h = 270
    elif num % 5 == 0:
        h = 270 * int(num / 5)
    else:
        h = 270 * int(num / 5) + 270
    case = cn2py(case_name)
    #            lan    zi    fen  hong   jin
    # skin_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #          lan   zi   fen   hong   jin  price
    uplist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0]
    img_list = []
    name_list = ["蓝", "蓝(暗金)", "紫", "紫(暗金)", "粉", "粉(暗金)", "红", "红(暗金)", "金", "金(暗金)"]
    async with db.transaction():
        for _ in range(num):
            knifes_flag = False
            rand = random.random()
            skin, mosun = get_color_quality(rand, case_name)
            if skin[:2] == "军规":
                if skin.find("StatTrak") == -1:
                    uplist[0] += 1
                else:
                    uplist[1] += 1
            if skin[:2] == "受限":
                if skin.find("StatTrak") == -1:
                    uplist[2] += 1
                else:
                    uplist[3] += 1
            if skin[:2] == "保密":
                if skin.find("StatTrak") == -1:
                    uplist[4] += 1
                else:
                    uplist[5] += 1
            if skin[:2] == "隐秘":
                if skin.find("StatTrak") == -1:
                    uplist[6] += 1
                else:
                    uplist[7] += 1
            if skin[:2] == "罕见":
                knifes_flag = True
                if skin.find("StatTrak") == -1:
                    uplist[8] += 1
                else:
                    uplist[9] += 1
            if skin.find("（") != -1:
                cskin = skin.split("（")
                skin = cskin[0].strip() + "（" + cskin[1].strip()
            skin = skin.split("|")[0].strip() + " | " + skin.split("|")[1].strip()
            # 价格
            if skin.find("无涂装") == -1:
                dbprice = await BuffPrice.ensure(skin[9:])
            else:
                dbprice = await BuffPrice.ensure(skin[9 : skin.rfind("(")].strip())
            if dbprice.skin_price != 0:
                price_result = dbprice.skin_price
                uplist[10] += price_result
            else:
                price_result = "未查询到"
            if knifes_flag:
                await user.update(
                    knifes_name=user.knifes_name
                    + f"{case}||{skin.split(':')[1].strip()} 磨损：{str(mosun)[:11]}， 价格：{dbprice.skin_price},"
                ).apply()
            cskin_word = skin.split(":")[1].replace("|", "-").replace("（StatTrak™）", "")
            cskin_word = cskin_word[: cskin_word.rfind("(")].strip()
            skin_name = ""
            for i in pypinyin.pinyin(
                cskin_word.replace("|", "-").replace("（StatTrak™）", "").strip(),
                style=pypinyin.NORMAL,
            ):
                skin_name += "".join(i)
            # img = image(skin_name, "cases/" + case, "png")
            wImg = BuildImage(200, 270, 200, 200)
            wImg.paste(
                alpha2white_pil(
                    Image.open(IMAGE_PATH / "cases" / case / f"{skin_name}.png").resize(
                        (200, 200), Image.ANTIALIAS
                    )
                ),
                (0, 0),
            )
            wImg.text((5, 200), skin)
            wImg.text((5, 220), f"磨损：{str(mosun)[:9]}")
            wImg.text((5, 240), f"价格：{price_result}")
            img_list.append(wImg)
            logger.info(
                f"USER {user_qq} GROUP {group} 开启{case_name}武器箱 获得 {skin} 磨损：{mosun}， 价格：{uplist[10]}"
            )
        if await update_user_total(user, uplist, 0):
            logger.info(
                f"USER {user_qq} GROUP {group} 开启{case_name}武器箱 {num} 次， 数据更新成功"
            )
        else:
            logger.warning(
                f"USER {user_qq} GROUP {group} 开启{case_name}武器箱 {num} 次， 价格：{uplist[10]}， 数据更新失败"
            )
    # markImg = BuildImage(1000, h, 200, 270)
    # for img in img_list:
    #     markImg.paste(img)
    markImg = await asyncio.get_event_loop().run_in_executor(
        None, paste_markImg, h, img_list
    )
    over_count = max_count - user.today_open_total
    result = ""
    for i in range(len(name_list)):
        if uplist[i]:
            result += f"[{name_list[i]}：{uplist[i]}] "
    return (
        f"开启{case_name}武器箱\n剩余开箱次数：{over_count}\n"
        + image(b64=markImg.pic2bs4())
        + "\n"
        + result[:-1]
        + f"\n总获取金额：{uplist[-1]:.2f}\n总花费：{17 * num}"
    )


def paste_markImg(h: int, img_list: list):
    markImg = BuildImage(1000, h, 200, 270)
    for img in img_list:
        markImg.paste(img)
    return markImg


def _handle_is_MAX_COUNT() -> str:
    return f"今天已达开箱上限了喔，明天再来吧\n(提升好感度可以增加每日开箱数 #疯狂暗示)"


async def update_user_total(user: OpenCasesUser, up_list: list, num: int = 1) -> bool:
    try:
        await user.update(
            total_count=user.total_count + num,
            blue_count=user.blue_count + up_list[0],
            blue_st_count=user.blue_st_count + up_list[1],
            purple_count=user.purple_count + up_list[2],
            purple_st_count=user.purple_st_count + up_list[3],
            pink_count=user.pink_count + up_list[4],
            pink_st_count=user.pink_st_count + up_list[5],
            red_count=user.red_count + up_list[6],
            red_st_count=user.red_st_count + up_list[7],
            knife_count=user.knife_count + up_list[8],
            knife_st_count=user.knife_st_count + up_list[9],
            spend_money=user.spend_money + 17 * num,
            make_money=user.make_money + up_list[10],
            today_open_total=user.today_open_total + num,
            open_cases_time_last=datetime.now(),
        ).apply()
        return True
    except:
        return False


async def total_open_statistics(user_qq: int, group: int) -> str:
    async with db.transaction():
        user = await OpenCasesUser.ensure(user_qq, group, for_update=True)
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
            f"最后开箱日期：{(user.open_cases_time_last + timedelta(hours=8)).date()}"
        )


async def group_statistics(group: int):
    user_list = await OpenCasesUser.get_user_all(group)
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


async def my_knifes_name(user_id: int, group: int):
    knifes_name = (await OpenCasesUser.ensure(user_id, group)).knifes_name
    if knifes_name:
        knifes_list = knifes_name[:-1].split(",")
        length = len(knifes_list)
        if length < 5:
            h = 600
            w = length * 540
        elif length % 5 == 0:
            h = 600 * int(length / 5)
            w = 540 * 5
        else:
            h = 600 * int(length / 5) + 600
            w = 540 * 5
        A = await asyncio.get_event_loop().run_in_executor(
            None, _pst_my_knife, w, h, knifes_list
        )
        return image(b64=A.pic2bs4())
    else:
        return "您木有开出金色级别的皮肤喔"


def _pst_my_knife(w, h, knifes_list):
    A = BuildImage(w, h, 540, 600)
    for knife in knifes_list:
        case = knife.split("||")[0]
        knife = knife.split("||")[1]
        name = knife[: knife.find("(")].strip()
        itype = knife[knife.find("(") + 1 : knife.find(")")].strip()
        mosun = knife[knife.find("磨损：") + 3 : knife.rfind("价格：")].strip()
        if mosun[-1] == "," or mosun[-1] == "，":
            mosun = mosun[:-1]
        price = knife[knife.find("价格：") + 3 :]
        skin_name = ""
        for i in pypinyin.pinyin(
            name.replace("|", "-").replace("（StatTrak™）", "").strip(),
            style=pypinyin.NORMAL,
        ):
            skin_name += "".join(i)
        knife_img = BuildImage(470, 600, 470, 470, font_size=20)
        knife_img.paste(
            alpha2white_pil(
                Image.open(IMAGE_PATH / f"cases" / case / f"{skin_name}.png").resize(
                    (470, 470), Image.ANTIALIAS
                )
            ),
            (0, 0),
        )
        knife_img.text((5, 500), f"\t{name}({itype})")
        knife_img.text((5, 530), f"\t磨损：{mosun}")
        knife_img.text((5, 560), f"\t价格：{price}")
        A.paste(knife_img)
    return A


# G3SG1（StatTrak™） |  血腥迷彩 (战痕累累)
# G3SG1（StatTrak™） | 血腥迷彩 (战痕累累)
# G3SG1（StatTrak™） | 血腥迷彩 (战痕累累)
