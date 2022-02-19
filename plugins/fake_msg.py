from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg
from nonebot import on_command
from utils.utils import get_message_img
from utils.message_builder import share
from services.log import logger


__zx_plugin_name__ = "构造分享消息"
__plugin_usage__ = """
usage：
    自定义的分享消息构造
    指令：
        假消息 [网址] [标题] ?[内容] ?[图片]
        示例：假消息 www.4399.com 我喜欢萝莉 为什么我喜欢... [图片]
""".strip()
__plugin_des__ = "自定义的分享消息构造"
__plugin_cmd__ = ["假消息 [网址] [标题] ?[内容] ?[图片]"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["假消息"],
}


fake_msg = on_command("假消息", priority=5, block=True)


@fake_msg.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip().split()
    img = get_message_img(event.json())
    if len(msg) > 1:
        if len(msg) == 2:
            url = msg[0]
            title = msg[1]
            content = ""
        else:
            url = msg[0]
            title = msg[1]
            content = msg[2]
        if img:
            img = img[0]
        else:
            img = ""
        if "http" not in url:
            url = "http://" + url
        await fake_msg.send(share(url, title, content, img))
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 构造假消息 url {url}， title {title}， content {content}"
        )
    else:
        await fake_msg.finish("消息格式错误：\n网址 标题 内容（可省略） 图片（可省略）")
