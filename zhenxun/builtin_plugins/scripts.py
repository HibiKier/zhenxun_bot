from asyncio.exceptions import TimeoutError

import aiofiles
import nonebot
from nonebot.drivers import Driver
from nonebot_plugin_apscheduler import scheduler
import ujson as json

from zhenxun.configs.path_config import TEXT_PATH
from zhenxun.models.group_console import GroupConsole
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx

driver: Driver = nonebot.get_driver()


@driver.on_startup
async def update_city():
    """
    部分插件需要中国省份城市
    这里直接更新，避免插件内代码重复
    """
    china_city = TEXT_PATH / "china_city.json"
    if not china_city.exists():
        data = {}
        try:
            logger.debug("开始更新城市列表...")
            res = await AsyncHttpx.get(
                "http://www.weather.com.cn/data/city3jdata/china.html", timeout=5
            )
            res.encoding = "utf8"
            provinces_data = json.loads(res.text)
            for province in provinces_data.keys():
                data[provinces_data[province]] = []
                res = await AsyncHttpx.get(
                    f"http://www.weather.com.cn/data/city3jdata/provshi/{province}.html",
                    timeout=5,
                )
                res.encoding = "utf8"
                city_data = json.loads(res.text)
                for city in city_data.keys():
                    data[provinces_data[province]].append(city_data[city])
            async with aiofiles.open(china_city, "w", encoding="utf8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info("自动更新城市列表完成.....")
        except TimeoutError as e:
            logger.warning("自动更新城市列表超时...", e=e)
        except ValueError as e:
            logger.warning("自动城市列表失败.....", e=e)
        except Exception as e:
            logger.error("自动城市列表未知错误", e=e)


# 自动更新城市列表
@scheduler.scheduled_job(
    "cron",
    hour=6,
    minute=1,
)
async def _():
    await update_city()


@driver.on_startup
async def _():
    """开启/禁用插件格式修改"""
    _, is_create = await GroupConsole.get_or_create(group_id=133133133)
    """标记"""
    if is_create:
        data_list = []
        for group in await GroupConsole.all():
            if group.block_plugin:
                if modules := group.block_plugin.split(","):
                    block_plugin = "".join(
                        (f"{module}," if module.startswith("<") else f"<{module},")
                        for module in modules
                        if module.strip()
                    )
                    group.block_plugin = block_plugin.replace("<,", "")
            if group.block_task:
                if modules := group.block_task.split(","):
                    block_task = "".join(
                        (f"{module}," if module.startswith("<") else f"<{module},")
                        for module in modules
                        if module.strip()
                    )
                    group.block_task = block_task.replace("<,", "")
            data_list.append(group)
        await GroupConsole.bulk_update(data_list, ["block_plugin", "block_task"], 10)
