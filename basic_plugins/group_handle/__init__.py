from nonebot import on_notice, on_request
from configs.path_config import IMAGE_PATH, DATA_PATH
from utils.message_builder import image
from models.group_member_info import GroupInfoUser
from datetime import datetime
from services.log import logger
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupIncreaseNoticeEvent,
    GroupDecreaseNoticeEvent,
)
from nonebot.adapters.onebot.v11.exception import ActionFailed
from utils.manager import group_manager, plugins2settings_manager, requests_manager
from configs.config import NICKNAME
from models.group_info import GroupInfo
from utils.utils import FreqLimiter
from configs.config import Config
from pathlib import Path
import random
import os

try:
    import ujson as json
except ModuleNotFoundError:
    import json


__zx_plugin_name__ = "群事件处理 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_task__ = {"group_welcome": "进群欢迎", "refund_group_remind": "退群提醒"}
Config.add_plugin_config(
    "invite_manager", "message", f"请不要未经同意就拉{NICKNAME}入群！告辞！", help_="强制拉群后进群回复的内容.."
)
Config.add_plugin_config(
    "invite_manager", "flag", True, help_="被强制拉群后是否直接退出", default_value=True
)
Config.add_plugin_config(
    "invite_manager", "welcome_msg_cd", 5, help_="群欢迎消息cd", default_value=5
)
Config.add_plugin_config(
    "_task",
    "DEFAULT_GROUP_WELCOME",
    True,
    help_="被动 进群欢迎 进群默认开关状态",
    default_value=True,
)
Config.add_plugin_config(
    "_task",
    "DEFAULT_REFUND_GROUP_REMIND",
    True,
    help_="被动 退群提醒 进群默认开关状态",
    default_value=True,
)


_flmt = FreqLimiter(Config.get_config("invite_manager", "welcome_msg_cd"))


# 群员增加处理
group_increase_handle = on_notice(priority=1, block=False)
# 群员减少处理
group_decrease_handle = on_notice(priority=1, block=False)
# （群管理）加群同意请求
add_group = on_request(priority=1, block=False)


@group_increase_handle.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    if event.user_id == int(bot.self_id):
        group = await GroupInfo.get_group_info(event.group_id)
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
                    message=f"触发强制入群保护，已成功退出群聊 {event.group_id}..",
                )
                logger.info(f"强制拉群或未有群信息，退出群聊 {group} 成功")
                requests_manager.remove_request("group", event.group_id)
            except Exception as e:
                logger.info(f"强制拉群或未有群信息，退出群聊 {group} 失败 e:{e}")
                await bot.send_private_msg(
                    user_id=int(list(bot.config.superusers)[0]),
                    message=f"触发强制入群保护，退出群聊 {event.group_id} 失败..",
                )
        # 默认群功能开关
        elif event.group_id not in group_manager["group_manager"].keys():
            data = plugins2settings_manager.get_data()
            for plugin in data.keys():
                if not data[plugin]["default_status"]:
                    group_manager.block_plugin(plugin, event.group_id)
    else:
        join_time = datetime.now()
        user_info = await bot.get_group_member_info(
            group_id=event.group_id, user_id=event.user_id
        )
        if await GroupInfoUser.add_member_info(
            user_info["user_id"],
            user_info["group_id"],
            user_info["nickname"],
            join_time,
        ):
            logger.info(f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新成功")
        else:
            logger.info(f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新失败")

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
                    if msg.find("[at]") != -1:
                        msg = msg.replace("[at]", "")
                        at_flag = True
            if (DATA_PATH / "custom_welcome_msg" / f"{event.group_id}.jpg").exists():
                img = image(
                    DATA_PATH / "custom_welcome_msg" / f"{event.group_id}.jpg"
                )
            if msg or img:
                msg = msg.strip() + img
                msg = "\n" + msg if at_flag else msg
                await group_increase_handle.send(
                    "[[_task|group_welcome]]" + msg, at_sender=at_flag
                )
            else:
                await group_increase_handle.send(
                    "[[_task|group_welcome]]新人快跑啊！！本群现状↓（快使用自定义！）"
                    + image(random.choice(os.listdir(IMAGE_PATH / "qxz")), "qxz")
                )


@group_decrease_handle.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent):
    # 被踢出群
    if event.sub_type == "kick_me":
        group_id = event.group_id
        operator_id = event.operator_id
        try:
            operator_name = (
                await GroupInfoUser.get_member_info(event.operator_id, event.group_id)
            ).user_name
        except AttributeError:
            operator_name = "None"
        group = await GroupInfo.get_group_info(group_id)
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
    try:
        user_name = (
            await GroupInfoUser.get_member_info(event.user_id, event.group_id)
        ).user_name
    except AttributeError:
        user_name = str(event.user_id)
    if await GroupInfoUser.delete_member_info(event.user_id, event.group_id):
        logger.info(f"用户{user_name}, qq={event.user_id} 所属{event.group_id} 删除成功")
    else:
        logger.info(f"用户{user_name}, qq={event.user_id} 所属{event.group_id} 删除失败")
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
