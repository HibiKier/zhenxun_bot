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


class BaChar(BaseData):
    pass


class BaHandle(BaseHandle[BaChar]):
    def __init__(self):
        super().__init__("ba", "碧蓝档案")
        self.max_star = 3
        self.config = draw_config.ba
        self.ALL_CHAR: List[BaChar] = []

    def get_card(self, mode: int = 1) -> BaChar:
        if mode == 2:
            star = self.get_star(
                [3, 2], [self.config.BA_THREE_P, self.config.BA_G_TWO_P]
            )
        else:
            star = self.get_star(
                [3, 2, 1],
                [self.config.BA_THREE_P, self.config.BA_TWO_P, self.config.BA_ONE_P],
            )
        chars = [x for x in self.ALL_CHAR if x.star == star and not x.limited]
        return random.choice(chars)

    def get_cards(self, count: int, **kwargs) -> List[Tuple[BaChar, int]]:
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

    def generate_card_img(self, card: BaChar) -> BuildImage:
        sep_w = 5
        sep_h = 5
        star_h = 15
        img_w = 90
        img_h = 100
        font_h = 20
        bar_h = 20
        bar_w = 90
        bg = BuildImage(img_w + sep_w * 2, img_h + font_h + sep_h * 2, color="#EFF2F5")
        img_path = str(self.img_path / f"{cn2py(card.name)}.png")
        img = BuildImage(img_w, img_h, background=img_path)
        bar = BuildImage(bar_w, bar_h, color="#6495ED")
        bg.paste(img, (sep_w, sep_h), alpha=True)
        bg.paste(bar, (sep_w, img_h - bar_h + sep_h), alpha=True)
        if (card.star == 1):
            star_path = str(self.img_path / "star-1.png")
            star_w = 15
        elif (card.star == 2):
            star_path = str(self.img_path / "star-2.png")
            star_w = 30
        else:
            star_path = str(self.img_path / "star-3.png")
            star_w = 45
        star = BuildImage(star_w, star_h, background=star_path)
        bg.paste(star, (img_w // 2 - 15 * (card.star - 1) // 2, img_h - star_h), alpha=True)
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
            BaChar(
                name=value["名称"],
                star=int(value["星级"]),
                limited=True if "（" in key else False,
            )
            for key, value in self.load_data().items()
        ]
    
    def title2star(self, title: int):
        if title == 'Star-3.png':
            return 3
        elif title == 'Star-2.png':
            return 2
        else:
            return 1

    async def _update_info(self):
        info = {}
        url = "https://wiki.biligame.com/bluearchive/学生筛选"
        result = await self.get_url(url)
        if not result:
            logger.warning(f"更新 {self.game_name_cn} 出错")
            return
        else:
            dom = etree.HTML(result, etree.HTMLParser())
            char_list = dom.xpath("//div[@class='filters']/table[2]/tbody/tr")
            for char in char_list:
                try:
                    name = char.xpath("./td[2]/a/div/text()")[0]
                    avatar = char.xpath("./td[1]/div/div/a/img/@data-src")[0]
                    star_pic = char.xpath("./td[4]/img/@alt")[0]
                except IndexError:
                    continue
                member_dict = {
                    "头像": unquote(str(avatar)),
                    "名称": remove_prohibited_str(name),
                    "星级": self.title2star(star_pic),
                }
                info[member_dict["名称"]] = member_dict
        self.dump_data(info)
        logger.info(f"{self.game_name_cn} 更新成功")
        # 下载头像
        for value in info.values():
            await self.download_img(value["头像"], value["名称"])
        # 下载星星
        await self.download_img(
            "https://patchwiki.biligame.com/images/bluearchive/thumb/e/e0/82nj2x9sxko473g7782r14fztd4zyky.png/15px-Star-1.png",
            "star-1",
        )
        await self.download_img(
            "https://patchwiki.biligame.com/images/bluearchive/thumb/0/0b/msaff2g0zk6nlyl1rrn7n1ri4yobcqc.png/30px-Star-2.png",
            "star-2",
        )
        await self.download_img(
            "https://patchwiki.biligame.com/images/bluearchive/thumb/8/8a/577yv79x1rwxk8efdccpblo0lozl158.png/46px-Star-3.png",
            "star-3"
        )