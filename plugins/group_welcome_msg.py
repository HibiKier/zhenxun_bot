from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from configs.path_config import DATA_PATH
from utils.message_builder import image

try:
    import ujson as json
except ModuleNotFoundError:
    import json

__zx_plugin_name__ = "查看群欢迎消息"
__plugin_usage__ = """
usage：
    查看当前的群欢迎消息
    指令：
        查看群欢迎消息
""".strip()
__plugin_des__ = "查看群欢迎消息"
__plugin_cmd__ = ["查看群欢迎消息"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查看群欢迎消息"],
}

view_custom_welcome = on_command(
    "群欢迎消息", aliases={"查看群欢迎消息", "查看当前群欢迎消息"}, permission=GROUP, priority=5, block=True
)


@view_custom_welcome.handle()
async def _(event: GroupMessageEvent):
    img = ""
    msg = ""
    if (DATA_PATH / "custom_welcome_msg" / f"{event.group_id}.jpg").exists():
        img = image(DATA_PATH / "custom_welcome_msg" / f"{event.group_id}.jpg")
    custom_welcome_msg_json = (
       DATA_PATH / "custom_welcome_msg" / "custom_welcome_msg.json"
    )
    if custom_welcome_msg_json.exists():
        data = json.load(open(custom_welcome_msg_json, "r"))
        if data.get(str(event.group_id)):
            msg = data[str(event.group_id)]
            if msg.find("[at]") != -1:
                msg = msg.replace("[at]", "")
    if img or msg:
        await view_custom_welcome.finish(msg + img, at_sender=True)
    else:
        await view_custom_welcome.finish("当前还没有自定义群欢迎消息哦", at_sender=True)
