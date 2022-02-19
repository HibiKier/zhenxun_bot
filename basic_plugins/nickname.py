from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, PrivateMessageEvent, Message
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.rule import to_me
from models.group_member_info import GroupInfoUser
from models.friend_user import FriendUser
from models.ban_user import BanUser
from services.log import logger
from configs.config import NICKNAME, Config
from nonebot.params import CommandArg
import random

__zx_plugin_name__ = "昵称系统"
__plugin_usage__ = f"""
usage：
    个人昵称系统，群聊 与 私聊 昵称相互独立
    指令：
        以后叫我 [昵称]
        {NICKNAME}我是谁
""".strip()
__plugin_des__ = "区区昵称，才不想叫呢！"
__plugin_cmd__ = ["以后叫我 [昵称]", f"{NICKNAME}我是谁"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_configs__ = {
    "BLACK_WORD": {
        "value": ["爸", "爹", "爷"],
        "help": "昵称所屏蔽的关键词，会被替换为 *",
        "default_value": None
    }
}

nickname = on_command(
    "nickname",
    aliases={"以后叫我", "以后请叫我", "称呼我", "以后请称呼我", "以后称呼我", "叫我", "请叫我"},
    rule=to_me(),
    priority=5,
    block=True,
)

my_nickname = on_command(
    "my_name", aliases={"我叫什么", "我是谁", "我的名字"}, rule=to_me(), priority=5, block=True
)


cancel_nickname = on_command("取消昵称", rule=to_me(), priority=5, block=True)


@nickname.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if not msg:
        await nickname.finish("叫你空白？叫你虚空？叫你无名？？", at_sender=True)
    if len(msg) > 10:
        await nickname.finish("昵称可不能超过10个字！", at_sender=True)
    if msg in bot.config.superusers:
        await nickname.finish("笨蛋！休想占用我的名字！#", at_sender=True)
    _tmp = ""
    black_word = Config.get_config("nickname", "BLACK_WORD")
    for x in msg:
        _tmp += "*" if x in black_word else x
    msg = _tmp
    if isinstance(event, GroupMessageEvent):
        if await GroupInfoUser.set_group_member_nickname(
            event.user_id, event.group_id, msg
        ):
            if len(msg) < 5:
                if random.random() < 0.3:
                    msg = "~".join(msg)
            await nickname.send(
                random.choice(
                    [
                        f"好啦好啦，我知道啦，{msg}，以后就这么叫你吧",
                        f"嗯嗯，{NICKNAME}记住你的昵称了哦，{msg}",
                        f"好突然，突然要叫你昵称什么的...{msg}..",
                        f"{NICKNAME}会好好记住的{msg}的，放心吧",
                        f"好..好.，那窝以后就叫你{msg}了.",
                    ]
                )
            )
            logger.info(f"USER {event.user_id} GROUP {event.group_id} 设置群昵称 {msg}")
        else:
            await nickname.send("设置昵称失败，请更新群组成员信息！", at_sender=True)
            logger.warning(f"USER {event.user_id} GROUP {event.group_id} 设置群昵称 {msg} 失败")
    else:
        if await FriendUser.set_friend_nickname(event.user_id, msg):
            await nickname.send(
                random.choice(
                    [
                        f"好啦好啦，我知道啦，{msg}，以后就这么叫你吧",
                        f"嗯嗯，{NICKNAME}记住你的昵称了哦，{msg}",
                        f"好突然，突然要叫你昵称什么的...{msg}..",
                        f"{NICKNAME}会好好记住的{msg}的，放心吧",
                        f"好..好.，那窝以后就叫你{msg}了.",
                    ]
                )
            )
            logger.info(f"USER {event.user_id} 设置昵称 {msg}")
        else:
            await nickname.send("设置昵称失败了，明天再来试一试！或联系管理员更新好友！", at_sender=True)
            logger.warning(f"USER {event.user_id} 设置昵称 {msg} 失败")


@my_nickname.handle()
async def _(event: GroupMessageEvent):
    try:
        nickname_ = await GroupInfoUser.get_group_member_nickname(
            event.user_id, event.group_id
        )
    except AttributeError:
        nickname_ = ""
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
        nickname_ = event.sender.card or event.sender.nickname
        await my_nickname.send(
            random.choice(
                ["没..没有昵称嘛，{}", "啊，你是{}啊，我想叫你的昵称！", "是{}啊，有什么事吗？", "你是{}？"]
            ).format(nickname_)
        )


@my_nickname.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    nickname_ = await FriendUser.get_friend_nickname(event.user_id)
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
        nickname_ = (await bot.get_stranger_info(user_id=event.user_id))["nickname"]
        await my_nickname.send(
            random.choice(
                ["没..没有昵称嘛，{}", "啊，你是{}啊，我想叫你的昵称！", "是{}啊，有什么事吗？", "你是{}？"]
            ).format(nickname_)
        )


@cancel_nickname.handle()
async def _(event: GroupMessageEvent):
    nickname_ = await GroupInfoUser.get_group_member_nickname(
        event.user_id, event.group_id
    )
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
        await GroupInfoUser.set_group_member_nickname(event.user_id, event.group_id, "")
        await BanUser.ban(event.user_id, 9, 60)
    else:
        await cancel_nickname.send("你在做梦吗？你没有昵称啊", at_sender=True)


@cancel_nickname.handle()
async def _(event: PrivateMessageEvent):
    nickname_ = await FriendUser.get_friend_nickname(event.user_id)
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
        await FriendUser.get_user_name(event.user_id)
        await BanUser.ban(event.user_id, 9, 60)
    else:
        await cancel_nickname.send("你在做梦吗？你没有昵称啊", at_sender=True)
