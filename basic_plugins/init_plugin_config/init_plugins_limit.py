from pathlib import Path
from ruamel.yaml import round_trip_load, round_trip_dump, YAML
from utils.manager import (
    plugins2cd_manager,
    plugins2block_manager,
    plugins2count_manager,
)
from utils.utils import get_matchers
from ruamel import yaml
import nonebot


_yaml = YAML(typ="safe")


def init_plugins_cd_limit(data_path):
    """
    加载 cd 限制
    """
    plugins2cd_file = data_path / "configs" / "plugins2cd.yaml"
    plugins2cd_file.parent.mkdir(exist_ok=True, parents=True)
    _data = {}
    _matchers = get_matchers()
    for matcher in _matchers:
        if not plugins2cd_manager.get_plugin_cd_data(matcher.plugin_name):
            _plugin = nonebot.plugin.get_plugin(matcher.plugin_name)
            try:
                _module = _plugin.module
                plugin_cd_limit = _module.__getattribute__("__plugin_cd_limit__")
                plugins2cd_manager.add_cd_limit(
                    matcher.plugin_name, data_dict=plugin_cd_limit
                )
            except AttributeError:
                pass
    if not plugins2cd_manager.keys():
        plugins2cd_manager.add_cd_limit(
            "这是一个示例"
        )
    _tmp_data = {"PluginCdLimit": plugins2cd_manager.get_data()}
    with open(plugins2cd_file, "w", encoding="utf8") as wf:
        yaml.dump(_tmp_data, wf, Dumper=yaml.RoundTripDumper, allow_unicode=True)
    _data = round_trip_load(open(plugins2cd_file, encoding="utf8"))
    _data["PluginCdLimit"].yaml_set_start_comment(
        """# 需要cd的功能
# 自定义的功能需要cd也可以在此配置
# key：模块名称
# cd：cd 时长（秒）
# status：此限制的开关状态
# check_type：'private'/'group'/'all'，限制私聊/群聊/全部
# limit_type：监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
#                                     示例：'user'：用户N秒内触发1次，'group'：群N秒内触发1次
# rst：回复的话，可以添加[at]，[uname]，[nickname]来对应艾特，用户群名称，昵称系统昵称
# rst 为 "" 或 None 时则不回复
# rst示例："[uname]你冲的太快了，[nickname]先生，请稍后再冲[at]"
# rst回复："老色批你冲的太快了，欧尼酱先生，请稍后再冲@老色批"
#      用户昵称↑     昵称系统的昵称↑          艾特用户↑""",
        indent=2,
    )
    with open(plugins2cd_file, "w", encoding="utf8") as wf:
        round_trip_dump(_data, wf, Dumper=yaml.RoundTripDumper, allow_unicode=True)
    plugins2cd_manager.reload_cd_limit()


def init_plugins_block_limit(data_path):
    """
    加载阻塞限制
    """
    plugins2block_file = data_path / "configs" / "plugins2block.yaml"
    plugins2block_file.parent.mkdir(exist_ok=True, parents=True)
    _data = {}
    _matchers = get_matchers()
    for matcher in _matchers:
        if not plugins2block_manager.get_plugin_block_data(matcher.plugin_name):
            _plugin = nonebot.plugin.get_plugin(matcher.plugin_name)
            try:
                _module = _plugin.module
                plugin_block_limit = _module.__getattribute__("__plugin_block_limit__")
                plugins2block_manager.add_block_limit(
                    matcher.plugin_name, data_dict=plugin_block_limit
                )
            except AttributeError:
                pass
    if not plugins2block_manager.keys():
        plugins2block_manager.add_block_limit(
            "这是一个示例"
        )
    _tmp_data = {"PluginBlockLimit": plugins2block_manager.get_data()}
    with open(plugins2block_file, "w", encoding="utf8") as wf:
        yaml.dump(_tmp_data, wf, Dumper=yaml.RoundTripDumper, allow_unicode=True)
    _data = round_trip_load(open(plugins2block_file, encoding="utf8"))
    _data["PluginBlockLimit"].yaml_set_start_comment(
        """# 用户调用阻塞
# 即 当用户调用此功能还未结束时
# 用发送消息阻止用户重复调用此命令直到该命令结束
# key：模块名称
# status：此限制的开关状态
# check_type：'private'/'group'/'all'，限制私聊/群聊/全部
# limit_type：监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
#                                     示例：'user'：阻塞用户，'group'：阻塞群聊
# rst：回复的话，可以添加[at]，[uname]，[nickname]来对应艾特，用户群名称，昵称系统昵称
# rst 为 "" 或 None 时则不回复
# rst示例："[uname]你冲的太快了，[nickname]先生，请稍后再冲[at]"
# rst回复："老色批你冲的太快了，欧尼酱先生，请稍后再冲@老色批"
#      用户昵称↑     昵称系统的昵称↑          艾特用户↑""",
        indent=2,
    )
    with open(plugins2block_file, "w", encoding="utf8") as wf:
        round_trip_dump(_data, wf, Dumper=yaml.RoundTripDumper, allow_unicode=True)
    plugins2block_manager.reload_block_limit()


def init_plugins_count_limit(data_path):
    """
    加载次数限制
    """
    plugins2count_file = data_path / "configs" / "plugins2count.yaml"
    plugins2count_file.parent.mkdir(exist_ok=True, parents=True)
    _data = {}
    _matchers = get_matchers()
    for matcher in _matchers:
        if not plugins2count_manager.get_plugin_count_data(matcher.plugin_name):
            _plugin = nonebot.plugin.get_plugin(matcher.plugin_name)
            try:
                _module = _plugin.module
                plugin_count_limit = _module.__getattribute__("__plugin_count_limit__")
                plugins2count_manager.add_count_limit(
                    matcher.plugin_name, data_dict=plugin_count_limit
                )
            except AttributeError:
                pass
    if not plugins2count_manager.keys():
        plugins2count_manager.add_count_limit(
            "这是一个示例"
        )
    _tmp_data = {"PluginCountLimit": plugins2count_manager.get_data()}
    with open(plugins2count_file, "w", encoding="utf8") as wf:
        yaml.dump(_tmp_data, wf, Dumper=yaml.RoundTripDumper, allow_unicode=True)
    _data = round_trip_load(open(plugins2count_file, encoding="utf8"))
    _data["PluginCountLimit"].yaml_set_start_comment(
        """# 命令每日次数限制
# 即 用户/群聊 每日可调用命令的次数 [数据内存存储，重启将会重置]
# 每日调用直到 00:00 刷新
# key：模块名称
# max_count: 每日调用上限
# status：此限制的开关状态
# limit_type：监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
#                                     示例：'user'：用户上限，'group'：群聊上限
# rst：回复的话，可以添加[at]，[uname]，[nickname]来对应艾特，用户群名称，昵称系统昵称
# rst 为 "" 或 None 时则不回复
# rst示例："[uname]你冲的太快了，[nickname]先生，请稍后再冲[at]"
# rst回复："老色批你冲的太快了，欧尼酱先生，请稍后再冲@老色批"
#      用户昵称↑     昵称系统的昵称↑          艾特用户↑""",
        indent=2,
    )
    with open(plugins2count_file, "w", encoding="utf8") as wf:
        round_trip_dump(_data, wf, Dumper=yaml.RoundTripDumper, allow_unicode=True)
    plugins2count_manager.reload_count_limit()
