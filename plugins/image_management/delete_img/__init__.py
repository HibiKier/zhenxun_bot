from configs.path_config import IMAGE_PATH, TEMP_PATH
from utils.message_builder import image
from services.log import logger
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from configs.config import DELETE_IMG_LEVEL
from configs.config import IMAGE_DIR_LIST
from utils.utils import is_number, cn2py, get_message_text
from pathlib import Path
import os

__zx_plugin_name__ = "删除图片 [Admin]"
__plugin_usage__ = """
usage：
    删除图库指定图片
    指令：
        删除图片 [图库] [id]
        查看图库
        示例：删除图片 美图 666
""".strip()
__plugin_des__ = "不好看的图片删掉删掉！"
__plugin_cmd__ = ["删除图片 [图库] [id]", "查看公开图库"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "admin_level": DELETE_IMG_LEVEL
}


delete_img = on_command("删除图片", priority=5, rule=to_me(), block=True)


@delete_img.args_parser
async def parse(bot: Bot, event: MessageEvent, state: T_State):
    if get_message_text(event.json()) in ["取消", "算了"]:
        await delete_img.finish("已取消操作..", at_sender=True)
    if state["_current_key"] in ["path"]:
        if get_message_text(event.json()) not in IMAGE_DIR_LIST:
            await delete_img.reject("此目录不正确，请重新输入目录！")
        state[state["_current_key"]] = get_message_text(event.json())
    if state["_current_key"] == "id":
        if not is_number(get_message_text(event.json())):
            await delete_img.reject("id不正确！请重新输入数字...")
        state[state["_current_key"]] = get_message_text(event.json())


@delete_img.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    raw_arg = get_message_text(event.json()).strip()
    if raw_arg:
        args = raw_arg.split(" ")
        if args[0] in ["帮助"]:
            await delete_img.finish(__plugin_usage__)
        if len(args) >= 2 and args[0] in IMAGE_DIR_LIST and is_number(args[1]):
            state["path"] = args[0]
            state["id"] = args[1]


@delete_img.got("path", prompt="请输入要删除的目标图库？")
@delete_img.got("id", prompt="请输入要删除的图片id？")
async def arg_handle(bot: Bot, event: MessageEvent, state: T_State):
    path = cn2py(state["path"])
    img_id = state["id"]
    # path = IMAGE_PATH + path
    path = Path(IMAGE_PATH) / path
    temp = Path(IMAGE_PATH) / "temp"
    max_id = len(os.listdir(path)) - 1
    if int(img_id) > max_id or int(img_id) < 0:
        await delete_img.finish(f"Id超过上下限，上限：{max_id}", at_sender=True)
    try:
        if os.path.exists(temp / "delete.jpg"):
            os.remove(temp / "delete.jpg")
        logger.info("删除图片 delete.jpg 成功")
    except Exception as e:
        logger.warning(f"删除图片 delete.jpg 失败 e{e}")
    try:
        os.rename(path / f"{img_id}.jpg", temp / "delete.jpg")
        logger.info(f"移动 {path}/{img_id}.jpg 移动成功")
    except Exception as e:
        logger.warning(f"{path}/{img_id}.jpg --> 移动失败 e:{e}")
    if not os.path.exists(path / f"{img_id}.jpg"):
        try:
            if int(img_id) != max_id:
                os.rename(path / f"{max_id}.jpg", path / f"{img_id}.jpg")
        except FileExistsError as e:
            logger.error(f"{path}/{max_id}.jpg 替换 {path}/{img_id}.jpg 失败 e:{e}")
        logger.info(f"{path}/{max_id}.jpg 替换 {path}/{img_id}.jpg 成功")
        logger.info(
            f"USER {event.user_id} GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}"
            f" -> id: {img_id} 删除成功"
        )
        await delete_img.finish(
            f"id: {img_id} 删除成功" + image("delete.jpg", TEMP_PATH), at_sender=True
        )
    await delete_img.finish(f"id: {img_id} 删除失败！")
