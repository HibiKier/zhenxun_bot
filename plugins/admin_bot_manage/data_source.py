from models.group_remind import GroupRemind
from services.log import logger
from configs.path_config import DATA_PATH
from utils.message_builder import image
from utils.utils import get_local_proxy, get_bot
from pathlib import Path
from models.group_member_info import GroupInfoUser
from datetime import datetime
from services.db_context import db
from models.level_user import LevelUser
from configs.config import ADMIN_DEFAULT_AUTH
from utils.static_data import group_manager
from utils.image_utils import CreateImg
from configs.config import plugins2info_dict
import aiofiles
import aiohttp
import asyncio
import time
import os

try:
    import ujson as json
except ModuleNotFoundError:
    import json


command_dict = {
    "早晚安": "zwa",
    "进群欢迎": "hy",
    "每日开箱重置提醒": "kxcz",
    "b站转发解析": "blpar",
    "epic": "epic",
    "丢人爬": "pa",
    "原神黄历提醒": "almanac",
}
command_list = list(command_dict.values())
command_info_dt = {
    "早晚安": "将会在每晚11:59晚安，在6:01早安哦",
    "每日开箱重置提醒": "将会在每日00:01提示开箱重置！",
    "epic": "将会在每日中午12:01发送可白嫖的epic游戏",
    "原神黄历提醒": "将会在每日8:00发送当日的原神黄历",
}


async def remind_status(group: int, name: str, flag: bool) -> str:
    _name = ""
    if name in command_dict.values():
        _name = list(command_dict.keys())[list(command_dict.values()).index(name)]
    if flag:
        rst = "开启"
        if await GroupRemind.get_status(group, name):
            return f"该群已经{rst}过 {_name}，请勿重复开启！"
    else:
        rst = "关闭"
        if not await GroupRemind.get_status(group, name):
            return f"该群已经{rst}过 {_name}，请勿重复关闭！"
    if await GroupRemind.set_status(group, name, flag):
        info = command_info_dt[_name] if command_info_dt.get(_name) else ""
        if info:
            info = "\n" + info
        return f"成功{rst} {_name}！0v0 {info}"
    else:
        return f"{rst} {_name} 失败了..."


async def set_group_status(name: str, group_id: int):
    flag = None
    if name[:2] == "开启":
        flag = True
    elif name[:2] == "关闭":
        flag = False
    cmd = name[2:]
    if cmd in ["全部通知", "所有通知"]:
        for command in command_list:
            await remind_status(group_id, command, flag)
        return f"已{name[:2]}所有通知！"
    return await remind_status(group_id, command_dict[cmd], flag)


async def group_current_status(group_id: int):
    result = (
        f'（被动技能）\n早晚安通知：{"√" if await GroupRemind.get_status(group_id, "zwa") else "×"}\n'
        f'进群欢迎：{"√" if await GroupRemind.get_status(group_id, "hy") else "×"}\n'
        f'每日开箱重置通知：{"√" if await GroupRemind.get_status(group_id, "kxcz") else "×"}\n'
        f'b站转发解析：{"√" if await GroupRemind.get_status(group_id, "blpar") else "×"}\n'
        f'丢人爬：{"√" if await GroupRemind.get_status(group_id, "pa") else "×"}\n'
        f'epic免费游戏：{"√" if await GroupRemind.get_status(group_id, "epic") else "×"}\n'
        f'原神黄历提醒：{"√" if await GroupRemind.get_status(group_id, "almanac") else "×"}'
    )
    return result


custom_welcome_msg_json = (
    Path() / "data" / "custom_welcome_msg" / "custom_welcome_msg.json"
)


