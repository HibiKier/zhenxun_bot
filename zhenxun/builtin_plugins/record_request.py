import time
from datetime import datetime

from nonebot.plugin import PluginMetadata
from nonebot import on_message, on_request
from nonebot_plugin_session import EventSession
from nonebot_plugin_apscheduler import scheduler
from nonebot.adapters.onebot.v11 import Bot as v11Bot
from nonebot.adapters.onebot.v12 import Bot as v12Bot
from nonebot.adapters.onebot.v11 import (
    ActionFailed,
    GroupRequestEvent,
    FriendRequestEvent,
)

from zhenxun.services.log import logger
from zhenxun.models.fg_request import FgRequest
from zhenxun.utils.platform import PlatformUtils
from zhenxun.models.friend_user import FriendUser
from zhenxun.configs.config import Config, BotConfig
from zhenxun.models.group_console import GroupConsole
from zhenxun.configs.utils import RegisterConfig, PluginExtraData
from zhenxun.utils.enum import PluginType, RequestType, RequestHandleType

base_config = Config.get("invite_manager")

__plugin_meta__ = PluginMetadata(
    name="记录请求",
    description="记录 好友/群组 请求",
    usage="",
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.HIDDEN,
        configs=[
            RegisterConfig(
                module="invite_manager",
                key="AUTO_ADD_FRIEND",
                value=False,
                help="是否自动同意好友添加",
                type=bool,
                default_value=False,
            )
        ],
    ).dict(),
)


class Timer:
    data: dict[str, float] = {}  # noqa: RUF012

    @classmethod
    def check(cls, uid: int | str):
        return True if uid not in cls.data else time.time() - cls.data[uid] > 5 * 60

    @classmethod
    def clear(cls):
        now = time.time()
        cls.data = {k: v for k, v in cls.data.items() if v - now < 5 * 60}


# TODO: 其他平台请求

friend_req = on_request(priority=5, block=True)
group_req = on_request(priority=5, block=True)
_t = on_message(priority=999, block=False, rule=lambda: False)


@friend_req.handle()
async def _(bot: v12Bot | v11Bot, event: FriendRequestEvent, session: EventSession):
    if event.user_id and Timer.check(event.user_id):
        logger.debug("收录好友请求...", "好友请求", target=event.user_id)
        user = await bot.get_stranger_info(user_id=event.user_id)
        nickname = user["nickname"]
        # sex = user["sex"]
        # age = str(user["age"])
        comment = event.comment
        if base_config.get("AUTO_ADD_FRIEND"):
            logger.debug(
                "已开启好友请求自动同意，成功通过该请求",
                "好友请求",
                target=event.user_id,
            )
            await bot.set_friend_add_request(flag=event.flag, approve=True)
            await FriendUser.create(
                user_id=str(user["user_id"]), user_name=user["nickname"]
            )
        else:
            # 旧请求全部设置为过期
            await FgRequest.filter(
                request_type=RequestType.FRIEND,
                user_id=str(event.user_id),
                handle_type__isnull=True,
            ).update(handle_type=RequestHandleType.EXPIRE)
            f = await FgRequest.create(
                request_type=RequestType.FRIEND,
                platform=session.platform,
                bot_id=bot.self_id,
                flag=event.flag,
                user_id=event.user_id,
                nickname=nickname,
                comment=comment,
            )
            await PlatformUtils.send_superuser(
                bot,
                f"*****一份好友申请*****\n"
                f"ID: {f.id}"
                f"昵称：{nickname}({event.user_id})\n"
                f"自动同意：{'√' if base_config.get('AUTO_ADD_FRIEND') else '×'}\n"
                f"日期：{str(datetime.now()).split('.')[0]}\n"
                f"备注：{event.comment}",
            )
    else:
        logger.debug("好友请求五分钟内重复, 已忽略", "好友请求", target=event.user_id)


@group_req.handle()
async def _(bot: v12Bot | v11Bot, event: GroupRequestEvent, session: EventSession):
    if event.sub_type != "invite":
        return
    if str(event.user_id) in bot.config.superusers:
        try:
            logger.debug(
                "超级用户自动同意加入群聊",
                "群聊请求",
                session=event.user_id,
                target=event.group_id,
            )
            group, _ = await GroupConsole.update_or_create(
                group_id=str(event.group_id),
                defaults={
                    "group_name": "",
                    "max_member_count": 0,
                    "member_count": 0,
                    "group_flag": 1,
                },
            )
            await bot.set_group_add_request(
                flag=event.flag, sub_type="invite", approve=True
            )
            if isinstance(bot, v11Bot):
                group_info = await bot.get_group_info(group_id=event.group_id)
                max_member_count = group_info["max_member_count"]
                member_count = group_info["member_count"]
            else:
                group_info = await bot.get_group_info(group_id=str(event.group_id))
                max_member_count = 0
                member_count = 0
            group.max_member_count = max_member_count
            group.member_count = member_count
            group.group_name = group_info["group_name"]
            await group.save(
                update_fields=["group_name", "max_member_count", "member_count"]
            )
        except ActionFailed as e:
            logger.error(
                "超级用户自动同意加入群聊发生错误",
                "群聊请求",
                session=event.user_id,
                target=event.group_id,
                e=e,
            )
    elif Timer.check(f"{event.user_id}:{event.group_id}"):
        logger.debug(
            f"收录 用户[{event.user_id}] 群聊[{event.group_id}] 群聊请求",
            "群聊请求",
            target=event.group_id,
        )
        nickname = await FriendUser.get_user_name(str(event.user_id))
        await bot.send_private_msg(
            user_id=event.user_id,
            message=f"想要邀请我偷偷入群嘛~已经提醒{BotConfig.self_nickname}的管理员大人了\n"
            "请确保已经群主或群管理沟通过！\n"
            "等待管理员处理吧！",
        )
        # 旧请求全部设置为过期
        await FgRequest.filter(
            request_type=RequestType.GROUP,
            user_id=str(event.user_id),
            group_id=str(event.group_id),
            handle_type__isnull=True,
        ).update(handle_type=RequestHandleType.EXPIRE)
        f = await FgRequest.create(
            request_type=RequestType.GROUP,
            platform=session.platform,
            bot_id=bot.self_id,
            flag=event.flag,
            user_id=str(event.user_id),
            nickname=nickname,
            group_id=str(event.group_id),
        )
        await PlatformUtils.send_superuser(
            bot,
            f"*****一份入群申请*****\n"
            f"ID：{f.id}\n"
            f"申请人：{nickname}({event.user_id})\n群聊："
            f"{event.group_id}\n邀请日期：{datetime.now().replace(microsecond=0)}",
        )
    else:
        logger.debug(
            "群聊请求五分钟内重复, 已忽略",
            "群聊请求",
            target=f"{event.user_id}:{event.group_id}",
        )


@scheduler.scheduled_job(
    "interval",
    minutes=5,
)
async def _():
    Timer.clear()


async def _():
    Timer.clear()
