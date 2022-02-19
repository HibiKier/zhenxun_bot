from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from utils.message_builder import image
from .data_source import create_help_image, admin_help_image


__zx_plugin_name__ = '管理帮助 [Admin]'
__plugin_usage__ = '管理员帮助，在群内回复“管理员帮助”'
__plugin_version__ = 0.1
__plugin_author__ = 'HibiKier'
__plugin_settings__ = {
    "admin_level": 1,
}

admin_help = on_command("管理员帮助", aliases={"管理帮助"}, priority=5, block=True)

if admin_help_image.exists():
    admin_help_image.unlink()


@admin_help.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if not admin_help_image.exists():
        await create_help_image()
    await admin_help.send(image('admin_help_img.png'))
