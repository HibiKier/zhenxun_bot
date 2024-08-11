from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, Option, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.depends import CheckConfig
from zhenxun.utils.image_utils import ImageTemplate
from zhenxun.utils.message import MessageUtils

from .data_source import language, translate_message

__plugin_meta__ = PluginMetadata(
    name="翻译",
    description="出国旅游好助手",
    usage="""
    指令：
        翻译语种: (查看soruce与to可用值，代码与中文都可)
        示例:
        翻译 你好: 将中文翻译为英文
        翻译 Hello: 将英文翻译为中文

        翻译 你好 -to 希腊语: 将"你好"翻译为希腊语
        翻译 你好: 允许form和to使用中文
        翻译 你好 -form:中文 to:日语 你好: 指定原语种并将"你好"翻译为日文
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        menu_type="一些工具",
        configs=[
            RegisterConfig(key="APPID", value=None, help="百度翻译APPID"),
            RegisterConfig(key="SECRET_KEY", value=None, help="百度翻译秘钥"),
        ],
    ).dict(),
)

_matcher = on_alconna(
    Alconna(
        "翻译",
        Args["text", str],
        Option("-s|--source", Args["source_text", str, "auto"]),
        Option("-t|--to", Args["to_text", str, "auto"]),
    ),
    priority=5,
    block=True,
)

_language_matcher = on_alconna(Alconna("翻译语种"), priority=5, block=True)


@_language_matcher.handle()
async def _(session: EventSession, arparma: Arparma):
    s = ""
    column_list = ["语种", "代码"]
    data_list = []
    for key, value in language.items():
        data_list.append([key, value])
    image = await ImageTemplate.table_page("翻译语种", "", column_list, data_list)
    await MessageUtils.build_message(image).send()
    logger.info(f"查看翻译语种", arparma.header_result, session=session)


@_matcher.handle(
    parameterless=[
        CheckConfig(config="APPID"),
        CheckConfig(config="SECRET_KEY"),
    ]
)
async def _(
    session: EventSession,
    arparma: Arparma,
    text: str,
    source_text: Match[str],
    to_text: Match[str],
):
    source = source_text.result if source_text.available else "auto"
    to = to_text.result if to_text.available else "auto"
    values = language.values()
    keys = language.keys()
    if source not in values and source not in keys:
        await MessageUtils.build_message("源语种不支持...").finish()
    if to not in values and to not in keys:
        await MessageUtils.build_message("目标语种不支持...").finish()
    result = await translate_message(text, source, to)
    await MessageUtils.build_message(result).send(reply_to=True)
    logger.info(
        f"source: {source}, to: {to}, 翻译: {text}",
        arparma.header_result,
        session=session,
    )
