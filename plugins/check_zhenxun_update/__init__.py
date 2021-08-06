from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot import on_command
from .data_source import check_update, get_latest_version
from services.log import logger
from utils.utils import scheduler, get_bot
from pathlib import Path


update_zhenxun = on_command('检查更新真寻', permission=SUPERUSER, priority=1, block=True)


@update_zhenxun.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    try:
        await check_update(bot)
    except Exception as e:
        logger.error(f'更新真寻未知错误 {type(e)}：{e}')
        await bot.send_private_msg(
            user_id=int(list(bot.config.superusers)[0]),
            message=f'更新真寻未知错误 {type(e)}：{e}'
        )
    else:
        await bot.send_private_msg(
            user_id=int(list(bot.config.superusers)[0]),
            message=f'更新完毕，请重启真寻....'
        )


@scheduler.scheduled_job(
    "interval",
    hour=24,
)
async def _():
    _version = "v0.0.0"
    _version_file = Path() / "__version__"
    if _version_file.exists():
        _version = (
            open(_version_file, "r", encoding="utf8").readline().split(":")[-1].strip()
        )
    latest_version, tar_gz_url = await get_latest_version()
    if latest_version and tar_gz_url:
        if _version != latest_version:
            bot = get_bot()
            await bot.send_private_msg(
                user_id=int(list(bot.config.superusers)[0]),
                message=f'检测到真寻版本更新\n'
                        f'当前版本：{_version}，最新版本：{latest_version}\n'
                        f'尝试自动更新...'
            )
            try:
                await check_update(bot)
            except Exception as e:
                logger.error(f'更新真寻未知错误 {type(e)}：{e}')
                await bot.send_private_msg(
                    user_id=int(list(bot.config.superusers)[0]),
                    message=f'更新真寻未知错误 {type(e)}：{e}\n'
                )



