from datetime import datetime

from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Bot as v11Bot
from nonebot.adapters.onebot.v12 import Bot as v12Bot
from nonebot_plugin_alconna import Image, UniMessage

from zhenxun.configs.config import NICKNAME
from zhenxun.services.log import logger
from zhenxun.utils._build_image import BuildImage
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.message import MessageUtils


# 获取所有 Epic Game Store 促销游戏
# 方法参考：RSSHub /epicgames 路由
# https://github.com/DIYgod/RSSHub/blob/master/lib/v2/epicgames/index.js
async def get_epic_game() -> dict | None:
    epic_url = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=zh-CN&country=CN&allowCountries=CN"
    headers = {
        "Referer": "https://www.epicgames.com/store/zh-CN/",
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
    }
    try:
        res = await AsyncHttpx.get(epic_url, headers=headers, timeout=10)
        res_json = res.json()
        games = res_json["data"]["Catalog"]["searchStore"]["elements"]
        return games
    except Exception as e:
        logger.error(f"Epic 访问接口错误", e=e)
    return None


# 此处用于获取游戏简介
async def get_epic_game_desp(name) -> dict | None:
    desp_url = (
        "https://store-content-ipv4.ak.epicgames.com/api/zh-CN/content/products/"
        + str(name)
    )
    headers = {
        "Referer": "https://store.epicgames.com/zh-CN/p/" + str(name),
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
    }
    try:
        res = await AsyncHttpx.get(desp_url, headers=headers, timeout=10)
        res_json = res.json()
        gamesDesp = res_json["pages"][0]["data"]["about"]
        return gamesDesp
    except Exception as e:
        logger.error(f"Epic 访问接口错误", e=e)
    return None


# 获取 Epic Game Store 免费游戏信息
# 处理免费游戏的信息方法借鉴 pip 包 epicstore_api 示例
# https://github.com/SD4RK/epicstore_api/blob/master/examples/free_games_example.py
async def get_epic_free(
    bot: Bot, type_event: str
) -> tuple[UniMessage | list | str, int]:
    games = await get_epic_game()
    if not games:
        return "Epic 可能又抽风啦，请稍后再试（", 404
    else:
        msg_list = []
        for game in games:
            game_name = game["title"]
            game_corp = game["seller"]["name"]
            game_price = game["price"]["totalPrice"]["fmtPrice"]["originalPrice"]
            # 赋初值以避免 local variable referenced before assignment
            game_thumbnail, game_dev, game_pub = None, game_corp, game_corp
            try:
                game_promotions = game["promotions"]["promotionalOffers"]
                upcoming_promotions = game["promotions"]["upcomingPromotionalOffers"]
                if not game_promotions and upcoming_promotions:
                    # 促销暂未上线，但即将上线
                    promotion_data = upcoming_promotions[0]["promotionalOffers"][0]
                    start_date_iso, end_date_iso = (
                        promotion_data["startDate"][:-1],
                        promotion_data["endDate"][:-1],
                    )
                    # 删除字符串中最后一个 "Z" 使 Python datetime 可处理此时间
                    start_date = datetime.fromisoformat(start_date_iso).strftime(
                        "%b.%d %H:%M"
                    )
                    end_date = datetime.fromisoformat(end_date_iso).strftime(
                        "%b.%d %H:%M"
                    )
                    if type_event == "Group":
                        _message = f"\n由 {game_corp} 公司发行的游戏 {game_name} ({game_price}) 在 UTC 时间 {start_date} 即将推出免费游玩，预计截至 {end_date}。"
                        msg_list.append(_message)
                    else:
                        msg = "\n由 {} 公司发行的游戏 {} ({}) 在 UTC 时间 {} 即将推出免费游玩，预计截至 {}。".format(
                            game_corp, game_name, game_price, start_date, end_date
                        )
                        msg_list.append(msg)
                else:
                    for image in game["keyImages"]:
                        if (
                            image.get("url")
                            and not game_thumbnail
                            and image["type"]
                            in [
                                "Thumbnail",
                                "VaultOpened",
                                "DieselStoreFrontWide",
                                "OfferImageWide",
                            ]
                        ):
                            game_thumbnail = image["url"]
                            break
                    for pair in game["customAttributes"]:
                        if pair["key"] == "developerName":
                            game_dev = pair["value"]
                        if pair["key"] == "publisherName":
                            game_pub = pair["value"]
                    if game.get("productSlug"):
                        if gamesDesp := await get_epic_game_desp(game["productSlug"]):
                            try:
                                # 是否存在简短的介绍
                                if "shortDescription" in gamesDesp:
                                    game_desp = gamesDesp["shortDescription"]
                            except KeyError:
                                game_desp = gamesDesp["description"]
                    else:
                        game_desp = game["description"]
                    try:
                        end_date_iso = game["promotions"]["promotionalOffers"][0][
                            "promotionalOffers"
                        ][0]["endDate"][:-1]
                        end_date = datetime.fromisoformat(end_date_iso).strftime(
                            "%b.%d %H:%M"
                        )
                    except IndexError:
                        end_date = "未知"
                    # API 返回不包含游戏商店 URL，此处自行拼接，可能出现少数游戏 404 请反馈
                    if game.get("productSlug"):
                        game_url = "https://store.epicgames.com/zh-CN/p/{}".format(
                            game["productSlug"].replace("/home", "")
                        )
                    elif game.get("url"):
                        game_url = game["url"]
                    else:
                        slugs = (
                            [
                                x["pageSlug"]
                                for x in game.get("offerMappings", [])
                                if x.get("pageType") == "productHome"
                            ]
                            + [
                                x["pageSlug"]
                                for x in game.get("catalogNs", {}).get("mappings", [])
                                if x.get("pageType") == "productHome"
                            ]
                            + [
                                x["value"]
                                for x in game.get("customAttributes", [])
                                if "productSlug" in x.get("key")
                            ]
                        )
                        game_url = "https://store.epicgames.com/zh-CN{}".format(
                            f"/p/{slugs[0]}" if len(slugs) else ""
                        )
                    if isinstance(bot, (v11Bot, v12Bot)) and type_event == "Group":
                        _message = [
                            Image(url=game_thumbnail),
                            f"\nFREE now :: {game_name} ({game_price})\n{game_desp}\n此游戏由 {game_dev} 开发、{game_pub} 发行，将在 UTC 时间 {end_date} 结束免费游玩，戳链接速度加入你的游戏库吧~\n{game_url}\n",
                        ]
                        msg_list.append(_message)
                    else:
                        _message = []
                        if game_thumbnail:
                            _message.append(Image(url=game_thumbnail))
                        _message.append(
                            f"\n\nFREE now :: {game_name} ({game_price})\n{game_desp}\n此游戏由 {game_dev} 开发、{game_pub} 发行，将在 UTC 时间 {end_date} 结束免费游玩，戳链接速度加入你的游戏库吧~\n{game_url}\n"
                        )
                        return MessageUtils.build_message(_message), 200
            except TypeError as e:
                # logger.info(str(e))
                pass
        return MessageUtils.template2forward(msg_list, bot.self_id), 200
