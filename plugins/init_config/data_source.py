from pathlib import Path
from ruamel.yaml import YAML, round_trip_load, round_trip_dump
from utils.manager import (
    plugins2settings_manager,
    plugins2cd_manager,
    plugins2block_manager,
    group_manager,
    admin_manager
)
from services.db_context import db
from asyncpg.exceptions import DuplicateColumnError
from services.log import logger
from utils.utils import get_matchers
import nonebot

try:
    import ujson as json
except ModuleNotFoundError:
    import json
try:
    from models.group_remind import GroupRemind
except ModuleNotFoundError:
    pass

yaml = YAML(typ="safe")


def init_plugins_settings(data_path: str):
    """
    初始化插件设置，从插件中获取 __zx_plugin_name__，__plugin_cmd__，__plugin_settings__
    """
    plugins2config_file = Path(data_path) / "configs" / "plugins2settings.yaml"
    plugins2config_file.parent.mkdir(exist_ok=True, parents=True)
    _matchers = get_matchers()
    _data = {}
    if plugins2config_file.exists():
        with open(plugins2config_file, "r", encoding="utf8") as f:
            _data = yaml.load(f)
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
            if _data[matcher.module]['cmd']:
                _tmp_module[matcher.module] = _data[matcher.module]['cmd'][0]
        else:
            _plugin = nonebot.plugin.get_plugin(matcher.module)
            _module = _plugin.module
            try:
                plugin_name = _module.__getattribute__("__zx_plugin_name__")
                if "[admin]" in plugin_name.lower():
                    try:
                        level = (_module.__getattribute__("__plugin_settings__"))['admin_level']
                    except (AttributeError, KeyError):
                        level = 5
                    admin_manager.add_admin_command(matcher.module, level)
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
                    plugin_settings = _module.__getattribute__("__plugin_settings__")
                    if plugin_settings['cmd'] and plugin_name not in plugin_settings['cmd']:
                        plugin_settings['cmd'].append(plugin_name)
                    if plugins2settings_manager.get(
                        matcher.module
                    ) and plugins2settings_manager[matcher.module].get("plugin_type"):
                        plugin_type = tuple(
                            plugins2settings_manager.get_plugin_data(matcher.module)[
                                "plugin_type"
                            ]
                        )
                    else:
                        try:
                            plugin_type = _module.__getattribute__("__plugin_type__")
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
    with open(plugins2config_file, "w", encoding="utf8") as wf:
        yaml.dump(_tmp_data, wf)
    _data = round_trip_load(open(plugins2config_file, encoding="utf8"))
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
    with open(plugins2config_file, "w", encoding="utf8") as wf:
        round_trip_dump(_data, wf)
    logger.info(f"已成功加载 {len(plugins2settings_manager.get_data())} 个非限制插件.")


def init_plugins_cd_limit(data_path):
    """
    加载 cd 限制
    """
    plugins2cd_file = Path(data_path) / "configs" / "plugins2cd.yaml"
    plugins2cd_file.parent.mkdir(exist_ok=True, parents=True)
    _data = {}
    _matchers = get_matchers()
    for matcher in _matchers:
        if not plugins2cd_manager.get_plugin_cd_data(matcher.module):
            _plugin = nonebot.plugin.get_plugin(matcher.module)
            _module = _plugin.module
            try:
                plugin_cd_limit = _module.__getattribute__("__plugin_cd_limit__")
                plugins2cd_manager.add_cd_limit(
                    matcher.module, data_dict=plugin_cd_limit
                )
            except AttributeError:
                pass
    if plugins2cd_file.exists():
        with open(plugins2cd_file, "r", encoding="utf8") as f:
            _data = yaml.load(f)
            _data = _data if _data else {}
    if _data.get("PluginCdLimit"):
        for plugin in _data["PluginCdLimit"].keys():
            plugins2cd_manager.add_cd_limit(
                plugin, data_dict=_data["PluginCdLimit"][plugin]
            )
    _tmp_data = {"PluginCdLimit": plugins2cd_manager.get_data()}
    with open(plugins2cd_file, "w", encoding="utf8") as wf:
        yaml.dump(_tmp_data, wf)
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
        round_trip_dump(_data, wf)
    plugins2cd_manager.reload_cd_limit()


