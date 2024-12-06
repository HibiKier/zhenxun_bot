import os
import random

from nonebot_plugin_htmlrender import template_to_pic
from playwright.async_api import Error as PlaywrightError
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from zhenxun.configs.path_config import TEMPLATE_PATH
from zhenxun.utils._build_image import BuildImage
from .models import Barh
from ..exception import PlaywrightRenderError

BACKGROUND_PATH = TEMPLATE_PATH / "bar_chart" / "background"


class ChartUtils:
    @classmethod
    async def barh(cls, data: Barh) -> BuildImage:
        """横向统计图"""
        to_json = data.dict()
        to_json["background_image"] = (
            f"./background/{random.choice(os.listdir(BACKGROUND_PATH))}"
        )
        try:
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
        except (PlaywrightError, PlaywrightTimeoutError) as e:
            raise PlaywrightRenderError("横向统计图渲染失败") from e
        return BuildImage.open(pic)
