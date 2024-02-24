from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Arparma,
    Option,
    on_alconna,
    store_true,
)
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_saa import Image, Text
from nonebot_plugin_session import EventSession
from nonebot_plugin_userinfo import EventUserInfo, UserInfo

from zhenxun.configs.utils import PluginCdBlock, PluginExtraData, RegisterConfig
from zhenxun.services.log import logger

from ._data_source import SignManage
from .goods_register import driver
from .utils import clear_sign_data_pic

__plugin_meta__ = PluginMetadata(
    name="签到",
    description="每日签到，证明你在这里",
    usage="""
    每日签到
    会影响色图概率和开箱次数，以及签到的随机道具获取
    指令：
        我的签到
        好感度排行
    * 签到时有 3% 概率 * 2 *
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        configs=[
            RegisterConfig(
                module="send_setu",
                key="INITIAL_SETU_PROBABILITY",
                value=0.7,
                help="初始色图概率，总概率 = 初始色图概率 + 好感度",
                default_value=0.7,
                type=float,
            ),
            RegisterConfig(
                key="MAX_SIGN_GOLD",
                value=200,
                help="签到好感度加成额外获得的最大金币数",
                default_value=200,
                type=int,
            ),
            RegisterConfig(
                key="SIGN_CARD1_PROB",
                value=0.2,
                help="签到好感度双倍加持卡Ⅰ掉落概率",
                default_value=0.2,
                type=float,
            ),
            RegisterConfig(
                key="SIGN_CARD2_PROB",
                value=0.09,
                help="签到好感度双倍加持卡Ⅲ掉落概率",
                default_value=0.09,
                type=float,
            ),
            RegisterConfig(
                key="SIGN_CARD3_PROB",
                value=0.05,
                help="签到好感度双倍加持卡Ⅲ掉落概率",
                default_value=0.05,
                type=float,
            ),
        ],
        limits=[PluginCdBlock()],
    ).dict(),
)


_sign_matcher = on_alconna(
    Alconna(
        "签到",
        Option("--my", action=store_true, help_text="我的签到"),
        Option(
            "-l|--list", Args["num", int, 10], action=store_true, help_text="好感度排行"
        ),
    ),
    priority=5,
    block=True,
)

# TODO: shortcut


@_sign_matcher.assign("$main")
async def _(
    session: EventSession, arparma: Arparma, user_info: UserInfo = EventUserInfo()
):
    nickname = (
        user_info.user_displayname or user_info.user_remark or user_info.user_name
    )
    if session.id1:
        if path := await SignManage.sign(session, nickname):
            logger.info("签到成功", arparma.header_result, session=session)
            await Image(path).finish(reply=True)
    return Text("用户id为空...").send()


@_sign_matcher.assign("my")
async def _(
    session: EventSession, arparma: Arparma, user_info: UserInfo = EventUserInfo()
):
    nickname = (
        user_info.user_displayname or user_info.user_remark or user_info.user_name
    )
    if session.id1:
        if image := await SignManage.sign(session, nickname, True):
            logger.info("查看我的签到", arparma.header_result, session=session)
            await Image(image).finish(reply=True)
    return Text("用户id为空...").send()


@_sign_matcher.assign("list")
async def _(
    session: EventSession,
    arparma: Arparma,
    num: int,
    user_info: UserInfo = EventUserInfo(),
):
    nickname = (
        user_info.user_displayname or user_info.user_remark or user_info.user_name
    )
    if session.id1:
        if image := await SignManage.rank(session.id1, num):
            logger.info("查看签到排行", arparma.header_result, session=session)
            await Image(image.pic2bs4()).finish()
    return Text("用户id为空...").send()


@scheduler.scheduled_job(
    "interval",
    hours=1,
)
async def _():
    try:
        clear_sign_data_pic()
        logger.info("清理日常签到图片数据数据完成...", "签到")
    except Exception as e:
        logger.error(f"清理日常签到图片数据数据失败...", e=e)
