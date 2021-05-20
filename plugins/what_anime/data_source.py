
import time
from services.log import logger
from util.langconv import *
import aiohttp
from util.user_agent import get_user_agent


async def get_anime(anime: str) -> str:
    s_time = time.time()
    url = 'https://trace.moe/api/search?url={}'.format(anime)
    logger.debug("[info]Now starting get the {}".format(url))
    try:
        async with aiohttp.ClientSession(headers=get_user_agent()) as session:
            async with session.get(url, timeout=45) as response:
                if response.status == 200:
                    anime_json = await response.json()
                    if anime_json == 'Error reading imagenull':
                        return "图像源错误，注意必须是静态图片哦"
                    repass = ""
                    for anime in anime_json["docs"][:5]:
                        anime_name = anime["anime"]
                        episode = anime["episode"]
                        at = int(anime["at"])
                        m, s = divmod(at, 60)
                        similarity = anime["similarity"]
                        putline = "[ {} ][{}][{}:{}] 相似度:{:.2%}". \
                            format(Converter("zh-hans").convert(anime_name),
                                   episode if episode else '?', m, s, similarity)
                        repass += putline + '\n'
                    return f'耗时 {int(time.time() - s_time)} 秒\n' + repass[:-1]
                else:
                    return f'访问失败，请再试一次吧, status: {response.status}'
    except Exception:
        return '直接超时，那就没办法了，再试一次？'