async def custom_group_welcome(msg, imgs, user_id, group_id):
    img_result = ""
    img = imgs[0] if imgs else ""
    result = ""
    if os.path.exists(DATA_PATH + f"custom_welcome_msg/{group_id}.jpg"):
        os.remove(DATA_PATH + f"custom_welcome_msg/{group_id}.jpg")
    # print(custom_welcome_msg_json)
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
            async with aiohttp.ClientSession() as session:
                async with session.get(img, proxy=get_local_proxy()) as response:
                    async with aiofiles.open(
                        DATA_PATH + f"custom_welcome_msg/{group_id}.jpg", "wb"
                    ) as f:
                        await f.write(await response.read())
            img_result = image(abspath=DATA_PATH + f"custom_welcome_msg/{group_id}.jpg")
            logger.info(f"USER {user_id} GROUP {group_id} 更换群欢迎消息图片")
    except Exception as e:
        logger.error(f"GROUP {group_id} 替换群消息失败 e:{e}")
        return "替换群消息失败.."
    return f"替换群欢迎消息成功：\n{result}" + img_result


def change_group_switch(cmd: str, group_id: int, is_super: bool = False):
    group_help_file = Path(DATA_PATH) / "group_help" / f"{group_id}.png"
    group_id = str(group_id)
    status = cmd[:2]
    cmd = cmd[2:]
    for plugin_cmd in plugins2info_dict.keys():
        if cmd in plugins2info_dict[plugin_cmd]["cmd"]:
            if is_super:
                plugin_cmd = f'{plugin_cmd}:super'
            if status == "开启":
                if group_manager.get_plugin_status(plugin_cmd, group_id):
                    return f"功能 {cmd} 正处于开启状态！不要重复开启."
                group_manager.unblock_plugin(plugin_cmd, group_id)
            else:
                if not group_manager.get_plugin_status(plugin_cmd, group_id):
                    return f"功能 {cmd} 正处于关闭状态！不要重复关闭."
                group_manager.block_plugin(plugin_cmd, group_id)
            if group_help_file.exists():
                group_help_file.unlink()
            return f"{status} {cmd} 功能！"
    return f"没有找到 {cmd} 功能..."


def set_plugin_status(cmd: str, block_type: str = "all"):
    status = cmd[:2]
    cmd = cmd[2:]
    for plugin_cmd in plugins2info_dict.keys():
        if cmd in plugins2info_dict[plugin_cmd]["cmd"]:
            if status == "开启":
                group_manager.unblock_plugin(plugin_cmd)
            else:
                group_manager.block_plugin(plugin_cmd, block_type=block_type)
            break


async def get_plugin_status():
    return await asyncio.get_event_loop().run_in_executor(None, _get_plugin_status)


def _get_plugin_status():
    rst = '\t功能\n'
    flag_str = '状态'.rjust(4) + '\n'
    for plugin_cmd in plugins2info_dict:
        flag = group_manager.get_plugin_block_type(plugin_cmd)
        flag = flag.upper() + ' CLOSE' if flag else 'OPEN'
        rst += f'{plugins2info_dict[plugin_cmd]["cmd"][0]}\n'
        flag_str += f'{flag}\n'
    height = len(rst.split('\n')) * 24
    a = CreateImg(150, height, font_size=20)
    a.text((10, 10), rst)
    b = CreateImg(200, height, font_size=20)
    b.text((10, 10), flag_str)
    A = CreateImg(380, height)
    A.paste(a)
    A.paste(b, (150, 0))
    return image(b64=A.pic2bs4())


async def update_member_info(group_id: int) -> bool:
    bot = get_bot()
    _group_user_list = await bot.get_group_member_list(group_id=group_id)
    _error_member_list = []
    _exist_member_list = []
    # try:
    for user_info in _group_user_list:
        if user_info["card"] == "":
            nickname = user_info["nickname"]
        else:
            nickname = user_info["card"]
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
                    user_info["user_id"], user_info["group_id"], ADMIN_DEFAULT_AUTH
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
    if _error_member_list:
        result = ""
        for error_user in _error_member_list:
            result += error_user
        await bot.send_private_msg(
            user_id=int(list(bot.config.superusers)[0]), message=result[:-1]
        )
    return True




