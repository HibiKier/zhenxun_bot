import random
import dateparser
from lxml import etree
from PIL import Image, ImageDraw
from urllib.parse import unquote
from typing import List, Optional, Tuple
from pydantic import ValidationError
from datetime import datetime, timedelta
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
from ..count_manager import GenshinCountManager
from ..util import remove_prohibited_str, cn2py, load_font
from utils.image_utils import BuildImage


class GenshinData(BaseData):
    pass


class GenshinChar(GenshinData):
    pass


class GenshinArms(GenshinData):
    pass


class GenshinHandle(BaseHandle[GenshinData]):
    def __init__(self):
        super().__init__("genshin", "原神", "#ebebeb")
        self.data_files.append("genshin_arms.json")
        self.max_star = 5
        self.config = draw_config.genshin

        self.ALL_CHAR: List[GenshinData] = []
        self.ALL_ARMS: List[GenshinData] = []
        self.UP_CHAR: Optional[UpEvent] = None
        self.UP_ARMS: Optional[UpEvent] = None

        self.count_manager = GenshinCountManager((10, 90), ("4", "5"), 180)

    # 抽取卡池
    def get_card(
        self, pool_name: str, mode: int = 1, add: float = 0.0, is_up: bool = False
    ):
        """
        mode 1：普通抽 2：四星保底 3：五星保底
        """
        if mode == 1:
            star = self.get_star(
                [5, 4, 3],
                [
                    self.config.GENSHIN_FIVE_P + add,
                    self.config.GENSHIN_FOUR_P,
                    self.config.GENSHIN_THREE_P,
                ],
            )
        elif mode == 2:
            star = self.get_star(
                [5, 4],
                [self.config.GENSHIN_G_FIVE_P + add, self.config.GENSHIN_G_FOUR_P],
            )
        else:
            star = 5

        if pool_name == "char":
            up_event = self.UP_CHAR
            all_list = self.ALL_CHAR + [
                x for x in self.ALL_ARMS if x.star == star and x.star < 5
            ]
        elif pool_name == "arms":
            up_event = self.UP_ARMS
            all_list = self.ALL_ARMS + [
                x for x in self.ALL_CHAR if x.star == star and x.star < 5
            ]
        else:
            up_event = None
            all_list = self.ALL_ARMS + self.ALL_CHAR

        acquire_char = None
        # 是否UP
        if up_event and star > 3:
            # 获取up角色列表
            up_list = [x.name for x in up_event.up_char if x.star == star]
            # 成功获取up角色
            if random.random() < 0.5 or is_up:
                up_name = random.choice(up_list)
                try:
                    acquire_char = [x for x in all_list if x.name == up_name][0]
                except IndexError:
                    pass
        if not acquire_char:
            chars = [x for x in all_list if x.star == star and not x.limited]
            acquire_char = random.choice(chars)
        return acquire_char

    def get_cards(
        self, count: int, user_id: int, pool_name: str
    ) -> List[Tuple[GenshinData, int]]:
        card_list = []  # 获取角色列表
        add = 0.0
        count_manager = self.count_manager
        count_manager.check_timeout(user_id)  # 检查上次抽卡次数是否超时
        count_manager.check_count(user_id, count)  # 检查次数累计
        pool = self.UP_CHAR if pool_name == "char" else self.UP_ARMS
        for i in range(count):
            count_manager.increase(user_id)
            star = count_manager.check(user_id)  # 是否有四星或五星保底
            if (
                count_manager.get_user_count(user_id)
                - count_manager.get_user_five_index(user_id)
            ) % count_manager.get_max_guarantee() >= 72:
                add += draw_config.genshin.I72_ADD
            if star:
                if star == 4:
                    card = self.get_card(pool_name, 2, add=add)
                else:
                    card = self.get_card(
                        pool_name, 3, add, count_manager.is_up(user_id)
                    )
            else:
                card = self.get_card(pool_name, 1, add, count_manager.is_up(user_id))
            # print(f"{count_manager.get_user_count(user_id)}：",
            # count_manager.get_user_five_index(user_id), star, card.star, add)
            # 四星角色
            if card.star == 4:
                count_manager.mark_four_index(user_id)
            # 五星角色
            elif card.star == self.max_star:
                add = 0
                count_manager.mark_five_index(user_id)  # 记录五星保底
                count_manager.mark_four_index(user_id)  # 记录四星保底
            if pool and card.name in [
                x.name for x in pool.up_char if x.star == self.max_star
            ]:
                count_manager.set_is_up(user_id, True)
            else:
                count_manager.set_is_up(user_id, False)
            card_list.append((card, count_manager.get_user_count(user_id)))
        count_manager.update_time(user_id)
        return card_list

    def generate_card_img(self, card: GenshinData) -> BuildImage:
        sep_w = 10
        sep_h = 5
        frame_w = 112
        frame_h = 132
        img_w = 106
        img_h = 106
        bg = BuildImage(frame_w + sep_w * 2, frame_h + sep_h * 2, color="#EBEBEB")
        frame_path = str(self.img_path / "avatar_frame.png")
        frame = Image.open(frame_path)
        # 加名字
        text = card.name
        font = load_font(fontsize=14)
        text_w, text_h = font.getsize(text)
        draw = ImageDraw.Draw(frame)
        draw.text(
            ((frame_w - text_w) / 2, frame_h - 15 - text_h / 2),
            text,
            font=font,
            fill="gray",
        )
        img_path = str(self.img_path / f"{cn2py(card.name)}.png")
        img = BuildImage(img_w, img_h, background=img_path)
        if isinstance(card, GenshinArms):
            # 武器卡背景不是透明的，切去上方两个圆弧
            r = 12
            circle = Image.new("L", (r * 2, r * 2), 0)
            alpha = Image.new("L", img.size, 255)
            alpha.paste(circle, (-r - 3, -r - 3))  # 左上角
            alpha.paste(circle, (img_h - r + 3, -r - 3))  # 右上角
            img.markImg.putalpha(alpha)
        star_path = str(self.img_path / f"{card.star}_star.png")
        star = Image.open(star_path)
        bg.paste(frame, (sep_w, sep_h), alpha=True)
        bg.paste(img, (sep_w + 3, sep_h + 3), alpha=True)
        bg.paste(star, (sep_w + int((frame_w - star.width) / 2), sep_h - 6), alpha=True)
        return bg

    def format_pool_info(self, pool_name: str) -> str:
        info = ""
        up_event = None
        if pool_name == "char":
            up_event = self.UP_CHAR
        elif pool_name == "arms":
            up_event = self.UP_ARMS
        if up_event:
            star5_list = [x.name for x in up_event.up_char if x.star == 5]
            star4_list = [x.name for x in up_event.up_char if x.star == 4]
            if star5_list:
                info += f"五星UP：{' '.join(star5_list)}\n"
            if star4_list:
                info += f"四星UP：{' '.join(star4_list)}\n"
            info = f"当前up池：{up_event.title}\n{info}"
        return info.strip()

    async def draw(self, count: int, user_id: int, pool_name: str = "", **kwargs) -> Message:
        return await asyncio.get_event_loop().run_in_executor(None, self._draw, count, user_id, pool_name)

    def _draw(self, count: int, user_id: int, pool_name: str = "", **kwargs) -> Message:
        index2cards = self.get_cards(count, user_id, pool_name)
        cards = [card[0] for card in index2cards]
        up_event = None
        if pool_name == "char":
            up_event = self.UP_CHAR
        elif pool_name == "arms":
            up_event = self.UP_ARMS
        up_list = [x.name for x in up_event.up_char] if up_event else []
        result = self.format_star_result(cards)
        result += (
            "\n" + max_star_str
            if (max_star_str := self.format_max_star(index2cards, up_list=up_list))
            else ""
        )
        result += f"\n距离保底发还剩 {self.count_manager.get_user_guarantee_count(user_id)} 抽"
        # result += "\n【五星：0.6%，四星：5.1%，第72抽开始五星概率每抽加0.585%】"
        pool_info = self.format_pool_info(pool_name)
        img = self.generate_img(cards)
        bk = BuildImage(img.w, img.h + 50, font_size=20, color="#ebebeb")
        bk.paste(img)
        bk.text((0, img.h + 10), "【五星：0.6%，四星：5.1%，第72抽开始五星概率每抽加0.585%】")
        return pool_info + image(b64=bk.pic2bs4()) + result

    def _init_data(self):
        self.ALL_CHAR = [
            GenshinChar(
                name=value["名称"],
                star=int(value["星级"]),
                limited=value["常驻/限定"] == "限定UP",
            )
            for key, value in self.load_data().items()
            if "旅行者" not in key
        ]
        self.ALL_ARMS = [
            GenshinArms(
                name=value["名称"],
                star=int(value["星级"]),
                limited="祈愿" not in value["获取途径"],
            )
            for value in self.load_data("genshin_arms.json").values()
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
        # genshin.json
        char_info = {}
        url = "https://wiki.biligame.com/ys/角色筛选"
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
                    star = char.xpath("./td[3]/text()")[0]
                except IndexError:
                    continue
                member_dict = {
                    "头像": unquote(str(avatar).split(" ")[-2]),
                    "名称": remove_prohibited_str(name),
                    "星级": int(str(star).strip()[:1]),
                }
                char_info[member_dict["名称"]] = member_dict
            # 更新额外信息
            for key in char_info.keys():
                result = await self.get_url(f"https://wiki.biligame.com/ys/{key}")
                if not result:
                    char_info[key]["常驻/限定"] = "未知"
                    logger.warning(f"{self.game_name_cn} 获取额外信息错误 {key}")
                    continue
                try:
                    dom = etree.HTML(result, etree.HTMLParser())
                    limit = dom.xpath(
                        "//table[contains(string(.),'常驻/限定')]/tbody/tr[6]/td/text()"
                    )[0]
                    char_info[key]["常驻/限定"] = str(limit).strip()
                except IndexError:
                    char_info[key]["常驻/限定"] = "未知"
                    logger.warning(f"{self.game_name_cn} 获取额外信息错误 {key}")
            self.dump_data(char_info)
            logger.info(f"{self.game_name_cn} 更新成功")
        # genshin_arms.json
        arms_info = {}
        url = "https://wiki.biligame.com/ys/武器图鉴"
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
                    star = char.xpath("./td[4]/img/@alt")[0]
                    sources = str(char.xpath("./td[5]/text()")[0]).split(",")
                except IndexError:
                    continue
                member_dict = {
                    "头像": unquote(str(avatar).split(" ")[-2]),
                    "名称": remove_prohibited_str(name),
                    "星级": int(str(star).strip()[:1]),
                    "获取途径": [s.strip() for s in sources if s.strip()],
                }
                arms_info[member_dict["名称"]] = member_dict
            self.dump_data(arms_info, "genshin_arms.json")
            logger.info(f"{self.game_name_cn} 武器更新成功")
        # 下载头像
        for value in char_info.values():
            await self.download_img(value["头像"], value["名称"])
        for value in arms_info.values():
            await self.download_img(value["头像"], value["名称"])
        # 下载星星
        idx = 1
        YS_URL = "https://patchwiki.biligame.com/images/ys"
        for url in [
            "/1/13/7xzg7tgf8dsr2hjpmdbm5gn9wvzt2on.png",
            "/b/bc/sd2ige6d7lvj7ugfumue3yjg8gyi0d1.png",
            "/e/ec/l3mnhy56pyailhn3v7r873htf2nofau.png",
            "/9/9c/sklp02ffk3aqszzvh8k1c3139s0awpd.png",
            "/c/c7/qu6xcndgj6t14oxvv7yz2warcukqv1m.png",
        ]:
            await self.download_img(YS_URL + url, f"{idx}_star")
            idx += 1
        # 下载头像框
        await self.download_img(
            YS_URL + "/2/2e/opbcst4xbtcq0i4lwerucmosawn29ti.png", f"avatar_frame"
        )
        await self.update_up_char()

    async def update_up_char(self):
        url = "https://wiki.biligame.com/ys/祈愿"
        result = await self.get_url(url)
        if not result:
            logger.warning(f"{self.game_name_cn}获取祈愿页面出错")
            return
        dom = etree.HTML(result, etree.HTMLParser())
        tables = dom.xpath(
            "//div[@class='mw-parser-output']/div[@class='row']/div/table[@class='wikitable']/tbody"
        )
        if not tables or len(tables) < 2:
            logger.warning(f"{self.game_name_cn}获取活动祈愿出错")
            return
        try:
            for index, table in enumerate(tables):
                title = table.xpath("./tr[1]/th/img/@title")[0]
                title = str(title).split("」")[0] + "」" if "」" in title else title
                pool_img = str(table.xpath("./tr[1]/th/img/@srcset")[0]).split(" ")[-2]
                time = table.xpath("./tr[2]/td/text()")[0]
                star5_list = table.xpath("./tr[3]/td/a/@title")
                star4_list = table.xpath("./tr[4]/td/a/@title")
                start, end = str(time).split("~")
                start_time = dateparser.parse(start)
                end_time = dateparser.parse(end)
                if not start_time and end_time:
                    start_time = end_time - timedelta(days=20)
                if start_time and end_time and start_time <= datetime.now() <= end_time:
                    up_event = UpEvent(
                        title=title,
                        pool_img=pool_img,
                        start_time=start_time,
                        end_time=end_time,
                        up_char=[
                            UpChar(name=name, star=5, limited=False, zoom=50)
                            for name in star5_list
                        ]
                        + [
                            UpChar(name=name, star=4, limited=False, zoom=50)
                            for name in star4_list
                        ],
                    )
                    if index == 0:
                        self.UP_CHAR = up_event
                    elif index == 1:
                        self.UP_ARMS = up_event
            if self.UP_CHAR and self.UP_ARMS:
                self.dump_up_char()
                logger.info(
                    f"成功获取{self.game_name_cn}当前up信息...当前up池: {self.UP_CHAR.title} & {self.UP_ARMS.title}"
                )
        except Exception as e:
            logger.warning(f"{self.game_name_cn}UP更新出错 {type(e)}：{e}")

    def reset_count(self, user_id: int) -> bool:
        self.count_manager.reset(user_id)
        return True

    async def _reload_pool(self) -> Optional[Message]:
        await self.update_up_char()
        self.load_up_char()
        if self.UP_CHAR and self.UP_ARMS:
            return Message(
                Message.template("重载成功！\n当前UP池子：{} & {}{:image}{:image}").format(
                    self.UP_CHAR.title,
                    self.UP_ARMS.title,
                    self.UP_CHAR.pool_img,
                    self.UP_ARMS.pool_img,
                )
            )
