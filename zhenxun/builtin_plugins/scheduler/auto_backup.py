from pathlib import Path
import shutil

from nonebot_plugin_apscheduler import scheduler

from zhenxun.configs.config import Config
from zhenxun.services.log import logger

Config.add_plugin_config(
    "_backup",
    "BACKUP_FLAG",
    True,
    help="是否开启文件备份",
    default_value=True,
    type=bool,
)

Config.add_plugin_config(
    "_backup",
    "BACKUP_DIR_OR_FILE",
    ["data"],
    help="备份的文件夹或文件",
    default_value=[],
    type=list[str],
)


# 自动备份
@scheduler.scheduled_job(
    "cron",
    hour=3,
    minute=25,
)
async def _():
    if not Config.get_config("_backup", "BACKUP_FLAG"):
        return
    _backup_path = Path() / "backup"
    _backup_path.mkdir(exist_ok=True, parents=True)
    if backup_dir_or_file := Config.get_config("_backup", "BACKUP_DIR_OR_FILE"):
        for path_file in backup_dir_or_file:
            try:
                path = Path(path_file)
                _p = _backup_path / path_file
                if path.exists():
                    if path.is_dir():
                        if _p.exists():
                            shutil.rmtree(_p, ignore_errors=True)
                        shutil.copytree(path_file, _p)
                    else:
                        if _p.exists():
                            _p.unlink()
                        shutil.copy(path_file, _p)
                    logger.debug(f"已完成自动备份：{path_file}", "自动备份")
            except Exception as e:
                logger.error(f"自动备份文件 {path_file} 发生错误", "自动备份", e=e)
    logger.info("自动备份成功...", "自动备份")
