from nonebot import on_regex, on_keyword
from nonebot.adapters.cqhttp import Bot, MessageEvent, Message, GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from .genshin_handle import (
    genshin_draw,
    update_genshin_info,
    reset_count,
    reload_genshin_pool,
)
from .prts_handle import update_prts_info, prts_draw, reload_prts_pool
from .pretty_handle import update_pretty_info, pretty_draw, reload_pretty_pool
from .guardian_handle import update_guardian_info, guardian_draw
from .pcr_handle import update_pcr_info, pcr_draw
from .azur_handle import update_azur_info, azur_draw
from .fgo_handle import update_fgo_info, fgo_draw
from .onmyoji_handle import update_onmyoji_info, onmyoji_draw
from .update_game_info import update_info
from .util import is_number, check_num
from .rule import is_switch
from .config import (
    PRTS_FLAG,
    PRETTY_FLAG,
    GUARDIAN_FLAG,
    GENSHIN_FLAG,
    PCR_FLAG,
    AZUR_FLAG,
    FGO_FLAG,
    ONMYOJI_FLAG,
)
from .async_update_game_info import async_update_game
import re
import asyncio
from utils.utils import scheduler
from services.log import logger

__zx_plugin_name__ = "游戏抽卡"
__plugin_usage__ = """
usage：
    模拟赛马娘，原神，明日方舟，坎公骑冠剑，公主连结(国/台)，碧蓝航线，FGO，阴阳师进行抽卡
    指令：
        原神[1-300]抽: 原神常驻池
        原神角色[1-300]抽: 原神角色UP池子
        原神武器[1-300]抽: 原神武器UP池子
        重置原神抽卡: 清空当前卡池的抽卡次数[即从0开始计算UP概率]
        方舟[1-300]抽: 方舟卡池，当有当期UP时指向UP池
        赛马娘[1-200]抽: 赛马娘卡池，当有当期UP时指向UP池
        坎公骑冠剑[1-300]抽: 坎公骑冠剑卡池，当有当期UP时指向UP池
        pcr/公主连接[1-300]抽: 公主连接卡池
        碧蓝航线/碧蓝[重型/轻型/特型][1-300]抽: 碧蓝航线重型/轻型/特型卡池
        fgo[1-300]抽: fgo卡池
        阴阳师[1-300]抽: 阴阳师卡池
    * 以上指令可以通过 XX一井 来指定最大抽取数量 *
    * 示例：原神一井 *
""".strip()
__plugin_superuser_usage__ = """
usage：
    卡池方面的更新
    指令：
        更新方舟信息
        重载方舟卡池
        更新原神信息
        重载原神卡池
        更新赛马娘信息
        重载赛马娘卡池
        更新坎公骑冠剑信息
        更新碧蓝航线信息
        更新fgo信息
        更新阴阳师信息
""".strip()
__plugin_des__ = "就算是模拟抽卡也不能改变自己是个非酋"
__plugin_cmd__ = [
    "原神[1-300]抽",
    "原神角色[1-300]抽",
    "原神武器[1-300]抽",
    "重置原神抽卡",
    "方舟[1-300]抽",
    "赛马娘[1-200]抽",
    "坎公骑冠剑[1-300]抽",
    "pcr/公主连接[1-300]抽",
    "fgo[1-300]抽",
    "阴阳师[1-300]抽",
    "更新方舟信息 [_superuser]",
    "重载方舟卡池 [_superuser]",
    "更新原神信息 [_superuser]",
    "重载原神卡池 [_superuser]",
    "更新赛马娘信息 [_superuser]",
    "重载赛马娘卡池 [_superuser]",
    "更新坎公骑冠剑信息 [_superuser]",
    "更新碧蓝航线信息 [_superuser]",
    "更新fgo信息 [_superuser]",
    "更新阴阳师信息 [_superuser]",
]
__plugin_type__ = ("抽卡相关", 1)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["游戏抽卡", "抽卡"],
}


prts = on_regex(
    r".*?方舟[1-9|一][0-9]{0,2}[抽|井]", rule=is_switch("prts"), priority=5, block=True
)
prts_update = on_keyword(
    {"更新方舟信息", "更新明日方舟信息"}, permission=SUPERUSER, priority=1, block=True
)
prts_up_reload = on_keyword({"重载方舟卡池"}, priority=1, block=True)

genshin = on_regex(
    ".*?原神(武器|角色)?池?[1-9|一][0-9]{0,2}[抽|井]",
    rule=is_switch("genshin"),
    priority=5,
    block=True,
)
genshin_update = on_keyword({"更新原神信息"}, permission=SUPERUSER, priority=1, block=True)
genshin_reset = on_keyword({"重置原神抽卡"}, priority=1, block=True)
genshin_up_reload = on_keyword({"重载原神卡池"}, priority=1, block=True)

