from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent

from configs.config import IMAGE_DIR_LIST
from utils.utils import get_message_imgs, get_message_text
from .data_source import upload_image_to_local

__plugin_name__ = "上传图片"
__plugin_usage__ = (
    "上传图片帮助：\n\t"
    "1.查看列表 --> 指令: 上传图片 列表/目录\n\t"
    "2.上传图片 [序号] [图片], 即在相应目录下添加图片\n\t\t示例: 上传图片 1 [图片]"
)

upload_img = on_command("上传图片", rule=to_me(), priority=5, block=True)

continuous_upload_img = on_command('连续上传图片', rule=to_me(), priority=5, block=True)


@upload_img.args_parser
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if msg in ["取消", "算了"]:
        await upload_img.finish("已取消操作..", at_sender=True)
    if state["_current_key"] in ["path"]:
        if msg not in IMAGE_DIR_LIST:
            await upload_img.reject("此目录不正确，请重新输入目录！")
        state['path'] = msg
    if state["_current_key"] in ["imgs"]:
        if not get_message_imgs(event.json()):
            await upload_img.reject("图呢图呢图呢图呢！GKD！")
        state['imgs'] = get_message_imgs(event.json())


@upload_img.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    raw_arg = get_message_text(event.json())
    img_list = get_message_imgs(event.json())
    if raw_arg:
        if raw_arg in IMAGE_DIR_LIST:
            state["path"] = raw_arg
        if img_list:
            state["imgs"] = img_list


@upload_img.got('path', prompt='要将图片上传至什么图库呢？')
async def _(bot: Bot, event: MessageEvent, state: T_State):
    pass


@upload_img.got("imgs", prompt="图呢图呢图呢图呢！GKD！")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    path = state['path']
    img_list = state['imgs']
    group_id = 0
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
    await upload_img.send(await upload_image_to_local(img_list, path, event.user_id, group_id))


@continuous_upload_img.args_parser
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if str(event.get_message()) in ["取消", "算了"]:
        await continuous_upload_img.finish("已取消操作..", at_sender=True)
    if state["_current_key"] in ["path"]:
        if str(event.get_message()) not in IMAGE_DIR_LIST:
            await continuous_upload_img.reject("此目录不正确，请重新输入目录！")
        state[state["_current_key"]] = str(event.get_message())
    else:
        if get_message_text(event.json()) not in ['stop']:
            img = get_message_imgs(event.json())
            if img:
                state['tmp'].extend(img)
            await continuous_upload_img.reject('图再来！！')
        else:
            state['imgs'] = state['tmp']


@continuous_upload_img.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    path = get_message_imgs(event.json())
    if path in IMAGE_DIR_LIST:
        state['path'] = path
        await continuous_upload_img.send('图来！！')
    state['tmp'] = []


@continuous_upload_img.got("path", prompt="要将图片上传至什么图库呢？")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    pass


@continuous_upload_img.got("imgs", prompt="图呢图呢图呢图呢！GKD！")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    path = state['path']
    img_list = state['imgs']
    group_id = 0
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
    await continuous_upload_img.send(await upload_image_to_local(img_list, path, event.user_id, group_id))

