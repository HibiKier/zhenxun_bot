from nonebot import on_command
from nonebot.adapters.cqhttp.permission import PRIVATE
from .data_source import from_reimu_get_info
from services.log import logger
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
from util.utils import is_number, get_message_text, UserExistLimiter, scheduler
from models.count_user import UserCount
from configs.config import COUNT_PER_DAY_REIMU

__plugin_name__ = '上车'
__plugin_usage__ = r"""
* 请各位使用后不要转发 *
* 大部分解压密码是⑨ *
/ 每人每天仅提供 5 次上车机会（只能私聊）更多次数请向管理员申请（用爱发电）限制小色批乱搜 /
/ 并不推荐小色批使用此功能（主要是不够色，目的不够明确） /
上车 [目的地]
上车 5 [目的地]  该目的地第5页停车场
ps: 请尽量提供具体的目的地名称
""".strip()


_ulmt = UserExistLimiter()

reimu = on_command('上车', permission=PRIVATE, block=True, priority=1)


@reimu.args_parser
async def _(bot: Bot, event: Event, state: T_State):
    if get_message_text(event.json()) in ['取消', '算了']:
        await reimu.finish("已取消操作..", at_sender=True)
    if not get_message_text(event.json()):
        await reimu.reject('没时间等了！快说你要去哪里？', at_sender=True)
    state['keyword'] = get_message_text(event.json())
    state['page'] = 1


@reimu.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if str(event.get_message()) in ['帮助']:
        await reimu.finish(__plugin_usage__)
    if await UserCount.check_count(event.user_id, 'reimu', COUNT_PER_DAY_REIMU):
        await reimu.finish('今天已经没车了，请明天再来...', at_sender=True)
    if _ulmt.check(event.user_id):
        await reimu.finish('您还没下车呢，请稍等...', at_sender=True)
    _ulmt.set_True(event.user_id)
    msg = get_message_text(event.json())
    args = msg.split(" ")
    if msg in ['!', '！', '?', '？', ',', '，', '.', '。']:
        await reimu.finish(__plugin_usage__)
    if msg:
        if len(args) > 1 and is_number(args[0]):
            state['keyword'] = args[1]
            state['page'] = args[0]
        else:
            state['keyword'] = msg
            state['page'] = 1


@reimu.got('keyword', '你的目的地是哪？')
async def _(bot: Bot, event: Event, state: T_State):
    try:
        keyword = state['keyword']
        page = state['page']
        print(keyword, page)
        await UserCount.add_count(event.user_id, 'reimu')
        await reimu.send('已经帮你关好车门了', at_sender=True)
        reimu_report = await from_reimu_get_info(keyword, page)
        if reimu_report:
            await reimu.send(reimu_report)
        else:
            logger.error("Not found reimuInfo")
            await reimu.send("没找着")
        _ulmt.set_False(event.user_id)
    except:
        _ulmt.set_False(event.user_id)


@scheduler.scheduled_job(
    'cron',
    # year=None,
    # month=None,
    # day=None,
    # week=None,
    # day_of_week="mon,tue,wed,thu,fri",
    hour=0,
    minute=1,
    # second=None,
    # start_date=None,
    # end_date=None,
    # timezone=None,
)
async def _():
    await UserCount.reset_count()


