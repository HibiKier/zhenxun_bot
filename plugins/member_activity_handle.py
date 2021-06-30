from nonebot import on_message, on_command
import time
from utils.utils import scheduler, get_bot, get_message_text, is_number, get_message_at
from models.group_member_info import GroupInfoUser
from services.log import logger
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, GROUP
from nonebot.typing import T_State
from pathlib import Path
from configs.path_config import DATA_PATH
try:
    import ujson as json
except ModuleNotFoundError:
    import json

__plugin_name__ = '群员发言检测 [Hidden]'


check_activity = on_message(priority=1, permission=GROUP, block=False)

show_setting = on_command('群员活跃检测设置', permission=GROUP, priority=1, block=True)

set_check_time = on_command('设置群员活跃检测时长', permission=GROUP, priority=1, block=True)

set_white_list = on_command('添加群员活跃检测白名单', aliases={'移除群员活跃检测白名单'}, permission=GROUP, priority=1, block=True)

show_white_list = on_command('查看群员活跃检测白名单', permission=GROUP, priority=1, block=True)

_file = Path(f'{DATA_PATH}/member_activity_check.json')

try:
    data = json.load(open(_file, 'r', encoding='utf8'))
except (FileNotFoundError, ValueError, TypeError):
    data = {
        'check_time': time.time()
    }


@check_activity.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group = str(event.group_id)
    user_id = str(event.user_id)
    now = time.time()
    if not data.get(group):
        await _init_group_member_info(bot, group)
    data[group]['data'][user_id] = now
    if now - data['check_time'] > 10 * 60:
        data['check_time'] = now
        with open(_file, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info('群员发言时间检测存储数据成功....')


@set_check_time.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if not is_number(msg):
        await set_check_time.finish('请检查输入是否是数字....', at_sender=True)
    group = str(event.group_id)
    if not data.get(group):
        await _init_group_member_info(bot, group)
    data[group]['check_time_day'] = int(msg)
    await set_check_time.send(f'设置群员活跃检测时长成功：{msg} 天\n【设置为 0 即为关闭】')
    with open(_file, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logger.info(f'USER {event.user_id} GROUP {event.group_id} 设置群员活跃检测时长：{msg}')


@set_white_list.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group = str(event.group_id)
    at = get_message_at(event.json())
    if not data.get(group):
        await _init_group_member_info(bot, group)
    if at:
        rst = ''
        if state["_prefix"]["raw_command"] == '添加群员活跃检测白名单':
            for user in at:
                try:
                    user_name = (await GroupInfoUser.select_member_info(int(user), event.group_id)).user_name
                except AttributeError:
                    user_name = str(user)
                if str(user) not in data[group]['white_list']:
                    rst += f'{user_name} '
                    data[group]['white_list'].append(str(user))
                else:
                    await set_white_list.send(f'{user_name} 已在群员活跃检测白名单中...')
            rst = f'已将\n{rst}\n等添加入群员活跃检测白名单'
        else:
            for user in at:
                try:
                    user_name = (await GroupInfoUser.select_member_info(int(user), event.group_id)).user_name
                except AttributeError:
                    user_name = str(user)
                if str(user) in data[group]['white_list']:
                    rst += f'{user_name} '
                    data[group]['white_list'].remove(str(user))
                else:
                    await set_white_list.send(f'{user_name} 未在群员活跃检测白名单中...')
            rst = f'已将 \n{rst}\n等添移除群员活跃检测白名单'
        await set_white_list.send(rst, sender=True)
        logger.info(f'群员活跃检测白名单变动 USER {event.user_id}：{rst}')
        with open(_file, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        await set_white_list.finish('添加群员活跃检测白名单时请艾特对象！', at_sender=True)


@show_white_list.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group = str(event.group_id)
    if not data.get(group):
        await _init_group_member_info(bot, group)
    if data[group]['white_list']:
        user_name_list = []
        for user in data[group]['white_list']:
            try:
                user_name = (await GroupInfoUser.select_member_info(int(user), event.group_id)).user_name
            except AttributeError:
                user_name = str(user)
            user_name_list.append(user_name)
        rst = ''
        for i in range(len(user_name_list)):
            rst += f'{user_name_list[i]}({data[group]["white_list"][i]})\n'
        await show_white_list.send(rst)
    else:
        await show_white_list.finish('群员活跃检测白名单中没有任何用户...')


@show_setting.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group = str(event.group_id)
    user_name_list = []
    if not data.get(group):
        await _init_group_member_info(bot, group)
    if data[group]['white_list']:
        for user in data[group]['white_list']:
            try:
                user_name = (await GroupInfoUser.select_member_info(int(user), event.group_id)).user_name
            except AttributeError:
                user_name = str(user)
            user_name_list.append(user_name)
    await show_setting.send(f'群员活跃检测：\n'
                            f'检测天数：{data[group]["check_time_day"]}\n'
                            f'白名单：{user_name_list}\n'
                            f'【检测天数=0时为关闭】')


@scheduler.scheduled_job(
    'cron',
    hour=7,
    minute=1,
)
async def _():
    bot = get_bot()
    now = time.time()
    rst = '群员发言时间检测：\n'
    for group in data.keys():
        if group != 'check_time':
            member_list = await bot.get_group_member_list(group_id=int(group), self_id=int(bot.self_id))
            member_list = [x['user_id'] for x in member_list]
            for user in member_list:
                if user not in data[group]['data']:
                    data[group][str(user)] = now
            logger.info('群员活跃检测：自动更新群员完成...')
        if group != 'check_time' and data[group]['check_time_day'] > 0:
            for user in list(data[group]['data'].keys()):
                user = str(user)
                if user not in data[group]['white_list'] and \
                        now - data[group]['data'][user] > data[group]['check_time_day'] * 24 * 60 * 60:
                    try:
                        # await bot.set_group_kick(group_id=int(group), user_id=int(user))
                        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data[group]['data'][user]))
                        try:
                            user_name = (await GroupInfoUser.select_member_info(int(user), int(group))).user_name
                        except AttributeError:
                            user_name = user
                        rst += f'检测 {user_name}({user}) 上次发言时间过久：\n时间：{t}\n'
                        # await bot.send_group_msg(group_id=int(group),
                        #                          message=f'群员发言时间检测：检测 {user_name}({user}) 上次'
                        #                                  f'发言时间过久：..\n时间：{t}..')
                        del data[group]['data'][user]
                    except Exception as e:
                        logger.warning(f'群员活跃检测：{user} 踢出失败，疑真寻不是管理或对方是管理或不在群内...e：{e}')
        if rst:
            await bot.send_group_msg(group_id=int(group),
                                     message=rst[:-1])
    with open(_file, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


async def _init_group_member_info(bot: Bot, group: str):
    global data
    now = time.time()
    data[group] = {}
    data[group]['data'] = {}
    data[group]['white_list'] = []
    data[group]['check_time_day'] = 0
    member_list = await bot.get_group_member_list(group_id=int(group), self_id=int(bot.self_id))
    member_list = [x['user_id'] for x in member_list]
    for user in member_list:
        data[group]['data'][str(user)] = now
    with open(_file, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)











