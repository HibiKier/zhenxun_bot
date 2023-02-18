import asyncio
import os
import time

from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me

from configs.path_config import TEMP_PATH
from services.log import logger
from utils.manager import resources_manager
from utils.utils import scheduler

__zx_plugin_name__ = "清理临时数据 [Superuser]"
__plugin_usage__ = """
usage：
    清理临时数据
    指令：
        清理临时数据
""".strip()
__plugin_des__ = "清理临时数据"
__plugin_cmd__ = [
    "清理临时数据",
]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


clear_data = on_command(
    "清理临时数据", rule=to_me(), permission=SUPERUSER, priority=1, block=True
)


resources_manager.add_temp_dir(TEMP_PATH)


@clear_data.handle()
async def _():
    await clear_data.send("开始清理临时数据....")
    size = await asyncio.get_event_loop().run_in_executor(None, _clear_data)
    await clear_data.send("共清理了 {:.2f}MB 的数据...".format(size / 1024 / 1024))
    logger.info("清理临时数据完成，" + "共清理了 {:.2f}MB 的数据...".format(size / 1024 / 1024))


def _clear_data() -> float:
    logger.debug("开始清理临时文件...")
    size = 0
    dir_list = [dir_ for dir_ in resources_manager.get_temp_data_dir() if dir_.exists()]
    for dir_ in dir_list:
        logger.debug(f"尝试清理文件夹: {dir_.absolute()}", "清理临时数据")
        dir_size = 0
        for file in os.listdir(dir_):
            file = dir_ / file
            if file.is_file():
                try:
                    if time.time() - os.path.getatime(file) > 10:
                        file_size = os.path.getsize(file)
                        file.unlink()
                        size += file_size
                        dir_size += file_size
                        logger.debug(f"移除临时文件: {file.absolute()}", "清理临时数据")
                except Exception as e:
                    logger.error(f"清理临时数据错误，临时文件夹: {dir_.absolute()}...", "清理临时数据", e=e)
        logger.debug("清理临时文件夹大小: {:.2f}MB".format(size / 1024 / 1024), "清理临时数据")
    return float(size)


@scheduler.scheduled_job(
    "cron",
    hour=1,
    minute=1,
)
async def _():
    size = await asyncio.get_event_loop().run_in_executor(None, _clear_data)
    logger.info("自动清理临时数据完成，" + "共清理了 {:.2f}MB 的数据...".format(size / 1024 / 1024))
