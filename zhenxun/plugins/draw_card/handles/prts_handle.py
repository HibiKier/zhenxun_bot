import random
import re
from datetime import datetime
from urllib.parse import unquote

import dateparser
import ujson as json
from lxml import etree
from lxml.etree import _Element
from nonebot_plugin_alconna import UniMessage
from PIL import ImageDraw
from pydantic import ValidationError

from zhenxun.services.log import logger
from zhenxun.utils.image_utils import BuildImage
from zhenxun.utils.message import MessageUtils

from ..config import draw_config
from ..util import cn2py, load_font, remove_prohibited_str
from .base_handle import BaseData, BaseHandle, UpChar, UpEvent


class Operator(BaseData):
    recruit_only: bool  # 公招限定
    event_only: bool  # 活动获得干员
    core_only: bool  # 中坚干员
    # special_only: bool  # 升变/异格干员


class PrtsHandle(BaseHandle[Operator]):
    def __init__(self):
        super().__init__(game_name="prts", game_name_cn="明日方舟")
        self.max_star = 6
        self.game_card_color = "#eff2f5"
        self.config = draw_config.prts

        self.ALL_OPERATOR: list[Operator] = []
        self.UP_EVENT: UpEvent | None = None

    def get_card(self, add: float) -> Operator:
        star = self.get_star(
            star_list=[6, 5, 4, 3],
            probability_list=[
                self.config.PRTS_SIX_P + add,
                self.config.PRTS_FIVE_P,
                self.config.PRTS_FOUR_P,
                self.config.PRTS_THREE_P,
            ],
        )

        all_operators = [
            x
            for x in self.ALL_OPERATOR
            if x.star == star
            and not any([x.limited, x.recruit_only, x.event_only, x.core_only])
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

    def get_cards(self, count: int, **kwargs) -> list[tuple[Operator, int]]:
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

    async def draw(self, count: int, **kwargs) -> UniMessage:
        index2card = self.get_cards(count)
        """这里cards修复了抽卡图文不符的bug"""
        cards = [card[0] for card in index2card]
        up_list = [x.name for x in self.UP_EVENT.up_char] if self.UP_EVENT else []
        result = self.format_result(index2card, up_list=up_list)
        pool_info = self.format_pool_info()
        img = await self.generate_img(cards)
        return MessageUtils.build_message([pool_info, img, result])

    async def generate_card_img(self, card: Operator) -> BuildImage:
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
        await bg.paste(img, (sep_w, sep_h))
        for i in range(card.star):
            await bg.paste(star, (sep_w + img_w - 5 - star_h * (i + 1), sep_h))
        # 加名字
        text = card.name[:7] + "..." if len(card.name) > 8 else card.name
        font = load_font(fontsize=16)
        text_w, text_h = BuildImage.get_text_size(text, font)
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
                limited="标准寻访" not in value["获取途径"]
                and "中坚寻访" not in value["获取途径"],
                recruit_only=(
                    True
                    if "标准寻访" not in value["获取途径"]
                    and "中坚寻访" not in value["获取途径"]
                    and "公开招募" in value["获取途径"]
                    else False
                ),
                event_only=True if "活动获取" in value["获取途径"] else False,
                core_only=(
                    True
                    if "标准寻访" not in value["获取途径"]
                    and "中坚寻访" in value["获取途径"]
                    else False
                ),
            )
            for key, value in self.load_data().items()
            if "阿米娅" not in key
        ]
        self.load_up_char()

    def load_up_char(self):
        try:
            data = self.load_data(f"draw_card_up/{self.game_name}_up_char.json")
            """这里的 waring 有点模糊，更新游戏信息时没有up池的情况下也会报错，所以细分了一下"""
            if not data:
                logger.warning(f"当前无UP池或 {self.game_name}_up_char.json 文件不存在")
            else:
                self.UP_EVENT = UpEvent.parse_obj(data.get("char", {}))
        except ValidationError:
            logger.warning(f"{self.game_name}_up_char 解析出错")

    def dump_up_char(self):
        if self.UP_EVENT:
            data = {"char": json.loads(self.UP_EVENT.json())}
            self.dump_data(data, f"draw_card_up/{self.game_name}_up_char.json")

    async def _update_info(self):
        """更新信息"""
        info = {}
        url = "https://wiki.biligame.com/arknights/干员数据表"
        result = await self.get_url(url)
        if not result:
            logger.warning(f"更新 {self.game_name_cn} 出错")
            return
        dom = etree.HTML(result, etree.HTMLParser())
        char_list: list[_Element] = dom.xpath("//table[@id='CardSelectTr']/tbody/tr")
        for char in char_list:
            try:
                avatar = char.xpath("./td[1]/div/div/div/a/img/@srcset")[0]
                name = char.xpath("./td[1]/center/a/text()")[0]
                star = char.xpath("./td[2]/text()")[0]
                """这里sources修好了干员获取标签有问题的bug，如三星只能抽到卡缇就是这个原因"""
                sources = [_.strip("\n") for _ in char.xpath("./td[7]/text()")]
            except IndexError:
                continue
            member_dict = {
                "头像": unquote(str(avatar).split(" ")[-2]),
                "名称": remove_prohibited_str(str(name).strip()),
                "星级": int(str(star).strip()),
                "获取途径": sources,
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
        """重载卡池"""
        announcement_url = "https://ak.hypergryph.com/news.html"
        result = await self.get_url(announcement_url)
        if not result:
            logger.warning(f"{self.game_name_cn}获取公告出错")
            return
        dom = etree.HTML(result, etree.HTMLParser())
        activity_urls = dom.xpath(
            "//ol[@class='articlelist' and @data-category-key='ACTIVITY']/li/a/@href"
        )
        start_time = None
        end_time = None
        up_chars = []
        pool_img = ""
        for activity_url in activity_urls[:10]:  # 减少响应时间, 10个就够了
            activity_url = f"https://ak.hypergryph.com{activity_url}"
            result = await self.get_url(activity_url)
            if not result:
                logger.warning(f"{self.game_name_cn}获取公告 {activity_url} 出错")
                continue

            """因为鹰角的前端太自由了，这里重写了匹配规则以尽可能避免因为前端乱七八糟而导致的重载失败"""
            dom = etree.HTML(result, etree.HTMLParser())
            contents = dom.xpath(
                "//div[@class='article-content']/p/text() | //div[@class='article-content']/p/span/text() | //div[@class='article-content']/div[@class='media-wrap image-wrap']/img/@src"
            )
            title = ""
            time = ""
            chars: list[str] = []
            for index, content in enumerate(contents):
                if re.search("(.*)(寻访|复刻).*?开启", content):
                    title = re.split(r"[【】]", content)
                    title = "".join(title[1:-1]) if "-" in title else title[1]
                    lines = [
                        contents[index - 2 + _] for _ in range(8)
                    ]  # 从 -2 开始是因为xpath获取的时间有的会在寻访开启这一句之前
                    lines.append("")  # 防止IndexError，加个空字符串
                    for idx, line in enumerate(lines):
                        match = re.search(
                            r"(\d{1,2}月\d{1,2}日.*?-.*?\d{1,2}月\d{1,2}日.*?$)", line
                        )
                        if match:
                            time = match.group(1)
                        """因为 <p> 的诡异排版，所以有了下面的一段"""
                        if ("★★" in line and "%" in line) or (
                            "★★" in line and "%" in lines[idx + 1]
                        ):
                            (
                                chars.append(line)
                                if ("★★" in line and "%" in line)
                                else chars.append(line + lines[idx + 1])
                            )
                    if not time:
                        continue
                    start, end = (
                        time.replace("月", "/").replace("日", " ").split("-")[:2]
                    )  # 日替换为空格是因为有日后面不接空格的情况，导致 split 出问题
                    start_time = dateparser.parse(start)
                    end_time = dateparser.parse(end)
                    pool_img = contents[index - 2]
                    r"""两类格式：用/分割，用\分割；★+(概率)+名字，★+名字+(概率)"""
                    for char in chars:
                        star = char.split("（")[0].count("★")
                        name = (
                            re.split(r"[：（]", char)[1]
                            if "★（" not in char
                            else re.split("）：", char)[1]
                        )  # 有的括号在前面有的在后面
                        dual_up = False
                        if "\\" in name:
                            names = name.split("\\")
                            dual_up = True
                        elif "/" in name:
                            names = name.split("/")
                            dual_up = True
                        else:
                            names = [name]  # 既有用/分割的，又有用\分割的

                        names = [name.replace("[限定]", "").strip() for name in names]
                        zoom = 1
                        if "权值" in char:
                            zoom = 0.03
                        else:
                            match = re.search(r"（占.*?的.*?(\d+).*?%）", char)
                            if dual_up == True:
                                zoom = float(match.group(1)) / 2
                            else:
                                zoom = float(match.group(1))
                            zoom = zoom / 100 if zoom > 1 else zoom
                        for name in names:
                            up_chars.append(
                                UpChar(name=name, star=star, limited=False, zoom=zoom)
                            )
                    break  # 这里break会导致个问题：如果一个公告里有两个池子，会漏掉下面的池子，比如 5.19 的定向寻访。但目前我也没啥好想法解决
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
                    logger.info(
                        f"成功获取{self.game_name_cn}当前up信息...当前up池: {title}"
                    )
                break

    async def _reload_pool(self) -> UniMessage | None:
        await self.update_up_char()
        self.load_up_char()
        if self.UP_EVENT:
            return MessageUtils.build_message(
                [
                    f"重载成功！\n当前UP池子：{self.UP_EVENT.title}",
                    self.UP_EVENT.pool_img,
                ]
            )
