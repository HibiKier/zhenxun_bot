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


class PrettyData(BaseData):
    pass


class PrettyChar(PrettyData):
    pass


class PrettyCard(PrettyData):
    @property
    def star_str(self) -> str:
        return ["R", "SR", "SSR"][self.star - 1]


class PrettyHandle(BaseHandle[PrettyData]):
    def __init__(self):
        super().__init__("pretty", "赛马娘", "#eff2f5")
        self.data_files.append("pretty_card.json")
        self.max_star = 3
        self.config = draw_config.pretty

        self.ALL_CHAR: List[PrettyChar] = []
        self.ALL_CARD: List[PrettyCard] = []
        self.UP_CHAR: Optional[UpEvent] = None
        self.UP_CARD: Optional[UpEvent] = None

    def get_card(self, pool_name: str, mode: int = 1) -> PrettyData:
        if mode == 1:
            star = self.get_star(
                [3, 2, 1],
                [
                    self.config.PRETTY_THREE_P,
                    self.config.PRETTY_TWO_P,
                    self.config.PRETTY_ONE_P,
                ],
            )
        else:
            star = self.get_star(
                [3, 2], [self.config.PRETTY_THREE_P, self.config.PRETTY_TWO_P]
            )
        up_pool = None
        if pool_name == "char":
            up_pool = self.UP_CHAR
            all_list = self.ALL_CHAR
        else:
            up_pool = self.UP_CARD
            all_list = self.ALL_CARD

        all_char = [x for x in all_list if x.star == star and not x.limited]
        acquire_char = None
        # 有UP池子
        if up_pool and star in [x.star for x in up_pool.up_char]:
            up_list = [x.name for x in up_pool.up_char if x.star == star]
            # 抽到UP
            if random.random() < 1 / len(all_char) * (0.7 / 0.1385):
                up_name = random.choice(up_list)
                try:
                    acquire_char = [x for x in all_list if x.name == up_name][0]
                except IndexError:
                    pass
        if not acquire_char:
            acquire_char = random.choice(all_char)
        return acquire_char

    def get_cards(self, count: int, pool_name: str) -> List[Tuple[PrettyData, int]]:
        card_list = []
        card_count = 0  # 保底计算
        for i in range(count):
            card_count += 1
            # 十连保底
            if card_count == 10:
                card = self.get_card(pool_name, 2)
                card_count = 0
            else:
                card = self.get_card(pool_name, 1)
                if card.star > self.max_star - 2:
                    card_count = 0
            card_list.append((card, i + 1))
        return card_list

    def format_pool_info(self, pool_name: str) -> str:
        info = ""
        up_event = self.UP_CHAR if pool_name == "char" else self.UP_CARD
        if up_event:
            star3_list = [x.name for x in up_event.up_char if x.star == 3]
            star2_list = [x.name for x in up_event.up_char if x.star == 2]
            star1_list = [x.name for x in up_event.up_char if x.star == 1]
            if star3_list:
                if pool_name == "char":
                    info += f'三星UP：{" ".join(star3_list)}\n'
                else:
                    info += f'SSR UP：{" ".join(star3_list)}\n'
            if star2_list:
                if pool_name == "char":
                    info += f'二星UP：{" ".join(star2_list)}\n'
                else:
                    info += f'SR UP：{" ".join(star2_list)}\n'
            if star1_list:
                if pool_name == "char":
                    info += f'一星UP：{" ".join(star1_list)}\n'
                else:
                    info += f'R UP：{" ".join(star1_list)}\n'
            info = f"当前up池：{up_event.title}\n{info}"
        return info.strip()

    async def draw(self, count: int, pool_name: str, **kwargs) -> Message:
        return await asyncio.get_event_loop().run_in_executor(None, self._draw, count, pool_name)

    def _draw(self, count: int, pool_name: str, **kwargs) -> Message:
        pool_name = "char" if not pool_name else pool_name
        index2card = self.get_cards(count, pool_name)
        cards = [card[0] for card in index2card]
        up_event = self.UP_CHAR if pool_name == "char" else self.UP_CARD
        up_list = [x.name for x in up_event.up_char] if up_event else []
        result = self.format_result(index2card, up_list=up_list)
        pool_info = self.format_pool_info(pool_name)
        return pool_info + image(b64=self.generate_img(cards).pic2bs4()) + result

    def generate_card_img(self, card: PrettyData) -> BuildImage:
        if isinstance(card, PrettyChar):
            star_h = 30
            img_w = 200
            img_h = 219
            font_h = 50
            bg = BuildImage(img_w, img_h + font_h, color="#EFF2F5")
            star_path = str(self.img_path / "star.png")
            star = BuildImage(star_h, star_h, background=star_path)
            img_path = str(self.img_path / f"{cn2py(card.name)}.png")
            img = BuildImage(img_w, img_h, background=img_path)
            star_w = star_h * card.star
            for i in range(card.star):
                bg.paste(star, (int((img_w - star_w) / 2) + star_h * i, 0), alpha=True)
            bg.paste(img, (0, 0), alpha=True)
            # 加名字
            text = card.name[:5] + "..." if len(card.name) > 6 else card.name
            font = load_font(fontsize=30)
            text_w, _ = font.getsize(text)
            draw = ImageDraw.Draw(bg.markImg)
            draw.text(
                ((img_w - text_w) / 2, img_h),
                text,
                font=font,
                fill="gray",
            )
            return bg
        else:
            sep_w = 10
            img_w = 200
            img_h = 267
            font_h = 75
            bg = BuildImage(img_w + sep_w * 2, img_h + font_h, color="#EFF2F5")
            label_path = str(self.img_path / f"{card.star}_label.png")
            label = BuildImage(40, 40, background=label_path)
            img_path = str(self.img_path / f"{cn2py(card.name)}.png")
            img = BuildImage(img_w, img_h, background=img_path)
            bg.paste(img, (sep_w, 0), alpha=True)
            bg.paste(label, (30, 3), alpha=True)
            # 加名字
            text = ""
            texts = []
            font = load_font(fontsize=25)
            for t in card.name:
                if font.getsize(text + t)[0] > 190:
                    texts.append(text)
                    text = ""
                    if len(texts) >= 2:
                        texts[-1] += "..."
                        break
                else:
                    text += t
            if text:
                texts.append(text)
            text = "\n".join(texts)
            text_w, _ = font.getsize_multiline(text)
            draw = ImageDraw.Draw(bg.markImg)
            draw.text(
                ((img_w - text_w) / 2, img_h),
                text,
                font=font,
                align="center",
                fill="gray",
            )
            return bg

    def _init_data(self):
        self.ALL_CHAR = [
            PrettyChar(
                name=value["名称"],
                star=int(value["初始星级"]),
                limited=False,
            )
            for value in self.load_data().values()
        ]
        self.ALL_CARD = [
            PrettyCard(
                name=value["中文名"],
                star=["R", "SR", "SSR"].index(value["稀有度"]) + 1,
                limited=True if "卡池" not in value["获取方式"] else False,
            )
            for value in self.load_data("pretty_card.json").values()
        ]
        self.load_up_char()

    def load_up_char(self):
        try:
            data = self.load_data(f"draw_card_up/{self.game_name}_up_char.json")
            self.UP_CHAR = UpEvent.parse_obj(data.get("char", {}))
            self.UP_CARD = UpEvent.parse_obj(data.get("card", {}))
        except ValidationError:
            logger.warning(f"{self.game_name}_up_char 解析出错")

    def dump_up_char(self):
        if self.UP_CHAR and self.UP_CARD:
            data = {
                "char": json.loads(self.UP_CHAR.json()),
                "card": json.loads(self.UP_CARD.json()),
            }
            self.dump_data(data, f"draw_card_up/{self.game_name}_up_char.json")

    async def _update_info(self):
        # pretty.json
        pretty_info = {}
        url = "https://wiki.biligame.com/umamusume/赛马娘图鉴"
        result = await self.get_url(url)
        if not result:
            logger.warning(f"更新 {self.game_name_cn} 出错")
        else:
            dom = etree.HTML(result, etree.HTMLParser())
            char_list = dom.xpath("//table[@id='CardSelectTr']/tbody/tr")
            for char in char_list:
                try:
                    name = char.xpath("./td[1]/a/@title")[0]
                    avatar = char.xpath("./td[1]/a/img/@srcset")[0]
                    star = len(char.xpath("./td[3]/img"))
                except IndexError:
                    continue
                member_dict = {
                    "头像": unquote(str(avatar).split(" ")[-2]),
                    "名称": remove_prohibited_str(name),
                    "初始星级": star,
                }
                pretty_info[member_dict["名称"]] = member_dict
            self.dump_data(pretty_info)
            logger.info(f"{self.game_name_cn} 更新成功")
        # pretty_card.json
        pretty_card_info = {}
        url = "https://wiki.biligame.com/umamusume/支援卡图鉴"
        result = await self.get_url(url)
        if not result:
            logger.warning(f"更新 {self.game_name_cn} 卡牌出错")
        else:
            dom = etree.HTML(result, etree.HTMLParser())
            char_list = dom.xpath("//table[@id='CardSelectTr']/tbody/tr")
            for char in char_list:
                try:
                    name = char.xpath("./td[1]/div/a/@title")[0]
                    name_cn = char.xpath("./td[3]/a/text()")[0]
                    avatar = char.xpath("./td[1]/div/a/img/@srcset")[0]
                    star = str(char.xpath("./td[5]/text()")[0]).strip()
                    sources = str(char.xpath("./td[7]/text()")[0]).strip()
                except IndexError:
                    continue
                member_dict = {
                    "头像": unquote(str(avatar).split(" ")[-2]),
                    "名称": remove_prohibited_str(name),
                    "中文名": remove_prohibited_str(name_cn),
                    "稀有度": star,
                    "获取方式": [sources] if sources else [],
                }
                pretty_card_info[member_dict["中文名"]] = member_dict
            self.dump_data(pretty_card_info, "pretty_card.json")
            logger.info(f"{self.game_name_cn} 卡牌更新成功")
        # 下载头像
        for value in pretty_info.values():
            await self.download_img(value["头像"], value["名称"])
        for value in pretty_card_info.values():
            await self.download_img(value["头像"], value["中文名"])
        # 下载星星
        PRETTY_URL = "https://patchwiki.biligame.com/images/umamusume"
        await self.download_img(
            PRETTY_URL + "/1/13/e1hwjz4vmhtvk8wlyb7c0x3ld1s2ata.png", "star"
        )
        # 下载稀有度标志
        idx = 1
        for url in [
            "/f/f7/afqs7h4snmvovsrlifq5ib8vlpu2wvk.png",
            "/3/3b/d1jmpwrsk4irkes1gdvoos4ic6rmuht.png",
            "/0/06/q23szwkbtd7pfkqrk3wcjlxxt9z595o.png",
        ]:
            await self.download_img(PRETTY_URL + url, f"{idx}_label")
            idx += 1
        await self.update_up_char()

    async def update_up_char(self):
        announcement_url = "https://wiki.biligame.com/umamusume/公告"
        result = await self.get_url(announcement_url)
        if not result:
            logger.warning(f"{self.game_name_cn}获取公告出错")
            return
        dom = etree.HTML(result, etree.HTMLParser())
        announcements = dom.xpath("//div[@id='mw-content-text']/div/div/span/a")
        title = ""
        url = ""
        for announcement in announcements:
            try:
                title = announcement.xpath("./@title")[0]
                url = "https://wiki.biligame.com/" + announcement.xpath("./@href")[0]
                if re.match(r".*?\d{8}$", title) or re.match(
                    r"^\d{1,2}月\d{1,2}日.*?", title
                ):
                    break
            except IndexError:
                continue
        if not title:
            logger.warning(f"{self.game_name_cn}未找到新UP公告")
            return
        result = await self.get_url(url)
        if not result:
            logger.warning(f"{self.game_name_cn}获取UP公告出错")
            return
        try:
            start_time = None
            end_time = None
            char_img = ""
            card_img = ""
            up_chars = []
            up_cards = []
            soup = BeautifulSoup(result, "lxml")
            heads = soup.find_all("span", {"class": "mw-headline"})
            for head in heads:
                if "时间" in head.text:
                    time = head.find_next("p").text.split("\n")[0]
                    if "～" in time:
                        start, end = time.split("～")
                        start_time = dateparser.parse(start)
                        end_time = dateparser.parse(end)
                elif "赛马娘" in head.text:
                    char_img = head.find_next("a", {"class": "image"}).find("img")[
                        "src"
                    ]
                    lines = str(head.find_next("p").text).split("\n")
                    chars = [
                        line
                        for line in lines
                        if "★" in line and "（" in line and "）" in line
                    ]
                    for char in chars:
                        star = char.count("★")
                        name = re.split(r"[（）]", char)[-2].strip()
                        up_chars.append(
                            UpChar(name=name, star=star, limited=False, zoom=70)
                        )
                elif "支援卡" in head.text:
                    card_img = head.find_next("a", {"class": "image"}).find("img")[
                        "src"
                    ]
                    lines = str(head.find_next("p").text).split("\n")
                    cards = [
                        line
                        for line in lines
                        if "R" in line and "（" in line and "）" in line
                    ]
                    for card in cards:
                        star = 3 if "SSR" in card else 2 if "SR" in card else 1
                        name = re.split(r"[（）]", card)[-2].strip()
                        up_cards.append(
                            UpChar(name=name, star=star, limited=False, zoom=70)
                        )
            if start_time and end_time:
                if start_time <= datetime.now() <= end_time:
                    self.UP_CHAR = UpEvent(
                        title=title,
                        pool_img=char_img,
                        start_time=start_time,
                        end_time=end_time,
                        up_char=up_chars,
                    )
                    self.UP_CARD = UpEvent(
                        title=title,
                        pool_img=card_img,
                        start_time=start_time,
                        end_time=end_time,
                        up_char=up_cards,
                    )
                    self.dump_up_char()
                    logger.info(f"成功获取{self.game_name_cn}当前up信息...当前up池: {title}")
        except Exception as e:
            logger.warning(f"{self.game_name_cn}UP更新出错 {type(e)}：{e}")

    async def _reload_pool(self) -> Optional[Message]:
        await self.update_up_char()
        self.load_up_char()
        if self.UP_CHAR and self.UP_CARD:
            return Message(
                Message.template("重载成功！\n当前UP池子：{}{:image}{:image}").format(
                    self.UP_CHAR.title,
                    self.UP_CHAR.pool_img,
                    self.UP_CARD.pool_img,
                )
            )
