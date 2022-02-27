import platform
import pypinyin
from PIL.ImageFont import FreeTypeFont
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as IMG
from configs.path_config import FONT_PATH


def cn2py(word) -> str:
    temp = ""
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
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


def load_font(font_name: str = "msyh.ttf", fontsize: int = 16) -> FreeTypeFont:
    return ImageFont.truetype(
        str(FONT_PATH / f"{font_name}"), fontsize, encoding="utf-8"
    )


def circled_number(num: int) -> IMG:
    font = load_font(fontsize=450)
    text = str(num)
    text_w = font.getsize(text)[0]
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

