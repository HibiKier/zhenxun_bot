import random
from typing import Any, List, Tuple

from nonebot import on_command, on_regex
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageEvent
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import Depends
from nonebot.params import CommandArg, RegexGroup
from nonebot.rule import to_me

from configs.config import NICKNAME
from models.ban_user import BanUser
from models.friend_user import FriendUser
from models.group_member_info import GroupInfoUser
from services.log import logger
from utils.depends import GetConfig

__zx_plugin_name__ = "昵称系统"
__plugin_usage__ = f"""
usage：
    个人昵称，将替换真寻称呼你的名称，群聊 与 私聊 昵称相互独立，全局昵称设置将更改您目前所有群聊中及私聊的昵称
    指令：
        以后叫我 [昵称]: 设置当前群聊/私聊的昵称
        全局昵称设置 [昵称]: 设置当前所有群聊和私聊的昵称
        {NICKNAME}我是谁
""".strip()
__plugin_des__ = "区区昵称，才不想叫呢！"
__plugin_cmd__ = ["以后叫我 [昵称]", f"{NICKNAME}我是谁", "全局昵称设置 [昵称]"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["昵称"],
}
__plugin_configs__ = {
    "BLACK_WORD": {
        "value": ["爸", "爹", "爷", "父"],
        "help": "昵称所屏蔽的关键词，已设置的昵称会被替换为 *，未设置的昵称会在设置时提示",
        "default_value": None,
        "type": List[str],
    }
}

nickname = on_regex(
    "(?:以后)?(?:叫我|请叫我|称呼我)(.*)",
    rule=to_me(),
    priority=5,
    block=True,
)

my_nickname = on_command(
    "我叫什么", aliases={"我是谁", "我的名字"}, rule=to_me(), priority=5, block=True
)

global_nickname = on_regex("设置全局昵称(.*)", rule=to_me(), priority=5, block=True)


cancel_nickname = on_command("取消昵称", rule=to_me(), priority=5, block=True)


def CheckNickname():
    """
    说明:
        检查名称是否合法
    """

    async def dependency(
        bot: Bot,
        matcher: Matcher,
        event: MessageEvent,
        reg_group: Tuple[Any, ...] = RegexGroup(),
        black_word: Any = GetConfig(config="BLACK_WORD"),
    ):
        (msg,) = reg_group
        logger.debug(f"昵称检查: {msg}", "昵称设置", event.user_id)
        if not msg:
            await matcher.finish("叫你空白？叫你虚空？叫你无名？？", at_sender=True)
        if str(event.user_id) in bot.config.superusers:
            logger.debug(f"超级用户设置昵称, 跳过合法检测: {msg}", "昵称设置", event.user_id)
            return
        if len(msg) > 20:
            await nickname.finish("昵称可不能超过20个字！", at_sender=True)
        if msg in bot.config.nickname:
            await nickname.finish("笨蛋！休想占用我的名字！#", at_sender=True)
        if black_word:
            for x in msg:
                if x in black_word:
                    logger.debug("昵称设置禁止字符: [{x}]", "昵称设置", event.user_id)
                    await nickname.finish(f"字符 [{x}] 为禁止字符！", at_sender=True)
            for word in black_word:
                if word in msg:
                    logger.debug("昵称设置禁止字符: [{word}]", "昵称设置", event.user_id)
                    await nickname.finish(f"字符 [{word}] 为禁止字符！", at_sender=True)

    return Depends(dependency)


@global_nickname.handle(parameterless=[CheckNickname()])
async def _(
    event: MessageEvent,
    reg_group: Tuple[Any, ...] = RegexGroup(),
):
    (msg,) = reg_group
    await FriendUser.set_user_nickname(event.user_id, msg)
    await GroupInfoUser.filter(user_id=str(event.user_id)).update(nickname=msg)
    logger.info(f"设置全局昵称成功: {msg}", "设置全局昵称", event.user_id)
    await global_nickname.send(f"设置全局昵称成功！亲爱的{msg}")


