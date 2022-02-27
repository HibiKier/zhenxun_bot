import random
from lxml import etree
from typing import List, Tuple
from PIL import ImageDraw
from nonebot.log import logger

try:
    import ujson as json
except ModuleNotFoundError:
    import json

from .base_handle import BaseHandle, BaseData
from ..config import draw_config
from ..util import remove_prohibited_str, cn2py, load_font
from utils.image_utils import BuildImage


class FgoData(BaseData):
    pass


class FgoChar(FgoData):
    pass


class FgoCard(FgoData):
    pass


class FgoHandle(BaseHandle[FgoData]):
    def __init__(self):
        super().__init__("fgo", "命运-冠位指定")
        self.data_files.append("fgo_card.json")
        self.max_star = 5
        self.config = draw_config.fgo
        self.ALL_CHAR: List[FgoChar] = []
        self.ALL_CARD: List[FgoCard] = []

    def get_card(self, mode: int = 1) -> FgoData:
        if mode == 1:
            star = self.get_star(
                [8, 7, 6, 5, 4, 3],
                [
                    self.config.FGO_SERVANT_FIVE_P,
                    self.config.FGO_SERVANT_FOUR_P,
                    self.config.FGO_SERVANT_THREE_P,
                    self.config.FGO_CARD_FIVE_P,
                    self.config.FGO_CARD_FOUR_P,
                    self.config.FGO_CARD_THREE_P,
                ],
            )
        elif mode == 2:
            star = self.get_star(
                [5, 4], [self.config.FGO_CARD_FIVE_P, self.config.FGO_CARD_FOUR_P]
            )
        else:
            star = self.get_star(
                [8, 7, 6],
                [
                    self.config.FGO_SERVANT_FIVE_P,
                    self.config.FGO_SERVANT_FOUR_P,
                    self.config.FGO_SERVANT_THREE_P,
                ],
            )
        if star > 5:
            star -= 3
            chars = [x for x in self.ALL_CHAR if x.star == star and not x.limited]
        else:
            chars = [x for x in self.ALL_CARD if x.star == star and not x.limited]
        return random.choice(chars)

    def get_cards(self, count: int, **kwargs) -> List[Tuple[FgoData, int]]:
        card_list = []  # 获取所有角色
        servant_count = 0  # 保底计算
        card_count = 0  # 保底计算
        for i in range(count):
            servant_count += 1
            card_count += 1
            if card_count == 9:  # 四星卡片保底
                mode = 2
            elif servant_count == 10:  # 三星从者保底
                mode = 3
            else:  # 普通抽
                mode = 1
            card = self.get_card(mode)
            if isinstance(card, FgoCard) and card.star > self.max_star - 2:
                card_count = 0
            if isinstance(card, FgoChar):
                servant_count = 0
            card_list.append((card, i + 1))
        return card_list

    def generate_card_img(self, card: FgoData) -> BuildImage:
        sep_w = 5
        sep_t = 5
        sep_b = 20
        w = 128
        h = 140
        bg = BuildImage(w + sep_w * 2, h + sep_t + sep_b)
        img_path = str(self.img_path / f"{cn2py(card.name)}.png")
        img = BuildImage(w, h, background=img_path)
        bg.paste(img, (sep_w, sep_t), alpha=True)
        # 加名字
        text = card.name[:6] + "..." if len(card.name) > 7 else card.name
        font = load_font(fontsize=16)
        text_w, text_h = font.getsize(text)
        draw = ImageDraw.Draw(bg.markImg)
        draw.text(
            (sep_w + (w - text_w) / 2, h + sep_t + (sep_b - text_h) / 2),
            text,
            font=font,
            fill="gray",
        )
        return bg

    def _init_data(self):
        self.ALL_CHAR = [
            FgoChar(
                name=value["名称"],
                star=int(value["星级"]),
                limited=True
                if not ("圣晶石召唤" in value["入手方式"] or "圣晶石召唤（Story卡池）" in value["入手方式"])
                else False,
            )
            for value in self.load_data().values()
        ]
        self.ALL_CARD = [
            FgoCard(name=value["名称"], star=int(value["星级"]), limited=False)
            for value in self.load_data("fgo_card.json").values()
        ]

    async def _update_info(self):
        # fgo.json
        fgo_info = {}
        for i in range(500):
            url = f"http://fgo.vgtime.com/servant/ajax?card=&wd=&ids=&sort=12777&o=desc&pn={i}"
            result = await self.get_url(url)
            if not result:
                logger.warning(f"更新 {self.game_name_cn} page {i} 出错")
                continue
            fgo_data = json.loads(result)
            if int(fgo_data["nums"]) <= 0:
                break
            for x in fgo_data["data"]:
                name = remove_prohibited_str(x["name"])
                member_dict = {
                    "id": x["id"],
                    "card_id": x["charid"],
                    "头像": x["icon"],
                    "名称": remove_prohibited_str(x["name"]),
                    "职阶": x["classes"],
                    "星级": int(x["star"]),
                    "hp": x["lvmax4hp"],
                    "atk": x["lvmax4atk"],
                    "card_quick": x["cardquick"],
                    "card_arts": x["cardarts"],
                    "card_buster": x["cardbuster"],
                    "宝具": x["tprop"],
                }
                fgo_info[name] = member_dict
        # 更新额外信息
        for key in fgo_info.keys():
            url = f'http://fgo.vgtime.com/servant/{fgo_info[key]["id"]}'
            result = await self.get_url(url)
            if not result:
                fgo_info[key]["入手方式"] = ["圣晶石召唤"]
                logger.warning(f"{self.game_name_cn} 获取额外信息错误 {key}")
                continue
            try:
                dom = etree.HTML(result, etree.HTMLParser())
                obtain = dom.xpath(
                    "//table[contains(string(.),'入手方式')]/tr[8]/td[3]/text()"
                )[0]
                obtain = str(obtain).strip()
                if "限时活动免费获取 活动结束后无法获得" in obtain:
                    obtain = ["活动获取"]
                elif "非限时UP无法获得" in obtain:
                    obtain = ["限时召唤"]
                else:
                    if "&" in obtain:
                        obtain = obtain.split("&")
                    else:
                        obtain = obtain.split(" ")
                obtain = [s.strip() for s in obtain if s.strip()]
                fgo_info[key]["入手方式"] = obtain
            except IndexError:
                fgo_info[key]["入手方式"] = ["圣晶石召唤"]
                logger.warning(f"{self.game_name_cn} 获取额外信息错误 {key}")
        self.dump_data(fgo_info)
        logger.info(f"{self.game_name_cn} 更新成功")
        # fgo_card.json
        fgo_card_info = {}
        for i in range(500):
            url = f"http://fgo.vgtime.com/equipment/ajax?wd=&ids=&sort=12958&o=desc&pn={i}"
            result = await self.get_url(url)
            if not result:
                logger.warning(f"更新 {self.game_name_cn}卡牌 page {i} 出错")
                continue
            fgo_data = json.loads(result)
            if int(fgo_data["nums"]) <= 0:
                break
            for x in fgo_data["data"]:
                name = remove_prohibited_str(x["name"])
                member_dict = {
                    "id": x["id"],
                    "card_id": x["equipid"],
                    "头像": x["icon"],
                    "名称": name,
                    "星级": int(x["star"]),
                    "hp": x["lvmax_hp"],
                    "atk": x["lvmax_atk"],
                    "skill_e": str(x["skill_e"]).split("<br />")[:-1],
                }
                fgo_card_info[name] = member_dict
        self.dump_data(fgo_card_info, "fgo_card.json")
        logger.info(f"{self.game_name_cn} 卡牌更新成功")
        # 下载头像
        for value in fgo_info.values():
            await self.download_img(value["头像"], value["名称"])
        for value in fgo_card_info.values():
            await self.download_img(value["头像"], value["名称"])
