from models.group_remind import GroupRemind
from services.log import logger
from configs.path_config import DATA_PATH
import os
import aiofiles
import aiohttp
from util.init_result import image
from util.utils import get_local_proxy, get_bot
from pathlib import Path
from nonebot import require
from configs.config import plugins2name_dict
from models.group_member_info import GroupInfoUser
import time
from datetime import datetime
from services.db_context import db
from models.level_user import LevelUser
from configs.config import ADMIN_DEFAULT_AUTH
try:
    import ujson as json
except ModuleNotFoundError:
    import json


export = require("nonebot_plugin_manager")


command_dict = {
    '早晚安': 'zwa',
    '进群欢迎': 'hy',
    '每日开箱重置提醒': 'kxcz',
    'b站转发解析': 'blpar',
    'epic': 'epic',
    '丢人爬': 'pa',
    '原神黄历提醒': 'almanac',
}
command_list = list(command_dict.values())
command_info_dt = {
    '早晚安': '将会在每晚11:59晚安，在6:01早安哦',
    '每日开箱重置提醒': '将会在每日00:01提示开箱重置！',
    'epic': '将会在每日中午12:01发送可白嫖的epic游戏',
    '原神黄历提醒': '将会在每日8:00发送当日的原神黄历',
}


async def remind_status(group: int, name: str, flag: bool) -> str:
    _name = ''
    if name in command_dict.values():
        _name = list(command_dict.keys())[list(command_dict.values()).index(name)]
    if flag:
        rst = '开启'
        if await GroupRemind.get_status(group, name):
            return f'该群已经{rst}过 {_name}，请勿重复开启！'
    else:
        rst = '关闭'
        if not await GroupRemind.get_status(group, name):
            return f'该群已经{rst}过 {_name}，请勿重复开启！'
    if await GroupRemind.set_status(group, name, flag):
        info = command_info_dt[_name] if command_info_dt.get(_name) else ''
        if info:
            info = '\n' + info
        return f'成功{rst} {_name}！0v0 {info}'
    else:
        return f'{rst} {_name} 失败了...'


async def set_group_status(name: str, group_id: int):
    flag = None
    if name[:2] == '开启':
        flag = True
    elif name[:2] == '关闭':
        flag = False
    cmd = name[2:]
    if cmd in ['全部通知', '所有通知']:
        for command in command_list:
            await remind_status(group_id, command, flag)
        return f'已{name[:2]}所有通知！'
    return await remind_status(group_id, command_dict[cmd], flag)


async def group_current_status(group_id: int):
    result = f'（被动技能）\n早晚安通知：{"√" if await GroupRemind.get_status(group_id, "zwa") else "×"}\n' \
             f'进群欢迎：{"√" if await GroupRemind.get_status(group_id, "hy") else "×"}\n' \
             f'每日开箱重置通知：{"√" if await GroupRemind.get_status(group_id, "kxcz") else "×"}\n' \
             f'b站转发解析：{"√" if await GroupRemind.get_status(group_id, "blpar") else "×"}\n' \
             f'丢人爬：{"√" if await GroupRemind.get_status(group_id, "pa") else "×"}\n' \
             f'epic免费游戏：{"√" if await GroupRemind.get_status(group_id, "epic") else "×"}\n' \
             f'原神黄历提醒：{"√" if await GroupRemind.get_status(group_id, "almanac") else "×"}'
    return result


custom_welcome_msg_json = Path() / "data" / "custom_welcome_msg" / "custom_welcome_msg.json"


