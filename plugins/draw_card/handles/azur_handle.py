import random
import dateparser
from lxml import etree
from typing import List, Optional
from urllib.parse import unquote
from pydantic import ValidationError
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Message
from utils.message_builder import image

from .base_handle import BaseHandle, BaseData, UpEvent as _UpEvent, UpChar as _UpChar
from ..config import draw_config
from ..util import remove_prohibited_str, cn2py
from utils.image_utils import BuildImage
import asyncio

try:
    import ujson as json
except ModuleNotFoundError:
    import json


class AzurChar(BaseData):
    type_: str  # 舰娘类型

    @property
    def star_str(self) -> str:
        return ["白", "蓝", "紫", "金"][self.star - 1]


class UpChar(_UpChar):
    type_: str   # 舰娘类型


class UpEvent(_UpEvent):
    up_char: List[UpChar]  # up对象


class AzurHandle(BaseHandle[AzurChar]):
    def __init__(self):
        super().__init__("azur", "碧蓝航线")
        self.max_star = 4
        self.config = draw_config.azur
        self.ALL_CHAR: List[AzurChar] = []
        self.UP_EVENT: Optional[UpEvent] = None

    def get_card(self, pool_name: str, **kwargs) -> AzurChar:
        if pool_name == "轻型":
            type_ = ["驱逐", "轻巡", "维修"]
        elif pool_name == "重型":
            type_ = ["重巡", "战列", "战巡", "重炮"]
        else:
            type_ = ["维修", "潜艇", "重巡", "轻航", "航母"]
        up_pool_flag = pool_name == "活动"
        # Up
        up_ship = [x for x in self.UP_EVENT.up_char if x.zoom > 0]
        # print(up_ship)
        acquire_char = None
        if up_ship and up_pool_flag:
            up_zoom = [(0, up_ship[0].zoom / 100)]
            # 初始化概率
            cur_ = up_ship[0].zoom / 100
            for i in range(len(up_ship)):
                try:
                    up_zoom.append((cur_, cur_ + up_ship[i+1].zoom / 100))
                    cur_ += up_ship[i+1].zoom / 100
                except IndexError:
                    pass
            rand = random.random()
            # 抽取up
            for i, zoom in enumerate(up_zoom):
                if zoom[0] <= rand <= zoom[1]:
                    try:
                        acquire_char = [x for x in self.ALL_CHAR if x.name == up_ship[i].name][0]
                    except IndexError:
                        pass
        # 没有up或者未抽取到up
        if not acquire_char:
            star = self.get_star(
                [4, 3, 2, 1],
                [
                    self.config.AZUR_FOUR_P,
                    self.config.AZUR_THREE_P,
                    self.config.AZUR_TWO_P,
                    self.config.AZUR_ONE_P,
                ],
            )
            acquire_char = random.choice([
                x
                for x in self.ALL_CHAR
                if x.star == star and x.type_ in type_ and not x.limited
            ])
        return acquire_char

    # async def draw(self, count: int, **kwargs) -> Message:
    #     return await asyncio.get_event_loop().run_in_executor(None, self._draw, count)

    async def draw(self, count: int, **kwargs) -> Message:
        index2card = self.get_cards(count, **kwargs)
        cards = [card[0] for card in index2card]
        up_list = [x.name for x in self.UP_EVENT.up_char] if self.UP_EVENT.up_char else []
        result = self.format_result(index2card, **{**kwargs, "up_list": up_list})
        return image(b64=self.generate_img(cards).pic2bs4()) + result

    def generate_card_img(self, card: AzurChar) -> BuildImage:
        sep_w = 5
        sep_t = 5
        sep_b = 20
        w = 100
        h = 100
        bg = BuildImage(w + sep_w * 2, h + sep_t + sep_b, font="msyh.ttf")
        frame_path = self.img_path / f"{card.star}_star.png"
        frame = BuildImage(w, h, background=frame_path)
        img_path = self.img_path / f"{cn2py(card.name)}.png"
        img = BuildImage(w, h, background=img_path)
        # 加圆角
        img.circle_corner(6)
        bg.paste(img, (sep_w, sep_t), alpha=True)
        bg.paste(frame, (sep_w, sep_t), alpha=True)
        bg.circle_corner(6)
        # 加名字
        text = card.name[:6] + "..." if len(card.name) > 7 else card.name
        text_w, text_h = bg.getsize(text)
        bg.text(
            (sep_w + (w - text_w) / 2, h + sep_t + (sep_b - text_h) / 2),
            text,
            fill=["#808080", "#3b8bff", "#8000ff", "#c90", "#ee494c"][card.star - 1],
        )
        return bg

    def _init_data(self):
        self.ALL_CHAR = [
            AzurChar(
                name=value["名称"],
                star=int(value["星级"]),
                limited="可以建造" not in value["获取途径"],
                type_=value["类型"],
            )
            for value in self.load_data().values()
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
        # 更新图鉴
        url = "https://wiki.biligame.com/blhx/舰娘图鉴"
        result = await self.get_url(url)
        if not result:
            logger.warning(f"更新 {self.game_name_cn} 出错")
            return
        dom = etree.HTML(result, etree.HTMLParser())
        contents = dom.xpath(
            "//div[@class='resp-tabs-container']/div[@class='resp-tab-content']"
        )
        for index, content in enumerate(contents):
            char_list = content.xpath("./table/tbody/tr[2]/td/div/div/div/div")
            for char in char_list:
                try:
                    name = char.xpath("./a/@title")[0]
                    frame = char.xpath("./div/a/img/@alt")[0]
                    avatar = char.xpath("./a/img/@srcset")[0]
                except IndexError:
                    continue
                member_dict = {
                    "名称": remove_prohibited_str(name),
                    "头像": unquote(str(avatar).split(" ")[-2]),
                    "星级": self.parse_star(frame),
                    "类型": self.parse_type(index),
                }
                info[member_dict["名称"]] = member_dict
        # 更新额外信息
        for key in info.keys():
            url = f"https://wiki.biligame.com/blhx/{key}"
            result = await self.get_url(url)
            if not result:
                info[key]["获取途径"] = []
                logger.warning(f"{self.game_name_cn} 获取额外信息错误 {key}")
                continue
            try:
                dom = etree.HTML(result, etree.HTMLParser())
                time = dom.xpath(
                    "//table[@class='wikitable sv-general']/tbody[1]/tr[4]/td[2]//text()"
                )[0]
                sources = []
                if "无法建造" in time:
                    sources.append("无法建造")
                elif "活动已关闭" in time:
                    sources.append("活动限定")
                else:
                    sources.append("可以建造")
                info[key]["获取途径"] = sources
            except IndexError:
                info[key]["获取途径"] = []
                logger.warning(f"{self.game_name_cn} 获取额外信息错误 {key}")
        self.dump_data(info)
        logger.info(f"{self.game_name_cn} 更新成功")
        # 下载头像
        for value in info.values():
            await self.download_img(value["头像"], value["名称"])
        # 下载头像框
        idx = 1
        BLHX_URL = "https://patchwiki.biligame.com/images/blhx"
        for url in [
            "/1/15/pxho13xsnkyb546tftvh49etzdh74cf.png",
            "/a/a9/k8t7nx6c8pan5vyr8z21txp45jxeo66.png",
            "/a/a5/5whkzvt200zwhhx0h0iz9qo1kldnidj.png",
            "/a/a2/ptog1j220x5q02hytpwc8al7f229qk9.png",
            "/6/6d/qqv5oy3xs40d3055cco6bsm0j4k4gzk.png",
        ]:
            await self.download_img(BLHX_URL + url, f"{idx}_star")
            idx += 1
        await self.update_up_char()

    @staticmethod
    def parse_star(star: str) -> int:
        if star in ["舰娘头像外框普通.png", "舰娘头像外框白色.png"]:
            return 1
        elif star in ["舰娘头像外框稀有.png", "舰娘头像外框蓝色.png"]:
            return 2
        elif star in ["舰娘头像外框精锐.png", "舰娘头像外框紫色.png"]:
            return 3
        elif star in ["舰娘头像外框超稀有.png", "舰娘头像外框金色.png"]:
            return 4
        elif star in ["舰娘头像外框海上传奇.png", "舰娘头像外框彩色.png"]:
            return 5
        elif star in [
            "舰娘头像外框最高方案.png",
            "舰娘头像外框决战方案.png",
            "舰娘头像外框超稀有META.png",
            "舰娘头像外框精锐META.png",
        ]:
            return 6
        else:
            return 6

    @staticmethod
    def parse_type(index: int) -> str:
        azur_types = [
            "驱逐",
            "轻巡",
            "重巡",
            "超巡",
            "战巡",
            "战列",
            "航母",
            "航站",
            "轻航",
            "重炮",
            "维修",
            "潜艇",
            "运输",
        ]
        try:
            return azur_types[index]
        except IndexError:
            return azur_types[0]

    async def update_up_char(self):
        url = "https://wiki.biligame.com/blhx/游戏活动表"
        result = await self.get_url(url)
        if not result:
            logger.warning(f"{self.game_name_cn}获取活动表出错")
            return
        try:
            dom = etree.HTML(result, etree.HTMLParser())
            dd = dom.xpath("//div[@class='timeline2']/dl/dd/a")[0]
            url = "https://wiki.biligame.com" + dd.xpath("./@href")[0]
            title = dd.xpath("string(.)")
            result = await self.get_url(url)
            if not result:
                logger.warning(f"{self.game_name_cn}获取活动页面出错")
                return
            dom = etree.HTML(result, etree.HTMLParser())
            timer = dom.xpath("//span[@class='eventTimer']")[0]
            start_time = dateparser.parse(timer.xpath("./@data-start")[0])
            end_time = dateparser.parse(timer.xpath("./@data-end")[0])
            ships = dom.xpath("//table[@class='shipinfo']")
            up_chars = []
            for ship in ships:
                name = ship.xpath("./tbody/tr/td[2]/p/a/@title")[0]
                type_ = ship.xpath("./tbody/tr/td[2]/p/small/text()")[0]        # 舰船类型
                try:
                    p = float(str(ship.xpath(".//sup/text()")[0]).strip("%"))
                except IndexError:
                    p = 0
                star = self.parse_star(
                    ship.xpath("./tbody/tr/td[1]/div/div/div/a/img/@alt")[0]
                )
                up_chars.append(UpChar(name=name, star=star, limited=False, zoom=p, type_=type_))
            self.UP_EVENT = UpEvent(
                title=title,
                pool_img="",
                start_time=start_time,
                end_time=end_time,
                up_char=up_chars,
            )
            self.dump_up_char()
        except Exception as e:
            logger.warning(f"{self.game_name_cn}UP更新出错 {type(e)}：{e}")

    async def _reload_pool(self) -> Optional[Message]:
        await self.update_up_char()
        self.load_up_char()
        if self.UP_EVENT:
            return Message(f"重载成功！\n当前活动：{self.UP_EVENT.title}")
