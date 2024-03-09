from zhenxun.configs.config import Config
from zhenxun.utils.http_utils import AsyncHttpx


async def get_data(url: str, params: dict | None = None) -> tuple[dict | str, int]:
    """获取ALAPI数据

    参数:
        url: 请求链接
        params: 参数

    返回:
        tuple[dict | str, int]: 返回信息
    """
    if not params:
        params = {}
    params["token"] = Config.get_config("alapi", "ALAPI_TOKEN")
    try:
        data = (await AsyncHttpx.get(url, params=params, timeout=5)).json()
        if data["code"] == 200:
            if not data["data"]:
                return "没有搜索到...", 997
            return data, 200
        else:
            if data["code"] == 101:
                return "缺失ALAPI TOKEN，请在配置文件中填写！", 999
            return f'发生了错误...code：{data["code"]}', 999
    except TimeoutError:
        return "超时了....", 998
