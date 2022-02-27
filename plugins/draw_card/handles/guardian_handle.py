import re
import random
import dateparser
from lxml import etree
from PIL import ImageDraw
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


class GuardianData(BaseData):
    pass


class GuardianChar(GuardianData):
    pass


class GuardianArms(GuardianData):
    pass


class GuardianHandle(BaseHandle[GuardianData]):
    def __init__(self):
        super().__init__("guardian", "坎公骑冠剑")
        self.data_files.append("guardian_arms.json")
        self.config = draw_config.guardian

        self.ALL_CHAR: List[GuardianChar] = []
        self.ALL_ARMS: List[GuardianArms] = []
        self.UP_CHAR: Optional[UpEvent] = None
        self.UP_ARMS: Optional[UpEvent] = None

    def get_card(self, pool_name: str, mode: int = 1) -> GuardianData:
        if pool_name == "char":
            if mode == 1:
                star = self.get_star(
                    [3, 2, 1],
                    [
                        self.config.GUARDIAN_THREE_CHAR_P,
                        self.config.GUARDIAN_TWO_CHAR_P,
                        self.config.GUARDIAN_ONE_CHAR_P,
                    ],
                )
            else:
                star = self.get_star(
                    [3, 2],
                    [
                        self.config.GUARDIAN_THREE_CHAR_P,
                        self.config.GUARDIAN_TWO_CHAR_P,
                    ],
                )
            up_event = self.UP_CHAR
            self.max_star = 3
            all_data = self.ALL_CHAR
        else:
            if mode == 1:
                star = self.get_star(
                    [5, 4, 3, 2],
                    [
                        self.config.GUARDIAN_FIVE_ARMS_P,
                        self.config.GUARDIAN_FOUR_ARMS_P,
                        self.config.GUARDIAN_THREE_ARMS_P,
                        self.config.GUARDIAN_TWO_ARMS_P,
                    ],
                )
            else:
                star = self.get_star(
                    [5, 4],
                    [
                        self.config.GUARDIAN_FIVE_ARMS_P,
                        self.config.GUARDIAN_FOUR_ARMS_P,
                    ],
                )
            up_event = self.UP_ARMS
            self.max_star = 5
            all_data = self.ALL_ARMS

        acquire_char = None
        # 是否UP
        if up_event and star == self.max_star and pool_name:
            # 获取up角色列表
            up_list = [x.name for x in up_event.up_char if x.star == star]
            # 成功获取up角色
            if random.random() < 0.5:
                up_name = random.choice(up_list)
                try:
                    acquire_char = [x for x in all_data if x.name == up_name][0]
                except IndexError:
                    pass
        if not acquire_char:
            chars = [x for x in all_data if x.star == star and not x.limited]
            acquire_char = random.choice(chars)
        return acquire_char

    def get_cards(self, count: int, pool_name: str) -> List[Tuple[GuardianData, int]]:
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
        up_event = self.UP_CHAR if pool_name == "char" else self.UP_ARMS
        if up_event:
            if pool_name == "char":
                up_list = [x.name for x in up_event.up_char if x.star == 3]
                info += f'三星UP：{" ".join(up_list)}\n'
            else:
                up_list = [x.name for x in up_event.up_char if x.star == 5]
                info += f'五星UP：{" ".join(up_list)}\n'
            info = f"当前up池：{up_event.title}\n{info}"
        return info.strip()

    async def draw(self, count: int, pool_name: str, **kwargs) -> Message:
        return await asyncio.get_event_loop().run_in_executor(None, self._draw, count, pool_name)

    def _draw(self, count: int, pool_name: str, **kwargs) -> Message:
        index2card = self.get_cards(count, pool_name)
        cards = [card[0] for card in index2card]
        up_event = self.UP_CHAR if pool_name == "char" else self.UP_ARMS
        up_list = [x.name for x in up_event.up_char] if up_event else []
        result = self.format_result(index2card, up_list=up_list)
        pool_info = self.format_pool_info(pool_name)
        return pool_info + image(b64=self.generate_img(cards).pic2bs4()) + result

    def generate_card_img(self, card: GuardianData) -> BuildImage:
        sep_w = 1
        sep_h = 1
        block_w = 170
        block_h = 90
        img_w = 90
        img_h = 90
        if isinstance(card, GuardianChar):
            block_color = "#2e2923"
            font_color = "#e2ccad"
            star_w = 90
            star_h = 30
            star_name = f"{card.star}_star.png"
            frame_path = ""
        else:
            block_color = "#EEE4D5"
            font_color = "#A65400"
            star_w = 45
            star_h = 45
            star_name = f"{card.star}_star_rank.png"
            frame_path = str(self.img_path / "avatar_frame.png")
        bg = BuildImage(block_w + sep_w * 2, block_h + sep_h * 2, color="#F6F4ED")
        block = BuildImage(block_w, block_h, color=block_color)
        star_path = str(self.img_path / star_name)
        star = BuildImage(star_w, star_h, background=star_path)
        img_path = str(self.img_path / f"{cn2py(card.name)}.png")
        img = BuildImage(img_w, img_h, background=img_path)
        block.paste(img, (0, 0), alpha=True)
        if frame_path:
            frame = BuildImage(img_w, img_h, background=frame_path)
            block.paste(frame, (0, 0), alpha=True)
        block.paste(
            star,
            (int((block_w + img_w - star_w) / 2), block_h - star_h - 30),
            alpha=True,
        )
        # 加名字
        text = card.name[:4] + "..." if len(card.name) > 5 else card.name
        font = load_font(fontsize=14)
        text_w, _ = font.getsize(text)
        draw = ImageDraw.Draw(block.markImg)
        draw.text(
            ((block_w + img_w - text_w) / 2, 55),
            text,
            font=font,
            fill=font_color,
        )
        bg.paste(block, (sep_w, sep_h))
        return bg

    def _init_data(self):
        self.ALL_CHAR = [
            GuardianChar(name=value["名称"], star=int(value["星级"]), limited=False)
            for value in self.load_data().values()
        ]
        self.ALL_ARMS = [
            GuardianArms(name=value["名称"], star=int(value["星级"]), limited=False)
            for value in self.load_data("guardian_arms.json").values()
        ]
        self.load_up_char()

    def load_up_char(self):
        try:
            data = self.load_data(f"draw_card_up/{self.game_name}_up_char.json")
            self.UP_CHAR = UpEvent.parse_obj(data.get("char", {}))
            self.UP_ARMS = UpEvent.parse_obj(data.get("arms", {}))
        except ValidationError:
            logger.warning(f"{self.game_name}_up_char 解析出错")

    def dump_up_char(self):
        if self.UP_CHAR and self.UP_ARMS:
            data = {
                "char": json.loads(self.UP_CHAR.json()),
                "arms": json.loads(self.UP_ARMS.json()),
            }
            self.dump_data(data, f"draw_card_up/{self.game_name}_up_char.json")

    async def _update_info(self):
        # guardian.json
        guardian_info = {}
        url = "https://wiki.biligame.com/gt/英雄筛选表"
        result = await self.get_url(url)
        if not result:
            logger.warning(f"更新 {self.game_name_cn} 出错")
        else:
            dom = etree.HTML(result, etree.HTMLParser())
            char_list = dom.xpath("//table[@id='CardSelectTr']/tbody/tr")
            for char in char_list:
                try:
                    name = char.xpath("./td[1]/a/@title")[0]
                    avatar = char.xpath("./td[1]/a/img/@src")[0]
                    star = char.xpath("./td[1]/span/img/@alt")[0]
                except IndexError:
                    continue
                member_dict = {
                    "头像": unquote(str(avatar)),
                    "名称": remove_prohibited_str(name),
                    "星级": int(str(star).split(" ")[0].replace("Rank", "")),
                }
                guardian_info[member_dict["名称"]] = member_dict
            self.dump_data(guardian_info)
            logger.info(f"{self.game_name_cn} 更新成功")
        # guardian_arms.json
        guardian_arms_info = {}
        url = "https://wiki.biligame.com/gt/武器"
        result = await self.get_url(url)
        if not result:
            logger.warning(f"更新 {self.game_name_cn} 武器出错")
        else:
            dom = etree.HTML(result, etree.HTMLParser())
            char_list = dom.xpath(
                "//div[@class='resp-tabs-container']/div[1]/div/table[2]/tbody/tr"
            )
            for char in char_list:
                try:
                    name = char.xpath("./td[2]/a/@title")[0]
                    avatar = char.xpath("./td[1]/div/div/div/a/img/@src")[0]
                    star = char.xpath("./td[3]/text()")[0]
                except IndexError:
                    continue
                member_dict = {
                    "头像": unquote(str(avatar)),
                    "名称": remove_prohibited_str(name),
                    "星级": int(str(star).strip()),
                }
                guardian_arms_info[member_dict["名称"]] = member_dict
            self.dump_data(guardian_arms_info, "guardian_arms.json")
            logger.info(f"{self.game_name_cn} 武器更新成功")
        url = "https://wiki.biligame.com/gt/盾牌"
        result = await self.get_url(url)
        if not result:
            logger.warning(f"更新 {self.game_name_cn} 盾牌出错")
        else:
            dom = etree.HTML(result, etree.HTMLParser())
            char_list = dom.xpath(
                "//div[@class='resp-tabs-container']/div[2]/div/table[1]/tbody/tr"
            )
            for char in char_list:
                try:
                    name = char.xpath("./td[2]/a/@title")[0]
                    avatar = char.xpath("./td[1]/div/div/div/a/img/@src")[0]
                    star = char.xpath("./td[3]/text()")[0]
                except IndexError:
                    continue
                member_dict = {
                    "头像": unquote(str(avatar)),
                    "名称": remove_prohibited_str(name),
                    "星级": int(str(star).strip()),
                }
                guardian_arms_info[member_dict["名称"]] = member_dict
            self.dump_data(guardian_arms_info, "guardian_arms.json")
            logger.info(f"{self.game_name_cn} 盾牌更新成功")
        # 下载头像
        for value in guardian_info.values():
            await self.download_img(value["头像"], value["名称"])
        for value in guardian_arms_info.values():
            await self.download_img(value["头像"], value["名称"])
        # 下载星星
        idx = 1
        GT_URL = "https://patchwiki.biligame.com/images/gt"
        for url in [
            "/4/4b/ardr3bi2yf95u4zomm263tc1vke6i3i.png",
            "/5/55/6vow7lh76gzus6b2g9cfn325d1sugca.png",
            "/b/b9/du8egrd2vyewg0cuyra9t8jh0srl0ds.png",
        ]:
            await self.download_img(GT_URL + url, f"{idx}_star")
            idx += 1
        # 另一种星星
        idx = 1
        for url in [
            "/6/66/4e2tfa9kvhfcbikzlyei76i9crva145.png",
            "/1/10/r9ihsuvycgvsseyneqz4xs22t53026m.png",
            "/7/7a/o0k86ru9k915y04azc26hilxead7xp1.png",
            "/c/c9/rxz99asysz0rg391j3b02ta09mnpa7v.png",
            "/2/2a/sfxz0ucv1s6ewxveycz9mnmrqs2rw60.png",
        ]:
            await self.download_img(GT_URL + url, f"{idx}_star_rank")
            idx += 1
        # 头像框
        await self.download_img(
            GT_URL + "/8/8e/ogbqslbhuykjhnc8trtoa0p0nhfzohs.png", f"avatar_frame"
        )
        await self.update_up_char()

    async def update_up_char(self):
        url = "https://wiki.biligame.com/gt/首页"
        result = await self.get_url(url)
        if not result:
            logger.warning(f"{self.game_name_cn}获取公告出错")
            return
        try:
            dom = etree.HTML(result, etree.HTMLParser())
            announcement = dom.xpath(
                "//div[@class='mw-parser-output']/div/div[3]/div[2]/div/div[2]/div[3]"
            )[0]
            title = announcement.xpath("./font/p/b/text()")[0]
            match = re.search(r"从(.*?)开始.*?至(.*?)结束", title)
            if not match:
                logger.warning(f"{self.game_name_cn}找不到UP时间")
                return
            start, end = match.groups()
            start_time = dateparser.parse(start.replace("月", "/").replace("日", ""))
            end_time = dateparser.parse(end.replace("月", "/").replace("日", ""))
            if not (start_time and end_time) or not (
                start_time <= datetime.now() <= end_time
            ):
                return
            divs = announcement.xpath("./font/div")
            char_index = 0
            arms_index = 0
            for index, div in enumerate(divs):
                if div.xpath("string(.)") == "角色":
                    char_index = index
                elif div.xpath("string(.)") == "武器":
                    arms_index = index
            chars = divs[char_index + 1 : arms_index]
            arms = divs[arms_index + 1 :]
            up_chars = []
            up_arms = []
            for char in chars:
                name = char.xpath("./p/a/@title")[0]
                up_chars.append(UpChar(name=name, star=3, limited=False, zoom=0))
            for arm in arms:
                name = arm.xpath("./p/a/@title")[0]
                up_arms.append(UpChar(name=name, star=5, limited=False, zoom=0))
            self.UP_CHAR = UpEvent(
                title=title,
                pool_img="",
                start_time=start_time,
                end_time=end_time,
                up_char=up_chars,
            )
            self.UP_ARMS = UpEvent(
                title=title,
                pool_img="",
                start_time=start_time,
                end_time=end_time,
                up_char=up_arms,
            )
            self.dump_up_char()
            logger.info(f"成功获取{self.game_name_cn}当前up信息...当前up池: {title}")
        except Exception as e:
            logger.warning(f"{self.game_name_cn}UP更新出错 {type(e)}：{e}")

    async def _reload_pool(self) -> Optional[Message]:
        await self.update_up_char()
        self.load_up_char()
        if self.UP_CHAR and self.UP_ARMS:
            return Message(f"重载成功！\n当前UP池子：{self.UP_CHAR.title}")