@nickname.handle(parameterless=[CheckNickname()])
async def _(
    event: MessageEvent,
    reg_group: Tuple[Any, ...] = RegexGroup(),
):
    (msg,) = reg_group
    if isinstance(event, GroupMessageEvent):
        await GroupInfoUser.set_user_nickname(event.user_id, event.group_id, msg)
        if len(msg) < 5:
            if random.random() < 0.3:
                msg = "~".join(msg)
        await nickname.send(
            random.choice(
                [
                    f"好啦好啦，我知道啦，{msg}，以后就这么叫你吧",
                    f"嗯嗯，{NICKNAME}记住你的昵称了哦，{msg}",
                    f"好突然，突然要叫你昵称什么的...{msg}..",
                    f"{NICKNAME}会好好记住{msg}的，放心吧",
                    f"好..好.，那窝以后就叫你{msg}了.",
                ]
            )
        )
        logger.info(f"设置群昵称成功: {msg}", "昵称设置", event.user_id, event.group_id)
    else:
        await FriendUser.set_user_nickname(event.user_id, msg)
        await nickname.send(
            random.choice(
                [
                    f"好啦好啦，我知道啦，{msg}，以后就这么叫你吧",
                    f"嗯嗯，{NICKNAME}记住你的昵称了哦，{msg}",
                    f"好突然，突然要叫你昵称什么的...{msg}..",
                    f"{NICKNAME}会好好记住{msg}的，放心吧",
                    f"好..好.，那窝以后就叫你{msg}了.",
                ]
            )
        )
        logger.info(f"设置私聊昵称成功: {msg}", "昵称设置", event.user_id)


@my_nickname.handle()
async def _(event: MessageEvent):
    nickname_ = None
    card = None
    if isinstance(event, GroupMessageEvent):
        nickname_ = await GroupInfoUser.get_user_nickname(event.user_id, event.group_id)
        card = event.sender.card or event.sender.nickname
    else:
        nickname_ = await FriendUser.get_user_nickname(event.user_id)
        card = event.sender.nickname
    if nickname_:
        await my_nickname.send(
            random.choice(
                [
                    f"我肯定记得你啊，你是{nickname_}啊",
                    f"我不会忘记你的，你也不要忘记我！{nickname_}",
                    f"哼哼，{NICKNAME}记忆力可是很好的，{nickname_}",
                    f"嗯？你是失忆了嘛...{nickname_}..",
                    f"不要小看{NICKNAME}的记忆力啊！笨蛋{nickname_}！QAQ",
                    f"哎？{nickname_}..怎么了吗..突然这样问..",
                ]
            )
        )
    else:
        await my_nickname.send(
            random.choice(
                ["没..没有昵称嘛，{}", "啊，你是{}啊，我想叫你的昵称！", "是{}啊，有什么事吗？", "你是{}？"]
            ).format(card)
        )


@cancel_nickname.handle()
async def _(event: MessageEvent):
    nickname_ = None
    if isinstance(event, GroupMessageEvent):
        nickname_ = await GroupInfoUser.get_user_nickname(event.user_id, event.group_id)
    else:
        nickname_ = await FriendUser.get_user_nickname(event.user_id)
    if nickname_:
        await cancel_nickname.send(
            random.choice(
                [
                    f"呜..{NICKNAME}睡一觉就会忘记的..和梦一样..{nickname_}",
                    f"窝知道了..{nickname_}..",
                    f"是{NICKNAME}哪里做的不好嘛..好吧..晚安{nickname_}",
                    f"呃，{nickname_}，下次我绝对绝对绝对不会再忘记你！",
                    f"可..可恶！{nickname_}！太可恶了！呜",
                ]
            )
        )
        if isinstance(event, GroupMessageEvent):
            await GroupInfoUser.set_user_nickname(event.user_id, event.group_id, "")
        else:
            await FriendUser.set_user_nickname(event.user_id, "")
        await BanUser.ban(event.user_id, 9, 60)
    else:
        await cancel_nickname.send("你在做梦吗？你没有昵称啊", at_sender=True)
