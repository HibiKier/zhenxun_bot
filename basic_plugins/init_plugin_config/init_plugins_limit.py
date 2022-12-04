from utils.manager import (
    plugins2cd_manager,
    plugins2block_manager,
    plugins2count_manager,
    plugin_data_manager,
)
from utils.utils import get_matchers
from configs.path_config import DATA_PATH


def init_plugins_cd_limit():
    """
    加载 cd 限制
    """
    plugins2cd_file = DATA_PATH / "configs" / "plugins2cd.yaml"
    plugins2cd_file.parent.mkdir(exist_ok=True, parents=True)
    for matcher in get_matchers(True):
        if not plugins2cd_manager.get_plugin_cd_data(matcher.plugin_name) and (
            plugin_data := plugin_data_manager.get(matcher.plugin_name)
        ):
            if plugin_data.plugin_cd:
                plugins2cd_manager.add_cd_limit(
                    matcher.plugin_name, plugin_data.plugin_cd
                )
    if not plugins2cd_manager.keys():
        plugins2cd_manager.add_cd_limit("这是一个示例")
    plugins2cd_manager.save()
    plugins2cd_manager.reload_cd_limit()


def init_plugins_block_limit():
    """
    加载阻塞限制
    """
    for matcher in get_matchers(True):
        if not plugins2block_manager.get_plugin_block_data(matcher.plugin_name) and (
            plugin_data := plugin_data_manager.get(matcher.plugin_name)
        ):
            if plugin_data.plugin_block:
                plugins2block_manager.add_block_limit(
                    matcher.plugin_name, plugin_data.plugin_block
                )
    if not plugins2block_manager.keys():
        plugins2block_manager.add_block_limit("这是一个示例")
    plugins2block_manager.save()
    plugins2block_manager.reload_block_limit()


def init_plugins_count_limit():
    """
    加载次数限制
    """
    for matcher in get_matchers(True):
        if not plugins2count_manager.get_plugin_count_data(matcher.plugin_name) and (
            plugin_data := plugin_data_manager.get(matcher.plugin_name)
        ):
            if plugin_data.plugin_count:
                plugins2count_manager.add_count_limit(
                    matcher.plugin_name, plugin_data.plugin_count
                )
    if not plugins2count_manager.keys():
        plugins2count_manager.add_count_limit("这是一个示例")
    plugins2count_manager.save()
    plugins2count_manager.reload_count_limit()
