from datetime import timedelta, timezone

from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.services.log import logger
from zhenxun.utils.image_utils import BuildImage
from zhenxun.utils.utils import cn2py

from .config import COLOR2COLOR, COLOR2NAME
from .models.buff_skin import BuffSkin

BASE_PATH = IMAGE_PATH / "csgo_cases"

ICON_PATH = IMAGE_PATH / "_icon"


async def draw_card(skin: BuffSkin, rand: str) -> BuildImage:
    """构造抽取图片

    参数:
        skin (BuffSkin): BuffSkin
        rand (str): 磨损

    返回:
        BuildImage: BuildImage
    """
    name = skin.name + "-" + skin.skin_name + "-" + skin.abrasion
    file_path = BASE_PATH / cn2py(skin.case_name.split(",")[0]) / f"{cn2py(name)}.jpg"
    if not file_path.exists():
        logger.warning(f"皮肤图片: {name} 不存在", "开箱")
    skin_bk = BuildImage(
        460, 200, color=(25, 25, 25, 100), font_size=25, font="CJGaoDeGuo.otf"
    )
    if file_path.exists():
        skin_image = BuildImage(205, 153, background=file_path)
        await skin_bk.paste(skin_image, (10, 30))
    await skin_bk.line((220, 10, 220, 180))
    await skin_bk.text((10, 10), skin.name, (255, 255, 255))
    name_icon = BuildImage(20, 20, background=ICON_PATH / "name_white.png")
    await skin_bk.paste(name_icon, (240, 13))
    await skin_bk.text((265, 15), f"名称:", (255, 255, 255), font_size=20)
    await skin_bk.text(
        (310, 15),
        f"{skin.skin_name + ('(St)' if skin.is_stattrak else '')}",
        (255, 255, 255),
    )
    tone_icon = BuildImage(20, 20, background=ICON_PATH / "tone_white.png")
    await skin_bk.paste(tone_icon, (240, 45))
    await skin_bk.text((265, 45), "品质:", (255, 255, 255), font_size=20)
    await skin_bk.text((310, 45), COLOR2NAME[skin.color][:2], COLOR2COLOR[skin.color])
    type_icon = BuildImage(20, 20, background=ICON_PATH / "type_white.png")
    await skin_bk.paste(type_icon, (240, 73))
    await skin_bk.text((265, 75), "类型:", (255, 255, 255), font_size=20)
    await skin_bk.text((310, 75), skin.weapon_type, (255, 255, 255))
    price_icon = BuildImage(20, 20, background=ICON_PATH / "price_white.png")
    await skin_bk.paste(price_icon, (240, 103))
    await skin_bk.text((265, 105), "价格:", (255, 255, 255), font_size=20)
    await skin_bk.text((310, 105), str(skin.sell_min_price), (0, 255, 98))
    abrasion_icon = BuildImage(20, 20, background=ICON_PATH / "abrasion_white.png")
    await skin_bk.paste(abrasion_icon, (240, 133))
    await skin_bk.text((265, 135), "磨损:", (255, 255, 255), font_size=20)
    await skin_bk.text((310, 135), skin.abrasion, (255, 255, 255))
    await skin_bk.text((228, 165), f"({rand})", (255, 255, 255))
    return skin_bk


async def generate_skin(skin: BuffSkin, update_count: int) -> BuildImage | None:
    """构造皮肤图片

    参数:
        skin (BuffSkin): BuffSkin

    返回:
        BuildImage | None: 图片
    """
    name = skin.name + "-" + skin.skin_name + "-" + skin.abrasion
    file_path = BASE_PATH / cn2py(skin.case_name.split(",")[0]) / f"{cn2py(name)}.jpg"
    if not file_path.exists():
        logger.warning(f"皮肤图片: {name} 不存在", "查看武器箱")
    if skin.color == "CASE":
        case_bk = BuildImage(
            700, 200, color=(25, 25, 25, 100), font_size=25, font="CJGaoDeGuo.otf"
        )
        if file_path.exists():
            skin_img = BuildImage(200, 200, background=file_path)
            await case_bk.paste(skin_img, (10, 10))
        await case_bk.line((250, 10, 250, 190))
        await case_bk.line((280, 160, 660, 160))
        name_icon = BuildImage(30, 30, background=ICON_PATH / "box_white.png")
        await case_bk.paste(name_icon, (260, 25))
        await case_bk.text((295, 30), "名称:", (255, 255, 255))
        await case_bk.text((345, 30), skin.case_name, (255, 0, 38), font_size=30)

        type_icon = BuildImage(30, 30, background=ICON_PATH / "type_white.png")
        await case_bk.paste(type_icon, (260, 70))
        await case_bk.text((295, 75), "类型:", (255, 255, 255))
        await case_bk.text((345, 75), "武器箱", (0, 157, 255), font_size=30)

        price_icon = BuildImage(30, 30, background=ICON_PATH / "price_white.png")
        await case_bk.paste(price_icon, (260, 114))
        await case_bk.text((295, 120), "单价:", (255, 255, 255))
        await case_bk.text(
            (340, 120), str(skin.sell_min_price), (0, 255, 98), font_size=30
        )

        update_count_icon = BuildImage(
            40, 40, background=ICON_PATH / "reload_white.png"
        )
        await case_bk.paste(update_count_icon, (575, 10))
        await case_bk.text((625, 12), str(update_count), (255, 255, 255), font_size=45)

        num_icon = BuildImage(30, 30, background=ICON_PATH / "num_white.png")
        await case_bk.paste(num_icon, (455, 70))
        await case_bk.text((490, 75), "在售:", (255, 255, 255))
        await case_bk.text((535, 75), str(skin.sell_num), (144, 0, 255), font_size=30)

        want_buy_icon = BuildImage(30, 30, background=ICON_PATH / "want_buy_white.png")
        await case_bk.paste(want_buy_icon, (455, 114))
        await case_bk.text((490, 120), "求购:", (255, 255, 255))
        await case_bk.text((535, 120), str(skin.buy_num), (144, 0, 255), font_size=30)

        await case_bk.text((275, 165), "更新时间", (255, 255, 255), font_size=22)
        date = str(
            skin.update_time.replace(microsecond=0).astimezone(
                timezone(timedelta(hours=8))
            )
        ).split("+")[0]
        await case_bk.text(
            (350, 165),
            date,
            (255, 255, 255),
            font_size=30,
        )
        return case_bk
    else:
        skin_bk = BuildImage(
            235, 250, color=(25, 25, 25, 100), font_size=25, font="CJGaoDeGuo.otf"
        )
        if file_path.exists():
            skin_image = BuildImage(205, 153, background=file_path)
            await skin_bk.paste(skin_image, (10, 30))
        update_count_icon = BuildImage(
            35, 35, background=ICON_PATH / "reload_white.png"
        )
        await skin_bk.line((10, 180, 220, 180))
        await skin_bk.text((10, 10), skin.name, (255, 255, 255))
        await skin_bk.paste(update_count_icon, (140, 10))
        await skin_bk.text((175, 15), str(update_count), (255, 255, 255))
        await skin_bk.text((10, 185), f"{skin.skin_name}", (255, 255, 255), "width")
        await skin_bk.text((10, 218), "品质:", (255, 255, 255))
        await skin_bk.text(
            (55, 218), COLOR2NAME[skin.color][:2], COLOR2COLOR[skin.color]
        )
        await skin_bk.text((100, 218), "类型:", (255, 255, 255))
        await skin_bk.text((145, 218), skin.weapon_type, (255, 255, 255))
        return skin_bk
