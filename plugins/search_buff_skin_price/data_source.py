from asyncio.exceptions import TimeoutError
from configs.config import Config
from utils.http_utils import AsyncHttpx
from services.log import logger


url = "https://buff.163.com/api/market/goods"


async def get_price(d_name: str) -> "str, int":
    """
    查看皮肤价格
    :param d_name: 武器皮肤，如：awp 二西莫夫
    """
    cookie = {"session": Config.get_config("search_buff_skin_price", "COOKIE")}
    name_list = []
    price_list = []
    parameter = {"game": "csgo", "page_num": "1", "search": d_name}
    try:
        response = await AsyncHttpx.get(
            url,
            proxy=Config.get_config("search_buff_skin_price", "BUFF_PROXY"),
            params=parameter,
            cookies=cookie,
        )
        if response.status_code == 200:
            try:
                if response.text.find("Login Required") != -1:
                    return "BUFF登录被重置，请联系管理员重新登入", 996
                data = response.json()["data"]
                total_page = data["total_page"]
                data = data["items"]
                for _ in range(total_page):
                    for i in range(len(data)):
                        name = data[i]["name"]
                        price = data[i]["sell_reference_price"]
                        name_list.append(name)
                        price_list.append(price)
            except Exception as e:
                logger.error(f"BUFF查询皮肤发生错误 {type(e)}：{e}")
                return "没有查询到...", 998
        else:
            return "访问失败！", response.status_code
    except TimeoutError:
        return "访问超时! 请重试或稍后再试!", 997
    result = f"皮肤: {d_name}({len(name_list)})\n"
    for i in range(len(name_list)):
        result += name_list[i] + ": " + price_list[i] + "\n"
    return result[:-1], 999


def update_buff_cookie(cookie: str) -> str:
    Config.set_config("search_buff_skin_price", "COOKIE", cookie)
    return "更新cookie成功"


if __name__ == "__main__":
    print(get_price("awp 二西莫夫"))
