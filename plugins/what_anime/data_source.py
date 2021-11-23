import time
from services.log import logger
from utils.langconv import *
from utils.http_utils import AsyncHttpx


async def get_anime(anime: str) -> str:
    s_time = time.time()
    url = "https://api.trace.moe/search?anilistInfo&url={}".format(anime)
    logger.debug("[info]Now starting get the {}".format(url))
    try:
        anime_json = (await AsyncHttpx.get(url)).json()
        if not anime_json["error"]:
            if anime_json == "Error reading imagenull":
                return "图像源错误，注意必须是静态图片哦"
            repass = ""
            # 拿到动漫 中文名
            for anime in anime_json["result"][:5]:
                synonyms = anime["anilist"]["synonyms"]
                for x in synonyms:
                    _count_ch = 0
                    for word in x:
                        if "\u4e00" <= word <= "\u9fff":
                            _count_ch += 1
                    if _count_ch > 3:
                        anime_name = x
                        break
                else:
                    anime_name = anime["anilist"]["title"]["native"]
                episode = anime["episode"]
                from_ = int(anime["from"])
                m, s = divmod(from_, 60)
                similarity = anime["similarity"]
                putline = "[ {} ][{}][{}:{}] 相似度:{:.2%}".format(
                    Converter("zh-hans").convert(anime_name),
                    episode if episode else "?",
                    m,
                    s,
                    similarity,
                )
                repass += putline + "\n"
            return f"耗时 {int(time.time() - s_time)} 秒\n" + repass[:-1]
        else:
            return f'访问错误 error：{anime_json["error"]}'
    except Exception as e:
        logger.error(f"识番发生错误 {type(e)}：{e}")
        return "发生了奇怪的错误，那就没办法了，再试一次？"
