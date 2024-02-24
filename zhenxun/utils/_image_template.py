from email.mime import image
from io import BytesIO
from pathlib import Path
from typing import Any, Callable

from nonebot.plugin import PluginMetadata
from PIL.ImageFont import FreeTypeFont
from pydantic import BaseModel

from ._build_image import BuildImage


class RowStyle(BaseModel):

    font: FreeTypeFont | str | Path | None = "HYWenHei-85W.ttf"
    """字体"""
    font_size: int = 20
    """字体大小"""
    font_color: str | tuple[int, int, int] = (0, 0, 0)
    """字体颜色"""

    class Config:
        arbitrary_types_allowed = True


class ImageTemplate:

    @classmethod
    async def table_page(
        cls,
        head_text: str,
        tip_text: str | None,
        column_name: list[str],
        data_list: list[list[str]],
        row_space: int = 35,
        column_space: int = 30,
        padding: int = 5,
        text_style: Callable[[str, str], RowStyle] | None = None,
    ) -> BuildImage:
        """表格页

        参数:
            head_text: 标题文本.
            tip_text: 标题注释.
            column_name: 表头列表.
            data_list: 数据列表.
            row_space: 行间距.
            column_space: 列间距.
            padding: 文本内间距.
            text_style: 文本样式.

        返回:
            BuildImage: 表格图片
        """
        table = await cls.table(
            column_name, data_list, row_space, column_space, padding, text_style
        )
        await table.circle_corner()
        table_bk = BuildImage(table.width + 100, table.height + 50, "#EAEDF2")
        await table_bk.paste(table, center_type="center")
        height = table_bk.height + 200
        background = BuildImage(table_bk.width, height, (255, 255, 255), font_size=50)
        await background.paste(table_bk, (0, 200))
        await background.text((0, 50), head_text, "#334762", center_type="width")
        if tip_text:
            text_image = await BuildImage.build_text_image(tip_text, size=22)
            await background.paste(text_image, (0, 110), center_type="width")
        return background

    @classmethod
    async def table(
        cls,
        column_name: list[str],
        data_list: list[list[str | tuple[Path, int, int]]],
        row_space: int = 25,
        column_space: int = 10,
        padding: int = 5,
        text_style: Callable[[str, str], RowStyle] | None = None,
    ) -> BuildImage:
        """表格

        参数:
            column_name: 表头列表
            data_list: 数据列表
            row_space: 行间距.
            column_space: 列间距.
            padding: 文本内间距.
            text_style: 文本样式.

        返回:
            BuildImage: 表格图片
        """
        font = BuildImage.load_font("HYWenHei-85W.ttf", 20)
        column_num = max([len(l) for l in data_list])
        list_data = []
        column_data = []
        for i in range(len(column_name)):
            c = []
            for l in data_list:
                if len(l) > i:
                    c.append(l[i])
                else:
                    c.append("")
            column_data.append(c)
        build_data_list = []
        _, base_h = BuildImage.get_text_size("A", font)
        for i, column_list in enumerate(column_data):
            name_width, name_height = BuildImage.get_text_size(column_name[i], font)
            _temp = {"width": name_width, "data": column_list}
            for s in column_list:
                if isinstance(s, tuple):
                    w = s[1]
                else:
                    w, _ = BuildImage.get_text_size(s, font)
                if w > _temp["width"]:
                    _temp["width"] = w
            build_data_list.append(_temp)
        column_image_list = []
        for i, data in enumerate(build_data_list):
            width = data["width"] + padding * 2
            height = (base_h + row_space) * (len(data["data"]) + 1) + padding * 2
            background = BuildImage(width, height, (255, 255, 255))
            column_name_image = await BuildImage.build_text_image(
                column_name[i], font, 12, "#C8CCCF"
            )
            await background.paste(column_name_image, (0, 20), center_type="width")
            cur_h = column_name_image.height + row_space + 20
            for item in data["data"]:
                style = RowStyle(font=font)
                if text_style:
                    style = text_style(column_name[i], item)
                if isinstance(item, tuple):
                    """图片"""
                    data, width, height = item
                    if isinstance(data, Path):
                        image_ = BuildImage(width, height, background=data)
                    elif isinstance(data, bytes):
                        image_ = BuildImage(width, height, background=BytesIO(data))
                    elif isinstance(data, BuildImage):
                        image_ = data
                    await background.paste(image_, (padding, cur_h))
                else:
                    await background.text(
                        (padding, cur_h),
                        item if item is not None else "",
                        style.font_color,
                        font=style.font,
                        font_size=style.font_size,
                    )
                cur_h += base_h + row_space
            column_image_list.append(background)
        height = max([bk.height for bk in column_image_list])
        width = sum([bk.width for bk in column_image_list])
        return await BuildImage.auto_paste(
            column_image_list, len(column_image_list), column_space
        )
