from datetime import datetime, timedelta
from typing import List, Optional

import nonebot
from fastapi import APIRouter

from configs.config import Config
from models.chat_history import ChatHistory
from services.log import logger
from utils.manager import plugin_data_manager, plugins2settings_manager, plugins_manager
from utils.manager.models import PluginData, PluginType

from ..models.model import BotInfo, Result
from ..models.params import UpdateConfig, UpdatePlugin
from ..utils import authentication

AVA_URL = "http://q1.qlogo.cn/g?b=qq&nk={}&s=160"

router = APIRouter()


@router.get("/get_bot_info", dependencies=[authentication()])
async def _(self_id: Optional[str] = None) -> Result:
    """
    获取Bot基础信息

    Args:
        qq (Optional[str], optional): qq号. Defaults to None.

    Returns:
        Result: 获取指定bot信息与bot列表
    """
    bot_list: List[BotInfo] = []
    if bots := nonebot.get_bots():
        select_bot: BotInfo
        for key, bot in bots.items():
            bot_list.append(
                BotInfo(
                    bot=bot,  # type: ignore
                    self_id=bot.self_id,
                    nickname="可爱的小真寻",
                    ava_url=AVA_URL.format(bot.self_id),
                )
            )
        if _bl := [b for b in bot_list if b.self_id == self_id]:
            select_bot = _bl[0]
        else:
            select_bot = bot_list[0]
        select_bot.is_select = True
        now = datetime.now()
        select_bot.received_messages = await ChatHistory.filter(
            bot_id=int(select_bot.self_id)
        ).count()
        select_bot.received_messages_day = await ChatHistory.filter(
            bot_id=int(select_bot.self_id),
            create_time__gte=now - timedelta(hours=now.hour),
        ).count()
        select_bot.received_messages_week = await ChatHistory.filter(
            bot_id=int(select_bot.self_id),
            create_time__gte=now - timedelta(days=7),
        ).count()
        select_bot.group_count = len(await select_bot.bot.get_group_list())
        select_bot.friend_count = len(await select_bot.bot.get_friend_list())
        for bot in bot_list:
            bot.bot = None  # type: ignore
        # 插件加载数量
        select_bot.plugin_count = len(plugins2settings_manager)
        pm_data = plugins_manager.get_data()
        select_bot.fail_plugin_count = len([pd for pd in pm_data if pm_data[pd].error])
        select_bot.success_plugin_count = (
            select_bot.plugin_count - select_bot.fail_plugin_count
        )

        return Result.ok(bot_list, "已获取操作列表")
    return Result.fail("无Bot连接")
