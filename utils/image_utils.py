from configs.path_config import IMAGE_PATH, TTF_PATH
from PIL import Image, ImageFile, ImageDraw, ImageFont
from imagehash import ImageHash
from io import BytesIO
from matplotlib import pyplot as plt
from typing import Tuple, Optional
from pathlib import Path
import cv2
import base64
import imagehash


def compare_image_with_hash(
    image_file1: str, image_file2: str, max_dif: int = 1.5
) -> bool:
    """
    说明：
        比较两张图片的hash值是否相同
    参数：
        :param image_file1: 图片文件路径
        :param image_file2: 图片文件路径
        :param max_dif: 允许最大hash差值, 越小越精确,最小为0
    """
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    hash_1 = get_img_hash(image_file1)
    hash_2 = get_img_hash(image_file2)
    dif = hash_1 - hash_2
    if dif < 0:
        dif = -dif
    if dif <= max_dif:
        return True
    else:
        return False


def get_img_hash(image_file: str) -> ImageHash:
    """
    说明：
        获取图片的hash值
    参数：
        :param image_file: 图片文件路径
    """
    with open(image_file, "rb") as fp:
        hash_value = imagehash.average_hash(Image.open(fp))
    return hash_value


def compressed_image(in_file: str, out_file: str = None, ratio: float = 0.9):
    """
    说明：
        压缩图片
    参数：
        :param in_file: 被压缩的文件路径
        :param out_file: 压缩后输出的文件路径
        :param ratio: 压缩率，宽高 * 压缩率
    """
    in_file = Path(IMAGE_PATH) / in_file
    out_file = Path(IMAGE_PATH) / out_file if out_file else in_file
    h, w, d = cv2.imread(str(in_file.absolute())).shape
    img = cv2.resize(cv2.imread(str(in_file.absolute())), (int(w * ratio), int(h * ratio)))
    cv2.imwrite(str(out_file.absolute()), img)


def alpha2white_PIL(pic: Image) -> Image:
    """
    说明：
        将图片透明背景转化为白色
    参数：
        :param pic: 通过PIL打开的图片文件
    """
    img = pic.convert("RGBA")
    width, height = img.size
    for yh in range(height):
        for xw in range(width):
            dot = (xw, yh)
            color_d = img.getpixel(dot)
            if color_d[3] == 0:
                color_d = (255, 255, 255, 255)
                img.putpixel(dot, color_d)
    return img


def pic2b64(pic: Image) -> str:
    """
    说明：
        PIL图片转base64
    参数：
        :param pic: 通过PIL打开的图片文件
    """
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return "base64://" + base64_str


def fig2b64(plt_: plt) -> str:
    """
    说明：
        matplotlib图片转base64
    参数：
        :param plt_: matplotlib生成的图片
    """
    buf = BytesIO()
    plt_.savefig(buf, format="PNG", dpi=100)
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return "base64://" + base64_str


def is_valid(file: str) -> bool:
    """
    说明：
        判断图片是否损坏
    参数：
        :param file: 图片文件路径
    """
    valid = True
    try:
        Image.open(file).load()
    except OSError:
        valid = False
    return valid


