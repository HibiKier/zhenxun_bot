from nonebot import on_notice, on_request
from configs.path_config import IMAGE_PATH, DATA_PATH
from util.init_result import image
import os
import random
from models.group_member_info import GroupInfoUser
from datetime import datetime
from services.log import logger
from models.group_remind import GroupRemind
from nonebot.adapters.cqhttp import Bot, GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent, GroupRequestEvent
from nonebot.adapters.cqhttp.exception import ActionFailed
from pathlib import Path
from nonebot import require
try:
    import ujson as json
except ModuleNotFoundError:
    import json


__plugin_name__ = '群事件处理 [Hidden]'

__usage__ = '用法：无'


export = require("admin_bot_manage")

# 群员增加处理
group_increase_handle = on_notice(priority=5)
# 群员减少处理
group_decrease_handle = on_notice(priority=5)
# （群管理）加群同意请求
add_group = on_request(priority=5)


@group_increase_handle.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent, state: dict):
    if event.user_id == int(bot.self_id):
        await export.update_member_info(event.group_id)
    else:
        join_time = datetime.now()
        user_info = await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id)
        if await GroupInfoUser.insert(
                user_info['user_id'],
                user_info['group_id'],
                user_info['nickname'],
                join_time,
        ):
            logger.info(f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新成功")
        else:
            logger.info(f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新失败")
        if await GroupRemind.get_status(event.group_id, 'hy'):
            msg = ''
            img = ''
            at_flag = False
            custom_welcome_msg_json = Path() / "data" / "custom_welcome_msg" / "custom_welcome_msg.json"
            if custom_welcome_msg_json.exists():
                data = json.load(open(custom_welcome_msg_json, 'r'))
                if data.get(str(event.group_id)):
                    msg = data[str(event.group_id)]
                    if msg.find('[at]') != -1:
                        msg = msg.replace('[at]', '')
                        at_flag = True
            if os.path.exists(DATA_PATH + f'custom_welcome_msg/{event.group_id}.jpg'):
                img = image(abspath=DATA_PATH + f'custom_welcome_msg/{event.group_id}.jpg')
            if msg or img:
                await group_increase_handle.send("\n" + msg + img, at_sender=at_flag)
            else:
                await group_increase_handle.send(
                    '新人快跑啊！！本群现状↓（快使用自定义！）' + image(random.choice(os.listdir(IMAGE_PATH + "qxz/")), "qxz"))


@group_decrease_handle.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent, state: dict):
    # 真寻被踢出群
    if event.sub_type == 'kick_me':
        group_id = event.group_id
        operator_id = event.operator_id
        try:
            operator_name = (await GroupInfoUser.select_member_info(event.operator_id, event.group_id)).user_name
        except AttributeError:
            operator_name = 'None'
        coffee = int(list(bot.config.superusers)[0])
        await bot.send_private_msg(
            user_id=coffee,
            message=f'报告..\n'
                    f'我被 {operator_name}({operator_id})\n'
                    f'踢出了 {group_id}')
        return
    try:
        user_name = (await GroupInfoUser.select_member_info(event.user_id, event.group_id)).user_name
    except AttributeError:
        user_name = str(event.user_id)
    rst = ''
    if event.sub_type == 'leave':
        rst = f'{user_name}离开了我们...'
    if event.sub_type == 'kick':
        try:
            operator_name = (await GroupInfoUser.select_member_info(event.operator_id, event.group_id)).user_name
        except AttributeError:
            operator_name = event.operator_id
        rst = f'{user_name} 被 {operator_name} 送走了.'
    try:
        await group_decrease_handle.send(f"{rst}")
    except ActionFailed:
        return
    if await GroupInfoUser.delete_member_info(event.user_id, event.group_id):
        logger.info(f"用户{user_name}, qq={event.user_id} 所属{event.group_id} 删除成功")
    else:
        logger.info(f"用户{user_name}, qq={event.user_id} 所属{event.group_id} 删除失败")


@add_group.handle()
async def _(bot: Bot, event: GroupRequestEvent, state: dict):
    pass
    # user_info = await bot._get_vip_info(user_id=event.user_id)
    # if user_info['level'] > 16:
    #     bot.set













