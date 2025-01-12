import time

from nonebot_plugin_htmlrender import template_to_pic
from pydantic import BaseModel
from tortoise.expressions import Q

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
    goods_list = (
        await GoodsInfo.filter(
            Q(goods_limit_time__gte=time.time()) | Q(goods_limit_time=0),
            goods_limit_time=0,
        )
        .annotate()
        .order_by("id")
        .all()
    )
    partition_dict: dict[str, list[dict]] = {}
    for idx, goods in enumerate(goods_list):
        if not goods.partition:
            goods.partition = "默认分区"
        if goods.partition not in partition_dict:
            partition_dict[goods.partition] = []
        icon = None
        if goods.icon:
            path = ICON_PATH / goods.icon
            if path.exists():
                icon = (
                    "data:image/png;base64,"
                    f"{BuildImage.open(ICON_PATH / goods.icon).pic2bs4()[9:]}"
                )
        partition_dict[goods.partition].append(
            {
                "id": idx + 1,
                "price": goods.goods_price,
                "daily_limit": goods.daily_limit or "∞",
                "name": goods.goods_name,
                "icon": icon,
                "description": goods.goods_description,
            }
        )
    data_list = [
        GoodsItem(goods_list=value, partition=partition)
        for partition, value in partition_dict.items()
    ]
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
