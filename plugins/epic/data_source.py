from httpx import AsyncClient
from datetime import datetime
from nonebot.log import logger
from nonebot.adapters.cqhttp import (
    Bot,
    Event,
    GroupMessageEvent,
)
from configs.config import NICKNAME


# 获取所有 Epic Game Store 促销游戏
# 方法参考：RSSHub /epicgames 路由
# https://github.com/DIYgod/RSSHub/blob/master/lib/routes/epicgames/index.js
async def get_epic_game():
    epic_url = "https://www.epicgames.com/store/backend/graphql-proxy"
    headers = {
        "Referer": "https://www.epicgames.com/store/zh-CN/",
        "Content-Type": "application/json; charset=utf-8",
    }
    data = {
        "query": "query searchStoreQuery($allowCountries: String, $category: String, $count: Int, $country: String!, $keywords: String, $locale: String, $namespace: String, $sortBy: String, $sortDir: String, $start: Int, $tag: String, $withPrice: Boolean = false, $withPromotions: Boolean = false) {\n Catalog {\n searchStore(allowCountries: $allowCountries, category: $category, count: $count, country: $country, keywords: $keywords, locale: $locale, namespace: $namespace, sortBy: $sortBy, sortDir: $sortDir, start: $start, tag: $tag) {\n elements {\n title\n id\n namespace\n description\n effectiveDate\n keyImages {\n type\n url\n }\n seller {\n id\n name\n }\n productSlug\n urlSlug\n url\n items {\n id\n namespace\n }\n customAttributes {\n key\n value\n }\n categories {\n path\n }\n price(country: $country) @include(if: $withPrice) {\n totalPrice {\n discountPrice\n originalPrice\n voucherDiscount\n discount\n currencyCode\n currencyInfo {\n decimals\n }\n fmtPrice(locale: $locale) {\n originalPrice\n discountPrice\n intermediatePrice\n }\n }\n lineOffers {\n appliedRules {\n id\n endDate\n discountSetting {\n discountType\n }\n }\n }\n }\n promotions(category: $category) @include(if: $withPromotions) {\n promotionalOffers {\n promotionalOffers {\n startDate\n endDate\n discountSetting {\n discountType\n discountPercentage\n }\n }\n }\n upcomingPromotionalOffers {\n promotionalOffers {\n startDate\n endDate\n discountSetting {\n discountType\n discountPercentage\n }\n }\n }\n }\n }\n paging {\n count\n total\n }\n }\n }\n}\n",
        "variables": {
            "allowCountries": "CN",
            "category": "freegames",
            "count": 1000,
            "country": "CN",
            "locale": "zh-CN",
            "sortBy": "effectiveDate",
            "sortDir": "asc",
            "withPrice": True,
            "withPromotions": True,
        },
    }
    async with AsyncClient(proxies={"all://": None}) as client:
        try:
            res = await client.post(epic_url, headers=headers, json=data, timeout=10.0)
            resJson = res.json()
            games = resJson["data"]["Catalog"]["searchStore"]["elements"]
            return games
        except Exception as e:
            logger.error(str(e))
            return None


# 获取 Epic Game Store 免费游戏信息
# 处理免费游戏的信息方法借鉴 pip 包 epicstore_api 示例
# https://github.com/SD4RK/epicstore_api/blob/master/examples/free_games_example.py
async def get_epic_free(bot: Bot, event: Event):
    games = await get_epic_game()
    if not games:
        return "Epic 可能又抽风啦，请稍后再试（", 404
    else:
        msg_list = []
        for game in games:
            try:
                msg = ""
                game_name = game["title"]
                game_corp = game["seller"]["name"]
                game_price = game["price"]["totalPrice"]["fmtPrice"]["originalPrice"]
                game_promotions = game["promotions"]["promotionalOffers"]
                upcoming_promotions = game["promotions"]["upcomingPromotionalOffers"]
                if not game_promotions and upcoming_promotions:
                    continue
                else:
                    for image in game["keyImages"]:
                        game_thumbnail = (
                            image["url"] if image["type"] == "Thumbnail" else None
                        )
                    for pair in game["customAttributes"]:
                        game_dev = (
                            pair["value"]
                            if pair["key"] == "developerName"
                            else game_corp
                        )
                        game_pub = (
                            pair["value"]
                            if pair["key"] == "publisherName"
                            else game_corp
                        )
                    game_desp = game["description"]
                    end_date = ""
                    if len(game["promotions"]["promotionalOffers"]) != 0:
                        end_date_iso = game["promotions"]["promotionalOffers"][0][
                            "promotionalOffers"
                        ][0]["endDate"][:-1]
                        end_date = datetime.fromisoformat(end_date_iso).strftime(
                            "%b.%d %H:%M"
                        )
                    # API 返回不包含游戏商店 URL，此处自行拼接，可能出现少数游戏 404 请反馈
                    game_url = f"https://www.epicgames.com/store/zh-CN/p/{game['productSlug'].replace('/home', '')}"
                    msg = (
                        f"[CQ:image,file={game_thumbnail}]\n\n"
                        if game_thumbnail
                        else ""
                    )
                    msg += f"FREE now :: {game_name} ({game_price})\n\n{game_desp}\n\n"
                    msg += (
                        f"游戏由 {game_pub} 发售，"
                        if game_dev == game_pub
                        else f"游戏由 {game_dev} 开发、{game_pub} 出版，"
                    )
                    msg += f"将在 UTC 时间 {end_date} 结束免费游玩，戳链接领取吧~\n{game_url}"
                    _message = msg
                    if isinstance(event, GroupMessageEvent):
                        data = {
                            "type": "node",
                            "data": {
                                "name": f"{NICKNAME}",
                                "uin": f"{bot.self_id}",
                                "content": _message,
                            },
                        }
                        msg_list.append(data)
                    else:
                        msg = "[CQ:image,file={}]\n\nFREE now :: {} ({})\n{}\n此游戏由 {} 开发、{} 发行，将在 UTC 时间 {} 结束免费游玩，戳链接速度加入你的游戏库吧~\n{}\n".format(
                            game_thumbnail,
                            game_name,
                            game_price,
                            game_desp,
                            game_dev,
                            game_pub,
                            end_date,
                            game_url,
                        )
                        msg_list.append(msg)
            except TypeError as e:
                # logger.info(str(e))
                pass
        return msg_list, 200
