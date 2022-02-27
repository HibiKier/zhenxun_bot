import random
from lxml import etree
from typing import List, Tuple
from PIL import ImageDraw
from urllib.parse import unquote
from nonebot.log import logger

from .base_handle import BaseHandle, BaseData
from ..config import draw_config
from ..util import remove_prohibited_str, cn2py, load_font
from utils.image_utils import BuildImage


class PcrChar(BaseData):
    pass


class PcrHandle(BaseHandle[PcrChar]):
    def __init__(self):
        super().__init__("pcr", "公主连结")
        self.max_star = 3
        self.config = draw_config.pcr
        self.ALL_CHAR: List[PcrChar] = []

    def get_card(self, mode: int = 1) -> PcrChar:
        if mode == 2:
            star = self.get_star(
                [3, 2], [self.config.PCR_G_THREE_P, self.config.PCR_G_TWO_P]
            )
        else:
            star = self.get_star(
                [3, 2, 1],
                [self.config.PCR_THREE_P, self.config.PCR_TWO_P, self.config.PCR_ONE_P],
            )
        chars = [x for x in self.ALL_CHAR if x.star == star and not x.limited]
        return random.choice(chars)

    def get_cards(self, count: int, **kwargs) -> List[Tuple[PcrChar, int]]:
        card_list = []
        card_count = 0  # 保底计算
        for i in range(count):
            card_count += 1
            # 十连保底
            if card_count == 10:
                card = self.get_card(2)
                card_count = 0
            else:
                card = self.get_card(1)
                if card.star > self.max_star - 2:
                    card_count = 0
            card_list.append((card, i + 1))
        return card_list

    def generate_card_img(self, card: PcrChar) -> BuildImage:
        sep_w = 5
        sep_h = 5
        star_h = 15
        img_w = 90
        img_h = 90
        font_h = 20
        bg = BuildImage(img_w + sep_w * 2, img_h + font_h + sep_h * 2, color="#EFF2F5")
        star_path = str(self.img_path / "star.png")
        star = BuildImage(star_h, star_h, background=star_path)
        img_path = str(self.img_path / f"{cn2py(card.name)}.png")
        img = BuildImage(img_w, img_h, background=img_path)
        bg.paste(img, (sep_w, sep_h), alpha=True)
        for i in range(card.star):
            bg.paste(star, (sep_w + img_w - star_h * (i + 1), sep_h), alpha=True)
        # 加名字
        text = card.name[:5] + "..." if len(card.name) > 6 else card.name
        font = load_font(fontsize=14)
        text_w, text_h = font.getsize(text)
        draw = ImageDraw.Draw(bg.markImg)
        draw.text(
            (sep_w + (img_w - text_w) / 2, sep_h + img_h + (font_h - text_h) / 2),
            text,
            font=font,
            fill="gray",
        )
        return bg

    def _init_data(self):
        self.ALL_CHAR = [
            PcrChar(
                name=value["名称"],
                star=int(value["星级"]),
                limited=True if "（" in key else False,
            )
            for key, value in self.load_data().items()
        ]

    async def _update_info(self):
        info = {}
        if draw_config.PCR_TAI:
            url = "https://wiki.biligame.com/pcr/角色图鉴"
            result = await self.get_url(url)
            if not result:
                logger.warning(f"更新 {self.game_name_cn} 出错")
                return
            dom = etree.HTML(result, etree.HTMLParser())
            char_list = dom.xpath(
                "//div[@class='resp-tab-content']/div[@class='unit-icon']"
            )
            for char in char_list:
                try:
                    name = char.xpath("./a/@title")[0]
                    avatar = char.xpath("./a/img/@srcset")[0]
                    star = len(char.xpath("./div[1]/img"))
                except IndexError:
                    continue
                member_dict = {
                    "头像": unquote(str(avatar).split(" ")[-2]),
                    "名称": remove_prohibited_str(name),
                    "星级": star,
                }
                info[member_dict["名称"]] = member_dict
        else:
            url = "https://wiki.biligame.com/pcr/角色筛选表"
            result = await self.get_url(url)
            if not result:
                logger.warning(f"更新 {self.game_name_cn} 出错")
                return
            dom = etree.HTML(result, etree.HTMLParser())
            char_list = dom.xpath("//table[@id='CardSelectTr']/tbody/tr")
            for char in char_list:
                try:
                    name = char.xpath("./td[1]/a/@title")[0]
                    avatar = char.xpath("./td[1]/a/img/@srcset")[0]
                    star = char.xpath("./td[4]/text()")[0]
                except IndexError:
                    continue
                member_dict = {
                    "头像": unquote(str(avatar).split(" ")[-2]),
                    "名称": remove_prohibited_str(name),
                    "星级": int(str(star).strip()),
                }
                info[member_dict["名称"]] = member_dict
        self.dump_data(info)
        logger.info(f"{self.game_name_cn} 更新成功")
        # 下载头像
        for value in info.values():
            await self.download_img(value["头像"], value["名称"])
        # 下载星星
        await self.download_img(
            "https://patchwiki.biligame.com/images/pcr/0/02/s75ys2ecqhu2xbdw1wf1v9ccscnvi5g.png",
            "star",
        )
