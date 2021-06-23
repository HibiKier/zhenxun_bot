from configs.path_config import DATA_PATH
from nonebot.matcher import Matcher
from nonebot.message import run_postprocessor
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from datetime import datetime
from configs.config import plugins2name_dict
from util.utils import scheduler
from nonebot.typing import Optional
try:
    import ujson as json
except ModuleNotFoundError:
    import json


try:
    with open(DATA_PATH + '_prefix_count.json', 'r', encoding='utf8') as f:
        _prefix_count_dict = json.load(f)
except (FileNotFoundError, ValueError):
    _prefix_count_dict = {
        'total_statistics': {
            'total': {},
        },
        'day_statistics': {
            'total': {},
        },
        'week_statistics': {
            'total': {},
        },
        'month_statistics': {
            'total': {},
        },
        'start_time': str(datetime.now().date()),
        'day_index': 0
    }
if not _prefix_count_dict.get('day_index'):
    tmp = _prefix_count_dict.copy()
    _prefix_count_dict = {'total_statistics': tmp['total_statistics'], 'day_statistics': {
        'total': {},
    }, 'week_statistics': {
        'total': {},
    }, 'month_statistics': {
        'total': {},
    }, 'start_time': str(datetime.now().date()), 'day_index': 0}


# 添加命令次数
@run_postprocessor
async def _(matcher: Matcher, exception: Optional[Exception], bot: Bot, event: GroupMessageEvent, state: T_State):
    global _prefix_count_dict
    if matcher.type == 'message' and matcher.priority not in [1, 9]:
        model = matcher.module
        day_index = _prefix_count_dict['day_index']
        # print(f'model --> {model}')
        for plugin in plugins2name_dict:
            if plugin == model:
                # print(f'plugin --> {plugin}')
                try:
                    group_id = str(event.group_id)
                except AttributeError:
                    group_id = 'total'
                plugin_name = plugins2name_dict[plugin][0]
                check_exists_key(group_id, plugin_name)
                _prefix_count_dict['total_statistics']['total'][plugin_name] += 1
                _prefix_count_dict['day_statistics']['total'][plugin_name] += 1
                _prefix_count_dict['week_statistics']['total'][plugin_name] += 1
                _prefix_count_dict['month_statistics']['total'][plugin_name] += 1
                # print(_prefix_count_dict)
                if group_id != 'total':
                    _prefix_count_dict['total_statistics'][group_id][plugin_name] += 1
                    _prefix_count_dict['day_statistics'][group_id][plugin_name] += 1
                    _prefix_count_dict['week_statistics'][group_id][str(day_index % 7)][plugin_name] += 1
                    _prefix_count_dict['month_statistics'][group_id][str(day_index % 30)][plugin_name] += 1
                with open(DATA_PATH + '_prefix_count.json', 'w', encoding='utf8') as f:
                    json.dump(_prefix_count_dict, f, indent=4, ensure_ascii=False)
                break


def check_exists_key(group_id: str, plugin_name: str):
    global _prefix_count_dict
    if not _prefix_count_dict['total_statistics']['total'].get(plugin_name):
        _prefix_count_dict['total_statistics']['total'][plugin_name] = 0
    if not _prefix_count_dict['day_statistics']['total'].get(plugin_name):
        _prefix_count_dict['day_statistics']['total'][plugin_name] = 0
    if not _prefix_count_dict['week_statistics']['total'].get(plugin_name):
        _prefix_count_dict['week_statistics']['total'][plugin_name] = 0
    if not _prefix_count_dict['month_statistics']['total'].get(plugin_name):
        _prefix_count_dict['month_statistics']['total'][plugin_name] = 0
    if not _prefix_count_dict['total_statistics'].get(group_id):
        _prefix_count_dict['total_statistics'][group_id] = {
            plugin_name: 0,
        }
    elif not _prefix_count_dict['total_statistics'][group_id].get(plugin_name):
        _prefix_count_dict['total_statistics'][group_id][plugin_name] = 0
    if not _prefix_count_dict['day_statistics'].get(group_id):
        _prefix_count_dict['day_statistics'][group_id] = {}
        _prefix_count_dict['day_statistics'][group_id][plugin_name] = 0
    elif not _prefix_count_dict['day_statistics'][group_id].get(plugin_name):
        _prefix_count_dict['day_statistics'][group_id][plugin_name] = 0
    if not _prefix_count_dict['week_statistics'].get(group_id):
        _prefix_count_dict['week_statistics'][group_id] = {}
        for i in range(7):
            _prefix_count_dict['week_statistics'][group_id][str(i)] = {}
            _prefix_count_dict['week_statistics'][group_id][str(i)][plugin_name] = 0
    elif not _prefix_count_dict['week_statistics'][group_id]['0'].get(plugin_name):
        for i in range(7):
            _prefix_count_dict['week_statistics'][group_id][str(i)][plugin_name] = 0
    if not _prefix_count_dict['month_statistics'].get(group_id):
        _prefix_count_dict['month_statistics'][group_id] = {}
        for i in range(30):
            _prefix_count_dict['month_statistics'][group_id][str(i)] = {}
            _prefix_count_dict['month_statistics'][group_id][str(i)][plugin_name] = 0
    elif not _prefix_count_dict['month_statistics'][group_id]['0'].get(plugin_name):
        for i in range(30):
            _prefix_count_dict['month_statistics'][group_id][str(i)][plugin_name] = 0


# 天
@scheduler.scheduled_job(
    'cron',
    hour=0,
    minute=1,
)
async def _():
    for group_id in _prefix_count_dict['day_statistics'].keys():
        for key in _prefix_count_dict['day_statistics'][group_id].keys():
            _prefix_count_dict['day_statistics'][group_id][key] = 0
    _prefix_count_dict['day_index'] += 1
    if _prefix_count_dict['day_index'] % 7 == 0:
        _prefix_count_dict['week_statistics']['total'] = {}
    if _prefix_count_dict['day_index'] % 30 == 0:
        _prefix_count_dict['month_statistics']['total'] = {}
    with open(DATA_PATH + '_prefix_count.json', 'w', encoding='utf8') as f:
        json.dump(_prefix_count_dict, f, indent=4, ensure_ascii=False)