pretty = on_regex(
    ".*?马娘卡?[1-9|一][0-9]{0,2}[抽|井]", rule=is_switch("pretty"), priority=5, block=True
)
pretty_update = on_keyword(
    {"更新马娘信息", "更新赛马娘信息"}, permission=SUPERUSER, priority=1, block=True
)
pretty_up_reload = on_keyword({"重载赛马娘卡池"}, priority=1, block=True)

guardian = on_regex(
    ".*?坎公骑冠剑武?器?[1-9|一][0-9]{0,2}[抽|井]",
    rule=is_switch("guardian"),
    priority=5,
    block=True,
)
guardian_update = on_keyword(
    {"更新坎公骑冠剑信息"}, permission=SUPERUSER, priority=1, block=True
)

pcr = on_regex(
    ".*?(pcr|公主连结|公主连接|公主链接|公主焊接)[1-9|一][0-9]{0,2}[抽|井]",
    rule=is_switch("pcr"),
    priority=5,
    block=True,
)
pcr_update = on_keyword(
    {"更新pcr信息", "更新公主连结信息"}, permission=SUPERUSER, priority=1, block=True
)

azur = on_regex(
    ".*?碧蓝航?线?(轻型|重型|特型)池?[1-9|一][0-9]{0,2}[抽]",
    rule=is_switch("azur"),
    priority=5,
    block=True,
)
azur_update = on_keyword(
    {"更新碧蓝信息", "更新碧蓝航线信息"}, permission=SUPERUSER, priority=1, block=True
)

fgo = on_regex(
    ".*?fgo[1-9|一][0-9]{0,2}[抽]", rule=is_switch("fgo"), priority=5, block=True
)
fgo_update = on_keyword({"更新fgo信息"}, permission=SUPERUSER, priority=1, block=True)

onmyoji = on_regex(
    ".*?阴阳师[1-9|一][0-9]{0,2}[抽]", rule=is_switch("onmyoji"), priority=5, block=True
)
onmyoji_update = on_keyword({"更新阴阳师信息"}, permission=SUPERUSER, priority=1, block=True)


@prts.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    if msg in ["方舟一井", "方舟1井"]:
        num = 300
    else:
        rmsg = re.search(r".*?方舟(.*)抽", msg)
        if rmsg:
            num, flag = check_num(rmsg.group(1), 300)
            if not flag:
                await prts.finish(num, at_sender=True)
        else:
            return
    await prts.send(await prts_draw(int(num)), at_sender=True)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 方舟 {num}抽"
    )


@prts_up_reload.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    text = await reload_prts_pool()
    await prts_up_reload.finish(Message(f"重载完成！\n{text}"))


@genshin.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    rmsg = re.search(r".*?原神(武器|角色)?池?(.*)[抽|井]", msg)
    if rmsg:
        pool_name = rmsg.group(1)
        if pool_name == "武器":
            pool_name = "arms"
        elif pool_name == "角色":
            pool_name = "char"
        else:
            pool_name = ""
        num = rmsg.group(2)
        if msg.find("一井") != -1 or msg.find("1井") != -1:
            num = 180
        else:
            num, flag = check_num(num, 180)
            if not flag:
                await genshin.finish(num, at_sender=True)
    else:
        return
    await genshin.send(
        await genshin_draw(event.user_id, int(num), pool_name), at_sender=True
    )
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 原神 {num}抽"
    )


@genshin_up_reload.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    text = await reload_genshin_pool()
    await genshin_reset.finish(Message(f"重载成功！\n{text}"))


@genshin_reset.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    reset_count(event.user_id)
    await genshin_reset.send("重置了原神抽卡次数", at_sender=True)


@pretty.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    if msg.find("1井") != -1 or msg.find("一井") != -1:
        num = 200
        if msg.find("卡") == -1:
            pool_name = "char"
        else:
            pool_name = "card"
    else:
        rmsg = re.search(r".*?马娘(.*)抽", msg)
        if rmsg:
            num = rmsg.group(1)
            if num[0] == "卡":
                num = num[1:]
                pool_name = "card"
            else:
                pool_name = "char"
            num, flag = check_num(num, 200)
            if not flag:
                await pretty.finish(num, at_sender=True)
        else:
            return
    await pretty.send(await pretty_draw(int(num), pool_name), at_sender=True)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 赛马娘 {num}抽"
    )


@pretty_up_reload.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    text = await reload_pretty_pool()
    await genshin_reset.finish(Message(f"重载成功！\n{text}"))


