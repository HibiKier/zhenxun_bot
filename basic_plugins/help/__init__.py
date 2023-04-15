import os

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageEvent
from nonebot.params import CommandArg
from nonebot.rule import to_me

from configs.path_config import DATA_PATH, IMAGE_PATH
from services.log import logger
from utils.message_builder import image

from ._data_source import create_help_img, get_plugin_help
from ._utils import GROUP_HELP_PATH

__zx_plugin_name__ = "帮助"

__plugin_configs__ = {
    "TYPE": {
        "value": "normal",
        "help": "帮助图片样式 ['normal', 'HTML']",
        "default_value": "normal",
        "type": str,
    }
}

simple_help_image = IMAGE_PATH / "simple_help.png"
if simple_help_image.exists():
    simple_help_image.unlink()


simple_help = on_command(
    "功能", rule=to_me(), aliases={"help", "帮助"}, priority=1, block=True
)


@simple_help.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    is_super = False
    if msg:
        if "-super" in msg:
            if str(event.user_id) in bot.config.superusers:
                is_super = True
            msg = msg.replace("-super", "").strip()
        img_msg = get_plugin_help(msg, is_super)
        if img_msg:
            await simple_help.send(image(b64=img_msg))
        else:
            await simple_help.send("没有此功能的帮助信息...")
        logger.info(
            f"查看帮助详情: {msg}", "帮助", event.user_id, getattr(event, "group_id", None)
        )
    else:
        if isinstance(event, GroupMessageEvent):
            _image_path = GROUP_HELP_PATH / f"{event.group_id}.png"
            if not _image_path.exists():
                await create_help_img(event.group_id)
            await simple_help.send(image(_image_path))
        else:
            if not simple_help_image.exists():
                if simple_help_image.exists():
                    simple_help_image.unlink()
                await create_help_img(None)
            await simple_help.finish(image("simple_help.png"))
