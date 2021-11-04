from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent

from configs.config import Config
from utils.utils import get_message_imgs, get_message_text
from .data_source import upload_image_to_local


__zx_plugin_name__ = "上传图片 [Admin]"
__plugin_usage__ = """
usage：
    上传图片至指定图库
    指令：
        查看图库
        上传图片 [图库] [图片]
        连续上传图片 [图库]
        示例：上传图片 美图 [图片]
    * 连续上传图片可以通过发送 “stop” 表示停止收集发送的图片，可以开始上传 *
""".strip()
__plugin_des__ = "指定图库图片上传"
__plugin_cmd__ = ["上传图片 [图库] [图片]", "连续上传图片 [图库]", "查看公开图库"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {"admin_level": Config.get_config("image_management", "DELETE_IMAGE_LEVEL")}

upload_img = on_command("上传图片", rule=to_me(), priority=5, block=True)

continuous_upload_img = on_command("连续上传图片", rule=to_me(), priority=5, block=True)

show_gallery = on_command("查看公开图库", priority=1, block=True)


@show_gallery.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    x = '公开图库列表：\n'
    for i, e in enumerate(Config.get_config("image_management", "IMAGE_DIR_LIST")):
        x += f'\t{i+1}.{e}\n'
    await show_gallery.send(x[:-1])


@upload_img.args_parser
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if msg in ["取消", "算了"]:
        await upload_img.finish("已取消操作..", at_sender=True)
    if state["_current_key"] in ["path"]:
        if msg not in Config.get_config("image_management", "IMAGE_DIR_LIST"):
            await upload_img.reject("此目录不正确，请重新输入目录！")
        state["path"] = msg
    if state["_current_key"] in ["imgs"]:
        if not get_message_imgs(event.json()):
            await upload_img.reject("图呢图呢图呢图呢！GKD！")
        state["imgs"] = get_message_imgs(event.json())


@upload_img.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    raw_arg = get_message_text(event.json())
    img_list = get_message_imgs(event.json())
    if raw_arg:
        if raw_arg in Config.get_config("image_management", "IMAGE_DIR_LIST"):
            state["path"] = raw_arg
        if img_list:
            state["imgs"] = img_list


@upload_img.got("path", prompt="要将图片上传至什么图库呢？")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    pass


@upload_img.got("imgs", prompt="图呢图呢图呢图呢！GKD！")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    path = state["path"]
    img_list = state["imgs"]
    group_id = 0
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
    await upload_img.send(
        await upload_image_to_local(img_list, path, event.user_id, group_id)
    )


@continuous_upload_img.args_parser
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if str(event.get_message()) in ["取消", "算了"]:
        await continuous_upload_img.finish("已取消操作..", at_sender=True)
    if state["_current_key"] in ["path"]:
        if str(event.get_message()) not in Config.get_config("image_management", "IMAGE_DIR_LIST"):
            await continuous_upload_img.reject("此目录不正确，请重新输入目录！")
        state[state["_current_key"]] = str(event.get_message())
    else:
        if get_message_text(event.json()) not in ["stop"]:
            img = get_message_imgs(event.json())
            if img:
                state["tmp"].extend(img)
            await continuous_upload_img.reject("图再来！！")
        else:
            state["imgs"] = state["tmp"]


@continuous_upload_img.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    path = get_message_imgs(event.json())
    if path in Config.get_config("image_management", "IMAGE_DIR_LIST"):
        state["path"] = path
        await continuous_upload_img.send("图来！！")
    state["tmp"] = []


@continuous_upload_img.got("path", prompt="要将图片上传至什么图库呢？")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    pass


@continuous_upload_img.got("imgs", prompt="图呢图呢图呢图呢！GKD！")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    path = state["path"]
    img_list = state["imgs"]
    group_id = 0
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
    await continuous_upload_img.send(
        await upload_image_to_local(img_list, path, event.user_id, group_id)
    )
