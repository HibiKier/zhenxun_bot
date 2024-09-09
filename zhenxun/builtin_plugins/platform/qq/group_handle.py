import os
import re
import random
from datetime import datetime

import ujson as json
from nonebot.adapters import Bot
from nonebot_plugin_alconna import At
from nonebot import on_notice, on_request
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import (
    GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent,
)
from nonebot.adapters.onebot.v12 import (
    GroupMemberDecreaseEvent,
    GroupMemberIncreaseEvent,
)

from zhenxun.services.log import logger
from zhenxun.utils.utils import FreqLimiter
from zhenxun.utils.message import MessageUtils
from zhenxun.models.fg_request import FgRequest
from zhenxun.models.level_user import LevelUser
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.utils.common_utils import CommonUtils
from zhenxun.configs.config import Config, BotConfig
from zhenxun.models.group_console import GroupConsole
from zhenxun.models.group_member_info import GroupInfoUser
from zhenxun.utils.enum import PluginType, RequestHandleType
from zhenxun.configs.path_config import DATA_PATH, IMAGE_PATH
from zhenxun.configs.utils import Task, RegisterConfig, PluginExtraData

__plugin_meta__ = PluginMetadata(
    name="QQ群事件处理",
    description="群事件处理",
    usage="",
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.HIDDEN,
        configs=[
            RegisterConfig(
                module="invite_manager",
                key="message",
                value=f"请不要未经同意就拉{BotConfig.self_nickname}入群！告辞！",
                help="强制拉群后进群回复的内容",
            ),
            RegisterConfig(
                module="invite_manager",
                key="flag",
                value=True,
                help="强制拉群后进群退出并回复内容",
                default_value=True,
                type=bool,
            ),
            RegisterConfig(
                module="invite_manager",
                key="welcome_msg_cd",
                value=5,
                help="群欢迎消息cd",
                default_value=5,
                type=int,
            ),
            RegisterConfig(
                module="_task",
                key="DEFAULT_GROUP_WELCOME",
                value=True,
                help="被动 进群欢迎 进群默认开关状态",
                default_value=True,
                type=bool,
            ),
            RegisterConfig(
                module="_task",
                key="DEFAULT_REFUND_GROUP_REMIND",
                value=True,
                help="被动 退群提醒 进群默认开关状态",
                default_value=True,
                type=bool,
            ),
        ],
        tasks=[
            Task(module="group_welcome", name="进群欢迎"),
            Task(module="refund_group_remind", name="退群提醒"),
        ],
    ).dict(),
)


base_config = Config.get("invite_manager")


limit_cd = base_config.get("welcome_msg_cd")

_flmt = FreqLimiter(limit_cd)


group_increase_handle = on_notice(priority=1, block=False)
"""群员增加处理"""
group_decrease_handle = on_notice(priority=1, block=False)
"""群员减少处理"""
add_group = on_request(priority=1, block=False)
"""加群同意请求"""


