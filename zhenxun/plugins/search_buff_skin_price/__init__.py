from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import BotConfig
from zhenxun.configs.utils import BaseBlock, PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from .data_source import get_price, update_buff_cookie

__plugin_meta__ = PluginMetadata(
    name="BUFF查询皮肤",
    description="BUFF皮肤底价查询",
    usage="""
    在线实时获取BUFF指定皮肤所有磨损底价
    指令：
        查询皮肤 [枪械名] [皮肤名称]
        示例：查询皮肤 ak47 二西莫夫
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        menu_type="一些工具",
        limits=[BaseBlock(result="您有皮肤正在搜索，请稍等...")],
        configs=[
            RegisterConfig(
                key="BUFF_PROXY",
                value=None,
                help="BUFF代理，有些厂ip可能被屏蔽",
            ),
            RegisterConfig(
                key="COOKIE",
                value=None,
                help="BUFF的账号cookie",
            ),
        ],
    ).dict(),
)


_matcher = on_alconna(
    Alconna("查询皮肤", Args["name", str]["skin", str]),
    aliases={"皮肤查询"},
    priority=5,
    block=True,
)

_cookie_matcher = on_alconna(
    Alconna("设置cookie", Args["cookie", str]),
    rule=to_me(),
    permission=SUPERUSER,
    priority=1,
)


@_matcher.handle()
async def _(name: Match[str], skin: Match[str]):
    if name.available:
        _matcher.set_path_arg("name", name.result)
    if skin.available:
        _matcher.set_path_arg("skin", skin.result)


@_matcher.got_path("name", prompt="要查询什么武器呢？")
@_matcher.got_path("skin", prompt="要查询该武器的什么皮肤呢？")
async def arg_handle(
    session: EventSession,
    arparma: Arparma,
    name: str,
    skin: str,
):
    if name in ["算了", "取消"] or skin in ["算了", "取消"]:
        await MessageUtils.build_message("已取消操作...").finish()
    result = ""
    if name in ["ak", "ak47"]:
        name = "ak-47"
    name = name + " | " + skin
    status_code = -1
    try:
        result, status_code = await get_price(name)
    except FileNotFoundError:
        await MessageUtils.build_message(
            f'请先对{BotConfig.self_nickname}说"设置cookie"来设置cookie！'
        ).send(at_sender=True)
    if status_code in [996, 997, 998]:
        await MessageUtils.build_message(result).finish()
    if result:
        logger.info(f"查询皮肤: {name}", arparma.header_result, session=session)
        await MessageUtils.build_message(result).finish()
    else:
        logger.info(
            f" 查询皮肤：{name} 没有查询到", arparma.header_result, session=session
        )
        await MessageUtils.build_message("没有查询到哦，请检查格式吧").send()


@_cookie_matcher.handle()
async def _(session: EventSession, arparma: Arparma, cookie: str):
    result = update_buff_cookie(cookie)
    await MessageUtils.build_message(result).send(at_sender=True)
    logger.info("更新BUFF COOKIE", arparma.header_result, session=session)
