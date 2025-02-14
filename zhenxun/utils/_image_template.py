from collections.abc import Callable
from io import BytesIO
from pathlib import Path
import random

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
    color_list = ["#C2CEFE", "#FFA94C", "#3FE6A0", "#D1D4F5"]  # noqa: RUF012

    @classmethod
    async def hl_page(
        cls,
        head_text: str,
        items: dict[str, str],
        row_space: int = 10,
        padding: int = 30,
    ) -> BuildImage:
        """列文档 (如插件帮助)

        参数:
            head_text: 头标签文本
            items: 列内容
            row_space: 列间距.
            padding: 间距.

        返回:
            BuildImage: 图片
        """
        font = BuildImage.load_font("HYWenHei-85W.ttf", 20)
        width, height = BuildImage.get_text_size(head_text, font)
        for title, item in items.items():
            title_width, title_height = await cls.__get_text_size(title, font)
            it_width, it_height = await cls.__get_text_size(item, font)
            width = max([width, title_width, it_width])
            height += title_height + it_height
        width = max([width + padding * 2 + 100, 300])
        height = max([height + padding * 2 + 150, 100])
        A = BuildImage(width + padding * 2, height + padding * 2, color="#FAF9FE")
        top_head = BuildImage(width, 100, color="#FFFFFF", font_size=40)
        await top_head.line((0, 1, width, 1), "#C2CEFE", 2)
        await top_head.text((15, 20), head_text, "#9FA3B2", "center")
        await top_head.circle_corner()
        await A.paste(top_head, (0, 20), "width")
        _min_width = top_head.width - 60
        cur_h = top_head.height + 35 + row_space * len(items)
        for title, item in items.items():
            title_width, title_height = BuildImage.get_text_size(title, font)
            title_background = BuildImage(
                title_width + 6, title_height + 10, font=font, color="#C1CDFF"
            )
            await title_background.text((3, 5), title)
            await title_background.circle_corner(5)
            _text_width, _text_height = await cls.__get_text_size(item, font)
            _width = max([title_background.width, _text_width, _min_width])
            text_image = await cls.__build_text_image(
                item, _width, _text_height, font, color="#FDFCFA"
            )
            B = BuildImage(_width + 20, title_height + text_image.height + 40)
            await B.paste(title_background, (10, 10))
            await B.paste(text_image, (10, 20 + title_background.height))
            await B.line((0, 0, 0, B.height), random.choice(cls.color_list))
            await A.paste(B, (0, cur_h), "width")
            cur_h += B.height + row_space
        return A

    @classmethod
    async def table_page(
        cls,
        head_text: str,
        tip_text: str | None,
        column_name: list[str],
        data_list: list[list[str | int | tuple[Path | BuildImage, int, int]]],
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
        font = BuildImage.load_font(font_size=50)
        min_width, _ = BuildImage.get_text_size(head_text, font)
        table = await cls.table(
            column_name,
            data_list,
            row_space,
            column_space,
            padding,
            text_style,
        )
        await table.circle_corner()
        table_bk = BuildImage(
            max(table.width, min_width) + 100, table.height + 50, "#EAEDF2"
        )
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
        data_list: list[list[str | int | tuple[Path | BuildImage, int, int]]],
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
            min_width: 最低宽度

        返回:
            BuildImage: 表格图片
        """
        font = BuildImage.load_font("HYWenHei-85W.ttf", 20)
        column_data = []
        for i in range(len(column_name)):
            c = []
            for item in data_list:
                if len(item) > i:
                    c.append(
                        item[i] if isinstance(item[i], tuple | list) else str(item[i])
                    )
                else:
                    c.append("")
            column_data.append(c)
        build_data_list = []
        _, base_h = BuildImage.get_text_size("A", font)
        for i, column_list in enumerate(column_data):
            name_width, _ = BuildImage.get_text_size(column_name[i], font)
            _temp = {"width": name_width, "data": column_list}
            for s in column_list:
                if isinstance(s, tuple):
                    w = s[1]
                else:
                    w, _ = BuildImage.get_text_size(str(s), font)
                if w > _temp["width"]:
                    _temp["width"] = w
            build_data_list.append(_temp)
        column_image_list = []
        column_name_image_list: list[BuildImage] = []
        for i, data in enumerate(build_data_list):
            column_name_image = await BuildImage.build_text_image(
                column_name[i], font, 12, "#C8CCCF"
            )
            column_name_image_list.append(column_name_image)
        max_h = max(c.height for c in column_name_image_list)
        for i, data in enumerate(build_data_list):
            width = data["width"] + padding * 2
            height = (base_h + row_space) * (len(data["data"]) + 1) + padding * 2
            background = BuildImage(width, height, (255, 255, 255))
            column_name_image = column_name_image_list[i]
            await background.paste(column_name_image, (0, 20), center_type="width")
            cur_h = max_h + row_space + 20
            for item in data["data"]:
                style = RowStyle(font=font)
                if text_style:
                    style = text_style(column_name[i], item)
                if isinstance(item, tuple | list):
                    """图片"""
                    data, width, height = item
                    image_ = None
                    if isinstance(data, Path):
                        image_ = BuildImage(width, height, background=data)
                    elif isinstance(data, bytes):
                        image_ = BuildImage(width, height, background=BytesIO(data))
                    elif isinstance(data, BuildImage):
                        image_ = data
                    if image_:
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
        return await BuildImage.auto_paste(
            column_image_list, len(column_image_list), column_space
        )

    @classmethod
    async def __build_text_image(
        cls,
        text: str,
        width: int,
        height: int,
        font: FreeTypeFont,
        font_color: str | tuple[int, int, int] = (0, 0, 0),
        color: str | tuple[int, int, int] = (255, 255, 255),
    ) -> BuildImage:
        """文本转图片

        参数:
            text: 文本
            width: 宽度
            height: 长度
            font: 字体
            font_color: 文本颜色
            color: 背景颜色

        返回:
            BuildImage: 文本转图片
        """
        _, h = BuildImage.get_text_size("A", font)
        A = BuildImage(width, height, color=color)
        cur_h = 0
        for s in text.split("\n"):
            text_image = await BuildImage.build_text_image(
                s, font, font_color=font_color
            )
            await A.paste(text_image, (0, cur_h))
            cur_h += h
        return A

    @classmethod
    async def __get_text_size(
        cls,
        text: str,
        font: FreeTypeFont,
    ) -> tuple[int, int]:
        """获取文本所占大小

        参数:
            text: 文本
            font: 字体

        返回:
            tuple[int, int]: 宽, 高
        """
        width = 0
        height = 0
        _, h = BuildImage.get_text_size("A", font)
        for s in text.split("\n"):
            s = s.strip() or "A"
            w, _ = BuildImage.get_text_size(s, font)
            width = max(width, w)
            height += h
        return width, height
