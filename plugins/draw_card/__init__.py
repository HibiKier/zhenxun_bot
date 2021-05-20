from nonebot import on_regex, on_keyword
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from .genshin_handle import genshin_draw, update_genshin_info, reset_count
from .prts_handle import update_prts_info, prts_draw, reload_pool
from .pretty_handle import update_pretty_info, pretty_draw
from .update_game_info import update_info
from util.utils import is_number, scheduler
from services.log import logger
import re


prts = on_regex(r'.*?方舟[1-9|一][0-9]{0,2}[抽|井]', priority=5, block=True)
prts_update = on_keyword({'更新方舟信息', '更新明日方舟信息'}, permission=SUPERUSER, priority=1, block=True)
prts_reload = on_keyword({'重载方舟卡池'}, priority=1, block=True)

genshin = on_regex('.*?原神[1-9|一][0-9]{0,2}[抽|井]', priority=5, block=True)
genshin_reset = on_keyword({'重置原神抽卡'}, priority=1, block=True)
genshin_update = on_keyword({'更新原神信息'}, permission=SUPERUSER, priority=1, block=True)

pretty = on_regex('.*?马娘卡?[1-9|一][0-9]{0,2}[抽|井]', priority=5, block=True)
pretty_update = on_keyword({'更新马娘信息', '更新赛马娘信息'}, permission=SUPERUSER, priority=1, block=True)


@prts.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    if msg in ['方舟一井', '方舟1井']:
        num = 300
    else:
        rmsg = re.search(r'.*?方舟(.*)抽', msg)
        if rmsg and is_number(rmsg.group(1)):
            try:
                num = int(rmsg.group(1))
            except ValueError:
                await prts.finish('必！须！是！数！字！', at_sender=True)
            if num > 300:
                await prts.finish('一井都满不足不了你嘛！快爬开！', at_sender=True)
            if num < 1:
                await prts.finish('虚空抽卡？？？', at_sender=True)
        else:
            return
    # print(num)
    await prts.send(await prts_draw(num), at_sender=True)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
        f" 方舟{num}抽")


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
        if rmsg and is_number(rmsg.group(1)):
            try:
                num = int(rmsg.group(1))
            except ValueError:
                await genshin.finish('必！须！是！数！字！', at_sender=True)
            if num > 300:
                await genshin.finish('一井都满不足不了你嘛！快爬开！', at_sender=True)
            if num < 1:
                await genshin.finish('虚空抽卡？？？', at_sender=True)
        else:
            return
    await genshin.send(await genshin_draw(event.user_id, num), at_sender=True)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
        f" 原神{num}抽")


@genshin_reset.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    reset_count(event.user_id)
    await genshin_reset.send('重置了原神抽卡次数', at_sender=True)


@pretty.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    if msg in ['赛马娘一井', '赛马娘1井', '马娘一井', '马娘1井', '赛马娘卡一井', '赛马娘卡1井', '马娘卡一井', '马娘卡1井']:
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
            if is_number(num):
                try:
                    num = int(num)
                except ValueError:
                    await genshin.finish('必！须！是！数！字！', at_sender=True)
                if num > 200:
                    await genshin.finish('一井都满不足不了你嘛！快爬开！', at_sender=True)
                if num < 1:
                    await genshin.finish('虚空抽卡？？？', at_sender=True)
            else:
                return
    await pretty.send(await pretty_draw(num, pool_name), at_sender=True)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
        f" 赛马娘{num}抽")


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


# 更新资源
@scheduler.scheduled_job(
    'cron',
    hour=4,
    minute=1,
)
async def _():
    try:
        await update_prts_info()
        logger.info('自动更新明日方舟信息')
    except Exception as e:
        logger.error(f'自动更新明日方舟信息出错 e:{e}')
    try:
        await update_genshin_info()
        logger.info('自动更新原神信息')
    except Exception as e:
        logger.error(f'自动更新原神信息出错 e:{e}')
    try:
        await update_pretty_info()
        logger.info('自动更新赛马娘信息')
    except Exception as e:
        logger.error(f'自动更新赛马娘信息出错 e:{e}')


# 每天四点重载up卡池
@scheduler.scheduled_job(
    'cron',
    hour=4,
    minute=1,
)
async def _():
    await reload_pool()


