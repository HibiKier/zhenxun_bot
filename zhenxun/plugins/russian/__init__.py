from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Arparma
from nonebot_plugin_alconna import At as alcAt
from nonebot_plugin_alconna import Match, UniMsg
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.depends import UserName
from zhenxun.utils.message import MessageUtils

from .command import (
    _accept_matcher,
    _rank_matcher,
    _record_matcher,
    _refuse_matcher,
    _russian_matcher,
    _settlement_matcher,
    _shoot_matcher,
)
from .data_source import Russian, russian_manage
from .model import RussianUser

__plugin_meta__ = PluginMetadata(
    name="俄罗斯轮盘",
    description="虽然是运气游戏，但这可是战场啊少年",
    usage="""
    又到了决斗时刻
    指令：
        装弹 [子弹数] ?[金额] ?[at]: 开启游戏，装填子弹，可选自定义金额，或邀请决斗对象
        接受对决: 接受当前存在的对决
        拒绝对决: 拒绝邀请的对决
        开枪: 开出未知的一枪
        结算: 强行结束当前比赛 (仅当一方未开枪超过30秒时可使用)
        我的战绩: 对，你的战绩
        轮盘胜场排行/轮盘败场排行/轮盘欧洲人排行/轮盘慈善家排行/轮盘最高连胜排行/轮盘最高连败排行: 各种排行榜
        示例：装弹 3 100 @sdd
        * 注：同一时间群内只能有一场对决 *
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        menu_type="群内小游戏",
        configs=[
            RegisterConfig(
                key="MAX_RUSSIAN_BET_GOLD",
                value=1000,
                help="俄罗斯轮盘最大赌注金额",
                default_value=1000,
                type=int,
            )
        ],
    ).dict(),
)


@_russian_matcher.handle()
async def _(num: Match[str], money: Match[int], at_user: Match[alcAt]):
    if num.available:
        _russian_matcher.set_path_arg("num", num.result)
    if money.available:
        _russian_matcher.set_path_arg("money", money.result)
    if at_user.available:
        _russian_matcher.set_path_arg("at_user", at_user.result.target)


@_russian_matcher.got_path(
    "num", prompt="请输入装填子弹的数量！(最多6颗，输入取消来取消装弹)"
)
async def _(
    bot: Bot,
    session: EventSession,
    message: UniMsg,
    arparma: Arparma,
    num: str,
    money:  Match[int],
    at_user: Match[alcAt],
    uname: str = UserName(),
):
    gid = session.id2
    if message.extract_plain_text() == "取消":
        await MessageUtils.build_message("已取消装弹...").finish()
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    if not gid:
        await MessageUtils.build_message("群组id为空...").finish()
    money = money.result if money.available else 200
    if num in ["取消", "算了"]:
        await MessageUtils.build_message("已取消装弹...").finish()
    if not num.isdigit():
        await MessageUtils.build_message("输入的子弹数必须是数字！").finish(
            reply_to=True
        )
    b_num = int(num)
    if b_num < 0 or b_num > 6:
        await MessageUtils.build_message("子弹数量必须在1-6之间!").finish(reply_to=True)
    _at_user = at_user.result.target if at_user.available else None
    rus = Russian(
        at_user=_at_user, player1=(session.id1, uname), money=money, bullet_num=b_num
    )
    result = await russian_manage.add_russian(bot, gid, rus)
    await result.send()
    logger.info(
        f"添加俄罗斯轮盘 装弹: {b_num}, 金额: {money}",
        arparma.header_result,
        session=session,
    )


@_accept_matcher.handle()
async def _(bot: Bot, session: EventSession, arparma: Arparma, uname: str = UserName()):
    gid = session.id2
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    if not gid:
        await MessageUtils.build_message("群组id为空...").finish()
    result = await russian_manage.accept(bot, gid, session.id1, uname)
    await result.send()
    logger.info(f"俄罗斯轮盘接受对决", arparma.header_result, session=session)


@_refuse_matcher.handle()
async def _(session: EventSession, arparma: Arparma, uname: str = UserName()):
    gid = session.id2
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    if not gid:
        await MessageUtils.build_message("群组id为空...").finish()
    result = russian_manage.refuse(gid, session.id1, uname)
    await result.send()
    logger.info(f"俄罗斯轮盘拒绝对决", arparma.header_result, session=session)


@_settlement_matcher.handle()
async def _(session: EventSession, arparma: Arparma):
    gid = session.id2
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    if not gid:
        await MessageUtils.build_message("群组id为空...").finish()
    result = await russian_manage.settlement(gid, session.id1, session.platform)
    await result.send()
    logger.info(f"俄罗斯轮盘结算", arparma.header_result, session=session)


@_shoot_matcher.handle()
async def _(bot: Bot, session: EventSession, arparma: Arparma, uname: str = UserName()):
    gid = session.id2
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    if not gid:
        await MessageUtils.build_message("群组id为空...").finish()
    result, settle = await russian_manage.shoot(
        bot, gid, session.id1, uname, session.platform
    )
    await result.send()
    if settle:
        await settle.send()
    logger.info(f"俄罗斯轮盘开枪", arparma.header_result, session=session)


@_record_matcher.handle()
async def _(session: EventSession, arparma: Arparma):
    gid = session.id2
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    if not gid:
        await MessageUtils.build_message("群组id为空...").finish()
    user, _ = await RussianUser.get_or_create(user_id=session.id1, group_id=gid)
    await MessageUtils.build_message(
        f"俄罗斯轮盘\n"
        f"总胜利场次：{user.win_count}\n"
        f"当前连胜：{user.winning_streak}\n"
        f"最高连胜：{user.max_winning_streak}\n"
        f"总失败场次：{user.fail_count}\n"
        f"当前连败：{user.losing_streak}\n"
        f"最高连败：{user.max_losing_streak}\n"
        f"赚取金币：{user.make_money}\n"
        f"输掉金币：{user.lose_money}",
    ).send(reply_to=True)
    logger.info(f"俄罗斯轮盘查看战绩", arparma.header_result, session=session)


@_rank_matcher.handle()
async def _(session: EventSession, arparma: Arparma, rank_type: str, num: int):
    gid = session.id2
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    if not gid:
        await MessageUtils.build_message("群组id为空...").finish()
    if 51 < num or num < 10:
        num = 10
    result = await russian_manage.rank(session.id1, gid, rank_type, num)
    if isinstance(result, str):
        await MessageUtils.build_message(result).finish(reply_to=True)
    result.show()
    await MessageUtils.build_message(result).send(reply_to=True)
    logger.info(
        f"查看轮盘排行: {rank_type} 数量: {num}", arparma.header_result, session=session
    )
