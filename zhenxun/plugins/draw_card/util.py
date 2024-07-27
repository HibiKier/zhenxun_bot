import platform
from pathlib import Path

import pypinyin
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as IMG
from PIL.ImageFont import FreeTypeFont

from zhenxun.configs.path_config import FONT_PATH
from zhenxun.utils._build_image import BuildImage

dir_path = Path(__file__).parent.absolute()


def cn2py(word) -> str:
    """保存声调，防止出现类似方舟干员红与吽拼音相同声调不同导致红照片无法保存的问题"""
    temp = ""
    for i in pypinyin.pinyin(word, style=pypinyin.Style.TONE3):
        temp += "".join(i)
    return temp


# 移除windows和linux下特殊字符
def remove_prohibited_str(name: str) -> str:
    if platform.system().lower() == "windows":
        tmp = ""
        for i in name:
            if i not in ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]:
                tmp += i
        name = tmp
    else:
        name = name.replace("/", "\\")
    return name


def load_font(fontname: str = "msyh.ttf", fontsize: int = 16) -> FreeTypeFont:
    return ImageFont.truetype(
        str(FONT_PATH / f"{fontname}"), fontsize, encoding="utf-8"
    )


def circled_number(num: int) -> IMG:
    font = load_font(fontsize=450)
    text = str(num)
    text_w = BuildImage.get_text_size(text, font=font)[0]
    w = 240 + text_w
    w = w if w >= 500 else 500
    img = Image.new("RGBA", (w, 500))
    draw = ImageDraw.Draw(img)
    draw.ellipse(((0, 0), (500, 500)), fill="red")
    draw.ellipse(((w - 500, 0), (w, 500)), fill="red")
    draw.rectangle(((250, 0), (w - 250, 500)), fill="red")
    draw.text(
        (120, -60),
        text,
        font=font,
        fill="white",
        stroke_width=10,
        stroke_fill="white",
    )
    return img
