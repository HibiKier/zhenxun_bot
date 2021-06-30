import json
import httpx
from pathlib import Path
from configs.config import plugins2info_dict

_DATA_PATH = Path() / "data" / "manager" / "plugin_list.json"


def get_store_plugin_info(plugin: str) -> str:
    store_plugin_list = _get_store_plugin_list()
    if plugin in store_plugin_list:
        plugin = store_plugin_list[plugin]
        return (
            f"ID: {plugin['id']}\n"
            f"Name: {plugin['name']}\n"
            f"Description: {plugin['desc']}\n"
            f"Version: {httpx.get('https://pypi.org/pypi/'+plugin['link']+'/json').json()['info']['version']}\n"
            f"Author: {plugin['author']}\n"
            f"Repo: https://github.com/{plugin['repo']}"
        )
    else:
        return "查无此插件！"


def get_group_plugin_list(group_id: str) -> dict:
    plugin_list = _load_plugin_list()
    group_plugin_list = {}
    for plugin in plugin_list:
        if group_id in plugin_list[plugin]:
            group_plugin_list[plugin] = plugin_list[plugin][group_id]
        else:
            group_plugin_list[plugin] = plugin_list[plugin]["default"]
    return group_plugin_list


def get_store_pulgin_list() -> str:
    message = "商店插件列表如下："
    for plugin in _get_store_plugin_list():
        if plugin in _load_plugin_list() or plugin == "nonebot_plugin_manager":
            message += f"\n[o] {plugin}"
        else:
            message += f"\n[x] {plugin}"
    return message


def auto_update_plugin_list(loaded_plugin_list: list, keep_history: bool = False):
    plugin_list = _load_plugin_list()
    for plugin in loaded_plugin_list:
        if plugin not in plugin_list:
            plugin_list[plugin] = {"default": True}
    if not keep_history:
        plugin_list = {
            key: plugin_list[key] for key in plugin_list if key in loaded_plugin_list
        }
    _dump_plugin_list(plugin_list)
    return plugin_list


def block_plugin(group_id: str, *plugins: str):
    return _update_plugin_list(group_id, True, *plugins)


def unblock_plugin(group_id: str, *plugins: str):
    return _update_plugin_list(group_id, False, *plugins)


# 获取商店插件列表
def _get_store_plugin_list() -> dict:
    store_plugin_list = {}
    for plugin in httpx.get(
        "https://cdn.jsdelivr.net/gh/nonebot/nonebot2@master/docs/.vuepress/public/plugins.json"
    ).json():
        store_plugin_list.update({plugin["id"]: plugin})
    return store_plugin_list


# 更新插件列表
def _update_plugin_list(group_id: str, block: bool, *plugins: str) -> str:
    plugin_list = _load_plugin_list()
    message = "结果如下："
    operate = "屏蔽" if block else "启用"
    for plugin in plugins:
        for values in plugins2info_dict.values():
            if plugin in values['cmd']:
                plugin = list(plugins2info_dict.keys())[list(plugins2info_dict.values()).index(values)]
                # print(plugin)
                break
        message += "\n"
        if plugin in plugin_list:
            if (
                not group_id in plugin_list[plugin]
                or plugin_list[plugin][group_id] == block
            ):
                plugin_list[plugin][group_id] = not block
                message += f"插件{plugin}{operate}成功！"
                print(plugin_list[plugin][group_id])
            else:
                message += f"插件{plugin}已经{operate}！"
        else:
            message += f"插件{plugin}不存在！"
    _dump_plugin_list(plugin_list)
    return message


# 加载插件列表
def _load_plugin_list() -> dict:
    try:
        return json.load(_DATA_PATH.open("r", encoding="utf-8"))
    except FileNotFoundError:
        return {}


# 保存插件列表
def _dump_plugin_list(plugin_list: dict):
    _DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    json.dump(
        plugin_list,
        _DATA_PATH.open("w", encoding="utf-8"),
        indent=4,
        separators=(",", ": "),
    )
