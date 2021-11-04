import os
from services.log import logger
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from configs.config import Config
from utils.utils import is_number, cn2py
from configs.path_config import IMAGE_PATH
from pathlib import Path


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


@move_img.args_parser
async def parse(bot: Bot, event: MessageEvent, state: T_State):
    if str(event.get_message()) in ["取消", "算了"]:
        await move_img.finish("已取消操作..", at_sender=True)
    if state["_current_key"] in ["source_path", "destination_path"]:
        if str(event.get_message()) not in Config.get_config(
            "image_management", "IMAGE_DIR_LIST"
        ):
            await move_img.reject("此目录不正确，请重新输入目录！")
        state[state["_current_key"]] = str(event.get_message())
    if state["_current_key"] == "id":
        if not is_number(str(event.get_message())):
            await move_img.reject("id不正确！请重新输入数字...")
        state[state["_current_key"]] = str(event.get_message())


@move_img.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    raw_arg = str(event.get_message()).strip()
    if raw_arg:
        args = raw_arg.split(" ")
        if args[0] in ["帮助"]:
            await move_img.finish(__plugin_usage__)
        if (
            len(args) >= 3
            and args[0] in Config.get_config("image_management", "IMAGE_DIR_LIST")
            and args[1] in Config.get_config("image_management", "IMAGE_DIR_LIST")
            and is_number(args[2])
        ):
            state["source_path"] = args[0]
            state["destination_path"] = args[1]
            state["id"] = args[2]
        else:
            await move_img.finish("参数错误，请重试", at_sender=True)


@move_img.got("source_path", prompt="要从哪个图库移出？")
@move_img.got("destination_path", prompt="要移动到哪个图库？")
@move_img.got("id", prompt="要移动的图片id是？")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    img_id = state["id"]
    source_path = Path(IMAGE_PATH) / cn2py(state["source_path"])
    destination_path = Path(IMAGE_PATH) / cn2py(state["destination_path"])
    destination_path.mkdir(parents=True, exist_ok=True)
    max_id = len(os.listdir(source_path)) - 1
    des_max_id = len(os.listdir(destination_path))
    if int(img_id) > max_id or int(img_id) < 0:
        await move_img.finish(f"Id超过上下限，上限：{max_id}", at_sender=True)
    try:
        os.rename(source_path / f"{img_id}.jpg", destination_path / f"{des_max_id}.jpg")
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
            os.rename(source_path / f"{max_id}.jpg", source_path / f"{img_id}.jpg")
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
