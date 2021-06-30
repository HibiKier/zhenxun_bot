import aiohttp
from utils.utils import get_local_proxy


async def get_data(url: str, params: dict):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, proxy=get_local_proxy(), timeout=2, params=params) as response:
                data = await response.json()
                if data['code'] == 200:
                    if not data['data']:
                        return '没有搜索到...', 997
                    return data, 200
                else:
                    return f'发生了错误...code：{data["code"]}', 999
        except TimeoutError:
            return '超时了....', 998