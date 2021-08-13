from nonebot import on_command
from configs.path_config import IMAGE_PATH
from services.log import logger
import os
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from utils.utils import get_message_imgs, get_message_text
import aiohttp
import aiofiles
from utils.utils import cn2py
from configs.config import IMAGE_DIR_LIST

__plugin_name__ = "上传图片"
__plugin_usage__ = (
    "上传图片帮助：\n\t"
    "1.查看列表 --> 指令: 上传图片 列表/目录\n\t"
    "2.上传图片 [序号] [图片], 即在相应目录下添加图片\n\t\t示例: 上传图片 1 [图片]"
)


upload_img = on_command("上传图片", rule=to_me(), priority=5, block=True)


@upload_img.args_parser
async def parse(bot: Bot, event: MessageEvent, state: T_State):
    if str(event.get_message()) in ["取消", "算了"]:
        await upload_img.finish("已取消操作..", at_sender=True)
    if state["_current_key"] in ["path"]:
        if str(event.get_message()) not in IMAGE_DIR_LIST:
            await upload_img.reject("此目录不正确，请重新输入目录！")
        state[state["_current_key"]] = str(event.get_message())
    if state["_current_key"] in ["imgs"]:
        if not get_message_imgs(event.json()):
            await upload_img.reject("图呢图呢图呢图呢！GKD！")
        state[state["_current_key"]] = get_message_imgs(event.json())


@upload_img.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    raw_arg = get_message_text(event.json())
    img_list = get_message_imgs(event.json())
    if raw_arg:
        if str(event.get_message()) in ["帮助"]:
            await upload_img.finish(__plugin_usage__)
        if raw_arg.split("[")[0] in IMAGE_DIR_LIST:
            state["path"] = raw_arg.split("[")[0]
        if img_list:
            state["imgs"] = img_list


@upload_img.got("path", prompt="要将图片上传至什么图库呢？")
@upload_img.got("imgs", prompt="图呢图呢图呢图呢！GKD！")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    path = IMAGE_PATH + cn2py(state["path"]) + '/'
    img_list = state["imgs"]
    img_id = len(os.listdir(path))
    failed_list = []
    success_id = ""
    async with aiohttp.ClientSession() as session:
        for img_url in img_list:
            try:
                async with session.get(img_url, timeout=7) as response:
                    if response.status == 200:
                        async with aiofiles.open(
                            path + str(img_id) + ".jpg", "wb"
                        ) as f:
                            await f.write(await response.read())
                            success_id += str(img_id) + "，"
                            img_id += 1
                    else:
                        failed_list.append(img_url)
                        logger.warning(f"图片：{img_url} 下载失败....")
            except TimeoutError as e:
                logger.warning(f"图片：{img_url} 下载超时....e:{e}")
                if img_url not in failed_list:
                    failed_list.append(img_url)
    failed_result = ""
    for img in failed_list:
        failed_result += str(img) + "\n"
    logger.info(
        f"USER {event.user_id}  GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}"
        f" 上传图片至 {state['path']} 共 {len(img_list)} 张，失败 {len(failed_list)} 张，id={success_id[:-1]}"
    )
    if failed_result:
        await upload_img.finish(
            f"这次一共为 {state['path']}库 添加了 {len(img_list) - len(failed_list)} 张图片\n"
            f"依次的Id为：{success_id[:-1]}\n"
            f"上传失败：{failed_result[:-1]}\n"
            f"小真寻感谢您对图库的扩充!WW",
            at_sender=True,
        )
    else:
        await upload_img.finish(
            f"这次一共为 {state['path']}库 添加了 {len(img_list)} 张图片\n"
            f"依次的Id为：{success_id[:-1]}\n"
            f"小真寻感谢您对图库的扩充!WW",
            at_sender=True,
        )
