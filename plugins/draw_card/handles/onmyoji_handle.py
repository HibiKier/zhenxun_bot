import random
from lxml import etree
from typing import List, Tuple
from nonebot.log import logger
from PIL import Image, ImageDraw
from PIL.Image import Image as IMG

try:
    import ujson as json
except ModuleNotFoundError:
    import json

from .base_handle import BaseHandle, BaseData
from ..config import draw_config
from ..util import remove_prohibited_str, cn2py, load_font
from utils.image_utils import BuildImage


class OnmyojiChar(BaseData):
    @property
    def star_str(self) -> str:
        return ["N", "R", "SR", "SSR", "SP"][self.star - 1]


class OnmyojiHandle(BaseHandle[OnmyojiChar]):
    def __init__(self):
        super().__init__("onmyoji", "阴阳师")
        self.max_star = 5
        self.config = draw_config.onmyoji
        self.ALL_CHAR: List[OnmyojiChar] = []

    def get_card(self, **kwargs) -> OnmyojiChar:
        star = self.get_star(
            [5, 4, 3, 2],
            [
                self.config.ONMYOJI_SP,
                self.config.ONMYOJI_SSR,
                self.config.ONMYOJI_SR,
                self.config.ONMYOJI_R,
            ],
        )
        chars = [x for x in self.ALL_CHAR if x.star == star and not x.limited]
        return random.choice(chars)

    def format_max_star(self, card_list: List[Tuple[OnmyojiChar, int]]) -> str:
        rst = ""
        for card, index in card_list:
            if card.star == self.max_star:
                rst += f"第 {index} 抽获取SP {card.name}\n"
            elif card.star == self.max_star - 1:
                rst += f"第 {index} 抽获取SSR {card.name}\n"
        return rst.strip()

    @staticmethod
    def star_label(star: int) -> IMG:
        text, color1, color2 = [
            ("N", "#7E7E82", "#F5F6F7"),
            ("R", "#014FA8", "#37C6FD"),
            ("SR", "#6E0AA4", "#E94EFD"),
            ("SSR", "#E5511D", "#FAF905"),
            ("SP", "#FA1F2D", "#FFBBAF"),
        ][star - 1]
        w = 200
        h = 110
        # 制作渐变色图片
        base = Image.new("RGBA", (w, h), color1)
        top = Image.new("RGBA", (w, h), color2)
        mask = Image.new("L", (w, h))
        mask_data = []
        for y in range(h):
            mask_data.extend([int(255 * (y / h))] * w)
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        # 透明图层
        font = load_font("gorga.otf", 100)
        alpha = Image.new("L", (w, h))
        draw = ImageDraw.Draw(alpha)
        draw.text((20, -30), text, fill="white", font=font)
        base.putalpha(alpha)
        # stroke
        bg = Image.new("RGBA", (w, h))
        draw = ImageDraw.Draw(bg)
        draw.text(
            (20, -30),
            text,
            font=font,
            fill="gray",
            stroke_width=3,
            stroke_fill="gray",
        )
        bg.paste(base, (0, 0), base)
        return bg

    def generate_img(self, card_list: List[OnmyojiChar]) -> BuildImage:
        return super().generate_img(card_list, num_per_line=10)

    def generate_card_img(self, card: OnmyojiChar) -> BuildImage:
        bg = BuildImage(73, 240, color="#F1EFE9")
        img_path = str(self.img_path / f"{cn2py(card.name)}_mark_btn.png")
        img = BuildImage(0, 0, background=img_path)
        img = Image.open(img_path).convert("RGBA")
        label = self.star_label(card.star).resize((60, 33), Image.ANTIALIAS)
        bg.paste(img, (0, 0), alpha=True)
        bg.paste(label, (0, 135), alpha=True)
        font = load_font("msyh.ttf", 16)
        draw = ImageDraw.Draw(bg.markImg)
        text = "\n".join([t for t in card.name[:4]])
        _, text_h = font.getsize_multiline(text, spacing=0)
        draw.text(
            (40, 150 + (90 - text_h) / 2), text, font=font, fill="gray", spacing=0
        )
        return bg

    def _init_data(self):
        self.ALL_CHAR = [
            OnmyojiChar(
                name=value["名称"],
                star=["N", "R", "SR", "SSR", "SP"].index(value["星级"]) + 1,
                limited=True
                if key
                in [
                    "奴良陆生",
                    "卖药郎",
                    "鬼灯",
                    "阿香",
                    "蜜桃&芥子",
                    "犬夜叉",
                    "杀生丸",
                    "桔梗",
                    "朽木露琪亚",
                    "黑崎一护",
                    "灶门祢豆子",
                    "灶门炭治郎",
                ]
                else False,
            )
            for key, value in self.load_data().items()
        ]

    async def _update_info(self):
        info = {}
        url = "https://yys.res.netease.com/pc/zt/20161108171335/js/app/all_shishen.json?v74="
        result = await self.get_url(url)
        if not result:
            logger.warning(f"更新 {self.game_name_cn} 出错")
            return
        data = json.loads(result)
        for x in data:
            name = remove_prohibited_str(x["name"])
            member_dict = {
                "id": x["id"],
                "名称": name,
                "星级": x["level"],
            }
            info[name] = member_dict
            # logger.info(f"{name} is update...")
        # 更新头像
        for key in info.keys():
            url = f'https://yys.163.com/shishen/{info[key]["id"]}.html'
            result = await self.get_url(url)
            if not result:
                info[key]["头像"] = ""
                continue
            try:
                dom = etree.HTML(result, etree.HTMLParser())
                avatar = dom.xpath("//div[@class='pic_wrap']/img/@src")[0]
                avatar = "https:" + avatar
                info[key]["头像"] = avatar
            except IndexError:
                info[key]["头像"] = ""
                logger.warning(f"{self.game_name_cn} 获取头像错误 {key}")
        self.dump_data(info)
        logger.info(f"{self.game_name_cn} 更新成功")
        # 下载头像
        for value in info.values():
            await self.download_img(value["头像"], value["名称"])
            # 下载书签形式的头像
            url = f"https://yys.res.netease.com/pc/zt/20161108171335/data/mark_btn/{value['id']}.png"
            await self.download_img(url, value["名称"] + "_mark_btn")
