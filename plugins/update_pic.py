from nonebot import on_command
from PIL import Image, ImageFilter
from utils.message_builder import image
from configs.path_config import IMAGE_PATH
from services.log import logger
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from utils.utils import get_message_imgs
import aiofiles
import aiohttp
from utils.utils import is_number, get_message_text
from utils.image_utils import CreateImg, pic2b64
from configs.config import NICKNAME
import cv2
import numpy as np


__zx_plugin_name__ = "各种图片简易操作"
__plugin_usage__ = """
usage：
    简易的基础图片操作，输入 指定操作 或 序号 来进行选择
    指令：
        1.修改尺寸 [宽] [高] [图片]
        2.等比压缩 [比例] [图片]
        3.旋转图片 [角度] [图片]
        4.水平翻转 [图片]
        5.铅笔滤镜 [图片]
        6.模糊效果 [图片]
        7.锐化效果 [图片]
        8.高斯模糊 [图片]
        9.边缘检测 [图片]
        10.底色替换 [红/蓝] [红/蓝/白/绿/黄] [图片]
        示例：图片修改尺寸 100 200 [图片]
        示例：图片 2 0.3 [图片]
""".strip()
__plugin_des__ = "10种快捷的图片简易操作"
__plugin_cmd__ = [
    "改图 修改尺寸 [宽] [高] [图片]",
    "改图 等比压缩 [比例] [图片]",
    "改图 旋转图片 [角度] [图片]",
    "改图 水平翻转 [图片]",
    "改图 铅笔滤镜 [图片]",
    "改图 模糊效果 [图片]",
    "改图 锐化效果 [图片]",
    "改图 高斯模糊 [图片]",
    "改图 边缘检测 [图片]",
    "改图 底色替换 [红/蓝] [红/蓝/白/绿/黄] [图片]",
]
__plugin_type__ = ("一些工具", 1)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["修改图片", "改图", "操作图片"],
}

# IMAGE_LOCAL = IMAGE_PATH + "temp/{}_update.png"
method_flag = ""

update_img = on_command(
    "修改图片", aliases={"操作图片", "改图"}, priority=5, rule=to_me(), block=True
)

method_list = [
    "修改尺寸",
    "等比压缩",
    "旋转图片",
    "水平翻转",
    "铅笔滤镜",
    "模糊效果",
    "锐化效果",
    "高斯模糊",
    "边缘检测",
    "底色替换",
]
method_str = ""
method_oper = []
for i in range(len(method_list)):
    method_str += f"\n{i + 1}.{method_list[i]}"
    method_oper.append(method_list[i])
    method_oper.append(str(i + 1))

update_img_help = CreateImg(960, 700, font_size=24)
update_img_help.text((10, 10), __plugin_usage__)
update_img_help.save(IMAGE_PATH + "update_img_help.png")


@update_img.args_parser
async def _(bot: Bot, event: MessageEvent, state: T_State):
    global method_flag
    if str(event.get_message()) in ["取消", "算了"]:
        await update_img.finish("已取消操作..", at_sender=True)
    if state["_current_key"] in ["method"]:
        if str(event.get_message()) not in method_oper:
            await update_img.reject(f"操作不正确，请重新输入！{method_str}")
        state[state["_current_key"]] = str(event.get_message())
        method_flag = str(event.get_message())
    if method_flag in ["1", "修改尺寸"]:
        if state["_current_key"] == "x":
            if not is_number(str(event.get_message())):
                await update_img.reject("宽度不正确！请重新输入数字...")
            state[state["_current_key"]] = str(event.get_message())
        if state["_current_key"] == "y":
            if not is_number(str(event.get_message())):
                await update_img.reject("长度不正确！请重新输入数字...")
            state[state["_current_key"]] = str(event.get_message())
    elif method_flag in ["2", "等比压缩", "3", "旋转图片"]:
        if state["_current_key"] == "x":
            if not is_number(str(event.get_message())):
                await update_img.reject("比率不正确！请重新输入数字...")
            state[state["_current_key"]] = str(event.get_message())
            state["y"] = ""
    elif method_flag in [
        "4",
        "水平翻转",
        "5",
        "铅笔滤镜",
        "6",
        "模糊效果",
        "7",
        "锐化效果",
        "8",
        "高斯模糊",
        "9",
        "边缘检测",
    ]:
        state["x"] = ""
        state["y"] = ""
    elif method_flag in ["10", "底色替换"]:
        if state["_current_key"] == "x":
            if str(event.get_message()) not in ["红色", "蓝色", "红", "蓝"]:
                await update_img.reject("请输入支持的被替换的底色：\n红色 蓝色")
            state["x"] = str(event.get_message())
        if state["_current_key"] == "y":
            if str(event.get_message()) not in [
                "红色",
                "白色",
                "蓝色",
                "绿色",
                "黄色",
                "红",
                "白",
                "蓝",
                "绿",
                "黄",
            ]:
                await update_img.reject("请输入支持的替换的底色：\n红色 蓝色 白色 绿色")
            state["y"] = str(event.get_message())
    if state["_current_key"] == "imgs":
        if not get_message_imgs(event.json()):
            await update_img.reject("没图？没图？没图？来图速来！")
        state[state["_current_key"]] = get_message_imgs(event.json())


