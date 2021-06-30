from nonebot import on_command, on_regex
from utils.utils import get_message_text, is_number, FreqLimiter
from nonebot.rule import to_me
from services.log import logger
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageEvent, GROUP
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from pathlib import Path
from configs.config import plugins2info_dict
from nonebot.message import run_preprocessor, IgnoredException
try:
    import ujson as json
except ModuleNotFoundError:
    import json

__plugin_name__ = '群权限'
__plugin_usage__ = '区分权限功能'

flmt = FreqLimiter(60)

group_level_data = Path() / 'data'/ 'manager' / 'group_level.json'
group_level_data.parent.mkdir(exist_ok=True, parents=True)
group_data = {}
if group_level_data.exists():
    group_data = json.load(open(group_level_data, 'r', encoding='utf8'))


@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent, state: T_State):
    if not isinstance(event, MessageEvent):
        return
    if matcher.type == 'message' and matcher.priority not in [1, 9]:
        if isinstance(event, GroupMessageEvent):
            if not group_data.get(str(event.group_id)):
                group_data[str(event.group_id)] = 5
            if plugins2info_dict.get(matcher.module):
                if plugins2info_dict[matcher.module]['level'] > group_data[str(event.group_id)]:
                    try:
                        if flmt.check(event.group_id):
                            flmt.start_cd(event.group_id)
                            await bot.send_group_msg(group_id=event.group_id, message='群权限不足...')
                    except Exception:
                        pass
                    raise IgnoredException('群权限不足')


add_group_level = on_command('修改群权限', priority=1, permission=SUPERUSER, block=True)
my_group_level = on_command('查看群权限', aliases={'群权限'}, priority=5, permission=GROUP, block=True)
what_up_group_level = on_regex('.*?(提高|提升|升高|增加|加上)(.*?)群权限.*?', rule=to_me(), priority=5, permission=GROUP, block=True)


@add_group_level.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if not msg:
        await add_group_level.finish('用法：修改群权限 [group] [level]')
    msg = msg.split(' ')
    if len(msg) < 2:
        await add_group_level.finish('参数不完全..[group] [level]')
    if is_number(msg[0]) and is_number(msg[1]):
        group_id = msg[0]
        level = int(msg[1])
    else:
        await add_group_level.finish('参数错误...group和level必须是数字..')
    if not group_data.get(group_id):
        group_data[group_id] = 5
    await add_group_level.send('修改成功...', at_sender=True)
    await bot.send_group_msg(group_id=int(group_id), message=f'管理员修改了此群权限：{group_data[group_id]} -> {level}')
    group_data[group_id] = level
    with open(group_level_data, 'w', encoding='utf8') as f:
        json.dump(group_data, f, ensure_ascii=False, indent=4)
    logger.info(f'{event.user_id} 修改了 {group_id} 的权限：{level}')


@my_group_level.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if group_data.get(str(event.group_id)):
        level = group_data[str(event.group_id)]
        tmp = ''
        for plugin in plugins2info_dict:
            if plugins2info_dict[plugin]['level'] > level:
                plugin_name = plugins2info_dict[plugin]['cmd'][0]
                if plugin_name == 'pixiv':
                    plugin_name = '搜图 p站排行'
                tmp += f'{plugin_name}\n'
        if tmp:
            tmp = '\n目前无法使用的功能：\n' + tmp
        await my_group_level.finish(f'当前群权限：{level}{tmp}')


@what_up_group_level.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await what_up_group_level.finish(f'[此功能用于防止内鬼，如果引起不便那真是抱歉了]\n'
                                     f'目前提高群权限的方法：\n'
                                     f'\t1.管理员修改权限')


