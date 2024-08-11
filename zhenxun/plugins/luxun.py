from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.configs.utils import BaseBlock, PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.image_utils import BuildImage
from zhenxun.utils.message import MessageUtils

__plugin_meta__ = PluginMetadata(
    name="鲁迅说",
    description="鲁迅说了啥？",
    usage="""
    鲁迅说 [文本]
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        limits=[BaseBlock(result="你的鲁迅正在说，等会")],
    ).dict(),
)

_matcher = on_alconna(
    Alconna("luxun", Args["content", str]),
    priority=5,
    block=True,
)

_matcher.shortcut(
    "鲁迅说",
    command="luxun",
    arguments=["{%0}"],
    prefix=True,
)


_sign = None


@_matcher.handle()
async def _(content: Match[str]):
    if content.available:
        _matcher.set_path_arg("content", content.result)


@_matcher.got_path("content", prompt="你让鲁迅说点啥?")
async def _(content: str, session: EventSession, arparma: Arparma):
    global _sign
    if content.startswith(",") or content.startswith("，"):
        content = content[1:]
    A = BuildImage(
        font_size=37, background=f"{IMAGE_PATH}/other/luxun.jpg", font="msyh.ttf"
    )
    text = ""
    if len(content) > 40:
        await MessageUtils.build_message("太长了，鲁迅说不完...").finish()
    while A.getsize(content)[0] > A.width - 50:
        n = int(len(content) / 2)
        text += content[:n] + "\n"
        content = content[n:]
    text += content
    if len(text.split("\n")) > 2:
        await MessageUtils.build_message("太长了，鲁迅说不完...").finish()
    await A.text(
        (int((480 - A.getsize(text.split("\n")[0])[0]) / 2), 300), text, (255, 255, 255)
    )
    if not _sign:
        _sign = await BuildImage.build_text_image(
            "--鲁迅", "msyh.ttf", 30, (255, 255, 255)
        )
    await A.paste(_sign, (320, 400))
    await MessageUtils.build_message(A).send()
    logger.info(f"鲁迅说: {content}", arparma.header_result, session=session)
