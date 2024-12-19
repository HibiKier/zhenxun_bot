from datetime import datetime, timedelta

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import nonebot
from nonebot import require
from nonebot.config import Config
from tortoise.expressions import RawSQL
from tortoise.functions import Count

from zhenxun.models.bot_connect_log import BotConnectLog
from zhenxun.models.chat_history import ChatHistory
from zhenxun.models.statistics import Statistics

from ....base_model import BaseResultModel, QueryModel, Result
from ....utils import authentication
from .data_source import BotManage
from .model import AllChatAndCallCount, BotInfo, ChatCallMonthCount, QueryChatCallCount

require("plugin_store")

router = APIRouter(prefix="/dashboard")

driver = nonebot.get_driver()


@router.get(
    "/get_bot_list",
    dependencies=[authentication()],
    response_model=Result[list[BotInfo]],
    response_class=JSONResponse,
    deprecated="获取bot列表",  # type: ignore
)
async def _() -> Result[list[BotInfo]]:
    try:
        return Result.ok(await BotManage.get_bot_list(), "拿到信息啦!")
    except Exception as e:
        return Result.fail(f"发生了一点错误捏 {type(e)}: {e}")


@router.get(
    "/get_chat_and_call_count",
    dependencies=[authentication()],
    response_model=Result[QueryChatCallCount],
    response_class=JSONResponse,
    description="获取聊天/调用记录的全部和今日数量",
)
async def _(bot_id: str | None = None) -> Result[QueryChatCallCount]:
    now = datetime.now()
    query = ChatHistory
    if bot_id:
        query = query.filter(bot_id=bot_id)
    chat_all_count = await query.annotate().count()
    chat_day_count = await query.filter(
        create_time__gte=now - timedelta(hours=now.hour, minutes=now.minute)
    ).count()
    query = Statistics
    if bot_id:
        query = query.filter(bot_id=bot_id)
    call_all_count = await query.annotate().count()
    call_day_count = await query.filter(
        create_time__gte=now - timedelta(hours=now.hour, minutes=now.minute)
    ).count()
    return Result.ok(
        QueryChatCallCount(
            chat_num=chat_all_count,
            chat_day=chat_day_count,
            call_num=call_all_count,
            call_day=call_day_count,
        )
    )


@router.get(
    "/get_all_chat_and_call_count",
    dependencies=[authentication()],
    response_model=Result[AllChatAndCallCount],
    response_class=JSONResponse,
    description="获取聊天/调用记录的全部数据次数",
)
async def _(bot_id: str | None = None) -> Result[AllChatAndCallCount]:
    now = datetime.now()
    query = ChatHistory
    if bot_id:
        query = query.filter(bot_id=bot_id)
    chat_week_count = await query.filter(
        create_time__gte=now - timedelta(days=7, hours=now.hour, minutes=now.minute)
    ).count()
    chat_month_count = await query.filter(
        create_time__gte=now - timedelta(days=30, hours=now.hour, minutes=now.minute)
    ).count()
    chat_year_count = await query.filter(
        create_time__gte=now - timedelta(days=365, hours=now.hour, minutes=now.minute)
    ).count()
    query = Statistics
    if bot_id:
        query = query.filter(bot_id=bot_id)
    call_week_count = await query.filter(
        create_time__gte=now - timedelta(days=7, hours=now.hour, minutes=now.minute)
    ).count()
    call_month_count = await query.filter(
        create_time__gte=now - timedelta(days=30, hours=now.hour, minutes=now.minute)
    ).count()
    call_year_count = await query.filter(
        create_time__gte=now - timedelta(days=365, hours=now.hour, minutes=now.minute)
    ).count()
    return Result.ok(
        AllChatAndCallCount(
            chat_week=chat_week_count,
            chat_month=chat_month_count,
            chat_year=chat_year_count,
            call_week=call_week_count,
            call_month=call_month_count,
            call_year=call_year_count,
        )
    )


@router.get(
    "/get_chat_and_call_month",
    dependencies=[authentication()],
    response_model=Result[ChatCallMonthCount],
    response_class=JSONResponse,
    deprecated="获取聊天/调用记录的一个月数量",  # type: ignore
)
async def _(bot_id: str | None = None) -> Result[ChatCallMonthCount]:
    now = datetime.now()
    filter_date = now - timedelta(days=30, hours=now.hour, minutes=now.minute)
    chat_query = ChatHistory
    call_query = Statistics
    if bot_id:
        chat_query = chat_query.filter(bot_id=bot_id)
        call_query = call_query.filter(bot_id=bot_id)
    chat_date_list = (
        await chat_query.filter(create_time__gte=filter_date)
        .annotate(date=RawSQL("DATE(create_time)"), count=Count("id"))
        .group_by("date")
        .values("date", "count")
    )
    call_date_list = (
        await call_query.filter(create_time__gte=filter_date)
        .annotate(date=RawSQL("DATE(create_time)"), count=Count("id"))
        .group_by("date")
        .values("date", "count")
    )
    date_list = []
    chat_count_list = []
    call_count_list = []
    chat_date2cnt = {str(date["date"]): date["count"] for date in chat_date_list}
    call_date2cnt = {str(date["date"]): date["count"] for date in call_date_list}
    date = now.date()
    for _ in range(30):
        if str(date) in chat_date2cnt:
            chat_count_list.append(chat_date2cnt[str(date)])
        else:
            chat_count_list.append(0)
        if str(date) in call_date2cnt:
            call_count_list.append(call_date2cnt[str(date)])
        else:
            call_count_list.append(0)
        date_list.append(str(date)[5:])
        date -= timedelta(days=1)
    chat_count_list.reverse()
    call_count_list.reverse()
    date_list.reverse()
    return Result.ok(
        ChatCallMonthCount(chat=chat_count_list, call=call_count_list, date=date_list)
    )


@router.post(
    "/get_connect_log",
    dependencies=[authentication()],
    response_model=Result[BaseResultModel],
    response_class=JSONResponse,
    deprecated="获取Bot连接记录",  # type: ignore
)
async def _(query: QueryModel) -> Result[BaseResultModel]:
    total = await BotConnectLog.all().count()
    if total % query.size:
        total += 1
    data = (
        await BotConnectLog.all()
        .order_by("-id")
        .offset((query.index - 1) * query.size)
        .limit(query.size)
    )
    for v in data:
        v.connect_time = v.connect_time.replace(tzinfo=None).replace(microsecond=0)
    return Result.ok(BaseResultModel(total=total, data=data))


@router.get(
    "/get_nonebot_config",
    dependencies=[authentication()],
    response_model=Result[Config],
    response_class=JSONResponse,
    deprecated="获取nb配置",  # type: ignore
)
async def _() -> Result[Config]:
    return Result.ok(driver.config)
