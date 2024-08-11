from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.message import MessageUtils

__plugin_meta__ = PluginMetadata(
    name="一言二次元语录",
    description="二次元语录给你力量",
    usage="""
    usage：
        一言二次元语录
        指令：
            语录/二次元
    """.strip(),
    extra=PluginExtraData(author="HibiKier", version="0.1").dict(),
)

URL = "https://international.v1.hitokoto.cn/?c=a"

_matcher = on_alconna(Alconna("语录"), aliases={"二次元"}, priority=5, block=True)


@_matcher.handle()
async def _(session: EventSession, arparma: Arparma):
    data = (await AsyncHttpx.get(URL, timeout=5)).json()
    result = f'{data["hitokoto"]}\t——{data["from"]}'
    await MessageUtils.build_message(result).send()
    logger.info(f" 发送语录:" + result, arparma.header_result, session=session)
