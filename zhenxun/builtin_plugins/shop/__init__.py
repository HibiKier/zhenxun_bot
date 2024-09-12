from nonebot.adapters import Bot, Event
from nonebot.plugin import PluginMetadata
from nonebot_plugin_session import EventSession
from nonebot_plugin_userinfo import UserInfo, EventUserInfo
from nonebot_plugin_alconna import (
    Args,
    Query,
    Option,
    UniMsg,
    Alconna,
    Arparma,
    Subcommand,
    UniMessage,
    AlconnaQuery,
    on_alconna,
    store_true,
)

from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.exception import GoodsNotFound
from zhenxun.utils.enum import BlockType, PluginType
from zhenxun.configs.utils import BaseBlock, PluginExtraData

from ._data_source import ShopManage, gold_rank

__plugin_meta__ = PluginMetadata(
    name="商店",
    description="商店系统[金币回收计划]",
    usage="""
    商品操作
    指令：
        我的金币
        我的道具
        使用道具 [名称/Id]
        购买道具 [名称/Id]
        金币排行 ?[num=10]
        金币总排行 ?[num=10]
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.NORMAL,
        menu_type="商店",
        limits=[BaseBlock(check_type=BlockType.GROUP)],
    ).dict(),
)


_matcher = on_alconna(
    Alconna(
        "商店",
        Option("--all", action=store_true),
        Subcommand("my-cost", help_text="我的金币"),
        Subcommand("my-props", help_text="我的道具"),
        Subcommand("buy", Args["name", str]["num", int, 1], help_text="购买道具"),
        Subcommand("use", Args["name", str]["num?", int, 1], help_text="使用道具"),
        Subcommand("gold-list", Args["num?", int], help_text="金币排行"),
    ),
    priority=5,
    block=True,
)

_matcher.shortcut(
    "我的金币",
    command="商店",
    arguments=["my-cost"],
    prefix=True,
)

_matcher.shortcut(
    "我的道具",
    command="商店",
    arguments=["my-props"],
    prefix=True,
)

_matcher.shortcut(
    "购买道具",
    command="商店",
    arguments=["buy", "{%0}"],
    prefix=True,
)

_matcher.shortcut(
    "使用道具",
    command="商店",
    arguments=["use", "{%0}"],
    prefix=True,
)

_matcher.shortcut(
    "金币排行",
    command="商店",
    arguments=["gold-list"],
    prefix=True,
)

_matcher.shortcut(
    r"金币总排行",
    command="商店",
    arguments=["--all", "gold-list"],
    prefix=True,
)


@_matcher.assign("$main")
async def _(session: EventSession, arparma: Arparma):
    image = await ShopManage.build_shop_image()
    logger.info("查看商店", arparma.header_result, session=session)
    await MessageUtils.build_message(image).send()


@_matcher.assign("my-cost")
async def _(session: EventSession, arparma: Arparma):
    if session.id1:
        logger.info("查看金币", arparma.header_result, session=session)
        gold = await ShopManage.my_cost(session.id1, session.platform)
        await MessageUtils.build_message(f"你的当前余额: {gold}").send(reply_to=True)
    else:
        await MessageUtils.build_message("用户id为空...").send(reply_to=True)


@_matcher.assign("my-props")
async def _(
    session: EventSession, arparma: Arparma, user_info: UserInfo = EventUserInfo()
):
    if session.id1:
        logger.info("查看道具", arparma.header_result, session=session)
        if image := await ShopManage.my_props(
            session.id1,
            user_info.user_displayname or user_info.user_name,
            session.platform,
        ):
            await MessageUtils.build_message(image.pic2bytes()).finish(reply_to=True)
        return await MessageUtils.build_message("你的道具为空捏...").send(reply_to=True)
    else:
        await MessageUtils.build_message("用户id为空...").send(reply_to=True)


@_matcher.assign("buy")
async def _(session: EventSession, arparma: Arparma, name: str, num: int):
    if session.id1:
        logger.info(
            f"购买道具 {name}, 数量: {num}",
            arparma.header_result,
            session=session,
        )
        result = await ShopManage.buy_prop(session.id1, name, num, session.platform)
        await MessageUtils.build_message(result).send(reply_to=True)
    else:
        await MessageUtils.build_message("用户id为空...").send(reply_to=True)


@_matcher.assign("use")
async def _(
    bot: Bot,
    event: Event,
    message: UniMsg,
    session: EventSession,
    arparma: Arparma,
    name: str,
    num: int,
):
    try:
        result = await ShopManage.use(bot, event, session, message, name, num, "")
        logger.info(
            f"使用道具 {name}, 数量: {num}", arparma.header_result, session=session
        )
        if isinstance(result, str):
            await MessageUtils.build_message(result).send(reply_to=True)
        elif isinstance(result, UniMessage):
            await result.finish(reply_to=True)
    except GoodsNotFound:
        await MessageUtils.build_message(f"没有找到道具 {name} 或道具数量不足...").send(
            reply_to=True
        )


@_matcher.assign("gold-list")
async def _(
    session: EventSession, arparma: Arparma, num: Query[int] = AlconnaQuery("num", 10)
):
    if num.result > 50:
        await MessageUtils.build_message("排行榜人数不能超过50哦...").finish()
    if session.id1:
        gid = session.id3 or session.id2
        if not arparma.find("all") and not gid:
            await MessageUtils.build_message(
                "私聊中无法查看 '金币排行'，请发送 '金币总排行'"
            ).finish()
        if arparma.find("all"):
            gid = None
        result = await gold_rank(session.id1, gid, num.result, session.platform)
        logger.info(
            "查看金币排行",
            arparma.header_result,
            session=session,
        )
        await MessageUtils.build_message(result).send(reply_to=True)
    else:
        await MessageUtils.build_message("用户id为空...").send(reply_to=True)
