from typing import Dict, List, Optional

from models.bag_user import BagUser
from models.goods_info import GoodsInfo
from utils.image_utils import BuildImage
from configs.path_config import IMAGE_PATH


icon_path = IMAGE_PATH / "shop_icon"


async def create_bag_image(props: Dict[str, int]):
    """
    说明:
        创建背包道具图片
    参数:
        :param props: 道具仓库字典
    """
    goods_list = await GoodsInfo.get_all_goods()
    active_props = await _init_prop(props, [x for x in goods_list if not x.is_passive])
    passive_props = await _init_prop(props, [x for x in goods_list if x.is_passive])
    active_w = 0
    active_h = 0
    passive_w = 0
    passive_h = 0
    if active_props:
        img = BuildImage(
            active_props.w,
            active_props.h + 70,
            font="CJGaoDeGuo.otf",
            font_size=30,
            color="#f9f6f2",
        )
        await img.apaste(active_props, (0, 70))
        await img.atext((0, 30), "主动道具")
        active_props = img
        active_w = img.w
        active_h = img.h
    if passive_props:
        img = BuildImage(
            passive_props.w,
            passive_props.h + 70,
            font="CJGaoDeGuo.otf",
            font_size=30,
            color="#f9f6f2",
        )
        await img.apaste(passive_props, (0, 70))
        await img.atext((0, 30), "被动道具")
        passive_props = img
        passive_w = img.w
        passive_h = img.h
    A = BuildImage(
        active_w + passive_w + 100,
        max(active_h, passive_h) + 60,
        font="CJGaoDeGuo.otf",
        font_size=30,
        color="#f9f6f2",
    )
    curr_w = 50
    if active_props:
        await A.apaste(active_props, (curr_w, 0))
        curr_w += active_props.w + 10
    if passive_props:
        await A.apaste(passive_props, (curr_w, 0))
    if active_props and passive_props:
        await A.aline(
            (active_props.w + 45, 70, active_props.w + 45, A.h - 20), fill=(0, 0, 0)
        )
    return A.pic2bs4()


async def _init_prop(
    props: Dict[str, int], _props: List[GoodsInfo]
) -> Optional[BuildImage]:
    """
    说明:
        构造道具列表图片
    参数:
        :param props: 道具仓库字典
        :param _props: 道具列表
    """
    active_name = [x.goods_name for x in _props]
    name_list = [x for x in props.keys() if x in active_name]
    if not name_list:
        return None
    temp_img = BuildImage(0, 0, font_size=20)
    image_list = []
    num_list = []
    for i, name in enumerate(name_list):
        img = BuildImage(
            temp_img.getsize(name)[0] + 50,
            30,
            font="msyh.ttf",
            font_size=20,
            color="#f9f6f2",
        )
        await img.atext((30, 5), f"{i + 1}.{name}")
        goods = [x for x in _props if x.goods_name == name][0]
        if goods.icon and (icon_path / goods.icon).exists():
            icon = BuildImage(30, 30, background=icon_path / goods.icon)
            await img.apaste(icon, alpha=True)
        image_list.append(img)
        num_list.append(
            BuildImage(
                30, 30, font_size=20, font="msyh.ttf", plain_text=f"×{props[name]}"
            )
        )
    max_w = 0
    num_max_w = 0
    h = 0
    for img, num in zip(image_list, num_list):
        h += img.h
        max_w = max_w if max_w > img.w else img.w
        num_max_w = num_max_w if num_max_w > num.w else num.w
    A = BuildImage(max_w + num_max_w + 30, h, color="#f9f6f2")
    curr_h = 0
    for img, num in zip(image_list, num_list):
        await A.apaste(img, (0, curr_h))
        await A.apaste(num, (max_w + 20, curr_h + 5), True)
        curr_h += img.h
    return A
