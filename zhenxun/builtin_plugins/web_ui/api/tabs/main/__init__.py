import asyncio
import contextlib
from datetime import datetime, timedelta
from pathlib import Path
import time

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import nonebot
from nonebot.config import Config
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState
from tortoise.functions import Count
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

from zhenxun.models.bot_connect_log import BotConnectLog
from zhenxun.models.chat_history import ChatHistory
from zhenxun.models.group_console import GroupConsole
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.models.statistics import Statistics
from zhenxun.services.log import logger
from zhenxun.utils.platform import PlatformUtils

from ....base_model import Result
from ....config import AVA_URL, GROUP_AVA_URL, QueryDateType
from ....utils import authentication, get_system_status
from .data_source import bot_live
from .model import (
    ActiveGroup,
    BaseInfo,
    HotPlugin,
    NonebotData,
    QueryCount,
    TemplateBaseInfo,
)

driver = nonebot.get_driver()
run_time = time.time()

ws_router = APIRouter()
router = APIRouter(prefix="/main")


@router.get(
    "/get_base_info",
    dependencies=[authentication()],
    response_model=Result[list[BaseInfo]],
    response_class=JSONResponse,
    description="基础信息",
)
async def _(bot_id: str | None = None) -> Result[list[BaseInfo]]:
    """获取Bot基础信息

    参数:
        bot_id (Optional[str], optional): bot_id. Defaults to None.

    返回:
        Result: 获取指定bot信息与bot列表
    """
    global run_time
    bot_list: list[TemplateBaseInfo] = []
    if bots := nonebot.get_bots():
        select_bot: BaseInfo
        for _, bot in bots.items():
            login_info = await bot.get_login_info()
            bot_list.append(
                TemplateBaseInfo(
                    bot=bot,  # type: ignore
                    self_id=bot.self_id,
                    nickname=login_info["nickname"],
                    ava_url=AVA_URL.format(bot.self_id),
                )
            )
        # 获取指定qq号的bot信息，若无指定   则获取第一个
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
        select_bot.plugin_count = await PluginInfo.all().count()
        fail_count = await PluginInfo.filter(load_status=False).count()
        select_bot.fail_plugin_count = fail_count
        select_bot.success_plugin_count = (
            select_bot.plugin_count - select_bot.fail_plugin_count
        )
        # 连接时间
        select_bot.connect_time = bot_live.get(select_bot.self_id) or 0
        if select_bot.connect_time:
            connect_date = datetime.fromtimestamp(select_bot.connect_time)
            select_bot.connect_date = connect_date.strftime("%Y-%m-%d %H:%M:%S")
        version_file = Path() / "__version__"
        if version_file.exists():
            if text := version_file.open().read():
                if ver := text.replace("__version__: ", "").strip():
                    select_bot.version = ver
        day_call = await Statistics.filter(
            create_time__gte=now - timedelta(hours=now.hour)
        ).count()
        select_bot.day_call = day_call
        select_bot.connect_count = await BotConnectLog.filter(
            bot_id=select_bot.self_id
        ).count()
        return Result.ok([BaseInfo(**e.dict()) for e in bot_list], "拿到信息啦!")
    return Result.warning_("无Bot连接...")


@router.get(
    "/get_all_chat_count",
    dependencies=[authentication()],
    response_model=Result[QueryCount],
    response_class=JSONResponse,
    description="获取接收消息数量",
)
async def _(bot_id: str | None = None) -> Result[QueryCount]:
    now = datetime.now()
    query = ChatHistory
    if bot_id:
        query = query.filter(bot_id=bot_id)
    all_count = await query.annotate().count()
    day_count = await query.filter(
        create_time__gte=now - timedelta(hours=now.hour, minutes=now.minute)
    ).count()
    week_count = await query.filter(
        create_time__gte=now - timedelta(days=7, hours=now.hour, minutes=now.minute)
    ).count()
    month_count = await query.filter(
        create_time__gte=now - timedelta(days=30, hours=now.hour, minutes=now.minute)
    ).count()
    year_count = await query.filter(
        create_time__gte=now - timedelta(days=365, hours=now.hour, minutes=now.minute)
    ).count()
    return Result.ok(
        QueryCount(
            num=all_count,
            day=day_count,
            week=week_count,
            month=month_count,
            year=year_count,
        )
    )


@router.get(
    "/get_all_call_count",
    dependencies=[authentication()],
    response_model=Result[QueryCount],
    response_class=JSONResponse,
    description="获取调用次数",
)
async def _(bot_id: str | None = None) -> Result[QueryCount]:
    now = datetime.now()
    query = Statistics
    if bot_id:
        query = query.filter(bot_id=bot_id)
    all_count = await query.annotate().count()
    day_count = await query.filter(
        create_time__gte=now - timedelta(hours=now.hour, minutes=now.minute)
    ).count()
    week_count = await query.filter(
        create_time__gte=now - timedelta(days=7, hours=now.hour, minutes=now.minute)
    ).count()
    month_count = await query.filter(
        create_time__gte=now - timedelta(days=30, hours=now.hour, minutes=now.minute)
    ).count()
    year_count = await query.filter(
        create_time__gte=now - timedelta(days=365, hours=now.hour, minutes=now.minute)
    ).count()
    return Result.ok(
        QueryCount(
            num=all_count,
            day=day_count,
            week=week_count,
            month=month_count,
            year=year_count,
        )
    )


