from services.log import logger
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from configs.config import Config
from utils.utils import is_number, cn2py
from configs.path_config import IMAGE_PATH
from nonebot.params import CommandArg, ArgStr
import os

__zx_plugin_name__ = "移动图片 [Admin]"
__plugin_usage__ = """
usage：
    图库间的图片移动操作
    指令：
        移动图片 [源图库] [目标图库] [id]
        查看图库
        示例：移动图片 萝莉 美图 234
""".strip()
__plugin_des__ = "图库间的图片移动操作"
__plugin_cmd__ = ["移动图片 [源图库] [目标图库] [id]", "查看公开图库"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "admin_level": Config.get_config("image_management", "MOVE_IMAGE_LEVEL")
}


move_img = on_command("移动图片", priority=5, rule=to_me(), block=True)


_path = IMAGE_PATH / "image_management"


@move_img.handle()
async def _(state: T_State, arg: Message = CommandArg()):
    args = arg.extract_plain_text().strip().split()
    if args:
        if n := len(args):
            if args[0] in Config.get_config("image_management", "IMAGE_DIR_LIST"):
                state["source_path"] = args[0]
        if n > 1:
            if args[1] in Config.get_config("image_management", "IMAGE_DIR_LIST"):
                state["destination_path"] = args[1]
        if n > 2 and is_number(args[2]):
            state["id"] = args[2]


@move_img.got("source_path", prompt="要从哪个图库移出？")
@move_img.got("destination_path", prompt="要移动到哪个图库？")
@move_img.got("id", prompt="要移动的图片id是？")
async def _(
    event: MessageEvent,
    source_path: str = ArgStr("source_path"),
    destination_path: str = ArgStr("destination_path"),
    img_id: str = ArgStr("id"),
):
    if (
        source_path in ["取消", "算了"]
        or img_id in ["取消", "算了"]
        or destination_path in ["取消", "算了"]
    ):
        await move_img.finish("已取消操作...")
    if source_path not in Config.get_config("image_management", "IMAGE_DIR_LIST"):
        await move_img.reject_arg("source_path", "移除目录不正确，请重新输入！")
    if destination_path not in Config.get_config("image_management", "IMAGE_DIR_LIST"):
        await move_img.reject_arg("destination_path", "移入目录不正确，请重新输入！")
    if not is_number(img_id):
        await move_img.reject_arg("id", "id不正确！请重新输入数字...")
    source_path = _path / cn2py(source_path)
    destination_path = _path / cn2py(destination_path)
    if not source_path.exists():
        if (source_path.parent.parent / cn2py(source_path.name)).exists():
            source_path = source_path.parent.parent / cn2py(source_path.name)
    if not destination_path.exists():
        if (destination_path.parent.parent / cn2py(destination_path.name)).exists():
            source_path = destination_path.parent.parent / cn2py(destination_path.name)
    source_path.mkdir(exist_ok=True, parents=True)
    destination_path.mkdir(exist_ok=True, parents=True)
    if not len(os.listdir(source_path)):
        await move_img.finish(f"{source_path}图库中没有任何图片，移动失败。")
    max_id = len(os.listdir(source_path)) - 1
    des_max_id = len(os.listdir(destination_path))
    if int(img_id) > max_id or int(img_id) < 0:
        await move_img.finish(f"Id超过上下限，上限：{max_id}", at_sender=True)
    try:
        move_file = source_path / f"{img_id}.jpg"
        move_file.rename(destination_path / f"{des_max_id}.jpg")
        logger.info(
            f"移动 {source_path}/{img_id}.jpg ---> {destination_path}/{des_max_id} 移动成功"
        )
    except Exception as e:
        logger.warning(
            f"移动 {source_path}/{img_id}.jpg ---> {destination_path}/{des_max_id} 移动失败 e:{e}"
        )
        await move_img.finish(f"移动图片id：{img_id} 失败了...", at_sender=True)
    if max_id > 0:
        try:
            rep_file = source_path / f"{max_id}.jpg"
            rep_file.rename(source_path / f"{img_id}.jpg")
            logger.info(f"{source_path}/{max_id}.jpg 替换 {source_path}/{img_id}.jpg 成功")
        except Exception as e:
            logger.warning(
                f"{source_path}/{max_id}.jpg 替换 {source_path}/{img_id}.jpg 失败 e:{e}"
            )
            await move_img.finish(f"替换图片id：{max_id} -> {img_id} 失败了...", at_sender=True)
    logger.info(
        f"USER {event.user_id} GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'} ->"
        f" {source_path} --> {destination_path} (id：{img_id}) 移动图片成功"
    )
    await move_img.finish(f"移动图片 id：{img_id} --> id：{des_max_id}成功", at_sender=True)
