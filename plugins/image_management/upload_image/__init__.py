from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from configs.config import Config
from utils.utils import get_message_img
from .data_source import upload_image_to_local
from nonebot.params import CommandArg, Arg, ArgStr
from typing import List


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
__plugin_settings__ = {
    "admin_level": Config.get_config("image_management", "UPLOAD_IMAGE_LEVEL")
}

upload_img = on_command("上传图片", rule=to_me(), priority=5, block=True)

continuous_upload_img = on_command("连续上传图片", rule=to_me(), priority=5, block=True)

show_gallery = on_command("查看公开图库", priority=1, block=True)


@show_gallery.handle()
async def _():
    x = "公开图库列表：\n"
    for i, e in enumerate(Config.get_config("image_management", "IMAGE_DIR_LIST")):
        x += f"\t{i+1}.{e}\n"
    await show_gallery.send(x[:-1])


@upload_img.handle()
async def _(event: MessageEvent, state: T_State, arg: Message = CommandArg()):
    args = arg.extract_plain_text().strip()
    img_list = get_message_img(event.json())
    if args:
        if args in Config.get_config("image_management", "IMAGE_DIR_LIST"):
            state["path"] = args
    if img_list:
        state["img_list"] = arg


@upload_img.got(
    "path",
    prompt=f"请选择要上传的图库\n- "
    + "\n- ".join(Config.get_config("image_management", "IMAGE_DIR_LIST")),
)
@upload_img.got("img_list", prompt="图呢图呢图呢图呢！GKD！")
async def _(
    bot: Bot,
    event: MessageEvent,
    state: T_State,
    path: str = ArgStr("path"),
    img_list: Message = Arg("img_list"),
):
    if path not in Config.get_config("image_management", "IMAGE_DIR_LIST"):
        await upload_img.reject_arg("path", "此目录不正确，请重新输入目录！")
    if not get_message_img(img_list):
        await upload_img.reject_arg("img_list", "图呢图呢图呢图呢！GKD！")
    img_list = get_message_img(img_list)
    group_id = 0
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
    await upload_img.send(
        await upload_image_to_local(img_list, path, event.user_id, group_id)
    )


@continuous_upload_img.handle()
async def _(event: MessageEvent, state: T_State):
    path = get_message_img(event.json())
    if path in Config.get_config("image_management", "IMAGE_DIR_LIST"):
        state["path"] = path
    state["img_list"] = []


@continuous_upload_img.got(
    "path",
    prompt=f"请选择要上传的图库\n- "
    + "\n- ".join(Config.get_config("image_management", "IMAGE_DIR_LIST")),
)
@continuous_upload_img.got("img", prompt="图呢图呢图呢图呢！GKD！【发送‘stop’为停止】")
async def _(
    event: MessageEvent,
    state: T_State,
    img_list: List[str] = Arg("img_list"),
    path: str = ArgStr("path"),
    img: Message = Arg("img"),
):
    if path not in Config.get_config("image_management", "IMAGE_DIR_LIST"):
        await upload_img.reject_arg("path", "此目录不正确，请重新输入目录！")
    if not img.extract_plain_text() == "stop":
        img = get_message_img(img)
        if img:
            for i in img:
                img_list.append(i)
        await upload_img.reject_arg("img", "图再来！！【发送‘stop’为停止】")
    group_id = 0
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
    await continuous_upload_img.send(
        await upload_image_to_local(img_list, path, event.user_id, group_id)
    )
