import os
import time

from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.utils import run_sync
from nonebot_plugin_alconna import Alconna, on_alconna
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_saa import Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.path_config import TEMP_PATH
from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.utils import ResourceDirManager

__plugin_meta__ = PluginMetadata(
    name="清理数据",
    description="清理已添加的临时文件夹中的数据",
    usage="""
    清理临时数据
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).dict(),
)


_matcher = on_alconna(
    Alconna("清理临时数据"),
    rule=to_me(),
    permission=SUPERUSER,
    priority=5,
    block=True,
)


ResourceDirManager.add_temp_dir(TEMP_PATH, True)


@_matcher.handle()
async def _(session: EventSession):
    await Text("开始清理临时数据...").send()
    size = await _clear_data()
    await Text("共清理了 {:.2f}MB 的数据...".format(size / 1024 / 1024)).send()
    logger.info(
        "清理临时数据完成，共清理了 {:.2f}MB 的数据...".format(size / 1024 / 1024), session=session
    )


@run_sync
def _clear_data() -> float:
    logger.debug("开始清理临时文件...")
    size = 0
    dir_list = [dir_ for dir_ in ResourceDirManager.temp_path if dir_.exists()]
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
    size = await _clear_data()
    logger.info("自动清理临时数据完成，共清理了 {:.2f}MB 的数据...".format(size / 1024 / 1024), "定时任务")
