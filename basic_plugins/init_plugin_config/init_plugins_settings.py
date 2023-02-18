from utils.manager import plugins2settings_manager, admin_manager, plugin_data_manager
from services.log import logger
from utils.manager.models import PluginType
from utils.utils import get_matchers
import nonebot


def init_plugins_settings():
    """
    初始化插件设置，从插件中获取 __zx_plugin_name__，__plugin_cmd__，__plugin_settings__
    """
    # for x in plugins2settings_manager.keys():
    #     try:
    #         _plugin = nonebot.plugin.get_plugin(x)
    #         _module = _plugin.module
    #         _module.__getattribute__("__zx_plugin_name__")
    #     except (KeyError, AttributeError) as e:
    #         logger.warning(f"配置文件 模块：{x} 获取 plugin_name 失败...{e}")
    for matcher in get_matchers(True):
        try:
            if matcher.plugin_name not in plugins2settings_manager.keys():
                _plugin = matcher.plugin
                try:
                    _module = _plugin.module
                except AttributeError:
                    logger.warning(f"插件 {matcher.plugin_name} 加载失败...，插件控制未加载.")
                else:
                    if plugin_data := plugin_data_manager.get(matcher.plugin_name):
                        if plugin_settings := plugin_data.plugin_setting:
                            if (name := _module.__getattribute__("__zx_plugin_name__")) not in plugin_settings.cmd:
                                plugin_settings.cmd.append(name)
                            # 管理员命令
                            if plugin_data.plugin_type == PluginType.ADMIN:
                                admin_manager.add_admin_plugin_settings(
                                    matcher.plugin_name, plugin_settings.cmd, plugin_settings.level
                                )
                            else:
                                plugins2settings_manager.add_plugin_settings(
                                    matcher.plugin_name, plugin_settings
                                )
        except Exception as e:
            logger.error(f'{matcher.plugin_name} 初始化 plugin_settings 发生错误 {type(e)}：{e}')
    plugins2settings_manager.save()
    logger.info(f"已成功加载 {len(plugins2settings_manager.get_data())} 个非限制插件.")
