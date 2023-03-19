import os
import random
from datetime import datetime
from pathlib import Path

import ujson as json
from nonebot import on_notice, on_request
from nonebot.adapters.onebot.v11 import (
    ActionFailed,
    Bot,
    GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent,
)

from configs.config import NICKNAME, Config
from configs.path_config import DATA_PATH, IMAGE_PATH
from models.group_info import GroupInfo
from models.group_member_info import GroupInfoUser
from models.level_user import LevelUser
from services.log import logger
from utils.depends import GetConfig
from utils.manager import group_manager, plugins2settings_manager, requests_manager
from utils.message_builder import image
from utils.utils import FreqLimiter

__zx_plugin_name__ = "群事件处理 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_task__ = {"group_welcome": "进群欢迎", "refund_group_remind": "退群提醒"}
Config.add_plugin_config(
    "invite_manager", "message", f"请不要未经同意就拉{NICKNAME}入群！告辞！", help_="强制拉群后进群回复的内容.."
)
Config.add_plugin_config(
    "invite_manager", "flag", True, help_="被强制拉群后是否直接退出", default_value=True, type=bool
)
Config.add_plugin_config(
    "invite_manager", "welcome_msg_cd", 5, help_="群欢迎消息cd", default_value=5, type=int
)
Config.add_plugin_config(
    "_task",
    "DEFAULT_GROUP_WELCOME",
    True,
    help_="被动 进群欢迎 进群默认开关状态",
    default_value=True,
    type=bool,
)
Config.add_plugin_config(
    "_task",
    "DEFAULT_REFUND_GROUP_REMIND",
    True,
    help_="被动 退群提醒 进群默认开关状态",
    default_value=True,
    type=bool,
)


_flmt = FreqLimiter(Config.get_config("invite_manager", "welcome_msg_cd") or 5)


# 群员增加处理
group_increase_handle = on_notice(priority=1, block=False)
# 群员减少处理
group_decrease_handle = on_notice(priority=1, block=False)
# （群管理）加群同意请求
add_group = on_request(priority=1, block=False)


