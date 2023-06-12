import asyncio
import random
from datetime import datetime, timedelta
from typing import Any, List, Tuple

from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.params import CommandArg, RegexGroup
from nonebot.permission import SUPERUSER
from nonebot.plugin import MatcherGroup
from nonebot.typing import T_State

from configs.config import Config
from configs.path_config import IMAGE_PATH
from services.log import logger
from utils.depends import OneCommand
from utils.image_utils import text2image
from utils.message_builder import image
from utils.utils import CN2NUM, is_number, scheduler

from .open_cases_c import (
    auto_update,
    get_my_knifes,
    group_statistics,
    open_case,
    open_multiple_case,
    total_open_statistics,
)
from .utils import (
    CASE2ID,
    KNIFE2ID,
    CaseManager,
    build_case_image,
    get_skin_case,
    init_skin_trends,
    reset_count_daily,
    update_skin_data,
)

__zx_plugin_name__ = "开箱"
__plugin_usage__ = """
usage：
    看看你的人品罢了
    模拟开箱，完美公布的真实概率，只想看看替你省了多少钱
    指令：
        开箱 ?[武器箱]
        [1-30]连开箱 ?[武器箱]
        我的开箱
        我的金色
        群开箱统计
        查看武器箱?[武器箱]
        * 不包含[武器箱]时随机开箱 *
        示例: 查看武器箱
        示例: 查看武器箱英勇
""".strip()
__plugin_superuser_usage__ = """
usage：
    更新皮肤指令
    重置开箱： 重置今日开箱所有次数
    指令：
        更新武器箱 ?[武器箱/ALL]
        更新皮肤 ?[名称/ALL1]
        更新皮肤 ?[名称/ALL1] -S: (必定更新罕见皮肤所属箱子)
    * 不指定武器箱时则全部更新 *
    * 过多的爬取会导致账号API被封 *
""".strip()
__plugin_des__ = "csgo模拟开箱[戒赌]"
__plugin_cmd__ = [
    "开箱 ?[武器箱]",
    "[1-30]连开箱 ?[武器箱]",
    "我的开箱",
    "我的金色",
    "群开箱统计",
    "查看武器箱?[武器箱]",
    "更新武器箱 ?[武器箱] [_superuser]",
    "更新皮肤 ?[刀具名称] [_superuser]",
]
__plugin_type__ = ("抽卡相关", 1)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["csgo开箱", "开箱"],
}
__plugin_task__ = {"open_case_reset_remind": "每日开箱重置提醒"}
__plugin_cd_limit__ = {"rst": "着什么急啊，慢慢来！"}
__plugin_resources__ = {f"cases": IMAGE_PATH}
__plugin_configs__ = {
    "INITIAL_OPEN_CASE_COUNT": {
        "value": 20,
        "help": "初始每日开箱次数",
        "default_value": 20,
        "type": int,
    },
    "EACH_IMPRESSION_ADD_COUNT": {
        "value": 3,
        "help": "每 * 点好感度额外增加开箱次数",
        "default_value": 3,
        "type": int,
    },
    "COOKIE": {"value": None, "help": "BUFF的cookie", "type": str},
    "BUFF_PROXY": {"value": None, "help": "使用代理访问BUFF"},
    "DAILY_UPDATE": {
        "value": None,
        "help": "每日自动更新的武器箱，存在'ALL'时则更新全部武器箱",
        "type": List[str],
    },
}

Config.add_plugin_config(
    "_task",
    "DEFAULT_OPEN_CASE_RESET_REMIND",
    True,
    help_="被动 每日开箱重置提醒 进群默认开关状态",
    default_value=True,
    type=bool,
)


cases_matcher_group = MatcherGroup(priority=5, permission=GROUP, block=True)


k_open_case = cases_matcher_group.on_command("开箱")
reload_count = cases_matcher_group.on_command("重置开箱", permission=SUPERUSER)
total_case_data = cases_matcher_group.on_command(
    "我的开箱", aliases={"开箱统计", "开箱查询", "查询开箱"}
)
group_open_case_statistics = cases_matcher_group.on_command("群开箱统计")
open_multiple = cases_matcher_group.on_regex("(.*)连开箱(.*)?")
update_case = on_command(
    "更新武器箱", aliases={"更新皮肤"}, priority=1, permission=SUPERUSER, block=True
)
show_case = on_command("查看武器箱", priority=5, block=True)
my_knifes = on_command("我的金色", priority=1, permission=GROUP, block=True)
show_skin = on_command("查看皮肤", priority=5, block=True)
price_trends = on_command("价格趋势", priority=5, block=True)


@price_trends.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().replace("武器箱", "").strip()
    if not msg:
        await price_trends.finish("未指定皮肤")
    msg_split = msg.split()
    if len(msg_split) < 3:
        await price_trends.finish("参数不足, [类型名称] [皮肤名称] [磨损程度] ?[天数=7]")
    abrasion = msg_split[2]
    day = 7
    if len(msg_split) > 3:
        if not is_number(msg_split[3]):
            await price_trends.finish("天数必须为数字")
        day = int(msg_split[3])
        if day <= 0 or day > 180:
            await price_trends.finish("天数必须大于0且小于180")
    result = await init_skin_trends(msg_split[0], msg_split[1], msg_split[2], day)
    if not result:
        await price_trends.finish("未查询到数据")
    await price_trends.send(
        image(await init_skin_trends(msg_split[0], msg_split[1], msg_split[2], day))
    )


