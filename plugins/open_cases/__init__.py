from typing import Type
from nonebot import on_command
from nonebot.matcher import Matcher
from utils.utils import scheduler, is_number
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent, Message
from nonebot.permission import SUPERUSER
import random
from nonebot.plugin import MatcherGroup
from configs.path_config import IMAGE_PATH
from nonebot.params import CommandArg
from .open_cases_c import (
    open_case,
    total_open_statistics,
    group_statistics,
    my_knifes_name,
    open_shilian_case,
)
from .utils import util_get_buff_price, util_get_buff_img, update_count_daily
from configs.config import Config

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
        * 不包含[武器箱]时随机开箱 *
    目前支持的武器箱：
        1.狂牙大行动武器箱
        2.突围大行动武器箱
        3.命悬一线武器箱
        4.裂空武器箱
        5.光谱武器箱
    示例：开箱 命悬一线
""".strip()
__plugin_superuser_usage__ = """
usage：
    更新皮肤指令
    指令：
        更新开箱图片 ?[武器箱]
        更新开箱价格 ?[武器箱]
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
    "更新开箱图片 ?[武器箱] [_superuser]",
    "更新开箱价格 ?[武器箱] [_superuser]",
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
    "INITIAL_OPEN_CASE_COUNT": {"value": 20, "help": "初始每日开箱次数", "default_value": 20},
    "EACH_IMPRESSION_ADD_COUNT": {
        "value": 3,
        "help": "每 * 点好感度额外增加开箱次数",
        "default_value": 3,
    },
    "COOKIE": {
        "value": None,
        "help": "BUFF的cookie",
    },
    "BUFF_PROXY": {"value": None, "help": "使用代理访问BUFF"},
}

Config.add_plugin_config(
    "_task",
    "DEFAULT_OPEN_CASE_RESET_REMIND",
    True,
    help_="被动 每日开箱重置提醒 进群默认开关状态",
    default_value=True,
)

cases_name = ["狂牙大行动", "突围大行动", "命悬一线", "裂空", "光谱"]

cases_matcher_group = MatcherGroup(priority=5, permission=GROUP, block=True)


k_open_case = cases_matcher_group.on_command("开箱")


@k_open_case.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    case_name = arg.extract_plain_text().strip()
    case_name = case_name.replace("武器箱", "").strip()
    if case_name:
        result = await open_case(event.user_id, event.group_id, case_name)
    else:
        result = await open_case(
            event.user_id, event.group_id, random.choice(cases_name)
        )
    await k_open_case.finish(result, at_sender=True)


total_case_data = cases_matcher_group.on_command(
    "我的开箱", aliases={"开箱统计", "开箱查询", "查询开箱"}
)


@total_case_data.handle()
async def _(event: GroupMessageEvent):
    await total_case_data.finish(
        await total_open_statistics(event.user_id, event.group_id),
        at_sender=True,
    )


group_open_case_statistics = cases_matcher_group.on_command("群开箱统计")


@group_open_case_statistics.handle()
async def _(event: GroupMessageEvent):
    await group_open_case_statistics.finish(await group_statistics(event.group_id))


my_kinfes = on_command("我的金色", priority=1, permission=GROUP, block=True)


@my_kinfes.handle()
async def _(event: GroupMessageEvent):
    await my_kinfes.finish(
        await my_knifes_name(event.user_id, event.group_id), at_sender=True
    )


open_shilian: Type[Matcher] = cases_matcher_group.on_regex("(.*)连开箱(.*?)")


@open_shilian.handle()
async def _(event: GroupMessageEvent, state: T_State):
    num = state["_matched_groups"][0].strip()
    if is_number(num) or num_dict.get(num):
        try:
            num = num_dict[num]
        except KeyError:
            num = int(num)
        if num > 30:
            await open_shilian.finish("开箱次数不要超过30啊笨蛋！", at_sender=True)
        if num < 0:
            await open_shilian.finish("再负开箱就扣你明天开箱数了！", at_sender=True)
    else:
        await open_shilian.finish("必须要是数字切不要超过30啊笨蛋！中文也可！", at_sender=True)
    case_name = state["_matched_groups"][1].strip()
    case_name = case_name.replace("武器箱", "").strip()
    if not case_name:
        case_name = random.choice(cases_name)
    elif case_name not in cases_name:
        await open_shilian.finish("武器箱未收录！", at_sender=True)
    await open_shilian.finish(
        await open_shilian_case(event.user_id, event.group_id, case_name, num),
        at_sender=True,
    )


num_dict = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
    "十一": 11,
    "十二": 12,
    "十三": 13,
    "十四": 14,
    "十五": 15,
    "十六": 16,
    "十七": 17,
    "十八": 18,
    "十九": 19,
    "二十": 20,
    "二十一": 21,
    "二十二": 22,
    "二十三": 23,
    "二十四": 24,
    "二十五": 25,
    "二十六": 26,
    "二十七": 27,
    "二十八": 28,
    "二十九": 29,
    "三十": 30,
}


update_price = on_command("更新开箱价格", priority=1, permission=SUPERUSER, block=True)


@update_price.handle()
async def _( event: MessageEvent):
    await update_price.send(await util_get_buff_price(str(event.get_message())))


update_img = on_command("更新开箱图片", priority=1, permission=SUPERUSER, block=True)


@update_img.handle()
async def _(event: MessageEvent):
    await update_img.send(await util_get_buff_img(str(event.get_message())))


# 重置开箱
@scheduler.scheduled_job(
    "cron",
    hour=0,
    minute=1,
)
async def _():
    await update_count_daily()