@group_increase_handle.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    if event.user_id == int(bot.self_id):
        group = await GroupInfo.get_or_none(group_id=event.group_id)
        # 群聊不存在或被强制拉群，退出该群
        if (not group or group.group_flag == 0) and Config.get_config(
            "invite_manager", "flag"
        ):
            try:
                msg = Config.get_config("invite_manager", "message")
                if msg:
                    await bot.send_group_msg(group_id=event.group_id, message=msg)
                await bot.set_group_leave(group_id=event.group_id)
                await bot.send_private_msg(
                    user_id=int(list(bot.config.superusers)[0]),
                    message=f"触发强制入群保护，已成功退出群聊 {event.group_id}...",
                )
                logger.info(f"强制拉群或未有群信息，退出群聊成功", "入群检测", group_id=event.group_id)
                requests_manager.remove_request("group", event.group_id)
            except Exception as e:
                logger.info(f"强制拉群或未有群信息，退出群聊失败", "入群检测", group_id=event.group_id, e=e)
                await bot.send_private_msg(
                    user_id=int(list(bot.config.superusers)[0]),
                    message=f"触发强制入群保护，退出群聊 {event.group_id} 失败...",
                )
        # 默认群功能开关
        elif event.group_id not in group_manager.get_data().group_manager.keys():
            data = plugins2settings_manager.get_data()
            for plugin in data.keys():
                if not data[plugin].default_status:
                    group_manager.block_plugin(plugin, event.group_id)
            admin_default_auth = Config.get_config(
                "admin_bot_manage", "ADMIN_DEFAULT_AUTH"
            )
            # 即刻刷新权限
            for user_info in await bot.get_group_member_list(group_id=event.group_id):
                if (
                    user_info["role"]
                    in [
                        "owner",
                        "admin",
                    ]
                    and not await LevelUser.is_group_flag(
                        user_info["user_id"], event.group_id
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
                        user_info["user_id"],
                        user_info["group_id"],
                    )
                if str(user_info["user_id"]) in bot.config.superusers:
                    await LevelUser.set_level(
                        user_info["user_id"], user_info["group_id"], 9
                    )
                    logger.debug(
                        f"添加超级用户权限: 9",
                        "入群检测",
                        user_info["user_id"],
                        user_info["group_id"],
                    )
    else:
        join_time = datetime.now()
        user_info = await bot.get_group_member_info(
            group_id=event.group_id, user_id=event.user_id
        )
        await GroupInfoUser.update_or_create(
            user_qq=user_info["user_id"],
            group_id=user_info["group_id"],
            defaults={"user_name": user_info["nickname"], "user_join_time": join_time},
        )
        logger.info(f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新成功")

        # 群欢迎消息
        if _flmt.check(event.group_id):
            _flmt.start_cd(event.group_id)
            msg = ""
            img = ""
            at_flag = False
            custom_welcome_msg_json = (
                Path() / "data" / "custom_welcome_msg" / "custom_welcome_msg.json"
            )
            if custom_welcome_msg_json.exists():
                data = json.load(open(custom_welcome_msg_json, "r"))
                if data.get(str(event.group_id)):
                    msg = data[str(event.group_id)]
                    if "[at]" in msg:
                        msg = msg.replace("[at]", "")
                        at_flag = True
            if (DATA_PATH / "custom_welcome_msg" / f"{event.group_id}.jpg").exists():
                img = image(DATA_PATH / "custom_welcome_msg" / f"{event.group_id}.jpg")
            if msg or img:
                msg = msg.strip() + img
                msg = "\n" + msg if at_flag else msg
                await group_increase_handle.send(
                    "[[_task|group_welcome]]" + msg, at_sender=at_flag
                )
            else:
                await group_increase_handle.send(
                    "[[_task|group_welcome]]新人快跑啊！！本群现状↓（快使用自定义！）"
                    + image(
                        IMAGE_PATH
                        / "qxz"
                        / random.choice(os.listdir(IMAGE_PATH / "qxz"))
                    )
                )


@group_decrease_handle.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent):
    # 被踢出群
    if event.sub_type == "kick_me":
        group_id = event.group_id
        operator_id = event.operator_id
        if user := await GroupInfoUser.get_or_none(
            user_qq=event.operator_id, group_id=event.group_id
        ):
            operator_name = user.user_name
        else:
            operator_name = "None"
        group = await GroupInfo.filter(group_id=group_id).first()
        group_name = group.group_name if group else ""
        coffee = int(list(bot.config.superusers)[0])
        await bot.send_private_msg(
            user_id=coffee,
            message=f"****呜..一份踢出报告****\n"
            f"我被 {operator_name}({operator_id})\n"
            f"踢出了 {group_name}({group_id})\n"
            f"日期：{str(datetime.now()).split('.')[0]}",
        )
        return
    if event.user_id == int(bot.self_id):
        group_manager.delete_group(event.group_id)
        return
    if user := await GroupInfoUser.get_or_none(
        user_qq=event.user_id, group_id=event.group_id
    ):
        user_name = user.user_name
    else:
        user_name = f"{event.user_id}"
    await GroupInfoUser.filter(user_qq=event.user_id, group_id=event.group_id).delete()
    logger.info(
        f"名称: {user_name} 退出群聊",
        "group_decrease_handle",
        event.user_id,
        event.group_id,
    )
    rst = ""
    if event.sub_type == "leave":
        rst = f"{user_name}离开了我们..."
    if event.sub_type == "kick":
        operator = await bot.get_group_member_info(
            user_id=event.operator_id, group_id=event.group_id
        )
        operator_name = operator["card"] if operator["card"] else operator["nickname"]
        rst = f"{user_name} 被 {operator_name} 送走了."
    try:
        await group_decrease_handle.send(f"[[_task|refund_group_remind]]{rst}")
    except ActionFailed:
        return
