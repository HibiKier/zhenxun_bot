from typing import Tuple, List, Literal

from utils.image_utils import BuildImage, text2image


async def help_template(title: str, usage: BuildImage) -> BuildImage:
    """
    说明:
        生成单个功能帮助模板
    参数:
        :param title: 标题
        :param usage: 说明图片
    """
    title_image = BuildImage(
        0,
        0,
        font_size=35,
        plain_text=title,
        font_color=(255, 255, 255),
        font="CJGaoDeGuo.otf",
    )
    background_image = BuildImage(
        max(title_image.w, usage.w) + 50,
        max(title_image.h, usage.h) + 100,
        color=(114, 138, 204),
    )
    await background_image.apaste(usage, (25, 80), True)
    await background_image.apaste(title_image, (25, 20), True)
    await background_image.aline(
        (25, title_image.h + 22, 25 + title_image.w, title_image.h + 22),
        (204, 196, 151),
        3,
    )
    return background_image

