import asyncio
from configs.path_config import IMAGE_PATH, FONT_PATH
from PIL import Image, ImageFile, ImageDraw, ImageFont, ImageFilter
from imagehash import ImageHash
from io import BytesIO
from matplotlib import pyplot as plt
from typing import Tuple, Optional, Union, List, Literal
from pathlib import Path
from math import ceil
import random
import cv2
import base64
import imagehash
import re

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None


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


def get_img_hash(image_file: Union[str, Path]) -> ImageHash:
    """
    说明：
        获取图片的hash值
    参数：
        :param image_file: 图片文件路径
    """
    with open(image_file, "rb") as fp:
        hash_value = imagehash.average_hash(Image.open(fp))
    return hash_value


def compressed_image(
    in_file: Union[str, Path], out_file: Union[str, Path] = None, ratio: float = 0.9
):
    """
    说明：
        压缩图片
    参数：
        :param in_file: 被压缩的文件路径
        :param out_file: 压缩后输出的文件路径
        :param ratio: 压缩率，宽高 * 压缩率
    """
    in_file = IMAGE_PATH / in_file if isinstance(in_file, str) else in_file
    if out_file:
        out_file = (
            IMAGE_PATH / out_file if isinstance(out_file, str) else out_file
        )
    else:
        out_file = in_file
    h, w, d = cv2.imread(str(in_file.absolute())).shape
    img = cv2.resize(
        cv2.imread(str(in_file.absolute())), (int(w * ratio), int(h * ratio))
    )
    cv2.imwrite(str(out_file.absolute()), img)


def alpha2white_pil(pic: Image) -> Image:
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