@update_img.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if str(event.get_message()) in ["帮助"]:
        await update_img.finish(image("update_img_help.png"))
    raw_arg = get_message_text(event.json())
    img_list = get_message_imgs(event.json())
    if raw_arg:
        args = raw_arg.split("[")[0].split(" ")
        print(args)
        state["method"] = args[0]
        if len(args) == 2:
            if args[0] in ["等比压缩", "旋转图片"]:
                if is_number(args[1]):
                    state["x"] = args[1]
                    state["y"] = ""
        elif len(args) > 2:
            if args[0] in ["修改尺寸"]:
                if is_number(args[1]):
                    state["x"] = args[1]
                if is_number(args[2]):
                    state["y"] = args[2]
            if args[0] in ["底色替换"]:
                if args[1] in ["红色", "蓝色", "蓝", "红"]:
                    state["x"] = args[1]
                if args[2] in ["红色", "白色", "蓝色", "绿色", "黄色", "红", "白", "蓝", "绿", "黄"]:
                    state["y"] = args[2]
        if args[0] in ["水平翻转", "铅笔滤镜", "模糊效果", "锐化效果", "高斯模糊", "边缘检测"]:
            state["x"] = ""
            state["y"] = ""
        if img_list:
            state["imgs"] = img_list


@update_img.got("method", prompt=f"要使用图片的什么操作呢？{method_str}")
@update_img.got("x", prompt="[宽度？ 比率？ 旋转角度？ 底色？]")
@update_img.got("y", prompt="[长度？ 0 0 底色？]")
@update_img.got("imgs", prompt="图呢图呢图呢图呢？GKD！")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    method = state["method"]
    x = state["x"] if state["x"] else ""
    y = state["y"] if state["y"] else ""
    img_list = state["imgs"]
    if is_number(x):
        x = float(x)
    if is_number(y):
        y = int(y)
    index = 0
    result = ""
    async with aiohttp.ClientSession() as session:
        for img_url in img_list:
            async with session.get(img_url, timeout=7) as response:
                if response.status == 200:
                    async with aiofiles.open(
                        IMAGE_PATH + f"temp/{event.user_id}_{index}_update.png", "wb"
                    ) as f:
                        await f.write(await response.read())
                        index += 1
                else:
                    logger.warning(
                        f"USER {event.user_id} GROUP "
                        f"{event.group_id if event.message_type != 'private' else 'private'} "
                        f"使用 {method} 时下载图片超时"
                    )
                    await update_img.finish("获取图片超时了...", at_sender=True)
    if index == 0:
        return
    if method in ["修改尺寸", "1"]:
        for i in range(index):
            img = Image.open(IMAGE_PATH + f"temp/{event.user_id}_{i}_update.png")
            img = img.convert("RGB")
            img = img.resize((int(x), int(y)), Image.ANTIALIAS)
            result += image(b64=pic2b64(img))
        await update_img.finish(result, at_sender=True)
    if method in ["等比压缩", "2"]:
        for i in range(index):
            img = Image.open(IMAGE_PATH + f"temp/{event.user_id}_{i}_update.png")
            width, height = img.size
            img = img.convert("RGB")
            if width * x < 8000 and height * x < 8000:
                img = img.resize((int(x * width), int(x * height)))
                result += image(b64=pic2b64(img))
            else:
                await update_img.finish(f"{NICKNAME}不支持图片压缩后宽或高大于8000的存在！！")
    if method in ["旋转图片", "3"]:
        for i in range(index):
            img = Image.open(IMAGE_PATH + f"temp/{event.user_id}_{i}_update.png")
            img = img.rotate(x)
            result += image(b64=pic2b64(img))
    if method in ["水平翻转", "4"]:
        for i in range(index):
            img = Image.open(IMAGE_PATH + f"temp/{event.user_id}_{i}_update.png")
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            result += image(b64=pic2b64(img))
    if method in ["铅笔滤镜", "5"]:
        for i in range(index):
            img = Image.open(
                IMAGE_PATH + f"temp/{event.user_id}_{i}_update.png"
            ).filter(ImageFilter.CONTOUR)
            result += image(b64=pic2b64(img))
    if method in ["模糊效果", "6"]:
        for i in range(index):
            img = Image.open(
                IMAGE_PATH + f"temp/{event.user_id}_{i}_update.png"
            ).filter(ImageFilter.BLUR)
            result += image(b64=pic2b64(img))
    if method in ["锐化效果", "7"]:
        for i in range(index):
            img = Image.open(
                IMAGE_PATH + f"temp/{event.user_id}_{i}_update.png"
            ).filter(ImageFilter.EDGE_ENHANCE)
            result += image(b64=pic2b64(img))
    if method in ["高斯模糊", "8"]:
        for i in range(index):
            img = Image.open(
                IMAGE_PATH + f"temp/{event.user_id}_{i}_update.png"
            ).filter(ImageFilter.GaussianBlur)
            result += image(b64=pic2b64(img))
    if method in ["边缘检测", "9"]:
        for i in range(index):
            img = Image.open(
                IMAGE_PATH + f"temp/{event.user_id}_{i}_update.png"
            ).filter(ImageFilter.FIND_EDGES)
            result += image(b64=pic2b64(img))
    if method in ["底色替换", "10"]:
        if x in ["蓝色", "蓝"]:
            lower = np.array([90, 70, 70])
            upper = np.array([110, 255, 255])
        if x in ["红色", "红"]:
            lower = np.array([0, 135, 135])
            upper = np.array([180, 245, 230])
        if y in ["蓝色", "蓝"]:
            color = (255, 0, 0)
        if y in ["红色", "红"]:
            color = (0, 0, 255)
        if y in ["白色", "白"]:
            color = (255, 255, 255)
        if y in ["绿色", "绿"]:
            color = (0, 255, 0)
        if y in ["黄色", "黄"]:
            color = (0, 255, 255)
        for k in range(index):
            img = cv2.imread(IMAGE_PATH + f"temp/{event.user_id}_{k}_update.png")
            img = cv2.resize(img, None, fx=0.3, fy=0.3)
            rows, cols, channels = img.shape
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower, upper)
            # erode = cv2.erode(mask, None, iterations=1)
            dilate = cv2.dilate(mask, None, iterations=1)
            for i in range(rows):
                for j in range(cols):
                    if dilate[i, j] == 255:
                        img[i, j] = color
            cv2.imwrite(IMAGE_PATH + f"temp/{event.user_id}_{k}_ok_update.png", img)
        for i in range(index):
            result += image(f"{event.user_id}_{i}_ok_update.png", "temp")
    if is_number(method):
        method = method_list[int(method) - 1]
    logger.info(
        f"(USER {event.user_id}, GROUP"
        f" {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 使用{method}"
    )
    await update_img.finish(result, at_sender=True)
