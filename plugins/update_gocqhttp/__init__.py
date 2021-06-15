from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from .data_source import download_gocq_lasted, upload_gocq_lasted
import os
from nonebot.adapters.cqhttp.permission import GROUP
from services.log import logger
from util.utils import scheduler, get_bot, UserExistLimiter
from configs.config import UPDATE_GOCQ_GROUP
from pathlib import Path

__plugin_name__ = '更新gocq'

__plugin_usage__ = '用法：发送’更新gocq‘，指定群 自动检测最新版gocq下载并上传'

path = str((Path() / "resources" / "gocqhttp_file").absolute()) + '/'

lasted_gocqhttp = on_command("更新gocq", permission=GROUP, priority=5, block=True)


_ulmt = UserExistLimiter()


@lasted_gocqhttp.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    # try:
    if event.group_id in UPDATE_GOCQ_GROUP:
        await lasted_gocqhttp.send('检测中...')
        info = await download_gocq_lasted(path)
        if info == 'gocqhttp没有更新！':
            await lasted_gocqhttp.finish('gocqhttp没有更新！')
        if _ulmt.check(event.group_id):
            await lasted_gocqhttp.finish('gocqhttp正在更新，请勿重复使用该命令', at_sender=True)
        _ulmt.set_True(event.group_id)
        try:
            for file in os.listdir(path):
                await upload_gocq_lasted(path, file, event.group_id)
                logger.info(f'更新了cqhttp...{file}')
            await lasted_gocqhttp.send(f'gocqhttp更新了，已上传成功！\n更新内容：\n{info}')
        except Exception as e:
            logger.error(f'更新gocq错误 e：{e}')
        _ulmt.set_False(event.group_id)


# 更新gocq
@scheduler.scheduled_job(
    'cron',
    hour=3,
    minute=1,
)
async def _():
    if UPDATE_GOCQ_GROUP:
        bot = get_bot()
        try:
            info = await download_gocq_lasted(path)
            if info == 'gocqhttp没有更新！':
                logger.info('gocqhttp没有更新！')
                return
            for group in UPDATE_GOCQ_GROUP:
                for file in os.listdir(path):
                    await upload_gocq_lasted(path, file, group)
                await bot.send_group_msg(group_id=group, message=f"gocqhttp更新了，已上传成功！\n更新内容：\n{info}")
        except Exception as e:
            logger.error(f'自动更新gocq出错 e:{e}')