@reload_count.handle()
async def _(event: GroupMessageEvent):
    await reset_count_daily()


@k_open_case.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    case_name = arg.extract_plain_text().strip()
    case_name = case_name.replace("武器箱", "").strip()
    result = await open_case(event.user_id, event.group_id, case_name)
    await k_open_case.finish(result, at_sender=True)


@total_case_data.handle()
async def _(event: GroupMessageEvent):
    await total_case_data.finish(
        await total_open_statistics(event.user_id, event.group_id),
        at_sender=True,
    )


@group_open_case_statistics.handle()
async def _(event: GroupMessageEvent):
    await group_open_case_statistics.finish(await group_statistics(event.group_id))


@my_knifes.handle()
async def _(event: GroupMessageEvent):
    await my_knifes.finish(
        await get_my_knifes(event.user_id, event.group_id), at_sender=True
    )


@open_multiple.handle()
async def _(
    event: GroupMessageEvent, state: T_State, reg_group: Tuple[Any, ...] = RegexGroup()
):
    num, case_name = reg_group
    if is_number(num) or CN2NUM.get(num):
        try:
            num = CN2NUM[num]
        except KeyError:
            num = int(num)
        if num > 30:
            await open_multiple.finish("开箱次数不要超过30啊笨蛋！", at_sender=True)
        if num < 0:
            await open_multiple.finish("再负开箱就扣你明天开箱数了！", at_sender=True)
    else:
        await open_multiple.finish("必须要是数字切不要超过30啊笨蛋！中文也可！", at_sender=True)
    case_name = case_name.replace("武器箱", "").strip()
    await open_multiple.finish(
        await open_multiple_case(event.user_id, event.group_id, case_name, num),
        at_sender=True,
    )


@update_case.handle()
async def _(event: MessageEvent, arg: Message = CommandArg(), cmd: str = OneCommand()):
    msg = arg.extract_plain_text().strip()
    is_update_case_name = "-S" in msg
    msg = msg.replace("-S", "").strip()
    if not msg:
        case_list = []
        skin_list = []
        for i, case_name in enumerate(CASE2ID):
            if case_name in CaseManager.CURRENT_CASES:
                case_list.append(f"{i+1}.{case_name} [已更新]")
            else:
                case_list.append(f"{i+1}.{case_name}")
        for skin_name in KNIFE2ID:
            skin_list.append(f"{skin_name}")
        text = "武器箱:\n" + "\n".join(case_list) + "\n皮肤:\n" + ", ".join(skin_list)
        await update_case.finish(
            "未指定武器箱, 当前已包含武器箱/皮肤\n"
            + image(await text2image(text, padding=20, color="#f9f6f2"))
        )
    if msg in ["ALL", "ALL1"]:
        if msg == "ALL":
            case_list = list(CASE2ID.keys())
            type_ = "武器箱"
        else:
            case_list = list(KNIFE2ID.keys())
            type_ = "罕见皮肤"
        await update_case.send(f"即将更新所有{type_}, 请稍等")
        for i, case_name in enumerate(case_list):
            try:
                info = await update_skin_data(case_name, is_update_case_name)
                if "请先登录" in info:
                    await update_case.send(f"未登录, 已停止更新, 请配置BUFF token...")
                    return
                rand = random.randint(300, 500)
                result = f"更新全部{type_}完成"
                if i < len(case_list) - 1:
                    next_case = case_list[i + 1]
                    result = f"将在 {rand} 秒后更新下一{type_}: {next_case}"
                await update_case.send(f"{info}, {result}")
                logger.info(f"info, {result}", "更新武器箱")
                await asyncio.sleep(rand)
            except Exception as e:
                logger.error(f"更新{type_}: {case_name}", e=e)
                await update_case.send(f"更新{type_}: {case_name} 发生错误: {type(e)}: {e}")
        await update_case.send(f"更新全部{type_}完成")
    else:
        await update_case.send(f"开始{cmd}: {msg}, 请稍等")
        try:
            await update_case.send(
                await update_skin_data(msg, is_update_case_name), at_sender=True
            )
        except Exception as e:
            logger.error(f"{cmd}: {msg}", e=e)
            await update_case.send(f"成功{cmd}: {msg} 发生错误: {type(e)}: {e}")


@show_case.handle()
async def _(arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    result = await build_case_image(msg)
    if isinstance(result, str):
        await show_case.send(result)
    else:
        await show_case.send(image(result))


# 重置开箱
@scheduler.scheduled_job(
    "cron",
    hour=0,
    minute=1,
)
async def _():
    await reset_count_daily()


@scheduler.scheduled_job(
    "cron",
    hour=0,
    minute=10,
)
async def _():
    now = datetime.now()
    hour = random.choice([0, 1, 2, 3])
    date = now + timedelta(hours=hour)
    logger.debug(f"将在 {date} 时自动更新武器箱...", "更新武器箱")
    scheduler.add_job(
        auto_update,
        "date",
        run_date=date.replace(microsecond=0),
        id=f"auto_update_csgo_cases",
    )