async def custom_group_welcome(msg, imgs, user_id, group_id):
    img_result = ''
    img = imgs[0] if imgs else ''
    result = ''
    if os.path.exists(DATA_PATH + f'custom_welcome_msg/{group_id}.jpg'):
        os.remove(DATA_PATH + f'custom_welcome_msg/{group_id}.jpg')
    # print(custom_welcome_msg_json)
    if not custom_welcome_msg_json.exists():
        custom_welcome_msg_json.parent.mkdir(parents=True, exist_ok=True)
        data = {}
    else:
        try:
            data = json.load(open(custom_welcome_msg_json, 'r'))
        except FileNotFoundError:
            data = {}
    try:
        if msg:
            data[str(group_id)] = str(msg)
            json.dump(data, open(custom_welcome_msg_json, 'w'), indent=4, ensure_ascii=False)
            logger.info(f'USER {user_id} GROUP {group_id} 更换群欢迎消息 {msg}')
            result += msg
        if img:
            async with aiohttp.ClientSession() as session:
                async with session.get(img, proxy=get_local_proxy()) as response:
                    async with aiofiles.open(DATA_PATH + f'custom_welcome_msg/{group_id}.jpg', 'wb') as f:
                        await f.write(await response.read())
            img_result = image(abspath=DATA_PATH + f'custom_welcome_msg/{group_id}.jpg')
            logger.info(f'USER {user_id} GROUP {group_id} 更换群欢迎消息图片')
    except Exception as e:
        logger.error(f'GROUP {group_id} 替换群消息失败 e:{e}')
        return '替换群消息失败..'
    return f'替换群欢迎消息成功：\n{result}' + img_result


async def change_group_switch(cmd: str, group_id: int):
    group_id = str(group_id)
    status = cmd[:2]
    cmd = cmd[2:]
    try:
        with open(DATA_PATH + 'manager/plugin_list.json', 'r', encoding='utf8') as f:
            plugin_list = json.load(f)
    except ValueError:
        pass
    except FileNotFoundError:
        pass
    for plugin_cmd in plugins2name_dict.keys():
        if cmd in plugins2name_dict[plugin_cmd]:
            # print(plugin_list[plugin_cmd])
            if status == '开启':
                # if group_id in plugin_list[plugin_cmd]:
                if group_id not in plugin_list[plugin_cmd] or plugin_list[plugin_cmd][group_id]:
                    return f'功能 {cmd} 正处于开启状态！不要重复开启.'
                export.unblock_plugin(group_id, plugin_cmd)
            else:
                if group_id in plugin_list[plugin_cmd]:
                    if not plugin_list[plugin_cmd][group_id]:
                        return f'功能 {cmd} 正处于关闭状态！不要重复关闭.'
                export.block_plugin(group_id, plugin_cmd)
            if os.path.exists(DATA_PATH + f'group_help/{group_id}.png'):
                os.remove(DATA_PATH + f'group_help/{group_id}.png')

            return f'{status} {cmd} 功能！'
    return f'没有找到 {cmd} 功能喔'


async def update_member_info(group_id: int) -> bool:
    bot = get_bot()
    _group_user_list = await bot.get_group_member_list(group_id=group_id)
    _error_member_list = []
    _exist_member_list = []
    # try:
    for user_info in _group_user_list:
        if user_info['card'] == "":
            nickname = user_info['nickname']
        else:
            nickname = user_info['card']
        async with db.transaction():
            # 更新权限
            if user_info['role'] in ['owner', 'admin'] and not await LevelUser.is_group_flag(user_info['user_id'], group_id):
                await LevelUser.set_level(user_info['user_id'], user_info['group_id'], ADMIN_DEFAULT_AUTH)
            if str(user_info['user_id']) in bot.config.superusers:
                await LevelUser.set_level(user_info['user_id'], user_info['group_id'], 9)
            user = await GroupInfoUser.select_member_info(user_info['user_id'], user_info['group_id'])
            if user:
                if user.user_name != nickname:
                    await user.update(user_name=nickname).apply()
                    logger.info(f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新群昵称成功")
                _exist_member_list.append(int(user_info['user_id']))
                continue
            join_time = datetime.strptime(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(user_info['join_time'])), "%Y-%m-%d %H:%M:%S")
            if await GroupInfoUser.insert(
                    user_info['user_id'],
                    user_info['group_id'],
                    nickname,
                    join_time,):
                _exist_member_list.append(int(user_info['user_id']))
                logger.info(f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新成功")
            else:
                _error_member_list.append(f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新失败\n")
    _del_member_list = list(set(_exist_member_list).difference(set(await GroupInfoUser.query_group_member_list(group_id))))
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
        await bot.send_private_msg(user_id=int(list(bot.config.superusers)[0]), message=result[:-1])
    return True




