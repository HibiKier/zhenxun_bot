import re
import random
import dateparser
from lxml import etree
from PIL import ImageDraw
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import unquote
from typing import List, Optional, Tuple
from pydantic import ValidationError
from nonebot.adapters.onebot.v11 import Message
from utils.message_builder import image
from nonebot.log import logger
import asyncio

try:
    import ujson as json
except ModuleNotFoundError:
    import json

from .base_handle import BaseHandle, BaseData, UpChar, UpEvent
from ..config import draw_config
from ..util import remove_prohibited_str, cn2py, load_font
from utils.image_utils import BuildImage


class Operator(BaseData):
    recruit_only: bool  # 公招限定
    event_only: bool  # 活动获得干员
    # special_only: bool  # 升变/异格干员


class PrtsHandle(BaseHandle[Operator]):
    def __init__(self):
        super().__init__("prts", "明日方舟", "#eff2f5")
        self.max_star = 6
        self.config = draw_config.prts

        self.ALL_OPERATOR: List[Operator] = []
        self.UP_EVENT: Optional[UpEvent] = None

    def get_card(self, add: float) -> Operator:
        star = self.get_star(
            [6, 5, 4, 3],
            [
                self.config.PRTS_SIX_P + add,
                self.config.PRTS_FIVE_P,
                self.config.PRTS_FOUR_P,
                self.config.PRTS_THREE_P,
            ],
        )

        all_operators = [
            x
            for x in self.ALL_OPERATOR
            if x.star == star and not any([x.limited, x.event_only, x.recruit_only])
        ]
        acquire_operator = None

        if self.UP_EVENT:
            up_operators = [x for x in self.UP_EVENT.up_char if x.star == star]
            # UPs
            try:
                zooms = [x.zoom for x in up_operators]
                zoom_sum = sum(zooms)
                if random.random() < zoom_sum:
                    up_name = random.choices(up_operators, weights=zooms, k=1)[0].name
                    acquire_operator = [
                        x for x in self.ALL_OPERATOR if x.name == up_name
                    ][0]
            except IndexError:
                pass
        if not acquire_operator:
            acquire_operator = random.choice(all_operators)
        return acquire_operator

    def get_cards(self, count: int) -> List[Tuple[Operator, int]]:
        card_list = []  # 获取所有角色
        add = 0.0
        count_idx = 0
        for i in range(count):
            count_idx += 1
            card = self.get_card(add)
            if card.star == self.max_star:
                add = 0.0
                count_idx = 0
            elif count_idx > 50:
                add += 0.02
            card_list.append((card, i + 1))
        return card_list

    def format_pool_info(self) -> str:
        info = ""
        if self.UP_EVENT:
            star6_list = [x.name for x in self.UP_EVENT.up_char if x.star == 6]
            star5_list = [x.name for x in self.UP_EVENT.up_char if x.star == 5]
            star4_list = [x.name for x in self.UP_EVENT.up_char if x.star == 4]
            if star6_list:
                info += f"六星UP：{' '.join(star6_list)}\n"
            if star5_list:
                info += f"五星UP：{' '.join(star5_list)}\n"
            if star4_list:
                info += f"四星UP：{' '.join(star4_list)}\n"
            info = f"当前up池: {self.UP_EVENT.title}\n{info}"
        return info.strip()

    async def draw(self, count: int, **kwargs) -> Message:
        return await asyncio.get_event_loop().run_in_executor(None, self._draw, count)

    def _draw(self, count: int, **kwargs) -> Message:
        index2card = self.get_cards(count)
        cards = [card[0] for card in self.get_cards(count)]
        up_list = [x.name for x in self.UP_EVENT.up_char] if self.UP_EVENT else []
        result = self.format_result(index2card, up_list=up_list)
        pool_info = self.format_pool_info()
        return pool_info + image(b64=self.generate_img(cards).pic2bs4()) + result

    def generate_card_img(self, card: Operator) -> BuildImage:
        sep_w = 5
        sep_h = 5
        star_h = 15
        img_w = 120
        img_h = 120
        font_h = 20
        bg = BuildImage(img_w + sep_w * 2, img_h + font_h + sep_h * 2, color="#EFF2F5")
        star_path = str(self.img_path / "star.png")
        star = BuildImage(star_h, star_h, background=star_path)
        img_path = str(self.img_path / f"{cn2py(card.name)}.png")
        img = BuildImage(img_w, img_h, background=img_path)
        bg.paste(img, (sep_w, sep_h), alpha=True)
        for i in range(card.star):
            bg.paste(star, (sep_w + img_w - 5 - star_h * (i + 1), sep_h), alpha=True)
        # 加名字
        text = card.name[:7] + "..." if len(card.name) > 8 else card.name
        font = load_font(fontsize=16)
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
        self.ALL_OPERATOR = [
            Operator(
                name=value["名称"],
                star=int(value["星级"]),
                limited="干员寻访" not in value["获取途径"],
                recruit_only=True
                if "干员寻访" not in value["获取途径"] and "公开招募" in value["获取途径"]
                else False,
                event_only=True if "活动获取" in value["获取途径"] else False,
            )
            for key, value in self.load_data().items()
            if "阿米娅" not in key
        ]
        self.load_up_char()

    def load_up_char(self):
        try:
            data = self.load_data(f"draw_card_up/{self.game_name}_up_char.json")
            self.UP_EVENT = UpEvent.parse_obj(data.get("char", {}))
        except ValidationError:
            logger.warning(f"{self.game_name}_up_char 解析出错")

    def dump_up_char(self):
        if self.UP_EVENT:
            data = {"char": json.loads(self.UP_EVENT.json())}
            self.dump_data(data, f"draw_card_up/{self.game_name}_up_char.json")

    async def _update_info(self):
        info = {}
        url = "https://wiki.biligame.com/arknights/干员数据表"
        result = await self.get_url(url)
        if not result:
            logger.warning(f"更新 {self.game_name_cn} 出错")
            return
        dom = etree.HTML(result, etree.HTMLParser())
        char_list = dom.xpath("//table[@id='CardSelectTr']/tbody/tr")
        for char in char_list:
            try:
                avatar = char.xpath("./td[1]/div/div/div/a/img/@srcset")[0]
                name = char.xpath("./td[2]/a/text()")[0]
                star = char.xpath("./td[5]/text()")[0]
                sources = str(char.xpath("./td[8]/text()")[0]).split("\n")
            except IndexError:
                continue
            member_dict = {
                "头像": unquote(str(avatar).split(" ")[-2]),
                "名称": remove_prohibited_str(str(name).strip()),
                "星级": int(str(star).strip()),
                "获取途径": [s for s in sources if s],
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
        await self.update_up_char()

    async def update_up_char(self):
        announcement_url = "https://ak.hypergryph.com/news.html"
        result = await self.get_url(announcement_url)
        if not result:
            logger.warning(f"{self.game_name_cn}获取公告出错")
            return
        dom = etree.HTML(result, etree.HTMLParser())
        activity_urls = dom.xpath(
            "//ol[@class='articleList' and @data-category-key='ACTIVITY']/li/a/@href"
        )
        start_time = None
        end_time = None
        up_chars = []
        pool_img = ""
        title = ""
        for activity_url in activity_urls:
            activity_url = f"https://ak.hypergryph.com{activity_url}"
            result = await self.get_url(activity_url)
            if not result:
                logger.warning(f"{self.game_name_cn}获取公告 {activity_url} 出错")
                continue
            soup = BeautifulSoup(result, "lxml")
            contents = soup.find_all("p")
            for index, content in enumerate(contents):
                if re.search("(.*)(寻访|复刻).*?开启", content.text):
                    title = content.text
                    if "【" in title and "】" in title:
                        title = re.split(r"[【】]", title)[1]
                    lines = [str(contents[index + i + 1].text) for i in range(5)]
                    time = ""
                    chars: List[str] = []
                    for line in lines:
                        match = re.search(
                            r"(\d{1,2}月\d{1,2}日.*?-.*?\d{1,2}月\d{1,2}日.*?$)", line
                        )
                        if match:
                            time = match.group(1)
                        if "★" in line:
                            chars.append(line)
                    if not time:
                        continue
                    start, end = time.replace("月", "/").replace("日", "").split("-")[:2]
                    start_time = dateparser.parse(start)
                    end_time = dateparser.parse(end)
                    pool_img = content.find_previous("img")["src"]
                    for char in chars:
                        star = char.split("（")[0].count("★")
                        name = re.split(r"[：（]", char)[1]
                        names = name.split("/") if "/" in name else [name]
                        names = [name.replace("[限定]", "").strip() for name in names]
                        if "权值" in char:
                            match = re.search(r"（在.*?以.*?(\d+).*?倍权值.*?）", char)
                        else:
                            match = re.search(r"（占.*?的.*?(\d+).*?%）", char)
                        zoom = 1
                        if match:
                            zoom = float(match.group(1))
                            zoom = zoom / 100 if zoom > 10 else zoom
                        for name in names:
                            up_chars.append(
                                UpChar(name=name, star=star, limited=False, zoom=zoom)
                            )
                    break
            if title and start_time and end_time:
                if start_time <= datetime.now() <= end_time:
                    self.UP_EVENT = UpEvent(
                        title=title,
                        pool_img=pool_img,
                        start_time=start_time,
                        end_time=end_time,
                        up_char=up_chars,
                    )
                    self.dump_up_char()
                    logger.info(f"成功获取{self.game_name_cn}当前up信息...当前up池: {title}")
                break

    async def _reload_pool(self) -> Optional[Message]:
        await self.update_up_char()
        self.load_up_char()
        if self.UP_EVENT:
            return f"重载成功！\n当前UP池子：{self.UP_EVENT.title}" + image(
                self.UP_EVENT.pool_img
            )
