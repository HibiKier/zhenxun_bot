from pydantic import BaseModel
from nonebot_plugin_htmlrender import template_to_pic

from zhenxun.utils.enum import BlockType
from zhenxun.utils.platform import PlatformUtils
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.configs.path_config import TEMPLATE_PATH
from zhenxun.models.group_console import GroupConsole

from ._utils import classify_plugin


class Item(BaseModel):
    plugin_name: str
    """插件名称"""


def __handle_item(plugin: PluginInfo, group: GroupConsole | None):
    """构造Item

    参数:
        plugin: PluginInfo
        group: 群组

    返回:
        Item: Item
    """
    if not plugin.status:
        if plugin.block_type == BlockType.ALL:
            plugin.name = f"{plugin.name}(不可用)"
        elif group and plugin.block_type == BlockType.GROUP:
            plugin.name = f"{plugin.name}(不可用)"
        elif not group and plugin.block_type == BlockType.PRIVATE:
            plugin.name = f"{plugin.name}(不可用)"
    elif group and f"{plugin.module}," in group.block_plugin:
        plugin.name = f"{plugin.name}(不可用)"
    return Item(plugin_name=f"{plugin.id}-{plugin.name}")


def build_plugin_data(classify: dict[str, list[Item]]) -> list[dict[str, str]]:
    """构建前端插件数据

    参数:
        classify: 插件数据

    返回:
        list[dict[str, str]]: 前端插件数据
    """

    lengths = [len(classify[c]) for c in classify]
    index = lengths.index(max(lengths))
    menu_key = list(classify.keys())[index]
    max_data = classify[menu_key]
    del classify[menu_key]
    plugin_list = [
        {
            "name": "主要功能" if menu in ["normal", "功能"] else menu,
            "items": value,
        }
        for menu, value in classify.items()
    ]
    plugin_list = build_line_data(plugin_list)
    plugin_list.insert(0, build_plugin_line(menu_key, max_data, 30, 100))
    return plugin_list


def build_plugin_line(
    name: str, items: list, left: int, width: int | None = None
) -> dict:
    """构造插件行数据

    参数:
        name: 菜单名称
        items: 插件名称列表
        left: 左边距
        width: 总插件长度.

    返回:
        dict: 插件数据
    """
    _plugins = []
    width = width or 50
    if len(items) // 2 > 6:
        width = 100
        plugin_list1 = []
        plugin_list2 = []
        for i in range(len(items)):
            if i % 2:
                plugin_list1.append(items[i])
            else:
                plugin_list2.append(items[i])
        _plugins = [(30, 50, plugin_list1), (0, 50, plugin_list2)]
    else:
        _plugins = [(left, 100, items)]
    return {"name": name, "items": _plugins, "width": width}


def build_line_data(plugin_list: list[dict]) -> list[dict]:
    """构造插件数据

    参数:
        plugin_list: 插件列表

    返回:
        list[dict]: 插件数据
    """
    left = 30
    data = []
    for plugin in plugin_list:
        data.append(build_plugin_line(plugin["name"], plugin["items"], left))
        if len(plugin["items"]) // 2 <= 6:
            left = 15 if left == 30 else 30
    return data


async def build_zhenxun_image(
    bot_id: str, group_id: str | None, platform: str
) -> bytes:
    """构造真寻帮助图片

    参数:
        bot_id: bot_id
        group_id: 群号
        platform: 平台
    """
    classify = await classify_plugin(group_id, __handle_item)
    plugin_list = build_plugin_data(classify)
    return await template_to_pic(
        template_path=str((TEMPLATE_PATH / "ss_menu").absolute()),
        template_name="main.html",
        templates={
            "data": {
                "plugin_list": plugin_list,
                "ava": PlatformUtils.get_user_avatar_url(bot_id, platform),
            }
        },
        pages={
            "viewport": {"width": 637, "height": 453},
            "base_url": f"file://{TEMPLATE_PATH}",
        },
        wait=2,
    )
