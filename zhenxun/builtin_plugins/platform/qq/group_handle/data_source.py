import os
import re
import random
from pathlib import Path
from datetime import datetime

import ujson as json
from nonebot.adapters import Bot
from nonebot_plugin_alconna import At
from nonebot_plugin_uninfo import Uninfo

from zhenxun.services.log import logger
from zhenxun.configs.config import Config
from zhenxun.utils.utils import FreqLimiter
from zhenxun.utils.message import MessageUtils
from zhenxun.models.fg_request import FgRequest
from zhenxun.models.level_user import LevelUser
from zhenxun.utils.enum import RequestHandleType
from zhenxun.utils.platform import PlatformUtils
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.utils.common_utils import CommonUtils
from zhenxun.models.group_console import GroupConsole
from zhenxun.models.group_member_info import GroupInfoUser
from zhenxun.configs.path_config import DATA_PATH, IMAGE_PATH

from ..exception import ForceAddGroupError

base_config = Config.get("invite_manager")

limit_cd = base_config.get("welcome_msg_cd")

WELCOME_PATH = DATA_PATH / "welcome_message" / "qq"

DEFAULT_IMAGE_PATH = IMAGE_PATH / "qxz"


class GroupManager:
    _flmt = FreqLimiter(limit_cd)

    @classmethod
    async def __handle_add_group(
        cls, bot: Bot, group_id: str, group: GroupConsole | None
    ):
        """允许群组并设置群认证，默认群功能开关

        参数:
            bot: Bot
            group_id: 群组id
            group: GroupConsole
        """
        if group:
            await GroupConsole.filter(
                group_id=group_id, channel_id__isnull=True
            ).update(group_flag=1)
        else:
            block_plugin = ""
            if plugin_list := await PluginInfo.filter(default_status=False).all():
                for plugin in plugin_list:
                    block_plugin += f"<{plugin.module},"
            group_info = await bot.get_group_info(group_id=group_id)
            await GroupConsole.create(
                group_id=group_info["group_id"],
                group_name=group_info["group_name"],
                max_member_count=group_info["max_member_count"],
                member_count=group_info["member_count"],
                group_flag=1,
                block_plugin=block_plugin,
                platform="qq",
            )

    @classmethod
    async def __refresh_level(cls, bot: Bot, group_id: str):
        """刷新权限

        参数:
            bot: Bot
            group_id: 群组id
        """
        admin_default_auth = Config.get_config("admin_bot_manage", "ADMIN_DEFAULT_AUTH")
        member_list = await bot.get_group_member_list(group_id=group_id)
        member_id_list = [str(user_info["user_id"]) for user_info in member_list]
        flag2u = await LevelUser.filter(
            user_id__in=member_id_list, group_id=group_id, group_flag=1
        ).values_list("user_id", flat=True)
        # 即刻刷新权限
        for user_info in member_list:
            user_id = str(user_info["user_id"])
            role = user_info["role"]
            if user_id in bot.config.superusers:
                await LevelUser.set_level(user_id, group_id, 9)
                logger.debug(
                    "添加超级用户权限: 9",
                    "入群检测",
                    session=user_id,
                    group_id=user_info["group_id"],
                )
            elif (
                admin_default_auth is not None
                and role in ["owner", "admin"]
                and user_id not in flag2u
            ):
                await LevelUser.set_level(
                    user_id,
                    group_id,
                    admin_default_auth if role == "admin" else admin_default_auth + 1,
                )
                logger.debug(
                    f"添加默认群管理员权限: {admin_default_auth}",
                    "入群检测",
                    session=user_id,
                    group_id=user_info["group_id"],
                )

    @classmethod
    async def add_bot(
        cls, bot: Bot, operator_id: str, group_id: str, group: GroupConsole | None
    ):
        """拉入bot

        参数:
            bot: Bot
            operator_id: 操作者id
            group_id: 群组id
            group: GroupConsole
        """
        if base_config.get("flag") and operator_id not in bot.config.superusers:
            """退出群组"""
            try:
                if result_msg := base_config.get("message"):
                    await bot.send_group_msg(group_id=int(group_id), message=result_msg)
                await bot.set_group_leave(group_id=int(group_id))
                logger.info(
                    "强制拉群或未有群信息，退出群聊成功", "入群检测", group_id=group_id
                )
                await FgRequest.filter(
                    group_id=group_id, handle_type__isnull=True
                ).update(handle_type=RequestHandleType.IGNORE)
            except Exception as e:
                logger.error(
                    "强制拉群或未有群信息，退出群聊失败",
                    "入群检测",
                    group_id=group_id,
                    e=e,
                )
                raise ForceAddGroupError("强制拉群或未有群信息，退出群聊失败...") from e
            await GroupConsole.filter(group_id=group_id).delete()
            raise ForceAddGroupError(f"触发强制入群保护，已成功退出群聊 {group_id}...")
        else:
            await cls.__handle_add_group(bot, group_id, group)
            """刷新群管理员权限"""
            await cls.__refresh_level(bot, group_id)

    @classmethod
    def __build_welcome_message(cls, user_id: str, path: Path) -> list[At | Path | str]:
        """构造群欢迎消息

        参数:
            user_id: 用户id
            path: 群欢迎消息存储路径

        返回:
            list[At | Path | str]: 消息列表
        """
        file = path / "text.json"
        data = json.load(file.open(encoding="utf-8"))
        message = data["message"]
        msg_split = re.split(r"\[image:\d+\]", message)
        msg_list = []
        if data["at"]:
            msg_list.append(At(flag="user", target=user_id))
        for i, text in enumerate(msg_split):
            msg_list.append(text)
            img_file = path / f"{i}.png"
            if img_file.exists():
                msg_list.append(img_file)
        return msg_list

    @classmethod
    async def __send_welcome_message(cls, user_id: str, group_id: str):
        """发送群欢迎消息

        参数:
            user_id: 用户id
            group_id: 群组id
        """
        cls._flmt.start_cd(group_id)
        path = WELCOME_PATH / f"{group_id}"
        file = path / "text.json"
        if file.exists():
            msg_list = cls.__build_welcome_message(user_id, path)
            logger.info("发送群欢迎消息...", "入群检测", group_id=group_id)
            if msg_list:
                await MessageUtils.build_message(msg_list).send()  # type: ignore
            else:
                image = DEFAULT_IMAGE_PATH / random.choice(
                    os.listdir(DEFAULT_IMAGE_PATH)
                )
                await MessageUtils.build_message(
                    [
                        "新人快跑啊！！本群现状↓（快使用自定义！）",
                        image,
                    ]
                ).send()

    @classmethod
    async def add_user(cls, session: Uninfo, bot: Bot, user_id: str, group_id: str):
        """拉入用户

        参数:
            bot: Bot
            user_id: 用户id
            group_id: 群组id
        """
        join_time = datetime.now()
        user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
        await GroupInfoUser.update_or_create(
            user_id=str(user_info["user_id"]),
            group_id=str(user_info["group_id"]),
            defaults={"user_name": user_info["nickname"], "user_join_time": join_time},
        )
        logger.info(f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新成功")
        if not await CommonUtils.task_is_block(
            session, "group_welcome"
        ) and cls._flmt.check(group_id):
            await cls.__send_welcome_message(user_id, group_id)

    @classmethod
    async def kick_bot(cls, bot: Bot, group_id: str, operator_id: str):
        """踢出bot

        参数:
            bot: Bot
            group_id: 群组id
            operator_id: 操作员id
        """
        if user := await GroupInfoUser.get_or_none(
            user_id=operator_id, group_id=group_id
        ):
            operator_name = user.user_name
        else:
            operator_name = "None"
        group = await GroupConsole.get_group(group_id)
        group_name = group.group_name if group else ""
        if group:
            await group.delete()
        await PlatformUtils.send_superuser(
            bot,
            f"****呜..一份踢出报告****\n"
            f"我被 {operator_name}({operator_id})\n"
            f"踢出了 {group_name}({group_id})\n"
            f"日期：{str(datetime.now()).split('.')[0]}",
        )

    @classmethod
    async def run_user(
        cls,
        bot: Bot,
        user_id: str,
        group_id: str,
        operator_id: str,
        sub_type: str,
    ) -> str | None:
        """踢出用户或用户离开

        参数:
            bot: Bot
            user_id: 用户id
            group_id: 群组id
            operator_id: 操作员id
            sub_type: 类型

        返回:
            str | None: 返回消息
        """
        if user := await GroupInfoUser.get_or_none(user_id=user_id, group_id=group_id):
            user_name = user.user_name
        else:
            user_name = f"{user_id}"
        if user:
            await user.delete()
        logger.info(
            f"名称: {user_name} 退出群聊",
            "group_decrease_handle",
            session=user_id,
            group_id=group_id,
        )
        if sub_type == "kick":
            operator = await bot.get_group_member_info(
                user_id=int(operator_id), group_id=int(group_id)
            )
            operator_name = operator["card"] or operator["nickname"]
            return f"{user_name} 被 {operator_name} 送走了."
        elif sub_type == "leave":
            return f"{user_name}离开了我们..."
        return None
