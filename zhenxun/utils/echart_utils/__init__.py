from nonebot_plugin_htmlrender import template_to_pic

from zhenxun.configs.path_config import TEMPLATE_PATH
from zhenxun.utils._build_image import BuildImage

from .models import Barh


class ChartUtils:

    @classmethod
    async def barh(cls, data: Barh) -> BuildImage:
        """横向统计图"""
        pic = await template_to_pic(
            template_path=str((TEMPLATE_PATH / "bar_chart").absolute()),
            template_name="main.html",
            templates={"data": data},
            pages={
                "viewport": {"width": 1000, "height": 500},
                "base_url": f"file://{TEMPLATE_PATH}",
            },
            wait=2,
        )
        return BuildImage.open(pic)
