from nonebot import on_regex, on_keyword
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from services.log import logger
from util.utils import scheduler
import re
from .genshin_handle import genshin_draw, update_genshin_info, reset_count
from .prts_handle import update_prts_info, prts_draw, reload_pool
from .pretty_handle import update_pretty_info, pretty_draw
from .guardian_handle import update_guardian_info, guardian_draw
from .pcr_handle import update_pcr_info, pcr_draw
from .update_game_info import update_info
from .util import check_num
from .rule import is_switch
from .config import PRTS_FLAG, PRETTY_FLAG, GUARDIAN_FLAG, GENSHIN_FLAG, PCR_FLAG



prts = on_regex(r'.*?方舟[1-9|一][0-9]{0,2}[抽|井]', rule=is_switch('prts'), priority=5, block=True)
prts_update = on_keyword({'更新方舟信息', '更新明日方舟信息'}, permission=SUPERUSER, priority=1, block=True)
prts_reload = on_keyword({'重载方舟卡池'}, priority=1, block=True)

genshin = on_regex('.*?原神[1-9|一][0-9]{0,2}[抽|井]', rule=is_switch('genshin'), priority=5, block=True)
genshin_reset = on_keyword({'重置原神抽卡'}, priority=1, block=True)
genshin_update = on_keyword({'更新原神信息'}, permission=SUPERUSER, priority=1, block=True)

pretty = on_regex('.*?马娘卡?[1-9|一][0-9]{0,2}[抽|井]', rule=is_switch('pretty'), priority=5, block=True)
pretty_update = on_keyword({'更新马娘信息', '更新赛马娘信息'}, permission=SUPERUSER, priority=1, block=True)

guardian = on_regex('.*?坎公骑冠剑武?器?[1-9|一][0-9]{0,2}[抽|井]', rule=is_switch('guardian'), priority=5, block=True)
guardian_update = on_keyword({'更新坎公骑冠剑信息'}, permission=SUPERUSER, priority=1, block=True)

pcr = on_regex('.*?(pcr|公主连结|公主连接|公主链接)[1-9|一][0-9]{0,2}[抽|井]', rule=is_switch('pcr'), priority=5, block=True)
pcr_update = on_keyword({'更新pcr信息', '更新公主连结信息'}, permission=SUPERUSER, priority=1, block=True)

test = on_keyword({'test'}, permission=SUPERUSER, priority=1, block=True)


@test.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_pcr_info()


@prts.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    if msg in ['方舟一井', '方舟1井']:
        num = 300
    else:
        rmsg = re.search(r'.*?方舟(.*)抽', msg)
        if rmsg:
            num, flag = check_num(rmsg.group(1), 300)
            if not flag:
                await prts.finish(num, at_sender=True)
        else:
            return
    await prts.send(await prts_draw(int(num)), at_sender=True)


@prts_reload.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await reload_pool()
    await prts_reload.finish('重载完成！')


@genshin.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    if msg in ['原神一井', '原神1井']:
        num = 180
    else:
        rmsg = re.search(r'.*?原神(.*)抽', msg)
        if rmsg:
            num, flag = check_num(rmsg.group(1), 180)
            if not flag:
                await genshin.finish(num, at_sender=True)
        else:
            return
    await genshin.send(await genshin_draw(event.user_id, int(num)), at_sender=True)


@genshin_reset.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    reset_count(event.user_id)
    await genshin_reset.send('重置了原神抽卡次数', at_sender=True)


@pretty.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    if msg.find('1井') != -1 or msg.find('一井') != -1:
        num = 200
        if msg.find("卡") == -1:
            pool_name = 'horse'
        else:
            pool_name = 'card'
    else:
        rmsg = re.search(r'.*?马娘(.*)抽', msg)
        if rmsg:
            num = rmsg.group(1)
            if num[0] == '卡':
                num = num[1:]
                pool_name = 'card'
            else:
                pool_name = 'horse'
            num, flag = check_num(num, 200)
            if not flag:
                await pretty.finish(num, at_sender=True)
        else:
            return
    await pretty.send(await pretty_draw(int(num), pool_name), at_sender=True)


@guardian.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    pool_name = 'char'
    if msg.find('1井') != -1 or msg.find('一井') != -1:
        num = 300
        if msg.find('武器') != -1:
            pool_name = 'arms'
    else:
        rmsg = re.search(r'.*?坎公骑冠剑(.*)抽', msg)
        if rmsg:
            num = rmsg.group(1)
            if num.find('武器') != -1:
                pool_name = 'arms'
                num = num.replace('武器', '')
            num, flag = check_num(num, 300)
            if not flag:
                await guardian.finish(num, at_sender=True)
        else:
            return
    await guardian.send(await guardian_draw(int(num), pool_name), at_sender=True)


@pcr.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    if msg.find('1井') != -1 or msg.find('一井') != -1:
        num = 300
    else:
        rmsg = re.search(r'.*?(pcr|公主连结)(.*)[抽|井]', msg)
        if rmsg:
            num, flag = check_num(rmsg.group(2), 300)
            if not flag:
                await pcr.finish(num, at_sender=True)
        else:
            return
    await pcr.send(await pcr_draw(int(num)), at_sender=True)


@prts_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_prts_info()
    await reload_pool()
    await prts_update.finish('更新完成！')


@genshin_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_genshin_info()
    await genshin_update.finish('更新完成！')


@pretty_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_pretty_info()
    await genshin_update.finish('更新完成！')


@guardian_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_guardian_info()
    await genshin_update.finish('更新完成！')


@pcr_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_pcr_info()
    await genshin_update.finish('更新完成！')


# 更新资源
@scheduler.scheduled_job(
    'cron',
    hour=4,
    minute=1,
)
async def _():
    try:
        if PRTS_FLAG:
            await update_prts_info()
    except Exception as e:
        logger.error(f'draw_card: 更新 明日方舟 失败 e：{e}')
    try:
        if GENSHIN_FLAG:
            await update_genshin_info()
    except Exception as e:
        logger.error(f'draw_card: 更新 原神 失败 e：{e}')
    try:
        if PRETTY_FLAG:
            await update_pretty_info()
    except Exception as e:
        logger.error(f'draw_card: 更新 赛马娘 失败 e：{e}')
    try:
        if GUARDIAN_FLAG:
            await update_guardian_info()
    except Exception as e:
        logger.error(f'draw_card: 更新 坎公骑冠剑 失败 e：{e}')
    try:
        if PCR_FLAG:
            await update_pcr_info()
    except Exception as e:
        logger.error(f'draw_card: 更新 公主连结 失败 e：{e}')


# 每天四点重载up卡池
@scheduler.scheduled_job(
    'cron',
    hour=4,
    minute=1,
)
async def _():
    if PRTS_FLAG:
        await reload_pool()
        logger.info(f'draw_card: 04: 01 重载方舟卡池')
