from pathlib import Path
from ruamel.yaml import round_trip_load, round_trip_dump, YAML
from utils.manager import admin_manager, plugins_manager, plugin_data_manager
from configs.config import Config
from services.log import logger
from utils.text_utils import prompt2cn
from utils.utils import get_matchers
from configs.path_config import DATA_PATH
from ruamel import yaml


_yaml = YAML(typ="safe")


def init_plugins_config():
    """
    初始化插件数据配置
    """
    plugins2config_file = DATA_PATH / "configs" / "plugins2config.yaml"
    _data = Config.get_data()
    # 优先使用 metadata 数据
    for matcher in get_matchers(True):
        if plugin_data := plugin_data_manager.get(matcher.plugin_name):
            # 插件配置版本更新或为Version为None或不在存储配置内，当使用metadata时，必定更新
            if plugin_data.plugin_configs and (
                isinstance(plugin_data.plugin_status.version, str)
                or (
                    plugin_data.plugin_status.version is None
                    or (
                        _data.get(matcher.plugin_name)
                        and _data[matcher.plugin_name].keys()
                        != plugin_data.plugin_configs.keys()
                    )
                    or plugin_data.plugin_status.version
                    > plugins_manager.get(matcher.plugin_name).version
                    or matcher.plugin_name not in _data.keys()
                )
            ):
                plugin_configs = plugin_data.plugin_configs
                for key in plugin_configs:
                    if isinstance(plugin_data.plugin_configs[key], dict):
                        Config.add_plugin_config(
                            matcher.plugin_name,
                            key,
                            plugin_configs[key].get("value"),
                            help_=plugin_configs[key].get("help"),
                            default_value=plugin_configs[key].get("default_value"),
                            _override=True,
                        )
                    else:
                        Config.add_plugin_config(
                            matcher.plugin_name, key, plugin_configs[key]
                        )
            elif plugin_configs := _data.get(matcher.plugin_name):
                for key in plugin_configs:
                    Config.add_plugin_config(
                        matcher.plugin_name,
                        key,
                        plugin_configs[key]["value"],
                        help_=plugin_configs[key]["help"],
                        default_value=plugin_configs[key]["default_value"],
                        _override=True,
                    )
    if not Config.is_empty():
        Config.save()
        _data = round_trip_load(open(plugins2config_file, encoding="utf8"))
        for plugin in _data.keys():
            try:
                plugin_name = plugins_manager.get(plugin).plugin_name
            except (AttributeError, TypeError):
                plugin_name = plugin
            _data[plugin].yaml_set_start_comment(plugin_name, indent=2)
        # 初始化未设置的管理员权限等级
        for k, v in Config.get_admin_level_data():
            admin_manager.set_admin_level(k, v)
        # 存完插件基本设置
        with open(plugins2config_file, "w", encoding="utf8") as wf:
            round_trip_dump(
                _data, wf, indent=2, Dumper=yaml.RoundTripDumper, allow_unicode=True
            )
    _replace_config()


def _replace_config():
    """
    说明:
        定时任务加载的配置读取替换
    """
    # 再开始读取用户配置
    user_config_file = Path() / "configs" / "config.yaml"
    _data = {}
    _tmp_data = {}
    if user_config_file.exists():
        with open(user_config_file, "r", encoding="utf8") as f:
            _data = _yaml.load(f)
    # 数据替换
    for plugin in Config.keys():
        _tmp_data[plugin] = {}
        for k in Config[plugin].keys():
            try:
                if _data.get(plugin) and k in _data[plugin].keys():
                    Config.set_config(plugin, k, _data[plugin][k])
                    if level2module := Config.get_level2module(plugin, k):
                        try:
                            admin_manager.set_admin_level(
                                level2module, _data[plugin][k]
                            )
                        except KeyError:
                            logger.warning(
                                f"{level2module} 设置权限等级失败：{_data[plugin][k]}"
                            )
                _tmp_data[plugin][k] = Config.get_config(plugin, k)
            except AttributeError as e:
                raise AttributeError(
                    f"{e}\n" + prompt2cn("可能为config.yaml配置文件填写不规范", 46)
                )
    Config.save()
    temp_file = Path() / "configs" / "temp_config.yaml"
    try:
        with open(temp_file, "w", encoding="utf8") as wf:
            yaml.dump(_tmp_data, wf, Dumper=yaml.RoundTripDumper, allow_unicode=True)
        with open(temp_file, "r", encoding="utf8") as rf:
            _data = round_trip_load(rf)
        # 添加注释
        for plugin in _data.keys():
            rst = ""
            plugin_name = None
            try:
                plugin_data = Config.get(plugin)
                for x in list(Config.get(plugin).keys()):
                    try:
                        _x = plugin_data[x].get("name")
                        if _x:
                            plugin_name = _x
                    except AttributeError:
                        pass
            except (KeyError, AttributeError):
                plugin_name = None
            if not plugin_name:
                try:
                    plugin_name = plugins_manager.get(plugin).plugin_name
                except (AttributeError, TypeError):
                    plugin_name = plugin
            plugin_name = (
                plugin_name.replace("[Hidden]", "")
                .replace("[Superuser]", "")
                .replace("[Admin]", "")
                .strip()
            )
            rst += plugin_name + "\n"
            for k in _data[plugin].keys():
                rst += f'{k}: {Config[plugin][k]["help"]}' + "\n"
            _data[plugin].yaml_set_start_comment(rst[:-1], indent=2)
        with open(Path() / "configs" / "config.yaml", "w", encoding="utf8") as wf:
            round_trip_dump(_data, wf, Dumper=yaml.RoundTripDumper, allow_unicode=True)
    except Exception as e:
        logger.error(f"生成简易配置注释错误 {type(e)}：{e}")
    if temp_file.exists():
        temp_file.unlink()