@router.get(
    "get_fg_count",
    dependencies=[authentication()],
    response_model=Result[dict[str, int]],
    response_class=JSONResponse,
    description="好友/群组数量",
)
async def _(bot_id: str) -> Result[dict[str, int]]:
    if bots := nonebot.get_bots():
        if bot_id not in bots:
            return Result.warning_("指定Bot未连接...")
        bot = bots[bot_id]
        platform = PlatformUtils.get_platform(bot)
        if platform == "qq":
            data = {
                "friend_count": len(await bot.get_friend_list()),
                "group_count": len(await bot.get_group_list()),
            }
            return Result.ok(data)
        return Result.warning_("暂不支持该平台...")
    return Result.warning_("无Bot连接...")


@router.get(
    "/get_nb_data",
    dependencies=[authentication()],
    response_model=Result[NonebotData],
    response_class=JSONResponse,
    description="获取nb数据",
)
async def _() -> Result[NonebotData]:
    return Result.ok(NonebotData(config=driver.config, run_time=int(run_time)))


@router.get(
    "/get_nb_config",
    dependencies=[authentication()],
    response_model=Result[Config],
    response_class=JSONResponse,
    description="获取nb配置",
)
async def _() -> Result[Config]:
    return Result.ok(driver.config)


@router.get(
    "/get_run_time",
    dependencies=[authentication()],
    response_model=Result[int],
    response_class=JSONResponse,
    description="获取nb运行时间",
)
async def _() -> Result[int]:
    return Result.ok(int(run_time))


@router.get(
    "/get_active_group",
    dependencies=[authentication()],
    response_model=Result[list[ActiveGroup]],
    response_class=JSONResponse,
    description="获取活跃群聊",
)
async def _(
    date_type: QueryDateType | None = None, bot_id: str | None = None
) -> Result[list[ActiveGroup]]:
    query = ChatHistory
    now = datetime.now()
    if bot_id:
        query = query.filter(bot_id=bot_id)
    if date_type == QueryDateType.DAY:
        query = query.filter(create_time__gte=now - timedelta(hours=now.hour))
    if date_type == QueryDateType.WEEK:
        query = query.filter(create_time__gte=now - timedelta(days=7))
    if date_type == QueryDateType.MONTH:
        query = query.filter(create_time__gte=now - timedelta(days=30))
    if date_type == QueryDateType.YEAR:
        query = query.filter(create_time__gte=now - timedelta(days=365))
    data_list = (
        await query.annotate(count=Count("id"))
        .filter(group_id__not_isnull=True)
        .group_by("group_id")
        .order_by("-count")
        .limit(5)
        .values_list("group_id", "count")
    )
    id2name = {}
    if data_list:
        if info_list := await GroupConsole.filter(
            group_id__in=[x[0] for x in data_list]
        ).all():
            for group_info in info_list:
                id2name[group_info.group_id] = group_info.group_name
    active_group_list = [
        ActiveGroup(
            group_id=data[0],
            name=id2name.get(data[0]) or data[0],
            chat_num=data[1],
            ava_img=GROUP_AVA_URL.format(data[0], data[0]),
        )
        for data in data_list
    ]
    active_group_list = sorted(
        active_group_list, key=lambda x: x.chat_num, reverse=True
    )
    if len(active_group_list) > 5:
        active_group_list = active_group_list[:5]
    return Result.ok(active_group_list)


@router.get(
    "/get_hot_plugin",
    dependencies=[authentication()],
    response_model=Result[list[HotPlugin]],
    response_class=JSONResponse,
    description="获取热门插件",
)
async def _(
    date_type: QueryDateType | None = None, bot_id: str | None = None
) -> Result[list[HotPlugin]]:
    query = Statistics
    now = datetime.now()
    if bot_id:
        query = query.filter(bot_id=bot_id)
    if date_type == QueryDateType.DAY:
        query = query.filter(create_time__gte=now - timedelta(hours=now.hour))
    if date_type == QueryDateType.WEEK:
        query = query.filter(create_time__gte=now - timedelta(days=7))
    if date_type == QueryDateType.MONTH:
        query = query.filter(create_time__gte=now - timedelta(days=30))
    if date_type == QueryDateType.YEAR:
        query = query.filter(create_time__gte=now - timedelta(days=365))
    data_list = (
        await query.annotate(count=Count("id"))
        .group_by("plugin_name")
        .order_by("-count")
        .limit(5)
        .values_list("plugin_name", "count")
    )
    hot_plugin_list = []
    module_list = [x[0] for x in data_list]
    plugins = await PluginInfo.filter(module__in=module_list).all()
    module2name = {p.module: p.name for p in plugins}
    for data in data_list:
        module = data[0]
        name = module2name.get(module) or module
        hot_plugin_list.append(HotPlugin(module=module, name=name, count=data[1]))
    hot_plugin_list = sorted(hot_plugin_list, key=lambda x: x.count, reverse=True)
    if len(hot_plugin_list) > 5:
        hot_plugin_list = hot_plugin_list[:5]
    return Result.ok(hot_plugin_list)


@ws_router.websocket("/system_status")
async def system_logs_realtime(websocket: WebSocket, sleep: int = 5):
    await websocket.accept()
    logger.debug("ws system_status is connect")
    with contextlib.suppress(
        WebSocketDisconnect, ConnectionClosedError, ConnectionClosedOK
    ):
        while websocket.client_state == WebSocketState.CONNECTED:
            system_status = await get_system_status()
            await websocket.send_text(system_status.json())
            await asyncio.sleep(sleep)
