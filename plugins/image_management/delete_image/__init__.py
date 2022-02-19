from configs.path_config import IMAGE_PATH, TEMP_PATH
from utils.message_builder import image
from services.log import logger
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from utils.utils import is_number, cn2py
from configs.config import Config
from nonebot.params import CommandArg, Arg
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
    "admin_level": Config.get_config("image_management", "DELETE_IMAGE_LEVEL")
}


delete_img = on_command("删除图片", priority=5, rule=to_me(), block=True)


_path = IMAGE_PATH / "image_management"


@delete_img.handle()
async def _(state: T_State, arg: Message = CommandArg()):
    args = arg.extract_plain_text().strip().split()
    if args:
        if args[0] in Config.get_config("image_management", "IMAGE_DIR_LIST"):
            state["path"] = args[0]
        if len(args) > 1 and is_number(args[1]):
            state["id"] = args[1]


@delete_img.got("path", prompt="请输入要删除的目标图库？")
@delete_img.got("id", prompt="请输入要删除的图片id？")
async def arg_handle(
    event: MessageEvent,
    state: T_State,
    path: str = Arg("path"),
    img_id: str = Arg("id"),
):
    if path in ["取消", "算了"] or img_id in ["取消", "算了"]:
        await delete_img.finish("已取消操作...")
    if path not in Config.get_config("image_management", "IMAGE_DIR_LIST"):
        await delete_img.reject_arg("path", "此目录不正确，请重新输入目录！")
    if not is_number(img_id):
        await delete_img.reject_arg("id", "id不正确！请重新输入数字...")
    path = _path / cn2py(path)
    if not path.exists() and (path.parent.parent / cn2py(state["path"])).exists():
        path = path.parent.parent / cn2py(state["path"])
    max_id = len(os.listdir(path)) - 1
    if int(img_id) > max_id or int(img_id) < 0:
        await delete_img.finish(f"Id超过上下限，上限：{max_id}", at_sender=True)
    try:
        if (TEMP_PATH / "delete.jpg").exists():
            (TEMP_PATH / "delete.jpg").unlink()
        logger.info(f"删除{cn2py(state['path'])}图片 {img_id}.jpg 成功")
    except Exception as e:
        logger.warning(f"删除图片 delete.jpg 失败 e{e}")
    try:
        os.rename(path / f"{img_id}.jpg", TEMP_PATH / f"{event.user_id}_delete.jpg")
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
            f"id: {img_id} 删除成功" + image(TEMP_PATH / f"{event.user_id}_delete.jpg",), at_sender=True
        )
    await delete_img.finish(f"id: {img_id} 删除失败！")