class BuildImage:
    """
    快捷生成图片与操作图片的工具类
    """

    def __init__(
        self,
        w: int,
        h: int,
        paste_image_width: int = 0,
        paste_image_height: int = 0,
        color: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]] = None,
        image_mode: str = "RGBA",
        font_size: int = 10,
        background: Union[Optional[str], BytesIO, Path] = None,
        font: str = "yz.ttf",
        ratio: float = 1,
        is_alpha: bool = False,
        plain_text: Optional[str] = None,
        font_color: Optional[Union[str, Tuple[int, int, int]]] = None,
    ):
        """
        参数：
            :param w: 自定义图片的宽度，w=0时为图片原本宽度
            :param h: 自定义图片的高度，h=0时为图片原本高度
            :param paste_image_width: 当图片做为背景图时，设置贴图的宽度，用于贴图自动换行
            :param paste_image_height: 当图片做为背景图时，设置贴图的高度，用于贴图自动换行
            :param color: 生成图片的颜色
            :param image_mode: 图片的类型
            :param font_size: 文字大小
            :param background: 打开图片的路径
            :param font: 字体，默认在 resource/ttf/ 路径下
            :param ratio: 倍率压缩
            :param is_alpha: 是否背景透明
            :param plain_text: 纯文字文本
        """
        self.w = int(w)
        self.h = int(h)
        self.paste_image_width = int(paste_image_width)
        self.paste_image_height = int(paste_image_height)
        self.current_w = 0
        self.current_h = 0
        self.font = ImageFont.truetype(str(FONT_PATH / font), int(font_size))
        if not plain_text and not color:
            color = (255, 255, 255)
        self.background = background
        if not background:
            if plain_text:
                if not color:
                    color = (255, 255, 255, 0)
                ttf_w, ttf_h = self.getsize(plain_text)
                self.w = self.w if self.w > ttf_w else ttf_w
                self.h = self.h if self.h > ttf_h else ttf_h
            self.markImg = Image.new(image_mode, (self.w, self.h), color)
            self.markImg.convert(image_mode)
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
        if is_alpha:
            array = self.markImg.load()
            for i in range(w):
                for j in range(h):
                    pos = array[i, j]
                    is_edit = sum([1 for x in pos[0:3] if x > 240]) == 3
                    if is_edit:
                        array[i, j] = (255, 255, 255, 0)
        self.draw = ImageDraw.Draw(self.markImg)
        self.size = self.w, self.h
        if plain_text:
            fill = font_color if font_color else (0, 0, 0)
            self.text((0, 0), plain_text, fill)
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            self.loop = asyncio.get_event_loop()

    async def apaste(
        self,
        img: "BuildImage" or Image,
        pos: Tuple[int, int] = None,
        alpha: bool = False,
        center_type: Optional[Literal["center", "by_height", "by_width"]] = None,
    ):
        """
        说明：
            异步 贴图
        参数：
            :param img: 已打开的图片文件，可以为 BuildImage 或 Image
            :param pos: 贴图位置（左上角）
            :param alpha: 图片背景是否为透明
            :param center_type: 居中类型，可能的值 center: 完全居中，by_width: 水平居中，by_height: 垂直居中
        """
        await self.loop.run_in_executor(None, self.paste, img, pos, alpha, center_type)

    def paste(
        self,
        img: "BuildImage" or Image,
        pos: Tuple[int, int] = None,
        alpha: bool = False,
        center_type: Optional[Literal["center", "by_height", "by_width"]] = None,
    ):
        """
        说明：
            贴图
        参数：
            :param img: 已打开的图片文件，可以为 BuildImage 或 Image
            :param pos: 贴图位置（左上角）
            :param alpha: 图片背景是否为透明
            :param center_type: 居中类型，可能的值 center: 完全居中，by_width: 水平居中，by_height: 垂直居中
        """
        if center_type:
            if center_type not in ["center", "by_height", "by_width"]:
                raise ValueError(
                    "center_type must be 'center', 'by_width' or 'by_height'"
                )
            width, height = 0, 0
            if not pos:
                pos = (0, 0)
            if center_type == "center":
                width = int((self.w - img.w) / 2)
                height = int((self.h - img.h) / 2)
            elif center_type == "by_width":
                width = int((self.w - img.w) / 2)
                height = pos[1]
            elif center_type == "by_height":
                width = pos[0]
                height = int((self.h - img.h) / 2)
            pos = (width, height)
        if isinstance(img, BuildImage):
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
        return self.font.getsize(msg)

    async def apoint(
        self, pos: Tuple[int, int], fill: Optional[Tuple[int, int, int]] = None
    ):
        """
        说明：
            异步 绘制多个或单独的像素
        参数：
            :param pos: 坐标
            :param fill: 填错颜色
        """
        await self.loop.run_in_executor(None, self.point, pos, fill)

    def point(self, pos: Tuple[int, int], fill: Optional[Tuple[int, int, int]] = None):
        """
        说明：
            绘制多个或单独的像素
        参数：
            :param pos: 坐标
            :param fill: 填错颜色
        """
        self.draw.point(pos, fill=fill)

    async def aellipse(
        self,
        pos: Tuple[int, int, int, int],
        fill: Optional[Tuple[int, int, int]] = None,
        outline: Optional[Tuple[int, int, int]] = None,
        width: int = 1,
    ):
        """
        说明：
            异步 绘制圆
        参数：
            :param pos: 坐标范围
            :param fill: 填充颜色
            :param outline: 描线颜色
            :param width: 描线宽度
        """
        await self.loop.run_in_executor(None, self.ellipse, pos, fill, outline, width)

    def ellipse(
        self,
        pos: Tuple[int, int, int, int],
        fill: Optional[Tuple[int, int, int]] = None,
        outline: Optional[Tuple[int, int, int]] = None,
        width: int = 1,
    ):
        """
        说明：
            绘制圆
        参数：
            :param pos: 坐标范围
            :param fill: 填充颜色
            :param outline: 描线颜色
            :param width: 描线宽度
        """
        self.draw.ellipse(pos, fill, outline, width)

    async def atext(
        self,
        pos: Union[Tuple[int, int], Tuple[float, float]],
        text: str,
        fill: Union[str, Tuple[int, int, int]] = (0, 0, 0),
        center_type: Optional[Literal["center", "by_height", "by_width"]] = None,
    ):
        """
        说明：
            异步 在图片上添加文字
        参数：
            :param pos: 文字位置
            :param text: 文字内容
            :param fill: 文字颜色
            :param center_type: 居中类型，可能的值 center: 完全居中，by_width: 水平居中，by_height: 垂直居中
        """
        await self.loop.run_in_executor(None, self.text, pos, text, fill, center_type)

    def text(
        self,
        pos: Union[Tuple[int, int], Tuple[float, float]],
        text: str,
        fill: Union[str, Tuple[int, int, int]] = (0, 0, 0),
        center_type: Optional[Literal["center", "by_height", "by_width"]] = None,
    ):
        """
        说明：
            在图片上添加文字
        参数：
            :param pos: 文字位置
            :param text: 文字内容
            :param fill: 文字颜色
            :param center_type: 居中类型，可能的值 center: 完全居中，by_width: 水平居中，by_height: 垂直居中
        """
        if center_type:
            if center_type not in ["center", "by_height", "by_width"]:
                raise ValueError(
                    "center_type must be 'center', 'by_width' or 'by_height'"
                )
            w, h = self.w, self.h
            ttf_w, ttf_h = self.getsize(text)
            if center_type == "center":
                w = int((w - ttf_w) / 2)
                h = int((h - ttf_h) / 2)
            elif center_type == "by_width":
                w = int((w - ttf_w) / 2)
                h = pos[1]
            elif center_type == "by_height":
                h = int((h - ttf_h) / 2)
                w = pos[0]
            pos = (w, h)
        self.draw.text(pos, text, fill=fill, font=self.font)

    async def asave(self, path: Optional[Union[str, Path]] = None):
        """
        说明：
            异步 保存图片
        参数：
            :param path: 图片路径
        """
        await self.loop.run_in_executor(None, self.save, path)

    def save(self, path: Optional[Union[str, Path]] = None):
        """
        说明：
            保存图片
        参数：
            :param path: 图片路径
        """
        if not path:
            path = self.background
        self.markImg.save(path)

    def show(self):
        """
        说明：
            显示图片
        """
        self.markImg.show(self.markImg)

    async def aresize(self, ratio: float = 0, w: int = 0, h: int = 0):
        """
        说明：
            异步 压缩图片
        参数：
            :param ratio: 压缩倍率
            :param w: 压缩图片宽度至 w
            :param h: 压缩图片高度至 h
        """
        await self.loop.run_in_executor(None, self.resize, ratio, w, h)

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

    async def acrop(self, box: Tuple[int, int, int, int]):
        """
        说明：
            异步 裁剪图片
        参数：
            :param box: 左上角坐标，右下角坐标 (left, upper, right, lower)
        """
        await self.loop.run_in_executor(None, self.crop, box)

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
        参数：
            :param word: 文本内容
        """
        return self.font.getsize(word)[0] > self.w

    async def atransparent(self, alpha_ratio: float = 1, n: int = 0):
        """
        说明：
            异步 图片透明化
        参数：
            :param alpha_ratio: 透明化程度
            :param n: 透明化大小内边距
        """
        await self.loop.run_in_executor(None, self.transparent, alpha_ratio, n)

    def transparent(self, alpha_ratio: float = 1, n: int = 0):
        """
        说明：
            图片透明化
        参数：
            :param alpha_ratio: 透明化程度
            :param n: 透明化大小内边距
        """
        self.markImg = self.markImg.convert("RGBA")
        x, y = self.markImg.size
        for i in range(n, x - n):
            for k in range(n, y - n):
                color = self.markImg.getpixel((i, k))
                color = color[:-1] + (int(100 * alpha_ratio),)
                self.markImg.putpixel((i, k), color)
        self.draw = ImageDraw.Draw(self.markImg)

    def pic2bs4(self) -> str:
        """
        说明：
            BuildImage 转 base64
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

    async def arectangle(
        self,
        xy: Tuple[int, int, int, int],
        fill: Optional[Tuple[int, int, int]] = None,
        outline: str = None,
        width: int = 1,
    ):
        """
        说明：
            异步 画框
        参数：
            :param xy: 坐标
            :param fill: 填充颜色
            :param outline: 轮廓颜色
            :param width: 线宽
        """
        await self.loop.run_in_executor(None, self.rectangle, xy, fill, outline, width)

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

    async def apolygon(
        self,
        xy: List[Tuple[int, int]],
        fill: Tuple[int, int, int] = (0, 0, 0),
        outline: int = 1,
    ):
        """
        说明:
            异步 画多边形
        参数：
            :param xy: 坐标
            :param fill: 颜色
            :param outline: 线宽
        """
        await self.loop.run_in_executor(None, self.polygon, xy, fill, outline)

    def polygon(
        self,
        xy: List[Tuple[int, int]],
        fill: Tuple[int, int, int] = (0, 0, 0),
        outline: int = 1,
    ):
        """
        说明:
            画多边形
        参数：
            :param xy: 坐标
            :param fill: 颜色
            :param outline: 线宽
        """
        self.draw.polygon(xy, fill, outline)

    async def aline(
        self,
        xy: Tuple[int, int, int, int],
        fill: Optional[Union[str, Tuple[int, int, int]]] = None,
        width: int = 1,
    ):
        """
        说明：
            异步 画线
        参数：
            :param xy: 坐标
            :param fill: 填充
            :param width: 线宽
        """
        await self.loop.run_in_executor(None, self.line, xy, fill, width)

    def line(
        self,
        xy: Tuple[int, int, int, int],
        fill: Optional[Union[Tuple[int, int, int], str]] = None,
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

    async def acircle(self):
        """
        说明：
            异步 将 BuildImage 图片变为圆形
        """
        await self.loop.run_in_executor(None, self.circle)

    def circle(self):
        """
        说明：
            使图像变圆
        """
        self.markImg.convert("RGBA")
        size = self.markImg.size
        r2 = min(size[0], size[1])
        if size[0] != size[1]:
            self.markImg = self.markImg.resize((r2, r2), Image.ANTIALIAS)
        width = 1
        antialias = 4
        ellipse_box = [0, 0, r2 - 2, r2 - 2]
        mask = Image.new(
            size=[int(dim * antialias) for dim in self.markImg.size],
            mode='L', color='black')
        draw = ImageDraw.Draw(mask)
        for offset, fill in (width / -2.0, 'black'), (width / 2.0, 'white'):
            left, top = [(value + offset) * antialias for value in ellipse_box[:2]]
            right, bottom = [(value - offset) * antialias for value in ellipse_box[2:]]
            draw.ellipse([left, top, right, bottom], fill=fill)
        mask = mask.resize(self.markImg.size, Image.LANCZOS)
        self.markImg.putalpha(mask)

    async def acircle_corner(self, radii: int = 30):
        """
        说明：
            异步 矩形四角变圆
        参数：
            :param radii: 半径
        """
        await self.loop.run_in_executor(None, self.circle_corner, radii)

    def circle_corner(self, radii: int = 30):
        """
        说明：
            矩形四角变圆
        参数：
            :param radii: 半径
        """
        # 画圆（用于分离4个角）
        circle = Image.new("L", (radii * 2, radii * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)
        self.markImg = self.markImg.convert("RGBA")
        w, h = self.markImg.size
        alpha = Image.new("L", self.markImg.size, 255)
        alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))
        alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))
        alpha.paste(
            circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii)
        )
        alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))
        self.markImg.putalpha(alpha)

    async def arotate(self, angle: int, expand: bool = False):
        """
        说明：
            异步 旋转图片
        参数：
            :param angle: 角度
            :param expand: 放大图片适应角度
        """
        await self.loop.run_in_executor(None, self.rotate, angle, expand)

    def rotate(self, angle: int, expand: bool = False):
        """
        说明：
            旋转图片
        参数：
            :param angle: 角度
            :param expand: 放大图片适应角度
        """
        self.markImg = self.markImg.rotate(angle, expand=expand)

    async def atranspose(self, angle: int):
        """
        说明：
            异步 旋转图片(包括边框)
        参数：
            :param angle: 角度
        """
        await self.loop.run_in_executor(None, self.transpose, angle)

    def transpose(self, angle: int):
        """
        说明：
            旋转图片(包括边框)
        参数：
            :param angle: 角度
        """
        self.markImg.transpose(angle)

    async def afilter(self, filter_: str, aud: int = None):
        """
        说明：
            异步 图片变化
        参数：
            :param filter_: 变化效果
            :param aud: 利率
        """
        await self.loop.run_in_executor(None, self.filter, filter_, aud)

    def filter(self, filter_: str, aud: int = None):
        """
        说明：
            图片变化
        参数：
            :param filter_: 变化效果
            :param aud: 利率
        """
        _x = None
        if filter_ == "GaussianBlur":  # 高斯模糊
            _x = ImageFilter.GaussianBlur
        elif filter_ == "EDGE_ENHANCE":  # 锐化效果
            _x = ImageFilter.EDGE_ENHANCE
        elif filter_ == "BLUR":  # 模糊效果
            _x = ImageFilter.BLUR
        elif filter_ == "CONTOUR":  # 铅笔滤镜
            _x = ImageFilter.CONTOUR
        elif filter_ == "FIND_EDGES":  # 边缘检测
            _x = ImageFilter.FIND_EDGES
        if _x:
            if aud:
                self.markImg = self.markImg.filter(_x(aud))
            else:
                self.markImg = self.markImg.filter(_x)
        self.draw = ImageDraw.Draw(self.markImg)

    async def areplace_color_tran(
        self,
        src_color: Union[
            Tuple[int, int, int], Tuple[Tuple[int, int, int], Tuple[int, int, int]]
        ],
        replace_color: Tuple[int, int, int],
    ):
        """
        说明：
            异步 颜色替换
        参数：
            :param src_color: 目标颜色，或者使用列表，设置阈值
            :param replace_color: 替换颜色
        """
        self.loop.run_in_executor(
            None, self.replace_color_tran, src_color, replace_color
        )

    def replace_color_tran(
        self,
        src_color: Union[
            Tuple[int, int, int], Tuple[Tuple[int, int, int], Tuple[int, int, int]]
        ],
        replace_color: Tuple[int, int, int],
    ):
        """
        说明：
            颜色替换
        参数：
            :param src_color: 目标颜色，或者使用元祖，设置阈值
            :param replace_color: 替换颜色
        """
        if isinstance(src_color, tuple):
            start_ = src_color[0]
            end_ = src_color[1]
        else:
            start_ = src_color
            end_ = None
        for i in range(self.w):
            for j in range(self.h):
                r, g, b = self.markImg.getpixel((i, j))
                if not end_:
                    if r == start_[0] and g == start_[1] and b == start_[2]:
                        self.markImg.putpixel((i, j), replace_color)
                else:
                    if (
                        start_[0] <= r <= end_[0]
                        and start_[1] <= g <= end_[1]
                        and start_[2] <= b <= end_[2]
                    ):
                        self.markImg.putpixel((i, j), replace_color)

    #
    def getchannel(self, type_):
        self.markImg = self.markImg.getchannel(type_)


