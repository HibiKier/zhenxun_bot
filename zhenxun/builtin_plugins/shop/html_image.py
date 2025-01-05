import random
import time

from nonebot_plugin_htmlrender import template_to_pic
from pydantic import BaseModel

from zhenxun.configs.config import BotConfig
from zhenxun.configs.path_config import TEMPLATE_PATH
from zhenxun.models.goods_info import GoodsInfo
from zhenxun.utils._build_image import BuildImage

from .config import ICON_PATH, LEFT_RIGHT_IMAGE


class GoodsItem(BaseModel):
    goods_list: list[dict]
    """商品列表"""
    partition: str
    """分区名称"""
    left_image: tuple[int, str, str]
    """左图"""
    right_image: tuple[int, str, str]
    """右图"""


def get_left_right_image() -> tuple[tuple[int, str, str], tuple[int, str, str]]:
    qq_top = random.randint(0, 280)
    img_top = random.randint(10, 80)
    left_image = random.choice(LEFT_RIGHT_IMAGE)
    right_image = None
    if left_image == "qq.png":
        left_top = qq_top
        right_top = img_top
        left_css = "shop-item-left-qq"
        right_css = "shop-item-right-zx"
        right_image = random.choice(LEFT_RIGHT_IMAGE[:-1])
    else:
        left_top = img_top
        right_top = qq_top
        right_image = "qq.png"
        left_css = "shop-item-right-zx"
        right_css = "shop-item-left-qq"
    return (left_top, left_css, left_image), (right_top, right_css, right_image)


async def html_image() -> bytes:
    """构建图片"""
    goods_list: list[tuple[int, GoodsInfo]] = [
        (i + 1, goods)
        for i, goods in enumerate(await GoodsInfo.get_all_goods())
        if goods.goods_limit_time == 0 or time.time() < goods.goods_limit_time
    ]
    partition_dict: dict[str, list[dict]] = {}
    for goods in goods_list:
        if not goods[1].partition:
            goods[1].partition = "默认分区"
        if goods[1].partition not in partition_dict:
            partition_dict[goods[1].partition] = []
        partition_dict[goods[1].partition].append(
            {
                "id": goods[0],
                "price": goods[1].goods_price,
                "daily_limit": goods[1].daily_limit or "∞",
                "name": goods[1].goods_name,
                "icon": "data:image/png;base64,"
                + BuildImage.open(ICON_PATH / goods[1].icon).pic2bs4()[9:],
                "description": goods[1].goods_description,
            }
        )
    data_list = []
    for partition in partition_dict:
        left, right = get_left_right_image()
        data_list.append(
            GoodsItem(
                goods_list=partition_dict[partition],
                partition=partition,
                left_image=left,
                right_image=right,
            )
        )

    return await template_to_pic(
        template_path=str((TEMPLATE_PATH / "shop").absolute()),
        template_name="main.html",
        templates={"name": BotConfig.self_nickname, "data_list": data_list},
        pages={
            "viewport": {"width": 800, "height": 1024},
            "base_url": f"file://{TEMPLATE_PATH}",
        },
        wait=2,
    )
