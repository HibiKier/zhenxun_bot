from asyncpg.exceptions import (
    DuplicateColumnError,
    UndefinedColumnError,
    PostgresSyntaxError,
)
from nonebot import Driver
from services.db_context import db
from models.group_info import GroupInfo
from models.bag_user import BagUser
from nonebot.adapters.onebot.v11 import Bot
from services.log import logger
from configs.path_config import TEXT_PATH
from asyncio.exceptions import TimeoutError
from typing import List
from utils.http_utils import AsyncHttpx
from utils.utils import scheduler
import nonebot

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
        except TimeoutError:
            logger.warning("自动更新城市列表超时.....")
        except ValueError:
            logger.warning("自动城市列表失败.....")
        except Exception as e:
            logger.error(f"自动城市列表未知错误 {type(e)}：{e}")


@driver.on_startup
async def _():
    """
    数据库表结构变换
    """
    _flag = []
    sql_str = [
        (
            "ALTER TABLE group_info ADD group_flag Integer NOT NULL DEFAULT 0;",
            "group_info",
        ),  # group_info表添加一个group_flag
        (
            "ALTER TABLE bag_users rename belonging_group To group_id;",
            "bag_users",
        ),  # 将 bag_users 的 belonging_group 改为 group_id
        (
            "ALTER TABLE group_info_users rename belonging_group To group_id;",
            "group_info_users",
        ),
        (
            "ALTER TABLE sign_group_users rename belonging_group To group_id;",
            "sign_group_users",
        ),
        (
            "ALTER TABLE open_cases_users rename belonging_group To group_id;",
            "open_cases_users",
        ),
        (
            "ALTER TABLE bag_users ADD property json NOT NULL DEFAULT '{}';",
            "bag_users",
        ),  # bag_users 新增字段 property 替代 props
        (
            "ALTER TABLE genshin ADD auto_sign_time timestamp with time zone;",
            "genshin"
        ),  # 新增原神自动签到字段
        (
            "ALTER TABLE genshin ADD resin_remind boolean DEFAULT False;",
            "genshin"
        ),  # 新增原神自动签到字段
        (
            "ALTER TABLE genshin ADD resin_recovery_time timestamp with time zone;",
            "genshin"
        ),  # 新增原神自动签到字段
        (
            "ALTER TABLE genshin ADD bind_group Integer;",
            "genshin"
        ),  # 新增原神群号绑定字段
    ]
    for sql in sql_str:
        try:
            flag = sql[1]
            sql = sql[0]
            query = db.text(sql)
            await db.first(query)
            logger.info(f"完成sql操作：{sql}")
            _flag.append(flag)
        except (DuplicateColumnError, UndefinedColumnError):
            pass
        except PostgresSyntaxError:
            logger.error(f"语法错误：执行sql失败：{sql}")
    # bag_user 将文本转为字典格式
    await __database_script(_flag)

    # 完成后
    end_sql_str = [
        # "ALTER TABLE bag_users DROP COLUMN props;"          # 删除 bag_users 的 props 字段（还不到时候）
    ]
    for sql in end_sql_str:
        try:
            query = db.text(sql)
            await db.first(query)
            logger.info(f"完成执行sql操作：{sql}")
        except (DuplicateColumnError, UndefinedColumnError):
            pass
        except PostgresSyntaxError:
            logger.error(f"语法错误：执行sql失败：{sql}")

    # str2json_sql = ["alter table bag_users alter COLUMN props type json USING props::json;"]       # 字段类型替换
    # rename_sql = 'alter table {} rename {} to {};'                              # 字段更名
    # for sql in str2json_sql:
    #     try:
    #         query = db.text(sql)
    #         await db.first(query)
    #     except DuplicateColumnError:
    #         pass


@driver.on_bot_connect
async def _(bot: Bot):
    """
    版本某些需要的变换
    """
    # 清空不存在的群聊信息，并将已所有已存在的群聊group_flag设置为1（认证所有已存在的群）
    if not await GroupInfo.get_group_info(114514):
        # 标识符，该功能只需执行一次
        await GroupInfo.add_group_info(114514, "114514", 114514, 114514, 1)
        group_list = await bot.get_group_list()
        group_list = [g["group_id"] for g in group_list]
        _gl = [x.group_id for x in await GroupInfo.get_all_group()]
        if 114514 in _gl:
            _gl.remove(114514)
        for group_id in _gl:
            if group_id in group_list:
                if await GroupInfo.get_group_info(group_id):
                    await GroupInfo.set_group_flag(group_id, 1)
                else:
                    group_info = await bot.get_group_info(group_id=group_id)
                    await GroupInfo.add_group_info(
                        group_info["group_id"],
                        group_info["group_name"],
                        group_info["max_member_count"],
                        group_info["member_count"],
                        1,
                    )
                logger.info(f"已将群聊 {group_id} 添加认证...")
            else:
                await GroupInfo.delete_group_info(group_id)
                logger.info(f"移除不存在的群聊信息：{group_id}")


async def __database_script(_flag: List[str]):
    # bag_user 将文本转为字典格式
    if "bag_users" in _flag:
        for x in await BagUser.get_all_users():
            props = {}
            if x.props:
                for prop in [p for p in x.props.split(",") if p]:
                    if props.get(prop):
                        props[prop] += 1
                    else:
                        props[prop] = 1
                logger.info(
                    f"__database_script USER {x.user_qq} GROUP {x.group_id} 更新数据 {props}"
                )
            await x.update(
                property=props,
                props="",
            ).apply()


# 自动更新城市列表
@scheduler.scheduled_job(
    "cron",
    hour=6,
    minute=1,
)
async def _():
    await update_city()
