import os
import random

from nonebot_plugin_htmlrender import template_to_pic

from zhenxun.configs.path_config import TEMPLATE_PATH
from zhenxun.utils._build_image import BuildImage

from .models import Barh

BACKGROUND_PATH = TEMPLATE_PATH / "bar_chart" / "background"


class ChartUtils:
    @classmethod
    async def barh(cls, data: Barh) -> BuildImage:
        """横向统计图"""
        to_json = data.to_dict()
        to_json["background_image"] = (
            f"./background/{random.choice(os.listdir(BACKGROUND_PATH))}"
        )
        pic = await template_to_pic(
            template_path=str((TEMPLATE_PATH / "bar_chart").absolute()),
            template_name="main.html",
            templates={"data": to_json},
            pages={
                "viewport": {"width": 1000, "height": 1000},
                "base_url": f"file://{TEMPLATE_PATH}",
            },
            wait=2,
        )
        return BuildImage.open(pic)
