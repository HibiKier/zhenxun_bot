import random
from asyncio.exceptions import TimeoutError

import nonebot
from nonebot.adapters.onebot.v11 import Bot
from nonebot.drivers import Driver

from configs.path_config import TEXT_PATH
from models.bag_user import BagUser
from models.group_info import GroupInfo
from services.log import logger
from utils.http_utils import AsyncHttpx
from utils.utils import GDict, scheduler

try:
    import ujson as json
except ModuleNotFoundError:
    import json


driver: Driver = nonebot.get_driver()


@driver.on_startup
async def update_city():
    """
    部分插件需要中国省份城市
    这里直接更新，避免插件内代码重复
    """
    china_city = TEXT_PATH / "china_city.json"
    data = {}
    if not china_city.exists():
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
            with open(china_city, "w", encoding="utf8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info("自动更新城市列表完成.....")
        except TimeoutError as e:
            logger.warning("自动更新城市列表超时...", e=e)
        except ValueError as e:
            logger.warning("自动城市列表失败.....", e=e)
        except Exception as e:
            logger.error(f"自动城市列表未知错误", e=e)


@driver.on_bot_connect
async def _(bot: Bot):
    """
    版本某些需要的变换
    """
    # 清空不存在的群聊信息，并将已所有已存在的群聊group_flag设置为1（认证所有已存在的群）
    if not await GroupInfo.get_or_none(group_id=114514):
        # 标识符，该功能只需执行一次
        await GroupInfo.create(
            group_id=114514,
            group_name="114514",
            max_member_count=114514,
            member_count=114514,
            group_flag=1,
        )
        group_list = await bot.get_group_list()
        group_list = [g["group_id"] for g in group_list]
        _gl = [x.group_id for x in await GroupInfo.all()]
        if 114514 in _gl:
            _gl.remove(114514)
        for group_id in _gl:
            if group_id in group_list:
                if group := await GroupInfo.get_or_none(group_id=group_id):
                    group.group_flag = 1
                    await group.save(update_fields=["group_flag"])
                else:
                    group_info = await bot.get_group_info(group_id=group_id)
                    await GroupInfo.create(
                        group_id=group_info["group_id"],
                        group_name=group_info["group_name"],
                        max_member_count=group_info["max_member_count"],
                        member_count=group_info["member_count"],
                        group_flag=1,
                    )
                logger.info(f"已添加群认证...", group_id=group_id)
            else:
                await GroupInfo.filter(group_id=group_id).delete()
                logger.info(f"移除不存在的群聊信息", group_id=group_id)


# 自动更新城市列表
@scheduler.scheduled_job(
    "cron",
    hour=6,
    minute=1,
)
async def _():
    await update_city()
