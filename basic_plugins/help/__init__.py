from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    Message
)
from nonebot.params import CommandArg
from nonebot.rule import to_me
from configs.path_config import IMAGE_PATH, DATA_PATH
from utils.message_builder import image
from .data_source import create_help_img, get_plugin_help
import os


__zx_plugin_name__ = "帮助"

# __plugin_configs__ = {
#     "TYPE": {"value": "normal", "help": "帮助图片样式 ['normal', 'VV']", "default_value": "normal"}
# }

group_help_path = DATA_PATH / "group_help"
simple_help_image = IMAGE_PATH / "simple_help.png"
if simple_help_image.exists():
    simple_help_image.unlink()
group_help_path.mkdir(exist_ok=True, parents=True)
for x in os.listdir(group_help_path):
    group_help_image = group_help_path / x
    group_help_image.unlink()


simple_help = on_command("功能", rule=to_me(), aliases={"help", "帮助"}, priority=1, block=True)


@simple_help.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    is_super = False
    if msg:
        if '-super' in msg:
            if str(event.user_id) in bot.config.superusers:
                is_super = True
            msg = msg.replace('-super', '').strip()
        msg = get_plugin_help(msg, is_super)
        if msg:
            await simple_help.send(image(b64=msg))
        else:
            await simple_help.send("没有此功能的帮助信息...")
    else:
        if isinstance(event, GroupMessageEvent):
            _image_path = group_help_path / f"{event.group_id}.png"
            if not _image_path.exists():
                await create_help_img(event.group_id, _image_path)
            await simple_help.send(image(_image_path))
        else:
            if not simple_help_image.exists():
                if simple_help_image.exists():
                    simple_help_image.unlink()
                await create_help_img(None, simple_help_image)
            await simple_help.finish(image("simple_help.png"))
