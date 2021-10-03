from utils.user_agent import get_user_agent
import aiohttp
from utils.utils import get_cookie_text
from configs.path_config import TEXT_PATH
from asyncio.exceptions import TimeoutError
from configs.config import BUFF_PROXY
from pathlib import Path
from services.log import logger


url = "https://buff.163.com/api/market/goods"


async def get_price(dname):
    cookie = {"session": get_cookie_text("buff")}
    name_list = []
    price_list = []
    parameter = {"game": "csgo", "page_num": "1", "search": dname}
    try:
        async with aiohttp.ClientSession(
            cookies=cookie, headers=get_user_agent()
        ) as session:
            async with session.get(
                url, proxy=BUFF_PROXY, params=parameter, timeout=5
            ) as response:
                if response.status == 200:
                    try:
                        if str(await response.text()).find("Login Required") != -1:
                            return "BUFF登录被重置，请联系管理员重新登入", 996
                        data = (await response.json())["data"]
                        total_page = data["total_page"]
                        data = data["items"]
                        for _ in range(total_page):
                            for i in range(len(data)):
                                name = data[i]["name"]
                                price = data[i]["sell_reference_price"]
                                name_list.append(name)
                                price_list.append(price)
                    except Exception as e:
                        return "没有查询到...", 998
                else:
                    return "访问失败！", response.status
    except TimeoutError as e:
        return "访问超时! 请重试或稍后再试!", 997
    result = f"皮肤: {dname}({len(name_list)})\n"
    # result = "皮肤: " + dname + "\n"
    for i in range(len(name_list)):
        result += name_list[i] + ": " + price_list[i] + "\n"
    return result[:-1], 999


def update_buff_cookie(cookie: str):
    _cookie = Path(TEXT_PATH + "cookie/buff.txt")
    try:
        _cookie.parent.mkdir(parents=True, exist_ok=True)
        with open(_cookie, "w") as f:
            f.write(cookie)
        return "更新cookie成功"
    except Exception as e:
        logger.error(f"更新cookie失败 e:{e}")
        return "更新cookie失败"


if __name__ == "__main__":
    print(get_price("awp 二西莫夫"))
