import asyncio
import time
from datetime import datetime, timedelta
from typing import List, Optional

import nonebot
from fastapi import APIRouter, WebSocket
from nonebot.utils import escape_tag
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState

from configs.config import NICKNAME
from models.chat_history import ChatHistory
from services.log import logger
from utils.manager import plugin_data_manager, plugins2settings_manager, plugins_manager
from utils.manager.models import PluginData, PluginType

from ....config import QueryDateType
from ....base_model import Result
from ....utils import authentication, get_system_status
from .data_source import bot_live
from .model import BaseInfo

AVA_URL = "http://q1.qlogo.cn/g?b=qq&nk={}&s=160"

run_time = time.time()

ws_router = APIRouter()
router = APIRouter()


@router.get("/get_base_info", dependencies=[authentication()], description="基础信息")
async def _(bot_id: Optional[str] = None) -> Result:
    """
    获取Bot基础信息

    Args:
        qq (Optional[str], optional): qq号. Defaults to None.

    Returns:
        Result: 获取指定bot信息与bot列表
    """
    bot_list: List[BaseInfo] = []
    if bots := nonebot.get_bots():
        select_bot: BaseInfo
        for key, bot in bots.items():
            bot_list.append(
                BaseInfo(
                    bot=bot,  # type: ignore
                    self_id=bot.self_id,
                    nickname=NICKNAME,
                    ava_url=AVA_URL.format(bot.self_id),
                )
            )
        # 获取指定qq号的bot信息，若无指定则获取第一个
        if _bl := [b for b in bot_list if b.self_id == bot_id]:
            select_bot = _bl[0]
        else:
            select_bot = bot_list[0]
        select_bot.is_select = True
        now = datetime.now()
        # 今日累计接收消息
        select_bot.received_messages = await ChatHistory.filter(
            bot_id=select_bot.self_id,
            create_time__gte=now - timedelta(hours=now.hour),
        ).count()
        # 群聊数量
        select_bot.group_count = len(await select_bot.bot.get_group_list())
        # 好友数量
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
        # 连接时间
        select_bot.connect_time = bot_live.get(select_bot.self_id) or 0

        return Result.ok(bot_list, "已获取操作列表")
    return Result.warning_("无Bot连接...")


@router.get("/get_ch_count", dependencies=[authentication()], description="获取接收消息数量")
async def _(bot_id: str, query_type: Optional[QueryDateType] = None) -> Result:
    if bots := nonebot.get_bots():
        if not query_type:
            return Result.ok(await ChatHistory.filter(bot_id=bot_id).count())
        now = datetime.now()
        if query_type == QueryDateType.DAY:
            return Result.ok(
                await ChatHistory.filter(
                    bot_id=bot_id, create_time__gte=now - timedelta(hours=now.hour)
                ).count()
            )
        if query_type == QueryDateType.WEEK:
            return Result.ok(
                await ChatHistory.filter(
                    bot_id=bot_id, create_time__gte=now - timedelta(days=7)
                ).count()
            )
        if query_type == QueryDateType.MONTH:
            return Result.ok(
                await ChatHistory.filter(
                    bot_id=bot_id, create_time__gte=now - timedelta(days=30)
                ).count()
            )
        if query_type == QueryDateType.YEAR:
            return Result.ok(
                await ChatHistory.filter(
                    bot_id=bot_id, create_time__gte=now - timedelta(days=365)
                ).count()
            )
    return Result.warning_("无Bot连接...")


@router.get("get_fg_count", dependencies=[authentication()], description="好友/群组数量")
async def _(bot_id: str) -> Result:
    if bots := nonebot.get_bots():
        if bot_id not in bots:
            return Result.warning_("指定Bot未连接...")
        bot = bots[bot_id]
        data = {
            "friend_count": len(await bot.get_friend_list()),
            "group_count": len(await bot.get_group_list()),
        }
        return Result.ok(data)
    return Result.warning_("无Bot连接...")


@router.get("/get_run_time", dependencies=[authentication()], description="获取nb运行时间")
async def _() -> Result:
    return Result.ok(int(time.time() - run_time))


@ws_router.websocket("/system_status")
async def system_logs_realtime(websocket: WebSocket):
    await websocket.accept()
    logger.debug("ws system_status is connect")
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            system_status = await get_system_status()
            await websocket.send_text(system_status.json())
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass
    return
