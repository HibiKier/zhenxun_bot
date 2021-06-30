import aiohttp
import aiofiles
from utils.utils import get_local_proxy
import feedparser
import platform
from utils.init_result import image
from configs.path_config import IMAGE_PATH
from utils.user_agent import get_user_agent
if platform.system() == 'Windows':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


url = 'https://rsshub.app/epicgames/freegames'


async def get_epic_game() -> str:
    result = '今天没有游戏可以白嫖了！'
    async with aiohttp.ClientSession(headers=get_user_agent()) as session:
        async with session.get(url, proxy=get_local_proxy(), timeout=7) as response:
            data = feedparser.parse(await response.text())['entries']
            if len(data) == 0:
                return result
            index = 0
            for item in data:
                title = item['title']
                img_url = item['summary'][item['summary'].find('src="')+5: item['summary'].rfind('"')]
                async with session.get(img_url, proxy=get_local_proxy(), timeout=7) as res:
                    async with aiofiles.open(IMAGE_PATH + f'temp/epic_{index}.jpg', 'wb') as f:
                        await f.write(await res.read())
                link = item['link']
                result += image(f'epic_{index}.jpg', 'temp') + f'\n【游戏】| {title}\n【链接】 | {link}\n'
                index += 1
    if result != '':
        result = 'epic限免游戏（速速白嫖）：\n' + result
    else:
        result = '今天没有游戏可以白嫖了！'
    return result




# print(asyncio.get_event_loop().run_until_complete(get_epic_game()))


