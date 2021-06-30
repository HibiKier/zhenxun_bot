from nonebot import on_command
from .data_source import get_price, update_buff_cookie
from services.log import logger
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from utils.utils import UserExistLimiter, get_message_text


__plugin_name__ = '查询皮肤'
__plugin_usage__ = '查询皮肤帮助:\n\t' \
            '查询皮肤 [枪械名] [皮肤]\n\t' \
            '示例: 查询皮肤 awp 二西莫夫'


_ulmt = UserExistLimiter()


search_skin = on_command('查询皮肤', aliases={'皮肤查询'}, priority=5, block=True)


@search_skin.args_parser
async def parse(bot: Bot, event: Event, state: T_State):
    if get_message_text(event.json()) in ['取消', '算了']:
        await search_skin.finish("已取消操作..", at_sender=True)
    state[state["_current_key"]] = str(event.get_message())


@search_skin.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if str(event.get_message()) in ['帮助']:
        await search_skin.finish(__plugin_usage__)
    raw_arg = get_message_text(event.json())
    if _ulmt.check(event.user_id):
        await search_skin.finish('您有皮肤正在搜索，请稍等...', at_sender=True)
    if raw_arg:
        args = raw_arg.split(" ")
        if len(args) >= 2:
            state['name'] = args[0]
            state['skin'] = args[1]


@search_skin.got('name', prompt="要查询什么武器呢？")
@search_skin.got('skin', prompt="要查询该武器的什么皮肤呢？")
async def arg_handle(bot: Bot, event: Event, state: T_State):
    _ulmt.set_True(event.user_id)
    if state['name'] in ['ak', 'ak47']:
        state['name'] = 'ak-47'
    name = state['name'] + " | " + state['skin']
    try:
        result, status_code = await get_price(name)
    except FileNotFoundError:
        await search_skin.finish('请先对真寻说"设置cookie"来设置cookie！')
    if status_code in [996, 997, 998]:
        _ulmt.set_False(event.user_id)
        await search_skin.finish(result)
    if result:
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'}) 查询皮肤:" + name)
        _ulmt.set_False(event.user_id)
        await search_skin.finish(result)
    else:
        logger.info(f"USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'}"
                    f" 查询皮肤：{name} 没有查询到")
        _ulmt.set_False(event.user_id)
        await search_skin.finish("没有查询到哦，请检查格式吧")


update_buff_session = on_command("更新cookie", rule=to_me(), permission=SUPERUSER, priority=1)


@update_buff_session.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await update_buff_session.finish(update_buff_cookie(str(event.get_message())), at_sender=True)
