import ujson as json
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.message import MessageUtils

__plugin_meta__ = PluginMetadata(
    name="能不能好好说话",
    description="能不能好好说话，说人话",
    usage="""
    说人话
    指令：
        nbnhhsh [文本]
        能不能好好说话 [文本]
        示例:
        nbnhhsh xsx
    """.strip(),
    extra=PluginExtraData(author="HibiKier", version="0.1", aliases={"nbnhhsh"}).dict(),
)

URL = "https://lab.magiconch.com/api/nbnhhsh/guess"

_matcher = on_alconna(
    Alconna("nbnhhsh", Args["text", str]),
    aliases={"能不能好好说话"},
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(session: EventSession, arparma: Arparma, text: str):
    response = await AsyncHttpx.post(
        URL,
        data=json.dumps({"text": text}),  # type: ignore
        timeout=5,
        headers={"content-type": "application/json"},
    )
    try:
        data = response.json()
        tmp = ""
        result = ""
        for x in data:
            trans = ""
            if x.get("trans"):
                trans = x["trans"][0]
            elif x.get("inputting"):
                trans = "，".join(x["inputting"])
            tmp += f'{x["name"]} -> {trans}\n'
            result += trans
        logger.info(
            f" 发送能不能好好说话: {text} -> {result}",
            arparma.header_result,
            session=session,
        )
        await MessageUtils.build_message(f"{tmp}={result}").send(reply_to=True)
    except (IndexError, KeyError):
        await MessageUtils.build_message("没有找到对应的翻译....").send()