def init_plugins_block_limit(data_path):
    """
    加载阻塞限制
    """
    plugins2block_file = Path(data_path) / "configs" / "plugins2block.yaml"
    plugins2block_file.parent.mkdir(exist_ok=True, parents=True)
    _data = {}
    _matchers = get_matchers()
    for matcher in _matchers:
        if not plugins2block_manager.get_plugin_block_data(matcher.module):
            _plugin = nonebot.plugin.get_plugin(matcher.module)
            _module = _plugin.module
            try:
                plugin_block_limit = _module.__getattribute__("__plugin_block_limit__")
                plugins2block_manager.add_block_limit(
                    matcher.module, data_dict=plugin_block_limit
                )
            except AttributeError:
                pass
    if plugins2block_file.exists():
        with open(plugins2block_file, "r", encoding="utf8") as f:
            _data = yaml.load(f)
            _data = _data if _data else {}
    if _data.get("PluginBlockLimit"):
        for plugin in _data["PluginBlockLimit"].keys():
            plugins2block_manager.add_block_limit(
                plugin, data_dict=_data["PluginBlockLimit"][plugin]
            )
    _tmp_data = {"PluginBlockLimit": plugins2block_manager.get_data()}
    with open(plugins2block_file, "w", encoding="utf8") as wf:
        yaml.dump(_tmp_data, wf)
    _data = round_trip_load(open(plugins2block_file, encoding="utf8"))
    _data["PluginBlockLimit"].yaml_set_start_comment(
        """# 用户调用阻塞
# 即 当用户调用此功能还未结束时
# 用发送消息阻止用户重复调用此命令直到该命令结束
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
    with open(plugins2block_file, "w", encoding="utf8") as wf:
        round_trip_dump(_data, wf)
    plugins2block_manager.reload_block_limit()


async def init_group_manager():
    """
    旧数据格式替换为新格式
    初始化数据
    """
    old_group_level_file = Path() / "data" / "manager" / "group_level.json"
    old_plugin_list_file = Path() / "data" / "manager" / "plugin_list.json"
    if old_group_level_file.exists():
        data = json.load(open(old_group_level_file, "r", encoding="utf8"))
        for key in data.keys():
            group = key
            level = data[key]
            group_manager.set_group_level(group, level)
        old_group_level_file.unlink()
        group_manager.save()

    if old_plugin_list_file.exists():
        data = json.load(open(old_plugin_list_file, "r", encoding="utf8"))
        for plugin in data.keys():
            for group in data[plugin].keys():
                if group == "default" and not data[plugin]["default"]:
                    group_manager.block_plugin(plugin)
                elif not data[plugin][group]:
                    group_manager.block_plugin(plugin, group)
        old_plugin_list_file.unlink()
    old_data_table = Path() / "models" / "group_remind.py"
    try:
        if old_data_table.exists():
            b = {
                "hy": "group_welcome",
                "kxcz": "open_case_reset_remind",
                "zwa": "zwa",
                "blpar": "bilibili_parse",
                "epic": "epic_free_game",
                "pa": "pa",
                "almanac": "genshin_alc",
            }
            for group in group_manager.get_data()["group_manager"]:
                for remind in b:
                    try:
                        status = await GroupRemind.get_status(int(group), remind)
                        if status is not None:
                            if status:
                                await group_manager.open_group_task(group, b[remind])
                                logger.info(f"读取旧数据-->{group} 开启 {b[remind]}")
                            else:
                                await group_manager.close_group_task(group, b[remind])
                                logger.info(f"读取旧数据-->{group} 关闭 {b[remind]}")
                    except Exception as e:
                        pass
            query = db.text("DROP TABLE group_reminds;")
            await db.first(query)
            old_data_table.unlink()
            logger.info("旧数据读取完毕，删除了舍弃表 group_reminds...")
    except (ModuleNotFoundError, DuplicateColumnError):
        pass
    group_manager.save()