class BuildMat:
    """
    针对 折线图/柱状图，基于 BuildImage 编写的 非常难用的 自定义画图工具
    目前仅支持 正整数
    """

    def __init__(
        self,
        y: List[int],
        mat_type: str = "line",
        *,
        x_name: Optional[str] = None,
        y_name: Optional[str] = None,
        x_index: List[Union[str, int, float]] = None,
        y_index: List[Union[str, int, float]] = None,
        x_rotate: int = 0,
        title: Optional[str] = None,
        size: Tuple[int, int] = (1000, 1000),
        font: str = "msyh.ttf",
        font_size: Optional[int] = None,
        display_num: bool = False,
        is_grid: bool = False,
        background: Optional[List[str]] = None,
        background_filler_type: Optional[str] = "center",
        bar_color: Optional[List[Union[str, Tuple[int, int, int]]]] = None,
    ):
        """
        说明：
            初始化 BuildMat
        参数：
            :param y: 坐标值
            :param mat_type: 图像类型 可能的值：[line]: 折线图，[bar]: 柱状图，[barh]: 横向柱状图
            :param x_name: 横坐标名称
            :param y_name: 纵坐标名称
            :param x_index: 横坐标值
            :param y_index: 纵坐标值
            :param x_rotate: 横坐标旋转角度
            :param title: 标题
            :param size: 图像大小，建议默认
            :param font: 字体
            :param font_size: 字体大小，建议默认
            :param display_num: 是否显示数值
            :param is_grid: 是否添加栅格
            :param background: 背景图片
            :param background_filler_type: 图像填充类型
            :param bar_color: 柱状图颜色，位 ['*'] 时替换位彩虹随机色
        """
        self.mat_type = mat_type
        self.markImg = None
        self._check_value(y, y_index)
        self.w = size[0]
        self.h = size[1]
        self.y = y
        self.x_name = x_name
        self.y_name = y_name
        self.x_index = x_index
        self.y_index = y_index
        self.x_rotate = x_rotate
        self.title = title
        self.font = font
        self.display_num = display_num
        self.is_grid = is_grid
        self.background = background
        self.background_filler_type = background_filler_type
        self.bar_color = bar_color if bar_color else [(0, 0, 0)]
        self.size = size
        self.padding_w = 120
        self.padding_h = 120
        self.line_length = 760
        self._deviation = 0.905
        self._color = {}
        if not font_size:
            self.font_size = int(25 * (1 - len(x_index) / 100))
        else:
            self.font_size = font_size
        if self.bar_color == ["*"]:
            self.bar_color = [
                "#FF0000",
                "#FF7F00",
                "#FFFF00",
                "#00FF00",
                "#00FFFF",
                "#0000FF",
                "#8B00FF",
            ]
        if not x_index:
            raise ValueError("缺少 x_index [横坐标值]...")
        self._x_interval = int((self.line_length - 70) / len(x_index))
        self._bar_width = int(30 * (1 - (len(x_index) + 10) / 100))
        # 没有 y_index 时自动生成
        if not y_index:
            _y_index = []
            _max_value = int(max(y))
            _max_value = ceil(
                _max_value / eval("1" + "0" * (len(str(_max_value)) - 1))
            ) * eval("1" + "0" * (len(str(_max_value)) - 1))
            _max_value = _max_value if _max_value >= 10 else 100
            _step = int(_max_value / 10)
            for i in range(_step, _max_value + _step, _step):
                _y_index.append(i)
            self.y_index = _y_index
        self._p = self.line_length / max(self.y_index)
        self._y_interval = int((self.line_length - 70) / len(self.y_index))

    def gen_graph(self):
        """
        说明:
            生成图像
        """
        self.markImg = self._init_graph(
            x_name=self.x_name,
            y_name=self.y_name,
            x_index=self.x_index,
            y_index=self.y_index,
            font_size=self.font_size,
            is_grid=self.is_grid,
        )
        if self.mat_type == "line":
            self._gen_line_graph(y=self.y, display_num=self.display_num)
        elif self.mat_type == "bar":
            self._gen_bar_graph(y=self.y, display_num=self.display_num)
        elif self.mat_type == "barh":
            self._gen_bar_graph(y=self.y, display_num=self.display_num, is_barh=True)

    def set_y(self, y: List[int]):
        """
        说明:
            给坐标点设置新值
        参数：
            :param y: 坐标点
        """
        self._check_value(y, self.y_index)
        self.y = y

    def set_y_index(self, y_index: List[Union[str, int, float]]):
        """
        说明:
            设置y轴坐标值
        参数：
            :param y_index: y轴坐标值
        """
        self._check_value(self.y, y_index)
        self.y_index = y_index

    def set_title(self, title: str, color: Optional[Union[str, Tuple[int, int, int]]]):
        """
        说明：
            设置标题
        参数：
            :param title: 标题
            :param color: 字体颜色
        """
        self.title = title
        if color:
            self._color["title"] = color

    def set_background(
        self, background: Optional[List[str]], type_: Optional[str] = None
    ):
        """
        说明：
            设置背景图片
        参数：
            :param background: 图片路径列表
            :param type_: 填充类型
        """
        self.background = background
        self.background_filler_type = type_ if type_ else self.background_filler_type

    def show(self):
        """
        说明：
            展示图像
        """
        self.markImg.show()

    def pic2bs4(self) -> str:
        """
        说明：
            转base64
        """
        return self.markImg.pic2bs4()

    def resize(self, ratio: float = 0.9):
        """
        说明：
            调整图像大小
        参数：
            :param ratio: 比例
        """
        self.markImg.resize(ratio)

    def save(self, path: Union[str, Path]):
        """
        说明：
            保存图片
        参数：
            :param path: 路径
        """
        self.markImg.save(path)

    def _check_value(
        self,
        y: List[int],
        y_index: List[Union[str, int, float]] = None,
        x_index: List[Union[str, int, float]] = None,
    ):
        """
        说明:
            检查值合法性
        参数：
            :param y: 坐标值
            :param y_index: y轴坐标值
            :param x_index: x轴坐标值
        """
        if y_index:
            _value = x_index if self.mat_type == "barh" else y_index
            if max(y) > max(y_index):
                raise ValueError("坐标点的值必须小于y轴坐标的最大值...")
            i = -9999999999
            for y in y_index:
                if y > i:
                    i = y
                else:
                    raise ValueError("y轴坐标值必须有序...")

    def _gen_line_graph(
        self,
        y: List[Union[int, float]],
        display_num: bool = False,
    ):
        """
        说明:
            生成折线图
        参数：
            :param y: 坐标点
            :param display_num: 显示该点的值
        """
        _black_point = BuildImage(7, 7, color=random.choice(self.bar_color))
        _black_point.circle()
        x_interval = self._x_interval
        current_w = self.padding_w + x_interval
        current_h = self.padding_h + self.line_length
        for i in range(len(y)):
            if display_num:
                w = int(self.markImg.getsize(str(y[i]))[0] / 2)
                self.markImg.text(
                    (
                        current_w - w,
                        current_h - int(y[i] * self._p * self._deviation) - 25 - 5,
                    ),
                    f"{y[i]:.2f}" if isinstance(y[i], float) else f"{y[i]}",
                )
            self.markImg.paste(
                _black_point,
                (
                    current_w - 3,
                    current_h - int(y[i] * self._p * self._deviation) - 3,
                ),
                True,
            )
            if i != len(y) - 1:
                self.markImg.line(
                    (
                        current_w,
                        current_h - int(y[i] * self._p * self._deviation),
                        current_w + x_interval,
                        current_h - int(y[i + 1] * self._p * self._deviation),
                    ),
                    fill=(0, 0, 0),
                    width=2,
                )
            current_w += x_interval

    def _gen_bar_graph(
        self,
        y: List[Union[int, float]],
        display_num: bool = False,
        is_barh: bool = False,
    ):
        """
        说明：
            生成柱状图
        参数：
            :param y: 坐标值
            :param display_num: 是否显示数值
            :param is_barh: 横柱状图
        """
        _interval = self._x_interval
        if is_barh:
            current_h = self.padding_h + self.line_length - _interval
            current_w = self.padding_w
        else:
            current_w = self.padding_w + _interval
            current_h = self.padding_h + self.line_length
        for i in range(len(y)):
            # 画出显示数字
            if display_num:
                # 横柱状图
                if is_barh:
                    font_h = self.markImg.getsize(str(y[i]))[1]
                    self.markImg.text(
                        (
                            self.padding_w
                            + int(y[i] * self._p * self._deviation)
                            + 2
                            + 5,
                            current_h - int(font_h / 2) - 1,
                        ),
                        f"{y[i]:.2f}" if isinstance(y[i], float) else f"{y[i]}",
                    )
                else:
                    w = int(self.markImg.getsize(str(y[i]))[0] / 2)
                    self.markImg.text(
                        (
                            current_w - w,
                            current_h - int(y[i] * self._p * self._deviation) - 25,
                        ),
                        f"{y[i]:.2f}" if isinstance(y[i], float) else f"{y[i]}",
                    )
            if i != len(y):
                bar_color = random.choice(self.bar_color)
                if is_barh:
                    A = BuildImage(
                        int(y[i] * self._p * self._deviation),
                        self._bar_width,
                        color=bar_color,
                    )
                    self.markImg.paste(
                        A,
                        (
                            current_w + 2,
                            current_h - int(self._bar_width / 2),
                        ),
                    )
                else:
                    A = BuildImage(
                        self._bar_width,
                        int(y[i] * self._p * self._deviation),
                        color=bar_color,
                    )
                    self.markImg.paste(
                        A,
                        (
                            current_w - int(self._bar_width / 2),
                            current_h - int(y[i] * self._p * self._deviation),
                        ),
                    )
            if is_barh:
                current_h -= _interval
            else:
                current_w += _interval

    def _init_graph(
        self,
        x_name: Optional[str] = None,
        y_name: Optional[str] = None,
        x_index: List[Union[str, int, float]] = None,
        y_index: List[Union[str, int, float]] = None,
        font_size: Optional[int] = None,
        is_grid: bool = False,
    ) -> BuildImage:
        """
        说明：
            初始化图像，生成xy轴
        参数：
            :param x_name: x轴名称
            :param y_name: y轴名称
            :param x_index: x轴坐标值
            :param y_index: y轴坐标值
            :param is_grid: 添加栅格
        """
        padding_w = self.padding_w
        padding_h = self.padding_h
        line_length = self.line_length
        background = random.choice(self.background) if self.background else None
        A = BuildImage(
            self.w, self.h, font_size=font_size, font=self.font, background=background
        )
        if background:
            _tmp = BuildImage(self.w, self.h)
            _tmp.transparent(2)
            A.paste(_tmp, alpha=True)
        if self.title:
            title = BuildImage(
                0,
                0,
                plain_text=self.title,
                color=(255, 255, 255, 0),
                font_size=35,
                font_color=self._color.get("title"),
                font=self.font,
            )
            A.paste(title, (0, 25), True, "by_width")
        A.line(
            (
                padding_w,
                padding_h + line_length,
                padding_w + line_length,
                padding_h + line_length,
            ),
            (0, 0, 0),
            2,
        )
        A.line(
            (
                padding_w,
                padding_h,
                padding_w,
                padding_h + line_length,
            ),
            (0, 0, 0),
            2,
        )
        _interval = self._x_interval
        if self.mat_type == "barh":
            tmp = x_index
            x_index = y_index
            y_index = tmp
            _interval = self._y_interval
        current_w = padding_w + _interval
        _text_font = BuildImage(0, 0, font_size=self.font_size, font=self.font)
        _grid = self.line_length if is_grid else 10
        x_rotate_height = 0
        for _x in x_index:
            _p = BuildImage(1, _grid, color="#a9a9a9")
            A.paste(_p, (current_w, padding_h + line_length - _grid))
            w = int(_text_font.getsize(f"{_x}")[0] / 2)
            text = BuildImage(
                0,
                0,
                plain_text=f"{_x}",
                font_size=self.font_size,
                color=(255, 255, 255, 0),
                font=self.font,
            )
            text.rotate(self.x_rotate, True)
            A.paste(text, (current_w - w, padding_h + line_length + 10), alpha=True)
            current_w += _interval
            x_rotate_height = text.h
        _interval = self._x_interval if self.mat_type == "barh" else self._y_interval
        current_h = padding_h + line_length - _interval
        _text_font = BuildImage(0, 0, font_size=self.font_size, font=self.font)
        for _y in y_index:
            _p = BuildImage(_grid, 1, color="#a9a9a9")
            A.paste(_p, (padding_w + 2, current_h))
            w, h = _text_font.getsize(f"{_y}")
            h = int(h / 2)
            text = BuildImage(
                0,
                0,
                plain_text=f"{_y}",
                font_size=self.font_size,
                color=(255, 255, 255, 0),
                font=self.font,
            )
            idx = 0
            while text.size[0] > self.padding_w - 10 and idx < 3:
                text = BuildImage(
                    0,
                    0,
                    plain_text=f"{_y}",
                    font_size=int(self.font_size * 0.75),
                    color=(255, 255, 255, 0),
                    font=self.font,
                )
                w, _ = text.getsize(f"{_y}")
                idx += 1
            A.paste(text, (padding_w - w - 10, current_h - h), alpha=True)
            current_h -= _interval
        if x_name:
            A.text((int(padding_w / 2), int(padding_w / 2)), x_name)
        if y_name:
            A.text(
                (
                    int(padding_w + line_length + 50 - A.getsize(y_name)[0]),
                    int(padding_h + line_length + 50 + x_rotate_height),
                ),
                y_name,
            )
        return A


