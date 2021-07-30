from configs.path_config import DATA_PATH
from nonebot.matcher import Matcher
from nonebot.message import run_postprocessor
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from datetime import datetime
from configs.config import plugins2info_dict
from utils.utils import scheduler
from nonebot.typing import Optional

try:
    import ujson as json
except ModuleNotFoundError:
    import json


try:
    with open(DATA_PATH + "_prefix_count.json", "r", encoding="utf8") as f:
        _prefix_count_dict = json.load(f)
except (FileNotFoundError, ValueError):
    _prefix_count_dict = {
        "total_statistics": {
            "total": {},
        },
        "day_statistics": {
            "total": {},
        },
        "week_statistics": {
            "total": {},
        },
        "month_statistics": {
            "total": {},
        },
        "start_time": str(datetime.now().date()),
        "day_index": 0,
    }

try:
    with open(DATA_PATH + "_prefix_user_count.json", "r", encoding="utf8") as f:
        _prefix_user_count_dict = json.load(f)
except (FileNotFoundError, ValueError):
    _prefix_user_count_dict = {
        "total_statistics": {
            "total": {},
        },
        "day_statistics": {
            "total": {},
        },
        "week_statistics": {
            "total": {},
        },
        "month_statistics": {
            "total": {},
        },
        "start_time": str(datetime.now().date()),
        "day_index": 0,
    }


# 以前版本转换
if not _prefix_count_dict.get("day_index"):
    tmp = _prefix_count_dict.copy()
    _prefix_count_dict = {
        "total_statistics": tmp["total_statistics"],
        "day_statistics": {
            "total": {},
        },
        "week_statistics": {
            "total": {},
        },
        "month_statistics": {
            "total": {},
        },
        "start_time": tmp["start_time"],
        "day_index": 0,
    }


# 添加命令次数
@run_postprocessor
async def _(
    matcher: Matcher,
    exception: Optional[Exception],
    bot: Bot,
    event: GroupMessageEvent,
    state: T_State,
):
    global _prefix_count_dict
    if matcher.type == "message" and matcher.priority not in [1, 9]:
        model = matcher.module
        day_index = _prefix_count_dict["day_index"]
        # print(f'model --> {model}')
        for plugin in plugins2info_dict:
            if plugin == model:
                print(f'plugin --> {plugin}')
                try:
                    group_id = str(event.group_id)
                except AttributeError:
                    group_id = "total"
                user_id = str(event.user_id)
                plugin_name = plugins2info_dict[plugin]["cmd"][0]
                check_exists_key(group_id, user_id, plugin_name)
                for data in [_prefix_count_dict, _prefix_user_count_dict]:
                    data["total_statistics"]["total"][plugin_name] += 1
                    data["day_statistics"]["total"][plugin_name] += 1
                    data["week_statistics"]["total"][plugin_name] += 1
                    data["month_statistics"]["total"][plugin_name] += 1
                # print(_prefix_count_dict)
                if group_id != "total":
                    for data in [_prefix_count_dict, _prefix_user_count_dict]:
                        if data == _prefix_count_dict:
                            key = group_id
                        else:
                            key = user_id
                        data["total_statistics"][key][plugin_name] += 1
                        data["day_statistics"][key][plugin_name] += 1
                        data["week_statistics"][key][str(day_index % 7)][
                            plugin_name
                        ] += 1
                        data["month_statistics"][key][str(day_index % 30)][
                            plugin_name
                        ] += 1
                with open(DATA_PATH + "_prefix_count.json", "w", encoding="utf8") as f:
                    json.dump(_prefix_count_dict, f, indent=4, ensure_ascii=False)
                with open(
                    DATA_PATH + "_prefix_user_count.json", "w", encoding="utf8"
                ) as f:
                    json.dump(_prefix_user_count_dict, f, ensure_ascii=False, indent=4)
                break


def check_exists_key(group_id: str, user_id: str, plugin_name: str):
    global _prefix_count_dict, _prefix_user_count_dict
    for data in [_prefix_count_dict, _prefix_user_count_dict]:
        if data == _prefix_count_dict:
            key = group_id
        else:
            key = user_id
        if not data["total_statistics"]["total"].get(plugin_name):
            data["total_statistics"]["total"][plugin_name] = 0
        if not data["day_statistics"]["total"].get(plugin_name):
            data["day_statistics"]["total"][plugin_name] = 0
        if not data["week_statistics"]["total"].get(plugin_name):
            data["week_statistics"]["total"][plugin_name] = 0
        if not data["month_statistics"]["total"].get(plugin_name):
            data["month_statistics"]["total"][plugin_name] = 0

        if not data["total_statistics"].get(key):
            data["total_statistics"][key] = {}
        if not data["total_statistics"][key].get(plugin_name):
            data["total_statistics"][key][plugin_name] = 0
        if not data["day_statistics"].get(key):
            data["day_statistics"][key] = {}
        if not data["day_statistics"][key].get(plugin_name):
            data["day_statistics"][key][plugin_name] = 0

        if not data["week_statistics"].get(key):
            data["week_statistics"][key] = {}
        if data["week_statistics"][key].get("0") is None:
            for i in range(7):
                data["week_statistics"][key][str(i)] = {}
        if data["week_statistics"][key]["0"].get(plugin_name) is None:
            for i in range(7):
                data["week_statistics"][key][str(i)][plugin_name] = 0

        if not data["month_statistics"].get(key):
            data["month_statistics"][key] = {}
        if data["month_statistics"][key].get("0") is None:
            for i in range(30):
                data["month_statistics"][key][str(i)] = {}
        if data["month_statistics"][key]["0"].get(plugin_name) is None:
            for i in range(30):
                data["month_statistics"][key][str(i)][plugin_name] = 0


# 天
@scheduler.scheduled_job(
    "cron",
    hour=0,
    minute=1,
)
async def _():
    for data in [_prefix_count_dict, _prefix_user_count_dict]:
        for x in _prefix_count_dict["day_statistics"].keys():
            for key in _prefix_count_dict["day_statistics"][x].keys():
                data["day_statistics"][x][key] = 0
        data["day_index"] += 1
    with open(DATA_PATH + "_prefix_count.json", "w", encoding="utf8") as f:
        json.dump(_prefix_count_dict, f, indent=4, ensure_ascii=False)
    with open(DATA_PATH + "_prefix_user_count.json", "w", encoding="utf8") as f:
        json.dump(_prefix_user_count_dict, f, indent=4, ensure_ascii=False)
