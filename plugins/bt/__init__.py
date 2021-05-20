from nonebot import on_command
from .data_source import get_bt_info
from services.log import logger
from nonebot.typing import T_State
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import PrivateMessageEvent
from util.utils import get_message_text
from nonebot.adapters.cqhttp.permission import PRIVATE
from util.utils import UserExistLimiter

__plugin_name__ = '磁力搜索'
__plugin_usage__ = r"""
* 请各位使用后不要转发 *
* 有时可能搜不到，再试一次就行了 *
参数: -U（时间） -H（热度） -S（大小）
     -V（仅视频） -P（仅图片） -A（仅压缩包）
     -R （R18懂的都懂）
     num（页数， 如果不知道页数请不要填，并且是倒叙，比如页数总数是29，你想查看第一页的内容， 就使用 bt 29 xxx）
-按相关度检索(默认)
bt [关键词]
-按更新时间检索(参数不区分大小写，但要注意空格)
bt -U [关键词]
-搜索第10页数
bt 10（倒着） [关键词]
""".strip()

_ulmt = UserExistLimiter()

bt = on_command('bt', permission=PRIVATE, priority=5, block=True)


@bt.args_parser
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    if str(event.get_message()) in ['取消', '算了']:
        await bt.finish("已取消操作..", at_sender=True)
    msg = get_message_text(event.json())
    if not msg:
        await bt.reject('你想搜索什么呢？', at_sender=True)
    mp = msg.split(" ")
    if len(mp) > 1:
        args = ''
        for i in range(len(mp) - 1):
            args += mp[i] + ' '
        state['args'] = args
        state['bt'] = mp[1]
    else:
        state['bt'] = get_message_text(event.json())
        state['args'] = ''


@bt.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    if get_message_text(event.json()) in ['帮助'] or str(event.get_message()) == '':
        await bt.finish(__plugin_usage__)
    if _ulmt.check(event.user_id):
        await bt.finish('您有bt任务正在进行，请等待结束.', at_sender=True)
    mp = get_message_text(event.json()).split(" ")
    if len(mp) > 1:
        args = ''
        for i in range(len(mp) - 1):
            args += mp[i] + ' '
        state['args'] = args.strip()
        state['bt'] = mp[-1]
    else:
        state['bt'] = get_message_text(event.json())
        state['args'] = ''


@bt.got('bt', prompt='虚空磁力？查什么GKD')
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    _ulmt.set_True(event.user_id)
    keyword = state['bt']
    args = state['args']
    await bt.send('开始搜索....', at_sender=True)
    try:
        if args.find('-R') == -1 and args.find('-r') == -1:
            bt_report = await get_bt_info(keyword, args)
        else:
            bt_report = await get_bt_info(keyword, args, '0')
        if bt_report:
            if len(bt_report.split("\n")) < 2:
                await bt.finish(bt_report + '搜索失败了，再试一次也许能成', at_sender=True)
            else:
                await bt.send("如果有页数没资源请再试一次\n" + bt_report)
                logger.info(
                    f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
                    f" 搜索bt {args} {keyword}")
        else:
            logger.error("没查询到资源")
            await bt.send("没有查询到资源（也有可能是超时，再试一次？）", at_sender=True)
        _ulmt.set_False(event.user_id)
    except Exception as e:
        _ulmt.set_False(event.user_id)
        await bt.send("bt出错啦，再试一次？", at_sender=True)
        logger.info(f'bt {keyword} 出错 e:{e}')