@guardian.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    pool_name = "char"
    if msg.find("1井") != -1 or msg.find("一井") != -1:
        num = 300
        if msg.find("武器") != -1:
            pool_name = "arms"
    else:
        rmsg = re.search(r".*?坎公骑冠剑(.*)抽", msg)
        if rmsg:
            num = rmsg.group(1)
            if num.find("武器") != -1:
                pool_name = "arms"
                num = num.replace("武器", "")
            num, flag = check_num(num, 300)
            if not flag:
                await guardian.finish(num, at_sender=True)
        else:
            return
    await guardian.send(await guardian_draw(int(num), pool_name), at_sender=True)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 坎公骑冠剑 {num}抽"
    )


@pcr.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    if msg.find("1井") != -1 or msg.find("一井") != -1:
        num = 300
    else:
        rmsg = re.search(r".*?(pcr|公主连结)(.*)[抽|井]", msg)
        if rmsg:
            num, flag = check_num(rmsg.group(2), 300)
            if not flag:
                await pcr.finish(num, at_sender=True)
        else:
            return
    await pcr.send(await pcr_draw(int(num)), at_sender=True)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 公主连结 {num}抽"
    )


@azur.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    rmsg = re.search(".*?碧蓝航?线?(轻型|重型|特型)池?(.*)[抽]", msg)
    if rmsg:
        pool_name = rmsg.group(1)
        num, flag = check_num(rmsg.group(2), 300)
        if not flag:
            await azur.finish(num, at_sender=True)
    else:
        return
    await azur.send(await azur_draw(int(num), pool_name), at_sender=True)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 碧蓝航线 {num}抽"
    )


@fgo.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    rmsg = re.search(".*?fgo(.*)抽", msg)
    if rmsg:
        num, flag = check_num(rmsg.group(1), 300)
        if not flag:
            await fgo.finish(num, at_sender=True)
    else:
        return
    await fgo.send(await fgo_draw(int(num)), at_sender=True)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) fgo {num}抽"
    )


@onmyoji.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    rmsg = re.search(".*?阴阳师(.*)抽", msg)
    if rmsg:
        num, flag = check_num(rmsg.group(1), 300)
        if not flag:
            await onmyoji.finish(num, at_sender=True)
    else:
        return
    await onmyoji.send(await onmyoji_draw(int(num)), at_sender=True)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 阴阳师 {num}抽"
    )


@prts_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_prts_info()
    await prts_update.finish("更新完成！")


@genshin_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_genshin_info()
    await genshin_update.finish("更新完成！")


@pretty_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_pretty_info()
    await genshin_update.finish("更新完成！")


@guardian_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_guardian_info()
    await genshin_update.finish("更新完成！")


@pcr_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_pcr_info()
    await genshin_update.finish("更新完成！")


@azur_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_azur_info()
    await genshin_update.finish("更新完成！")


@fgo_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_fgo_info()
    await genshin_update.finish("更新完成！")


@onmyoji_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_onmyoji_info()
    await genshin_update.finish("更新完成！")


# 更新资源
@scheduler.scheduled_job(
    "cron",
    hour=4,
    minute=1,
)
async def _():
    tasks = []
    if PRTS_FLAG:
        tasks.append(asyncio.ensure_future(update_prts_info()))
    if GENSHIN_FLAG:
        tasks.append(asyncio.ensure_future(update_genshin_info()))
    if PRETTY_FLAG:
        tasks.append(asyncio.ensure_future(update_pretty_info()))
    if GUARDIAN_FLAG:
        tasks.append(asyncio.ensure_future(update_guardian_info()))
    if PCR_FLAG:
        tasks.append(asyncio.ensure_future(update_pcr_info()))
    if AZUR_FLAG:
        tasks.append(asyncio.ensure_future(update_azur_info()))
    if FGO_FLAG:
        tasks.append(asyncio.ensure_future(update_fgo_info()))
    if ONMYOJI_FLAG:
        tasks.append(asyncio.ensure_future(update_onmyoji_info()))
    await asyncio.gather(*tasks)
    logger.info("draw_card 抽卡自动更新完成...")


# 每天四点重载方舟up卡池
@scheduler.scheduled_job(
    "cron",
    hour=4,
    minute=1,
)
async def _():
    if PRTS_FLAG:
        await reload_prts_pool()
        logger.info("自动重载方舟卡池UP成功")


# 每天四点重载赛马娘up卡池
@scheduler.scheduled_job(
    "cron",
    hour=4,
    minute=1,
)
async def _():
    if PRETTY_FLAG:
        await reload_pretty_pool()
        logger.info("自动重载赛马娘UP成功")


# 每天下午六点点重载原神up卡池
@scheduler.scheduled_job(
    "cron",
    hour=18,
    minute=1,
)
async def _():
    if PRTS_FLAG:
        await reload_genshin_pool()
        logger.info("自动重载原神卡池UP成功")
