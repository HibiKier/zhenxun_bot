from utils.manager import plugins2settings_manager, admin_manager
from services.log import logger
from utils.utils import get_matchers
import nonebot


def init_plugins_settings():
    """
    初始化插件设置，从插件中获取 __zx_plugin_name__，__plugin_cmd__，__plugin_settings__
    """
    _tmp_module = {}
    for x in plugins2settings_manager.keys():
        try:
            _plugin = nonebot.plugin.get_plugin(x)
            _module = _plugin.module
            metadata = _plugin.metadata
            plugin_name = (
                metadata.name
                if metadata
                else _module.__getattribute__("__zx_plugin_name__")
            )
            _tmp_module[x] = plugin_name
        except (KeyError, AttributeError) as e:
            logger.warning(f"配置文件 模块：{x} 获取 plugin_name 失败...{e}")
            _tmp_module[x] = ""
    for matcher in [x for x in get_matchers(True) if x.plugin]:
        try:
            if matcher.plugin_name not in plugins2settings_manager.keys():
                _plugin = matcher.plugin
                metadata = _plugin.metadata
                try:
                    _module = _plugin.module
                except AttributeError:
                    logger.warning(f"插件 {matcher.plugin_name} 加载失败...，插件控制未加载.")
                else:
                    try:
                        plugin_name = metadata.name if metadata else _module.__getattribute__("__zx_plugin_name__")
                        # 管理员命令
                        if "[admin]" in plugin_name.lower():
                            level = 5
                            cmd = None
                            if hasattr(_module, "__plugin_settings__"):
                                admin_settings = _module.__getattribute__(
                                    "__plugin_settings__"
                                )
                                level = admin_settings.get("admin_level", 5)
                                cmd = admin_settings.get("cmd")
                            admin_manager.add_admin_plugin_settings(
                                matcher.plugin_name, cmd, level
                            )
                        if (
                            "[hidden]" in plugin_name.lower()
                            or "[admin]" in plugin_name.lower()
                            or "[superuser]" in plugin_name.lower()
                            or matcher.plugin_name in plugins2settings_manager.keys()
                        ):
                            continue
                    except AttributeError:
                        logger.warning(
                            f"获取插件 {matcher.plugin_name} __zx_plugin_name__ 失败...，插件控制未加载."
                        )
                    else:
                        _tmp_module[matcher.plugin_name] = plugin_name
                        if hasattr(_module, "__plugin_settings__"):
                            plugin_settings = _module.__getattribute__(
                                "__plugin_settings__"
                            )
                        else:
                            plugin_settings = {"cmd": [matcher.plugin_name, plugin_name]}
                        if plugin_settings.get("cost_gold") is None:
                            plugin_settings["cost_gold"] = 0
                        if (
                            plugin_settings.get("cmd") is not None
                            and plugin_name not in plugin_settings["cmd"]
                        ):
                            plugin_settings["cmd"].append(plugin_name)
                        if plugins2settings_manager.get(
                            matcher.plugin_name
                        ) and plugins2settings_manager[matcher.plugin_name].get(
                            "plugin_type"
                        ):
                            plugin_type = tuple(
                                plugins2settings_manager.get_plugin_data(
                                    matcher.plugin_name
                                ).plugin_type
                            )
                        else:
                            if hasattr(_module, "__plugin_type__"):
                                plugin_type = _module.__getattribute__("__plugin_type__")
                            else:
                                plugin_type = ("normal",)
                        if plugin_settings and matcher.plugin_name:
                            plugins2settings_manager.add_plugin_settings(
                                matcher.plugin_name,
                                plugin_type=plugin_type,
                                **plugin_settings,
                            )
        except Exception as e:
            logger.error(f'{matcher.plugin_name} 初始化 plugin_settings 发生错误 {type(e)}：{e}')
    plugins2settings_manager.save()
    logger.info(f"已成功加载 {len(plugins2settings_manager.get_data())} 个非限制插件.")
