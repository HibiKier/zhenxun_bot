from typing import List
from nonebot.adapters.onebot.v11.message import MessageSegment
from services.log import logger
from configs.path_config import DATA_PATH
from utils.message_builder import image
from utils.utils import get_bot, get_matchers
from pathlib import Path
from models.group_member_info import GroupInfoUser
from datetime import datetime
from services.db_context import db
from models.level_user import LevelUser
from configs.config import Config
from utils.manager import group_manager, plugins2settings_manager, plugins_manager
from utils.image_utils import BuildImage
from utils.http_utils import AsyncHttpx
import asyncio
import time
import os

try:
    import ujson as json
except ModuleNotFoundError:
    import json


async def group_current_status(group_id: int) -> str:
    """
    获取当前所有通知的开关
    :param group_id: 群号
    """
    rst = "[被动技能 状态]\n"
    _data = group_manager.get_task_data()
    for task in _data.keys():
        rst += f'{_data[task]}: {"√" if await group_manager.check_group_task_status(group_id, task) else "×"}\n'
    return rst.strip()


custom_welcome_msg_json = (
    Path() / "data" / "custom_welcome_msg" / "custom_welcome_msg.json"
)


async def custom_group_welcome(
    msg: str, imgs: List[str], user_id: int, group_id: int
) -> str:
    """
    替换群欢迎消息
    :param msg: 欢迎消息文本
    :param imgs: 欢迎消息图片，只取第一张
    :param user_id: 用户id，用于log记录
    :param group_id: 群号
    """
    img_result = ""
    img = imgs[0] if imgs else ""
    result = ""
    if (DATA_PATH / f"custom_welcome_msg/{group_id}.jpg").exists():
        (DATA_PATH / f"custom_welcome_msg/{group_id}.jpg").unlink()
    if not custom_welcome_msg_json.exists():
        custom_welcome_msg_json.parent.mkdir(parents=True, exist_ok=True)
        data = {}
    else:
        try:
            data = json.load(open(custom_welcome_msg_json, "r"))
        except FileNotFoundError:
            data = {}
    try:
        if msg:
            data[str(group_id)] = str(msg)
            json.dump(
                data, open(custom_welcome_msg_json, "w"), indent=4, ensure_ascii=False
            )
            logger.info(f"USER {user_id} GROUP {group_id} 更换群欢迎消息 {msg}")
            result += msg
        if img:
            await AsyncHttpx.download_file(
                img, DATA_PATH / "custom_welcome_msg" / f"{group_id}.jpg"
            )
            img_result = image(DATA_PATH / "custom_welcome_msg" / f"{group_id}.jpg")
            logger.info(f"USER {user_id} GROUP {group_id} 更换群欢迎消息图片")
    except Exception as e:
        logger.error(f"GROUP {group_id} 替换群消息失败 e:{e}")
        return "替换群消息失败.."
    return f"替换群欢迎消息成功：\n{result}" + img_result


task_data = None


async def change_group_switch(cmd: str, group_id: int, is_super: bool = False):
    """
    修改群功能状态
    :param cmd: 功能名称
    :param group_id: 群号
    :param is_super: 是否位超级用户，超级用户用于私聊开关功能状态
    """
    global task_data
    if not task_data:
        task_data = group_manager.get_task_data()
    group_help_file = DATA_PATH / "group_help" / f"{group_id}.png"
    status = cmd[:2]
    cmd = cmd[2:]
    type_ = "plugin"
    modules = plugins2settings_manager.get_plugin_module(cmd, True)
    if cmd == "全部被动":
        for task in task_data:
            if status == "开启":
                if not await group_manager.check_group_task_status(group_id, task):
                    await group_manager.open_group_task(group_id, task)
            else:
                if await group_manager.check_group_task_status(group_id, task):
                    await group_manager.close_group_task(group_id, task)
        if group_help_file.exists():
            group_help_file.unlink()
        return f"已 {status} 全部被动技能！"
    if cmd == "全部功能":
        for f in plugins2settings_manager.get_data():
            if status == "开启":
                group_manager.unblock_plugin(f, group_id)
            else:
                group_manager.block_plugin(f, group_id)
        if group_help_file.exists():
            group_help_file.unlink()
        return f"已 {status} 全部功能！"
    if cmd.lower() in [task_data[x].lower() for x in task_data.keys()]:
        type_ = "task"
        modules = [x for x in task_data.keys() if task_data[x].lower() == cmd.lower()]
    for module in modules:
        if is_super:
            module = f"{module}:super"
        if status == "开启":
            if type_ == "task":
                if await group_manager.check_group_task_status(group_id, module):
                    return f"被动 {task_data[module]} 正处于开启状态！不要重复开启."
                await group_manager.open_group_task(group_id, module)
            else:
                if group_manager.get_plugin_status(module, group_id):
                    return f"功能 {cmd} 正处于开启状态！不要重复开启."
                group_manager.unblock_plugin(module, group_id)
        else:
            if type_ == "task":
                if not await group_manager.check_group_task_status(group_id, module):
                    return f"被动 {task_data[module]} 正处于关闭状态！不要重复关闭."
                await group_manager.close_group_task(group_id, module)
            else:
                if not group_manager.get_plugin_status(module, group_id):
                    return f"功能 {cmd} 正处于关闭状态！不要重复关闭."
                group_manager.block_plugin(module, group_id)
    if group_help_file.exists():
        group_help_file.unlink()
    if is_super:
        for file in os.listdir(DATA_PATH / "group_help"):
            file = DATA_PATH / "group_help" / file
            file.unlink()
    else:
        _help_image = DATA_PATH / "group_help" / f"{group_id}.png"
        if _help_image.exists():
            _help_image.unlink()
    return f"{status} {cmd} 功能！"


