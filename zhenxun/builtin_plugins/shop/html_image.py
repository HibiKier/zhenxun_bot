import time

from nonebot_plugin_htmlrender import template_to_pic
from pydantic import BaseModel

from zhenxun.configs.config import BotConfig
from zhenxun.configs.path_config import TEMPLATE_PATH
from zhenxun.models.goods_info import GoodsInfo
from zhenxun.utils._build_image import BuildImage

from .config import ICON_PATH


class GoodsItem(BaseModel):
    goods_list: list[dict]
    """商品列表"""
    partition: str
    """分区名称"""


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
        data_list.append(
            GoodsItem(
                goods_list=partition_dict[partition],
                partition=partition,
            )
        )

    return await template_to_pic(
        template_path=str((TEMPLATE_PATH / "shop").absolute()),
        template_name="main.html",
        templates={"name": BotConfig.self_nickname, "data_list": data_list},
        pages={
            "viewport": {"width": 850, "height": 1024},
            "base_url": f"file://{TEMPLATE_PATH}",
        },
        wait=2,
    )
