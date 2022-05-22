from datetime import datetime
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot
from configs.config import NICKNAME
from utils.http_utils import AsyncHttpx


# 获取所有 Epic Game Store 促销游戏
# 方法参考：RSSHub /epicgames 路由
# https://github.com/DIYgod/RSSHub/blob/master/lib/routes/epicgames/index.js
async def get_epic_game():
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
        logger.error(f"Epic 访问接口错误 {type(e)}：{e}")
    return None


# 获取 Epic Game Store 免费游戏信息
# 处理免费游戏的信息方法借鉴 pip 包 epicstore_api 示例
# https://github.com/SD4RK/epicstore_api/blob/master/examples/free_games_example.py
async def get_epic_free(bot: Bot, type_event: str):
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
            game_dev, game_pub, game_thumbnail = (None, None, None)
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
                        _message = "\n由 {} 公司发行的游戏 {} ({}) 在 UTC 时间 {} 即将推出免费游玩，预计截至 {}。".format(
                            game_corp, game_name, game_price, start_date, end_date
                        )
                        data = {
                            "type": "node",
                            "data": {
                                "name": f"这里是{NICKNAME}酱",
                                "uin": f"{bot.self_id}",
                                "content": _message,
                            },
                        }
                        msg_list.append(data)
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
                    # 如 game['customAttributes'] 未找到则均使用 game_corp 值
                    game_dev = game_dev if game_dev is not None else game_corp
                    game_pub = game_pub if game_pub is not None else game_corp
                    game_desp = game["description"]
                    end_date_iso = game["promotions"]["promotionalOffers"][0][
                        "promotionalOffers"
                    ][0]["endDate"][:-1]
                    end_date = datetime.fromisoformat(end_date_iso).strftime(
                        "%b.%d %H:%M"
                    )
                    # API 返回不包含游戏商店 URL，此处自行拼接，可能出现少数游戏 404 请反馈
                    game_url_part = (
                        (game["productSlug"].replace("/home", ""))
                        if ("/home" in game["productSlug"])
                        else game["productSlug"]
                    )
                    game_url = "https://www.epicgames.com/store/zh-CN/p/{}".format(
                        game_url_part
                    )
                    if type_event == "Group":
                        _message = "[CQ:image,file={}]\n\nFREE now :: {} ({})\n{}\n此游戏由 {} 开发、{} 发行，将在 UTC 时间 {} 结束免费游玩，戳链接速度加入你的游戏库吧~\n{}\n".format(
                            game_thumbnail,
                            game_name,
                            game_price,
                            game_desp,
                            game_dev,
                            game_pub,
                            end_date,
                            game_url,
                        )
                        data = {
                            "type": "node",
                            "data": {
                                "name": f"这里是{NICKNAME}酱",
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
