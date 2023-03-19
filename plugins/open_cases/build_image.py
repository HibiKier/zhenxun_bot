from datetime import timedelta, timezone
from typing import Optional

from configs.path_config import IMAGE_PATH
from services.log import logger
from utils.image_utils import BuildImage
from utils.utils import cn2py

from .config import COLOR2COLOR, COLOR2NAME
from .models.buff_skin import BuffSkin

BASE_PATH = IMAGE_PATH / "csgo_cases"

ICON_PATH = IMAGE_PATH / "_icon"


async def generate_skin(skin: BuffSkin, update_count: int) -> Optional[BuildImage]:
    """构造皮肤图片

    Args:
        skin (BuffSkin): BuffSkin

    Returns:
        Optional[BuildImage]: 图片
    """
    name = skin.name + "-" + skin.skin_name + "-" + skin.abrasion
    file_path = BASE_PATH / cn2py(skin.case_name) / f"{cn2py(name)}.jpg"
    if not file_path.exists():
        logger.warning(f"皮肤图片: {name} 不存在", "查看武器箱")
        return None
    if skin.color == "CASE":
        skin_img = BuildImage(200, 200, background=file_path)
        case_bk = BuildImage(
            700, 200, color=(25, 25, 25, 100), font_size=25, font="CJGaoDeGuo.otf"
        )
        await case_bk.apaste(skin_img, (10, 10), True)
        await case_bk.aline((250, 10, 250, 190))
        await case_bk.aline((280, 160, 660, 160))
        name_icon = BuildImage(30, 30, background=ICON_PATH / "box_white.png")
        await case_bk.apaste(name_icon, (260, 25), True)
        await case_bk.atext((295, 30), "名称:", (255, 255, 255))
        await case_bk.atext((345, 25), skin.case_name, (255, 0, 38), font_size=30)

        type_icon = BuildImage(30, 30, background=ICON_PATH / "type_white.png")
        await case_bk.apaste(type_icon, (260, 70), True)
        await case_bk.atext((295, 75), "类型:", (255, 255, 255))
        await case_bk.atext((345, 72), "武器箱", (0, 157, 255), font_size=30)

        price_icon = BuildImage(30, 30, background=ICON_PATH / "price_white.png")
        await case_bk.apaste(price_icon, (260, 114), True)
        await case_bk.atext((295, 120), "单价:", (255, 255, 255))
        await case_bk.atext(
            (340, 116), str(skin.sell_min_price), (0, 255, 98), font_size=30
        )

        update_count_icon = BuildImage(
            40, 40, background=ICON_PATH / "reload_white.png"
        )
        await case_bk.apaste(update_count_icon, (575, 10), True)
        await case_bk.atext((625, 12), str(update_count), (255, 255, 255), font_size=45)

        num_icon = BuildImage(30, 30, background=ICON_PATH / "num_white.png")
        await case_bk.apaste(num_icon, (455, 70), True)
        await case_bk.atext((490, 75), "在售:", (255, 255, 255))
        await case_bk.atext((535, 72), str(skin.sell_num), (144, 0, 255), font_size=30)

        want_buy_icon = BuildImage(30, 30, background=ICON_PATH / "want_buy_white.png")
        await case_bk.apaste(want_buy_icon, (455, 114), True)
        await case_bk.atext((490, 120), "求购:", (255, 255, 255))
        await case_bk.atext((535, 116), str(skin.buy_num), (144, 0, 255), font_size=30)

        await case_bk.atext((275, 165), "更新时间", (255, 255, 255), font_size=22)
        date = str(
            skin.update_time.replace(microsecond=0).astimezone(
                timezone(timedelta(hours=8))
            )
        ).split("+")[0]
        await case_bk.atext(
            (344, 170),
            date,
            (255, 255, 255),
            font_size=30,
        )
        return case_bk
    else:
        skin_bk = BuildImage(
            235, 250, color=(25, 25, 25, 100), font_size=25, font="CJGaoDeGuo.otf"
        )
        skin_image = BuildImage(205, 153, background=file_path)
        update_count_icon = BuildImage(
            35, 35, background=ICON_PATH / "reload_white.png"
        )
        await skin_bk.apaste(skin_image, (10, 30), alpha=True)
        await skin_bk.aline((10, 180, 220, 180))
        await skin_bk.atext((10, 10), skin.name, (255, 255, 255))
        await skin_bk.apaste(update_count_icon, (140, 10), True)
        await skin_bk.atext((175, 15), str(update_count), (255, 255, 255))
        await skin_bk.atext((10, 185), f"{skin.skin_name}", (255, 255, 255), "by_width")
        await skin_bk.atext((10, 218), "品质:", (255, 255, 255))
        await skin_bk.atext(
            (55, 218), COLOR2NAME[skin.color][:2], COLOR2COLOR[skin.color]
        )
        await skin_bk.atext((100, 218), "类型:", (255, 255, 255))
        await skin_bk.atext((145, 218), skin.weapon_type, (255, 255, 255))
        return skin_bk
