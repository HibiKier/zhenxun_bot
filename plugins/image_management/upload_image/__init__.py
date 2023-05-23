from typing import List

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageEvent
from nonebot.params import Arg, ArgStr, CommandArg
from nonebot.rule import to_me
from nonebot.typing import T_State

from configs.config import Config
from utils.depends import ImageList
from utils.utils import get_message_img

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
__plugin_settings__ = {
    "admin_level": Config.get_config("image_management", "UPLOAD_IMAGE_LEVEL")
}

upload_img = on_command("上传图片", rule=to_me(), priority=5, block=True)

continuous_upload_img = on_command("连续上传图片", rule=to_me(), priority=5, block=True)

show_gallery = on_command("查看公开图库", priority=1, block=True)


@show_gallery.handle()
async def _():
    image_dir_list = Config.get_config("image_management", "IMAGE_DIR_LIST")
    if not image_dir_list:
        await show_gallery.finish("未发现任何图库")
    x = "公开图库列表：\n"
    for i, e in enumerate(image_dir_list):
        x += f"\t{i+1}.{e}\n"
    await show_gallery.send(x[:-1])


@upload_img.handle()
async def _(
    event: MessageEvent,
    state: T_State,
    arg: Message = CommandArg(),
    img_list: List[str] = ImageList(),
):
    image_dir_list = Config.get_config("image_management", "IMAGE_DIR_LIST")
    if not image_dir_list:
        await show_gallery.finish("未发现任何图库")
    args = arg.extract_plain_text().strip()
    if args:
        if args in image_dir_list:
            state["path"] = args
    if img_list:
        state["img_list"] = arg
    state["dir_list"] = "\n-".join(image_dir_list)


@upload_img.got(
    "path",
    prompt=Message.template("请选择要上传的图库\n-{dir_list}"),
)
@upload_img.got("img_list", prompt="图呢图呢图呢图呢！GKD！")
async def _(
    bot: Bot,
    event: MessageEvent,
    state: T_State,
    path: str = ArgStr("path"),
    img_list: List[str] = ImageList(),
):
    image_dir_list = Config.get_config("image_management", "IMAGE_DIR_LIST") or []
    if path not in image_dir_list:
        await upload_img.reject_arg("path", "此目录不正确，请重新输入目录！")
    if not img_list:
        await upload_img.reject_arg("img_list", "图呢图呢图呢图呢！GKD！")
    group_id = 0
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
    await upload_img.send(
        await upload_image_to_local(img_list, path, event.user_id, group_id)
    )


@continuous_upload_img.handle()
async def _(
    event: MessageEvent,
    state: T_State,
    arg: Message = CommandArg(),
    img_list: List[str] = ImageList(),
):
    image_dir_list = Config.get_config("image_management", "IMAGE_DIR_LIST") or []
    path = arg.extract_plain_text().strip()
    if path in image_dir_list:
        state["path"] = path
    state["img_list"] = []
    state["dir_list"] = "\n-".join(image_dir_list)


@continuous_upload_img.got("path", prompt=Message.template("请选择要上传的图库\n-{dir_list}"))
@continuous_upload_img.got("img", prompt="图呢图呢图呢图呢！GKD！【发送‘stop’为停止】")
async def _(
    event: MessageEvent,
    state: T_State,
    collect_img_list: List[str] = Arg("img_list"),
    path: str = ArgStr("path"),
    img: Message = Arg("img"),
    img_list: List[str] = ImageList(),
):
    image_dir_list = Config.get_config("image_management", "IMAGE_DIR_LIST") or []
    if path not in image_dir_list:
        await upload_img.reject_arg("path", "此目录不正确，请重新输入目录！")
    if not img.extract_plain_text() == "stop":
        if img_list:
            for i in img_list:
                collect_img_list.append(i)
        await upload_img.reject_arg("img", "图再来！！【发送‘stop’为停止】")
    group_id = 0
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
    await continuous_upload_img.send(
        await upload_image_to_local(collect_img_list, path, event.user_id, group_id)
    )
