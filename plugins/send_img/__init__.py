from nonebot import on_command, on_keyword
from configs.path_config import IMAGE_PATH
from util.init_result import image
import os
import random
from util.utils import is_number
from services.log import logger
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from util.utils import FreqLimiter, cn2py
from models.group_remind import GroupRemind
from configs.config import IMAGE_DIR_LIST


__plugin_name__ = '壁纸/萝莉/美图'
__plugin_usage__ = '用法： 发送"壁纸/萝莉/美图", 回复图片，后添加id获得指定图片'

_flmt = FreqLimiter(1)

IMAGE_DIR_LIST.remove('色图')
cmd = set(IMAGE_DIR_LIST)

# print(cmd)

send_img = on_command("img", aliases=cmd, priority=5, block=True)


@send_img.handle()
async def _(bot: Bot, event: Event, state: T_State):
    img_id = str(event.get_message())
    if img_id in ['帮助']:
        await send_img.finish(__plugin_usage__)
    path = cn2py(state["_prefix"]["raw_command"]) + '/'
    if not os.path.exists(IMAGE_PATH + path):
        logger.warning(f'未找到 {path} 文件夹，调用取消!')
        return
    length = len(os.listdir(IMAGE_PATH + path)) - 1
    if length == 0:
        logger.warning(f'图库 {path} 为空，调用取消！')
        return
    index = img_id if img_id else str(random.randint(0, length))
    if not is_number(index):
        await send_img.finish("id错误！")
    if int(index) > length or int(index) < 0:
        await send_img.finish(f"超过当前上下限！({length - 1})")
    result = image(f'{index}.jpg', path)
    if result:
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'}) 发送{path}:" + result)
        await send_img.finish(f"id：{index}" + result)
    else:
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'}) 发送 {path} 失败")
        await send_img.finish(f"不想给你看Ov|")


pa = on_keyword({"爬"}, priority=1, block=True)


@pa.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if await GroupRemind.get_status(event.group_id, 'pa'):
        try:
            if str(event.get_message()[:2]) in ['开启', '关闭']:
                return
        except:
            return
        if not _flmt.check(event.user_id):
            return
        _flmt.start_cd(event.user_id)
        await pa.finish(image(random.choice(os.listdir(IMAGE_PATH + "pa")), 'pa'))
