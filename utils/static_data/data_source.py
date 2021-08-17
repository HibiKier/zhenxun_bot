from pathlib import Path
import ujson as json
from .group_manager import GroupManager


def init(group_manager: GroupManager):
    old_group_level_file = Path() / "data" / "manager" / "group_level.json"
    old_plugin_list_file = Path() / "data" / "manager" / "plugin_list.json"
    if old_group_level_file.exists():
        data = json.load(open(old_group_level_file, 'r', encoding='utf8'))
        for key in data.keys():
            group = key
            level = data[key]
            group_manager.set_group_level(group, level)
        old_group_level_file.unlink()
        group_manager.save()

    if old_plugin_list_file.exists():
        data = json.load(open(old_plugin_list_file, 'r', encoding='utf8'))
        for plugin in data.keys():
            for group in data[plugin].keys():
                if group == 'default' and not data[plugin]['default']:
                    group_manager.block_plugin(plugin)
                elif not data[plugin][group]:
                    group_manager.block_plugin(plugin, group)
        old_plugin_list_file.unlink()
        group_manager.save()
