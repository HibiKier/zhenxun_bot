from decimal import Decimal

from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, At, Field, on_alconna
from nonebot_plugin_uninfo import Uninfo

from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.sign_user import SignUser
from zhenxun.models.user_console import UserConsole
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.platform import PlatformUtils

__plugin_meta__ = PluginMetadata(
    name="高贵的作弊器",
    description="这是一个作弊器，设置用户金币数量和好感度",
    usage="""
    金币设置 100（金币数量） @用户
    好感度设置 100（好感度） @用户
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).to_dict(),
)

_gold_matcher = on_alconna(
    Alconna(
        "金币设置",
        Args[
            "gold",
            int,
            Field(
                missing_tips=lambda: "请在命令后跟随金币数量！",
                unmatch_tips=lambda _: "金币数量必须为数字！",
            ),
        ][
            "at_user",
            At,
            Field(
                missing_tips=lambda: "必须要at一名指定用户！",
            ),
        ],
    ),
    skip_for_unmatch=False,
    permission=SUPERUSER,
    priority=5,
    block=True,
)


_impression_matcher = on_alconna(
    Alconna(
        "好感度设置",
        Args[
            "impression",
            float,
            Field(
                missing_tips=lambda: "请在命令后跟随好感度！",
                unmatch_tips=lambda _: "好感度数量必须为数字！",
            ),
        ][
            "at_user",
            At,
            Field(
                missing_tips=lambda: "必须要at一名指定用户！",
            ),
        ],
    ),
    skip_for_unmatch=False,
    permission=SUPERUSER,
    priority=5,
    block=True,
)


@_gold_matcher.handle()
async def _(session: Uninfo, arparma: Arparma, gold: int, at_user: At):
    user = await UserConsole.get_user(
        at_user.target, PlatformUtils.get_platform(session)
    )
    user.gold = gold
    await user.save(update_fields=["gold"])
    await MessageUtils.build_message(
        ["成功将用户", at_user, f"的金币设置为 {gold}"]
    ).send(reply_to=True)
    logger.info(
        f"成功将用户{at_user.target}的金币设置为{gold}",
        arparma.header_result,
        session=session,
    )


@_impression_matcher.handle()
async def _(session: Uninfo, arparma: Arparma, impression: float, at_user: At):
    platform = PlatformUtils.get_platform(session)
    user_console = await UserConsole.get_user(at_user.target, platform)
    user, _ = await SignUser.get_or_create(
        user_id=at_user.target,
        defaults={"user_console": user_console, "platform": platform},
    )
    user.impression = Decimal(impression)
    await user.save(update_fields=["impression"])
    await MessageUtils.build_message(
        ["成功将用户", at_user, f"的好感度设置为 {impression}"]
    ).send(reply_to=True)
    logger.info(
        f"成功将用户{at_user.target}的好感度设置为{impression}",
        arparma.header_result,
        session=session,
    )