@group_increase_handle.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent | GroupMemberIncreaseEvent):
    superusers = BotConfig.get_superuser("qq")
    user_id = str(event.user_id)
    group_id = str(event.group_id)
    if user_id == bot.self_id:
        """新成员为bot本身"""
        group = await GroupConsole.get_or_none(
            group_id=group_id, channel_id__isnull=True
        )
        if not group or group.group_flag == 0:
            """群聊不存在或被强制拉群"""
            if base_config.get("flag"):
                """退出群组"""
                try:
                    if result_msg := base_config.get("message"):
                        await bot.send_group_msg(
                            group_id=event.group_id, message=result_msg
                        )
                    await bot.set_group_leave(group_id=event.group_id)
                    if superusers:
                        await bot.send_private_msg(
                            user_id=int(superusers[0]),
                            message=f"触发强制入群保护，已成功退出群聊 {group_id}...",
                        )
                    logger.info(
                        "强制拉群或未有群信息，退出群聊成功",
                        "入群检测",
                        group_id=event.group_id,
                    )
                    if req := await FgRequest.get_or_none(
                        group_id=group_id, handle_type__isnull=True
                    ):
                        req.handle_type = RequestHandleType.IGNORE
                        await req.save(update_fields=["handle_type"])
                except Exception as e:
                    logger.error(
                        "强制拉群或未有群信息，退出群聊失败",
                        "入群检测",
                        group_id=event.group_id,
                        e=e,
                    )
                    if superusers:
                        await bot.send_private_msg(
                            user_id=int(superusers[0]),
                            message="触发强制入群保护，"
                            f"退出群聊 {event.group_id} 失败...",
                        )
                await GroupConsole.filter(group_id=group_id).delete()
            else:
                """允许群组并设置群认证，默认群功能开关"""
                if group:
                    await GroupConsole.filter(
                        group_id=group_id, channel_id__isnull=True
                    ).update(group_flag=1)
                else:
                    block_plugin = ""
                    if plugin_list := await PluginInfo.filter(
                        default_status=False
                    ).all():
                        for plugin in plugin_list:
                            block_plugin += f"{plugin.module},"
                    group_info = await bot.get_group_info(group_id=event.group_id)
                    await GroupConsole.create(
                        group_id=group_info["group_id"],
                        group_name=group_info["group_name"],
                        max_member_count=group_info["max_member_count"],
                        member_count=group_info["member_count"],
                        group_flag=1,
                        block_plugin=block_plugin,
                        platform="qq",
                    )
                """刷新群管理员权限"""
                admin_default_auth = Config.get_config(
                    "admin_bot_manage", "ADMIN_DEFAULT_AUTH"
                )
                # 即刻刷新权限
                for user_info in await bot.get_group_member_list(
                    group_id=event.group_id
                ):
                    """即刻刷新权限"""
                    if (
                        user_info["role"]
                        in [
                            "owner",
                            "admin",
                        ]
                        and not await LevelUser.is_group_flag(
                            user_info["user_id"], group_id
                        )
                        and admin_default_auth is not None
                    ):
                        await LevelUser.set_level(
                            user_info["user_id"],
                            user_info["group_id"],
                            admin_default_auth,
                        )
                        logger.debug(
                            f"添加默认群管理员权限: {admin_default_auth}",
                            "入群检测",
                            session=user_info["user_id"],
                            group_id=user_info["group_id"],
                        )
                    if str(user_info["user_id"]) in bot.config.superusers:
                        await LevelUser.set_level(
                            user_info["user_id"], user_info["group_id"], 9
                        )
                        logger.debug(
                            "添加超级用户权限: 9",
                            "入群检测",
                            session=user_info["user_id"],
                            group_id=user_info["group_id"],
                        )
    else:
        join_time = datetime.now()
        user_info = await bot.get_group_member_info(
            group_id=event.group_id, user_id=event.user_id
        )
        await GroupInfoUser.update_or_create(
            user_id=str(user_info["user_id"]),
            group_id=str(user_info["group_id"]),
            defaults={"user_name": user_info["nickname"], "user_join_time": join_time},
        )
        logger.info(f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新成功")

        if _flmt.check(group_id):
            """群欢迎消息"""
            _flmt.start_cd(group_id)
            path = DATA_PATH / "welcome_message" / "qq" / f"{group_id}"
            file = path / "text.json"
            msg_list = []
            if file.exists():
                data = json.load((path / "text.json").open(encoding="utf-8"))
                message = data["message"]
                msg_split = re.split(r"\[image:\d+\]", message)
                if data["at"]:
                    msg_list.append(At(flag="user", target=user_id))
                for i, text in enumerate(msg_split):
                    msg_list.append(text)
                    img_file = path / f"{i}.png"
                    if img_file.exists():
                        msg_list.append(img_file)
            if not await CommonUtils.task_is_block("group_welcome", group_id):
                logger.info("发送群欢迎消息...", "入群检测", group_id=group_id)
                if msg_list:
                    await MessageUtils.build_message(msg_list).send()
                else:
                    image = (
                        IMAGE_PATH
                        / "qxz"
                        / random.choice(os.listdir(IMAGE_PATH / "qxz"))
                    )
                    await MessageUtils.build_message(
                        [
                            "新人快跑啊！！本群现状↓（快使用自定义！）",
                            image,
                        ]
                    ).send()


@group_decrease_handle.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent | GroupMemberDecreaseEvent):
    if event.sub_type == "kick_me":
        """踢出Bot"""
        group_id = event.group_id
        operator_id = event.operator_id
        if user := await GroupInfoUser.get_or_none(
            user_id=str(event.operator_id), group_id=str(event.group_id)
        ):
            operator_name = user.user_name
        else:
            operator_name = "None"
        group = await GroupConsole.filter(group_id=str(group_id)).first()
        group_name = group.group_name if group else ""
        if superusers := BotConfig.get_superuser("qq"):
            coffee = int(superusers[0])
            await bot.send_private_msg(
                user_id=coffee,
                message=f"****呜..一份踢出报告****\n"
                f"我被 {operator_name}({operator_id})\n"
                f"踢出了 {group_name}({group_id})\n"
                f"日期：{str(datetime.now()).split('.')[0]}",
            )
            if group:
                await group.delete()
            return
    if str(event.user_id) == bot.self_id:
        """踢出Bot"""
        await GroupConsole.filter(group_id=str(event.group_id)).delete()
        return
    if user := await GroupInfoUser.get_or_none(
        user_id=str(event.user_id), group_id=str(event.group_id)
    ):
        user_name = user.user_name
    else:
        user_name = f"{event.user_id}"
    await GroupInfoUser.filter(
        user_id=str(event.user_id), group_id=str(event.group_id)
    ).delete()
    logger.info(
        f"名称: {user_name} 退出群聊",
        "group_decrease_handle",
        session=event.user_id,
        group_id=event.group_id,
    )
    result = ""
    if event.sub_type == "leave":
        result = f"{user_name}离开了我们..."
    if event.sub_type == "kick":
        operator = await bot.get_group_member_info(
            user_id=event.operator_id, group_id=event.group_id
        )
        operator_name = operator["card"] or operator["nickname"]
        result = f"{user_name} 被 {operator_name} 送走了."
    if not await CommonUtils.task_is_block("refund_group_remind", str(event.group_id)):
        await group_decrease_handle.send(f"{result}")
