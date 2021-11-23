from pathlib import Path
from utils.manager import group_manager
from services.db_context import db
from asyncpg.exceptions import DuplicateColumnError
from services.log import logger

try:
    import ujson as json
except ModuleNotFoundError:
    import json
try:
    from models.group_remind import GroupRemind
except ModuleNotFoundError:
    pass


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
