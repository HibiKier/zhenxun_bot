import random
from typing import Any

from nonebot import on_regex
from nonebot.rule import to_me
from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot.params import Depends, RegexGroup
from nonebot_plugin_session import EventSession
from nonebot_plugin_userinfo import UserInfo, EventUserInfo
from nonebot_plugin_alconna import Option, Alconna, on_alconna, store_true

from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.depends import UserName
from zhenxun.utils.message import MessageUtils
from zhenxun.models.ban_console import BanConsole
from zhenxun.models.friend_user import FriendUser
from zhenxun.configs.config import Config, BotConfig
from zhenxun.models.group_member_info import GroupInfoUser
from zhenxun.configs.utils import RegisterConfig, PluginExtraData

__plugin_meta__ = PluginMetadata(
    name="昵称系统",
    description="区区昵称，才不想叫呢！",
    usage=f"""
    个人昵称，将替换{BotConfig.self_nickname}称呼你的名称，群聊 与 私聊 昵称相互独立，
    全局昵称设置将更改您目前所有群聊中及私聊的昵称
    指令：
        以后叫我 [昵称]: 设置当前群聊/私聊的昵称
        全局昵称设置 [昵称]: 设置当前所有群聊和私聊的昵称
        {BotConfig.self_nickname}我是谁
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.NORMAL,
        menu_type="其他",
        configs=[
            RegisterConfig(
                key="BLACK_WORD",
                value=["爸", "爹", "爷", "父"],
                help="昵称所屏蔽的关键词，已设置的昵称会被替换为 *，"
                "未设置的昵称会在设置时提示",
                default_value=None,
                type=list[str],
            )
        ],
    ).dict(),
)

_nickname_matcher = on_regex(
    "(?:以后)?(?:叫我|请叫我|称呼我)(.*)",
    rule=to_me(),
    priority=5,
    block=True,
)

_global_nickname_matcher = on_regex(
    "设置全局昵称(.*)", rule=to_me(), priority=5, block=True
)

_matcher = on_alconna(
    Alconna(
        "nickname",
        Option("--name", action=store_true, help_text="用户昵称"),
        Option("--cancel", action=store_true, help_text="取消昵称"),
    ),
    rule=to_me(),
    priority=5,
    block=True,
)

_matcher.shortcut(
    "我(是谁|叫什么)",
    command="nickname",
    arguments=["--name"],
    prefix=True,
)

_matcher.shortcut(
    "取消昵称",
    command="nickname",
    arguments=["--cancel"],
    prefix=True,
)


CALL_NAME = [
    "好啦好啦，我知道啦，{}，以后就这么叫你吧",
    f"嗯嗯，{BotConfig.self_nickname}" + "记住你的昵称了哦，{}",
    "好突然，突然要叫你昵称什么的...{}..",
    f"{BotConfig.self_nickname}" + "会好好记住{}的，放心吧",
    "好..好.，那窝以后就叫你{}了.",
]

REMIND = [
    "我肯定记得你啊，你是{}啊",
    "我不会忘记你的，你也不要忘记我！{}",
    f"哼哼，{BotConfig.self_nickname}" + "记忆力可是很好的，{}",
    "嗯？你是失忆了嘛...{}..",
    f"不要小看{BotConfig.self_nickname}" + "的记忆力啊！笨蛋{}！QAQ",
    "哎？{}..怎么了吗..突然这样问..",
]

CANCEL = [
    f"呜..{BotConfig.self_nickname}" + "睡一觉就会忘记的..和梦一样..{}",
    "窝知道了..{}..",
    f"是{BotConfig.self_nickname}" + "哪里做的不好嘛..好吧..晚安{}",
    "呃，{}，下次我绝对绝对绝对不会再忘记你！",
    "可..可恶！{}！太可恶了！呜",
]


def CheckNickname():
    """
    检查名称是否合法
    """

    async def dependency(
        bot: Bot,
        session: EventSession,
        reg_group: tuple[Any, ...] = RegexGroup(),
    ):
        black_word = Config.get_config("nickname", "BLACK_WORD")
        (name,) = reg_group
        logger.debug(f"昵称检查: {name}", "昵称设置", session=session)
        if not name:
            await MessageUtils.build_message("叫你空白？叫你虚空？叫你无名??").finish(
                at_sender=True
            )
        if session.id1 in bot.config.superusers:
            logger.debug(
                f"超级用户设置昵称, 跳过合法检测: {name}", "昵称设置", session=session
            )
            return
        if len(name) > 20:
            await MessageUtils.build_message("昵称可不能超过20个字!").finish(
                at_sender=True
            )
        if name in bot.config.nickname:
            await MessageUtils.build_message("笨蛋！休想占用我的名字! #").finish(
                at_sender=True
            )
        if black_word:
            for x in name:
                if x in black_word:
                    logger.debug("昵称设置禁止字符: [{x}]", "昵称设置", session=session)
                    await MessageUtils.build_message(f"字符 [{x}] 为禁止字符!").finish(
                        at_sender=True
                    )
            for word in black_word:
                if word in name:
                    logger.debug(
                        "昵称设置禁止字符: [{word}]", "昵称设置", session=session
                    )
                    await MessageUtils.build_message(
                        f"字符 [{word}] 为禁止字符!"
                    ).finish(at_sender=True)

    return Depends(dependency)


@_nickname_matcher.handle(parameterless=[CheckNickname()])
async def _(
    session: EventSession,
    user_info: UserInfo = EventUserInfo(),
    reg_group: tuple[Any, ...] = RegexGroup(),
):
    if session.id1:
        (name,) = reg_group
        if len(name) < 5 and random.random() < 0.3:
            name = "~".join(name)
        if gid := session.id3 or session.id2:
            await GroupInfoUser.set_user_nickname(
                session.id1,
                gid,
                name,
                user_info.user_displayname
                or user_info.user_remark
                or user_info.user_name,
                session.platform,
            )
            logger.info(f"设置群昵称成功: {name}", "昵称设置", session=session)
        else:
            await FriendUser.set_user_nickname(
                session.id1,
                name,
                user_info.user_displayname
                or user_info.user_remark
                or user_info.user_name,
                session.platform,
            )
            logger.info(f"设置私聊昵称成功: {name}", "昵称设置", session=session)
        await MessageUtils.build_message(random.choice(CALL_NAME).format(name)).finish(
            reply_to=True
        )
    await MessageUtils.build_message("用户id为空...").send()


@_global_nickname_matcher.handle(parameterless=[CheckNickname()])
async def _(
    session: EventSession,
    nickname: str = UserName(),
    reg_group: tuple[Any, ...] = RegexGroup(),
):
    if session.id1:
        (name,) = reg_group
        await FriendUser.set_user_nickname(
            session.id1,
            name,
            nickname,
            session.platform,
        )
        await GroupInfoUser.filter(user_id=session.id1).update(nickname=name)
        logger.info(f"设置全局昵称成功: {name}", "设置全局昵称", session=session)
        await MessageUtils.build_message(random.choice(CALL_NAME).format(name)).finish(
            reply_to=True
        )
    await MessageUtils.build_message("用户id为空...").send()


@_matcher.assign("name")
async def _(session: EventSession, user_info: UserInfo = EventUserInfo()):
    if session.id1:
        if gid := session.id3 or session.id2:
            nickname = await GroupInfoUser.get_user_nickname(session.id1, gid)
            card = user_info.user_displayname or user_info.user_name
        else:
            nickname = await FriendUser.get_user_nickname(session.id1)
            card = user_info.user_name
        if nickname:
            await MessageUtils.build_message(
                random.choice(REMIND).format(nickname)
            ).finish(reply_to=True)
        else:
            await MessageUtils.build_message(
                random.choice(
                    [
                        "没..没有昵称嘛，{}",
                        "啊，你是{}啊，我想叫你的昵称！",
                        "是{}啊，有什么事吗？",
                        "你是{}？",
                    ]
                ).format(card)
            ).finish(reply_to=True)
    await MessageUtils.build_message("用户id为空...").send()


@_matcher.assign("cancel")
async def _(bot: Bot, session: EventSession, user_info: UserInfo = EventUserInfo()):
    if session.id1:
        gid = session.id3 or session.id2
        if gid:
            nickname = await GroupInfoUser.get_user_nickname(session.id1, gid)
        else:
            nickname = await FriendUser.get_user_nickname(session.id1)
        if nickname:
            await MessageUtils.build_message(
                random.choice(CANCEL).format(nickname)
            ).send(reply_to=True)
            if gid:
                await GroupInfoUser.set_user_nickname(session.id1, gid, "")
            else:
                await FriendUser.set_user_nickname(session.id1, "")
            await BanConsole.ban(session.id1, gid, 9, 60, bot.self_id)
            return
        else:
            await MessageUtils.build_message("你在做梦吗？你没有昵称啊").finish(
                reply_to=True
            )
    await MessageUtils.build_message("用户id为空...").send()
