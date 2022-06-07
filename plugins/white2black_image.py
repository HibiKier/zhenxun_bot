from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from nonebot import on_command
from nonebot.params import CommandArg
from utils.utils import get_message_img, is_chinese
from utils.message_builder import image
from configs.path_config import TEMP_PATH
from utils.image_utils import BuildImage
from services.log import logger
from utils.http_utils import AsyncHttpx

# ZH_CN2EN 中文　»　英语
# ZH_CN2JA 中文　»　日语
# ZH_CN2KR 中文　»　韩语
# ZH_CN2FR 中文　»　法语
# ZH_CN2RU 中文　»　俄语
# ZH_CN2SP 中文　»　西语
# EN2ZH_CN 英语　»　中文
# JA2ZH_CN 日语　»　中文
# KR2ZH_CN 韩语　»　中文
# FR2ZH_CN 法语　»　中文
# RU2ZH_CN 俄语　»　中文
# SP2ZH_CN 西语　»　中文


__zx_plugin_name__ = "黑白草图"
__plugin_usage__ = """
usage：
    将图片黑白化并配上中文与日语
    指令：
        黑白图 [文本] [图片]
""".strip()
__plugin_des__ = "为设想过得黑白草图"
__plugin_cmd__ = ["黑白图"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["黑白图", "黑白草图"],
}

w2b_img = on_command("黑白草图", aliases={"黑白图"}, priority=5, block=True)


@w2b_img.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    # try:
    img = get_message_img(event.json())
    msg = arg.extract_plain_text().strip()
    if not img or not msg:
        await w2b_img.finish(f"格式错误：\n" + __plugin_usage__)
    img = img[0]
    if not await AsyncHttpx.download_file(
        img, TEMP_PATH / f"{event.user_id}_w2b.png"
    ):
        await w2b_img.finish("下载图片失败...请稍后再试...")
    msg = await get_translate(msg)
    w2b = BuildImage(0, 0, background=TEMP_PATH / f"{event.user_id}_w2b.png")
    w2b.convert("L")
    msg_sp = msg.split("<|>")
    w, h = w2b.size
    add_h, font_size = init_h_font_size(h)
    bg = BuildImage(w, h + add_h, color="black", font_size=font_size)
    bg.paste(w2b)
    chinese_msg = formalization_msg(msg)
    if not bg.check_font_size(chinese_msg):
        if len(msg_sp) == 1:
            centered_text(bg, chinese_msg, add_h)
        else:
            centered_text(bg, chinese_msg + "<|>" + msg_sp[1], add_h)
    elif not bg.check_font_size(msg_sp[0]):
        centered_text(bg, msg, add_h)
    else:
        ratio = (bg.getsize(msg_sp[0])[0] + 20) / bg.w
        add_h = add_h * ratio
        bg.resize(ratio)
        centered_text(bg, msg, add_h)
    await w2b_img.send(image(b64=bg.pic2bs4()))
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 制作黑白草图 {msg}"
    )


def centered_text(img: BuildImage, text: str, add_h: int):
    top_h = img.h - add_h + (img.h / 100)
    bottom_h = img.h - (img.h / 100)
    text_sp = text.split("<|>")
    w, h = img.getsize(text_sp[0])
    if len(text_sp) == 1:
        w = int((img.w - w) / 2)
        h = int(top_h + (bottom_h - top_h - h) / 2)
        img.text((w, h), text_sp[0], (255, 255, 255))
    else:
        br_h = int(top_h + (bottom_h - top_h) / 2)
        w = int((img.w - w) / 2)
        h = int(top_h + (br_h - top_h - h) / 2)
        img.text((w, h), text_sp[0], (255, 255, 255))
        w, h = img.getsize(text_sp[1])
        w = int((img.w - w) / 2)
        h = int(br_h + (bottom_h - br_h - h) / 2)
        img.text((w, h), text_sp[1], (255, 255, 255))


async def get_translate(msg: str) -> str:
    url = f"http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"
    data = {
        "type": "ZH_CN2JA",
        "i": msg,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true",
    }
    data = (await AsyncHttpx.post(url, data=data)).json()
    if data["errorCode"] == 0:
        translate = data["translateResult"][0][0]["tgt"]
        msg += "<|>" + translate
    return msg


def formalization_msg(msg: str) -> str:
    rst = ""
    for i in range(len(msg)):
        if is_chinese(msg[i]):
            rst += msg[i] + " "
        else:
            rst += msg[i]
        if i + 1 < len(msg) and is_chinese(msg[i + 1]) and msg[i].isalpha():
            rst += " "
    return rst


def init_h_font_size(h):
    #       高度      字体
    if h < 400:
        return init_h_font_size(400)
    elif 400 < h < 800:
        return init_h_font_size(800)
    return h * 0.2, h * 0.05
