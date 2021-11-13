from pathlib import Path
from ruamel.yaml import round_trip_load, round_trip_dump, YAML
from utils.manager import plugins2settings_manager, admin_manager
from services.log import logger
from utils.utils import get_matchers
from ruamel import yaml
import nonebot


_yaml = YAML(typ="safe")


def init_plugins_settings(data_path: str):
    """
    初始化插件设置，从插件中获取 __zx_plugin_name__，__plugin_cmd__，__plugin_settings__
    """
    plugins2settings_file = Path(data_path) / "configs" / "plugins2settings.yaml"
    plugins2settings_file.parent.mkdir(exist_ok=True, parents=True)
    _matchers = get_matchers()
    _data = {}
    if plugins2settings_file.exists():
        with open(plugins2settings_file, "r", encoding="utf8") as f:
            _data = _yaml.load(f)
            _data = _data["PluginSettings"] if _data else {}
    _tmp_module = {}
    _tmp = []
    for matcher in _matchers:
        if matcher.module in _data.keys():
            plugins2settings_manager.add_plugin_settings(
                matcher.module,
                plugin_type=_data[matcher.module]["plugin_type"],
                data_dict=_data[matcher.module],
            )
            if _data[matcher.module]["cmd"]:
                _tmp_module[matcher.module] = _data[matcher.module]["cmd"][0]
        else:
            _plugin = nonebot.plugin.get_plugin(matcher.module)
            try:
                _module = _plugin.module
            except AttributeError:
                logger.warning(f"插件 {matcher.module} 加载失败...，插件控制未加载.")
            else:
                try:
                    plugin_name = _module.__getattribute__("__zx_plugin_name__")
                    if "[admin]" in plugin_name.lower():
                        try:
                            admin_settings = _module.__getattribute__(
                                "__plugin_settings__"
                            )
                            level = admin_settings["admin_level"]
                            cmd = admin_settings.get("cmd")
                        except (AttributeError, KeyError):
                            level = 5
                            cmd = None
                        if not level:
                            level = 5
                        admin_manager.add_admin_plugin_settings(
                            matcher.module, cmd, level
                        )
                    if (
                        "[hidden]" in plugin_name.lower()
                        or "[admin]" in plugin_name.lower()
                        or "[superuser]" in plugin_name.lower()
                        or matcher.module in plugins2settings_manager.keys()
                    ):
                        continue
                except AttributeError:
                    if matcher.module not in _tmp:
                        logger.warning(
                            f"获取插件 {matcher.module} __zx_plugin_name__ 失败...，插件控制未加载."
                        )
                else:
                    try:
                        _tmp_module[matcher.module] = plugin_name
                        plugin_settings = _module.__getattribute__(
                            "__plugin_settings__"
                        )
                        if (
                            plugin_settings["cmd"]
                            and plugin_name not in plugin_settings["cmd"]
                        ):
                            plugin_settings["cmd"].append(plugin_name)
                        if plugins2settings_manager.get(
                            matcher.module
                        ) and plugins2settings_manager[matcher.module].get(
                            "plugin_type"
                        ):
                            plugin_type = tuple(
                                plugins2settings_manager.get_plugin_data(
                                    matcher.module
                                )["plugin_type"]
                            )
                        else:
                            try:
                                plugin_type = _module.__getattribute__(
                                    "__plugin_type__"
                                )
                            except AttributeError:
                                plugin_type = ("normal",)
                        if plugin_settings and matcher.module:
                            plugins2settings_manager.add_plugin_settings(
                                matcher.module,
                                plugin_type=plugin_type,
                                data_dict=plugin_settings,
                            )
                    except AttributeError:
                        pass
        _tmp.append(matcher.module)
    _tmp_data = {"PluginSettings": plugins2settings_manager.get_data()}
    with open(plugins2settings_file, "w", encoding="utf8") as wf:
        yaml.dump(_tmp_data, wf, Dumper=yaml.RoundTripDumper, allow_unicode=True)
    _data = round_trip_load(open(plugins2settings_file, encoding="utf8"))
    _data["PluginSettings"].yaml_set_start_comment(
        """# 模块与对应命令和对应群权限
# 用于生成帮助图片 和 开关功能
# key：模块名称
# level：需要的群等级
# default_status：加入群时功能的默认开关状态
# limit_superuser: 功能状态是否限制超级用户
# cmd: 关闭[cmd] 都会触发命令 关闭对应功能，cmd列表第一个词为统计的功能名称
# plugin_type: 帮助类别 示例：('原神相关',) 或 ('原神相关', 1)，1代表帮助命令列向排列，否则为横向排列""",
        indent=2,
    )
    for plugin in _data["PluginSettings"].keys():
        _data["PluginSettings"][plugin].yaml_set_start_comment(
            f"{plugin}：{_tmp_module[plugin]}", indent=2
        )
    with open(plugins2settings_file, "w", encoding="utf8") as wf:
        round_trip_dump(_data, wf, Dumper=yaml.RoundTripDumper, allow_unicode=True)
    logger.info(f"已成功加载 {len(plugins2settings_manager.get_data())} 个非限制插件.")
