from configs.path_config import DATA_PATH
from utils.utils import get_bot
from models.group_remind import GroupRemind
from datetime import datetime
import time
from services.log import logger
try:
    import ujson as json
except ModuleNotFoundError:
    import json


time_data = {}


async def init():
    global time_data
    bot = get_bot()
    gl = await bot.get_group_list(self_id=bot.self_id)
    gl = [g['group_id'] for g in gl]
    data = read_data('group_last_chat_time.json')
    for g in gl:
        if not data.get(g):
            time_data[g] = time.time()
    if not time_data.get('check_time'):
        time_data['check_time'] = time.time()
    if not time_data.get('_group'):
        time_data['_group'] = []
    save_data()
    return time_data


def read_data(file_name: str):
    try:
        with open(DATA_PATH + file_name, 'r', encoding='utf8') as f:
            return json.load(f)
    except (ValueError, FileNotFoundError):
        return {}


def save_data():
    with open(DATA_PATH + 'group_last_chat_time.json', 'w') as f:
        json.dump(time_data, f, indent=4)
    logger.info(f'自动存储 group_last_chat_time.json 时间：{str(datetime.now()).split(".")[0]}')


command_list = ['zwa', 'hy', 'kxcz', 'blpar', 'epic', 'pa']


# 取消全部通知
async def cancel_all_notice(group_id):
    group_id = int(group_id)
    for command in command_list:
        if await GroupRemind.get_status(group_id, command):
            await GroupRemind.set_status(group_id, command, False)
    logger.info(f'关闭了 {group_id} 群的全部通知')


async def get_data():
    global time_data
    if not time_data:
        time_data = await init()
    return time_data


def set_data_value(key, value):
    global time_data
    time_data[key] = value






