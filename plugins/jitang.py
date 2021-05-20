from nonebot import on_command
from util.user_agent import get_user_agent
from bs4 import BeautifulSoup
from services.log import logger
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
import aiohttp


__plugin_name__ = '鸡汤'
__plugin_usage__ = '用法： 要喝一点鸡汤吗？'


url = "https://new.toodo.fun/funs/content?type=du"


jitang = on_command("鸡汤", aliases={"毒鸡汤"}, priority=5, block=True)


@jitang.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if str(event.get_message()) in ['帮助']:
        await jitang.finish(__plugin_usage__)
    try:
        async with aiohttp.ClientSession(headers=get_user_agent()) as session:
            async with session.get(url, timeout=7) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                result = (soup.find_all('h3', {'class': 'text-center'}))[0].text
                await jitang.send(result)
                logger.info(
                    f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
                    f" 发送鸡汤:" + result)
    except Exception as e:
        await jitang.send("出错啦！再试一次吧！", at_sender=True)
        logger.info(f'鸡汤error e:{e}')