def set_plugin_status(cmd: str, block_type: str = "all"):
    """
    设置插件功能状态（超级用户使用）
    :param cmd: 功能名称
    :param block_type: 限制类型, 'all': 私聊+群里, 'private': 私聊, 'group': 群聊
    """
    status = cmd[:2]
    cmd = cmd[2:]
    module = plugins2settings_manager.get_plugin_module(cmd)
    if status == "开启":
        plugins_manager.unblock_plugin(module)
    else:
        plugins_manager.block_plugin(module, block_type=block_type)
    for file in os.listdir(DATA_PATH / "group_help"):
        file = DATA_PATH / "group_help" / file
        file.unlink()


async def get_plugin_status():
    """
    获取功能状态
    """
    return await asyncio.get_event_loop().run_in_executor(None, _get_plugin_status)


def _get_plugin_status() -> MessageSegment:
    """
    合成功能状态图片
    """
    rst = "\t功能\n"
    flag_str = "状态".rjust(4) + "\n"
    tmp_name = []
    for matcher in get_matchers():
        if matcher.plugin_name not in tmp_name:
            tmp_name.append(matcher.plugin_name)
            module = matcher.plugin_name
            flag = plugins_manager.get_plugin_block_type(module)
            flag = flag.upper() + " CLOSE" if flag else "OPEN"
            try:
                plugin_name = plugins_manager.get(module)["plugin_name"]
                if (
                    "[Hidden]" in plugin_name
                    or "[Admin]" in plugin_name
                    or "[Superuser]" in plugin_name
                ):
                    continue
                rst += f"{plugin_name}"
            except KeyError:
                rst += f"{module}"
            if plugins_manager.get(module)["error"]:
                rst += "[ERROR]"
            rst += "\n"
            flag_str += f"{flag}\n"
    height = len(rst.split("\n")) * 24
    a = BuildImage(250, height, font_size=20)
    a.text((10, 10), rst)
    b = BuildImage(200, height, font_size=20)
    b.text((10, 10), flag_str)
    A = BuildImage(500, height)
    A.paste(a)
    A.paste(b, (270, 0))
    return image(b64=A.pic2bs4())


async def update_member_info(group_id: int, remind_superuser: bool = False) -> bool:
    """
    更新群成员信息
    :param group_id: 群号
    :param remind_superuser: 失败信息提醒超级用户
    """
    bot = get_bot()
    _group_user_list = await bot.get_group_member_list(group_id=group_id)
    _error_member_list = []
    _exist_member_list = []
    # try:
    for user_info in _group_user_list:
        nickname = user_info["card"] or user_info["nickname"]
        async with db.transaction():
            # 更新权限
            if (
                user_info["role"]
                in [
                    "owner",
                    "admin",
                ]
                and not await LevelUser.is_group_flag(user_info["user_id"], group_id)
            ):
                await LevelUser.set_level(
                    user_info["user_id"],
                    user_info["group_id"],
                    Config.get_config("admin_bot_manage", "ADMIN_DEFAULT_AUTH"),
                )
            if str(user_info["user_id"]) in bot.config.superusers:
                await LevelUser.set_level(
                    user_info["user_id"], user_info["group_id"], 9
                )
            user = await GroupInfoUser.get_member_info(
                user_info["user_id"], user_info["group_id"]
            )
            if user:
                if user.user_name != nickname:
                    await user.update(user_name=nickname).apply()
                    logger.info(
                        f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新群昵称成功"
                    )
                _exist_member_list.append(int(user_info["user_id"]))
                continue
            join_time = datetime.strptime(
                time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(user_info["join_time"])
                ),
                "%Y-%m-%d %H:%M:%S",
            )
            if await GroupInfoUser.add_member_info(
                user_info["user_id"],
                user_info["group_id"],
                nickname,
                join_time,
            ):
                _exist_member_list.append(int(user_info["user_id"]))
                logger.info(f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新成功")
            else:
                _error_member_list.append(
                    f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新失败\n"
                )
    _del_member_list = list(
        set(_exist_member_list).difference(
            set(await GroupInfoUser.get_group_member_id_list(group_id))
        )
    )
    if _del_member_list:
        for del_user in _del_member_list:
            if await GroupInfoUser.delete_member_info(del_user, group_id):
                logger.info(f"退群用户{del_user} 所属{group_id} 已删除")
            else:
                logger.info(f"退群用户{del_user} 所属{group_id} 删除失败")
    if _error_member_list and remind_superuser:
        result = ""
        for error_user in _error_member_list:
            result += error_user
        await bot.send_private_msg(
            user_id=int(list(bot.config.superusers)[0]), message=result[:-1]
        )
    return True


def set_group_bot_status(group_id: int, status: bool) -> str:
    """
    设置群聊bot开关状态
    :param group_id: 群号
    :param status: 状态
    """
    if status:
        if group_manager.check_group_bot_status(group_id):
            return "我还醒着呢！"
        group_manager.turn_on_group_bot_status(group_id)
        return "呜..醒来了..."
    else:
        group_manager.shutdown_group_bot_status(group_id)
        # for x in group_manager.get_task_data():
        #     group_manager.close_group_task(group_id, x)
        return "那我先睡觉了..."