class CreateImg:
    """
    快捷生成图片与操作图片的工具类
    """

    def __init__(
        self,
        w,
        h,
        paste_image_width=0,
        paste_image_height=0,
        color="white",
        image_type="RGBA",
        font_size=10,
        background="",
        ttf="yz.ttf",
        ratio=1,
    ):
        """
        参数：
            :param w: 自定义图片的宽度，w=0时为图片原本宽度
            :param h: 自定义图片的高度，h=0时为图片原本高度
            :param paste_image_width: 当图片做为背景图时，设置贴图的宽度，用于贴图自动换行
            :param paste_image_height: 当图片做为背景图时，设置贴图的高度，用于贴图自动换行
            :param color: 生成图片的颜色
            :param image_type: 图片的类型
            :param font_size: 文字大小
            :param background: 打开图片的路径
            :param ttf: 字体，默认在 resource/ttf/ 路径下
            :param ratio: 倍率压缩
        """
        self.w = int(w)
        self.h = int(h)
        self.paste_image_width = int(paste_image_width)
        self.paste_image_height = int(paste_image_height)
        self.current_w = 0
        self.current_h = 0
        self.ttfont = ImageFont.truetype(TTF_PATH + ttf, int(font_size))
        if not background:
            self.markImg = Image.new(image_type, (self.w, self.h), color)
        else:
            if not w and not h:
                self.markImg = Image.open(background)
                w, h = self.markImg.size
                if ratio and ratio > 0 and ratio != 1:
                    self.w = int(ratio * w)
                    self.h = int(ratio * h)
                    self.markImg = self.markImg.resize(
                        (self.w, self.h), Image.ANTIALIAS
                    )
                else:
                    self.w = w
                    self.h = h
            else:
                self.markImg = Image.open(background).resize(
                    (self.w, self.h), Image.ANTIALIAS
                )
        self.draw = ImageDraw.Draw(self.markImg)
        self.size = self.w, self.h

    def paste(
        self,
        img: "CreateImg" or Image,
        pos: Tuple[int, int] = None,
        alpha: bool = False,
    ):
        """
        说明：
            贴图
        参数：
            :param img: 已打开的图片文件，可以为 CreateImg 或 Image
            :param pos: 贴图位置（左上角）
            :param alpha: 图片背景是否为透明
        """
        if isinstance(img, CreateImg):
            img = img.markImg
        if self.current_w == self.w:
            self.current_w = 0
            self.current_h += self.paste_image_height
        if not pos:
            pos = (self.current_w, self.current_h)
        if alpha:
            try:
                self.markImg.paste(img, pos, img)
            except ValueError:
                img = img.convert("RGBA")
                self.markImg.paste(img, pos, img)
        else:
            self.markImg.paste(img, pos)
        self.current_w += self.paste_image_width

    def getsize(self, msg: str) -> Tuple[int, int]:
        """
        说明：
            获取文字在该图片 font_size 下所需要的空间
        参数：
            :param msg: 文字内容
        """
        return self.ttfont.getsize(msg)

    def text(
        self, pos: Tuple[int, int], text: str, fill: Tuple[int, int, int] = (0, 0, 0)
    ):
        """
        说明：
            在图片上添加文字
        参数：
            :param pos: 文字位置
            :param text: 文字内容
            :param fill: 文字颜色
        """
        self.draw.text(pos, text, fill=fill, font=self.ttfont)

    def save(self, path: str):
        """
        说明：
            保存图片
        参数：
            :param path: 图片路径
        """
        self.markImg.save(path)

    def show(self):
        """
        说明：
            显示图片
        """
        self.markImg.show(self.markImg)

    def resize(self, ratio: float = 0, w: int = 0, h: int = 0):
        """
        说明：
            压缩图片
        参数：
            :param ratio: 压缩倍率
            :param w: 压缩图片宽度至 w
            :param h: 压缩图片高度至 h
        """
        if not w and not h and not ratio:
            raise Exception("缺少参数...")
        if not w and not h and ratio:
            w = int(self.w * ratio)
            h = int(self.h * ratio)
        self.markImg = self.markImg.resize((w, h), Image.ANTIALIAS)
        self.w, self.h = self.markImg.size
        self.size = self.w, self.h
        self.draw = ImageDraw.Draw(self.markImg)

    def crop(self, box: Tuple[int, int, int, int]):
        """
        说明：
            裁剪图片
        参数：
            :param box: 左上角坐标，右下角坐标 (left, upper, right, lower)
        """
        self.markImg = self.markImg.crop(box)
        self.w, self.h = self.markImg.size
        self.size = self.w, self.h
        self.draw = ImageDraw.Draw(self.markImg)

    def check_font_size(self, word: str) -> bool:
        """
        说明：
            检查文本所需宽度是否大于图片宽度
        :param word: 文本内容
        """
        return self.ttfont.getsize(word)[0] > self.w

    def transparent(self, n: int = 0):
        """
        说明：
            图片透明化
        参数：
            :param n: 透明化大小内边距
        """
        self.markImg = self.markImg.convert("RGBA")
        x, y = self.markImg.size
        for i in range(n, x - n):
            for k in range(n, y - n):
                color = self.markImg.getpixel((i, k))
                color = color[:-1] + (100,)
                self.markImg.putpixel((i, k), color)

    def pic2bs4(self) -> str:
        """
        说明：
            CreateImg 转 base64
        """
        buf = BytesIO()
        self.markImg.save(buf, format="PNG")
        base64_str = base64.b64encode(buf.getvalue()).decode()
        return base64_str

    def convert(self, type_: str):
        """
        说明：
            修改图片类型
        参数：
            :param type_: 类型
        """
        self.markImg = self.markImg.convert(type_)

    def rectangle(
        self,
        xy: Tuple[int, int, int, int],
        fill: Optional[Tuple[int, int, int]] = None,
        outline: str = None,
        width: int = 1,
    ):
        """
        说明：
            画框
        参数：
            :param xy: 坐标
            :param fill: 填充颜色
            :param outline: 轮廓颜色
            :param width: 线宽
        """
        self.draw.rectangle(xy, fill, outline, width)

    def line(
        self,
        xy: Tuple[int, int, int, int],
        fill: Optional[Tuple[int, int, int]] = None,
        width: int = 1,
    ):
        """
        说明：
            画线
        参数：
            :param xy: 坐标
            :param fill: 填充
            :param width: 线宽
        """
        self.draw.line(xy, fill, width)

    def circle(self):
        """
        说明：
            将 CreateImg 图片变为圆形
        """
        self.convert("RGBA")
        r2 = min(self.w, self.h)
        if self.w != self.h:
            self.resize(w=r2, h=r2)
        r3 = int(r2 / 2)
        imb = Image.new("RGBA", (r3 * 2, r3 * 2), (255, 255, 255, 0))
        pim_a = self.markImg.load()  # 像素的访问对象
        pim_b = imb.load()
        r = float(r2 / 2)
        for i in range(r2):
            for j in range(r2):
                lx = abs(i - r)  # 到圆心距离的横坐标
                ly = abs(j - r)  # 到圆心距离的纵坐标
                l = (pow(lx, 2) + pow(ly, 2)) ** 0.5  # 三角函数 半径
                if l < r3:
                    pim_b[i - (r - r3), j - (r - r3)] = pim_a[i, j]
        self.markImg = imb

    #
    def getchannel(self, itype):
        self.markImg = self.markImg.getchannel(itype)


if __name__ == "__main__":
    pass
