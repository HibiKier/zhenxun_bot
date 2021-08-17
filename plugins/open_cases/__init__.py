from nonebot import on_command
from utils.utils import FreqLimiter, scheduler, get_message_text, is_number
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageEvent
from nonebot.permission import SUPERUSER
import random
from nonebot.plugin import MatcherGroup
import re
from .open_cases_c import (
    open_case,
    total_open_statistics,
    group_statistics,
    my_knifes_name,
    open_shilian_case,
)
from .utils import util_get_buff_price, util_get_buff_img, update_count_daily
from configs.config import NICKNAME

__plugin_name__ = "开箱"
__plugin_usage__ = (
    "用法：\n"
    "看看你的人品罢了\n"
    "目前只支持\n\t"
    "1.狂牙大行动武器箱\n\t"
    "2.突围大行动武器箱\n\t"
    "3.命悬一线武器箱\n\t"
    "4.裂空武器箱\n\t"
    "5.光谱武器箱\n"
    f"示例：{NICKNAME}开箱 突围大行动（不输入指定武器箱则随机）\n"
    "示例：我的开箱(开箱统计)\n"
    "示例：群开箱统计\n"
    "示例：我的金色"
)

_flmt = FreqLimiter(3)

cases_name = ["狂牙大行动", "突围大行动", "命悬一线", "裂空", "光谱"]

cases_matcher_group = MatcherGroup(priority=5, permission=GROUP, block=True)


k_open_case = cases_matcher_group.on_command("开箱")


@k_open_case.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if str(event.get_message()).strip() in ["帮助"]:
        await k_open_case.finish(__plugin_usage__)
    if not _flmt.check(event.user_id):
        await k_open_case.finish("着什么急啊，慢慢来！", at_sender=True)
    _flmt.start_cd(event.user_id)
    case_name = get_message_text(event.json())
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
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await total_case_data.finish(
        await total_open_statistics(event.user_id, event.group_id),
        at_sender=True,
    )


group_open_case_statistics = cases_matcher_group.on_command("群开箱统计")


@group_open_case_statistics.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await group_open_case_statistics.finish(await group_statistics(event.group_id))


my_kinfes = on_command("我的金色", priority=1, permission=GROUP, block=True)


@my_kinfes.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await my_kinfes.finish(
        await my_knifes_name(event.user_id, event.group_id), at_sender=True
    )


open_shilian = cases_matcher_group.on_regex(".*连开箱")


@open_shilian.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    # if not _flmt.check(event.user_id):
    #     await k_open_case.finish('着什么急啊，慢慢来！', at_sender=True)
    _flmt.start_cd(event.user_id)
    msg = get_message_text(event.json())
    rs = re.search(r"(.*)连开箱(.*)", msg)
    if rs:
        num = rs.group(1).strip()
        if is_number(num) or num_dict.get(num):
            try:
                num = num_dict[num]
            except KeyError:
                num = int(num)
            if num > 30:
                await open_shilian.finish("开箱次数不要超过30啊笨蛋！", at_sender=True)
        else:
            await open_shilian.finish("必须要是数字切不要超过30啊笨蛋！中文也可！", at_sender=True)
        case_name = rs.group(2).strip()
        if case_name.find("武器箱") != -1:
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


update_price = on_command("更新价格", priority=1, permission=SUPERUSER, block=True)


@update_price.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_price.send(await util_get_buff_price(str(event.get_message())))


update_img = on_command("更新图片", priority=1, permission=SUPERUSER, block=True)


@update_img.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_img.send(await util_get_buff_img(str(event.get_message())))


# 重置开箱
@scheduler.scheduled_job(
    "cron",
    hour=0,
    minute=1,
)
async def _():
    await update_count_daily()