async def text2image(
    text: str,
    auto_parse: bool = True,
    font_size: int = 20,
    color: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]] = "white",
    font: str = "CJGaoDeGuo.otf",
    font_color: Union[str, Tuple[int, int, int]] = "black",
    padding: Union[int, Tuple[int, int, int, int]] = 0,
) -> BuildImage:
    """
    说明：
        解析文本并转为图片
        使用标签
            <f> </f>
        可选配置项
            font: str -> 特殊文本字体
            fs / font_size: int -> 特殊文本大小
            fc / font_color: Union[str, Tuple[int, int, int]] -> 特殊文本颜色
        示例
            在不在，<f font=YSHaoShenTi-2.ttf font_size=30 font_color=red>HibiKi小姐</f>，
            你最近还好吗，<f font_size=15 font_color=black>我非常想你</f>，这段时间我非常不好过，
            <f font_size=25>抽卡抽不到金色</f>，这让我很痛苦
    参数：
        :param text: 文本
        :param auto_parse: 是否自动解析，否则原样发送
        :param font_size: 普通字体大小
        :param color: 背景颜色
        :param font: 普通字体
        :param font_color: 普通字体颜色
        :param padding: 文本外边距，元组类型时为 （上，左，下，右）
    """
    pw = ph = top_padding = left_padding = 0
    if padding:
        if isinstance(padding, int):
            pw = padding * 2
            ph = padding * 2
            top_padding = left_padding = padding
        elif isinstance(padding, tuple):
            pw = padding[0] + padding[2]
            ph = padding[1] + padding[3]
            top_padding = padding[0]
            left_padding = padding[1]
    if auto_parse and re.search(r"<f(.*)>(.*)</f>", text):
        _data = []
        new_text = ""
        placeholder_index = 0
        for s in text.split("</f>"):
            r = re.search(r"<f(.*)>(.*)", s)
            if r:
                start, end = r.span()
                if start != 0 and (t := s[:start]):
                    new_text += t
                _data.append(
                    [
                        (start, end),
                        f"[placeholder_{placeholder_index}]",
                        r.group(1).strip(),
                        r.group(2),
                    ]
                )
                new_text += f"[placeholder_{placeholder_index}]"
                placeholder_index += 1
        new_text += text.split("</f>")[-1]
        image_list = []
        current_placeholder_index = 0
        # 切分换行，每行为单张图片
        for s in new_text.split("\n"):
            _tmp_text = s
            img_height = BuildImage(0, 0, font_size=font_size).getsize("正")[1]
            img_width = 0
            _tmp_index = current_placeholder_index
            for _ in range(s.count("[placeholder_")):
                placeholder = _data[_tmp_index]
                if "font_size" in placeholder[2]:
                    r = re.search(r"font_size=['\"]?(\d+)", placeholder[2])
                    if r:
                        w, h = BuildImage(0, 0, font_size=int(r.group(1))).getsize(
                            placeholder[3]
                        )
                        img_height = img_height if img_height > h else h
                        img_width += w
                else:
                    img_width += BuildImage(0, 0, font_size=font_size).getsize(
                        placeholder[3]
                    )[0]
                _tmp_text = _tmp_text.replace(f"[placeholder_{_tmp_index}]", "")
                _tmp_index += 1
            img_width += BuildImage(0, 0, font_size=font_size).getsize(_tmp_text)[0]
            # img_width += len(_tmp_text) * font_size
            # 开始画图
            A = BuildImage(
                img_width, img_height, color=color, font=font, font_size=font_size
            )
            basic_font_h = A.getsize("正")[1]
            current_width = 0
            # 遍历占位符
            for _ in range(s.count("[placeholder_")):
                if not s.startswith(f"[placeholder_{current_placeholder_index}]"):
                    slice_ = s.split(f"[placeholder_{current_placeholder_index}]")
                    await A.atext(
                        (current_width, A.h - basic_font_h - 1), slice_[0], font_color
                    )
                    current_width += A.getsize(slice_[0])[0]
                placeholder = _data[current_placeholder_index]
                # 解析配置
                _font = font
                _font_size = font_size
                _font_color = font_color
                for e in placeholder[2].split():
                    if e.startswith("font="):
                        _font = e.split("=")[-1]
                    if e.startswith("font_size=") or e.startswith("fs="):
                        _font_size = int(e.split("=")[-1])
                        if _font_size > 1000:
                            _font_size = 1000
                        if _font_size < 1:
                            _font_size = 1
                    if e.startswith("font_color") or e.startswith("fc="):
                        _font_color = e.split("=")[-1]
                text_img = BuildImage(
                    0,
                    0,
                    plain_text=placeholder[3],
                    font_size=_font_size,
                    font_color=_font_color,
                    font=_font,
                )
                _img_h = (
                    int(A.h / 2 - text_img.h / 2)
                    if new_text == "[placeholder_0]"
                    else A.h - text_img.h
                )
                await A.apaste(text_img, (current_width, _img_h - 1), True)
                current_width += text_img.w
                s = s[
                    s.index(f"[placeholder_{current_placeholder_index}]")
                    + len(f"[placeholder_{current_placeholder_index}]") :
                ]
                current_placeholder_index += 1
            if s:
                slice_ = s.split(f"[placeholder_{current_placeholder_index}]")
                await A.atext((current_width, A.h - basic_font_h), slice_[0])
                current_width += A.getsize(slice_[0])[0]
            A.crop((0, 0, current_width, A.h))
            # A.show()
            image_list.append(A)
        height = 0
        width = 0
        for img in image_list:
            height += img.h
            width = width if width > img.w else img.w
        width += pw
        height += ph
        A = BuildImage(width + left_padding, height + top_padding, color=color)
        current_height = top_padding
        for img in image_list:
            await A.apaste(img, (left_padding, current_height), True)
            current_height += img.h
    else:
        width = 0
        height = 0
        _tmp = BuildImage(0, 0, font_size=font_size)
        for x in text.split("\n"):
            w, h = _tmp.getsize(x)
            height += h
            width = width if width > w else w
        width += pw
        height += ph
        A = BuildImage(
            width + left_padding,
            height + top_padding,
            font_size=font_size,
            color=color,
            font=font,
        )
        await A.atext((left_padding, top_padding), text, font_color)
    # A.show()
    return A


if __name__ == "__main__":
    pass
