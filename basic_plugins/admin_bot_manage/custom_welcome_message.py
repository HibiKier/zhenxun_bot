from nonebot import on_command
from utils.utils import get_message_img
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from nonebot.params import CommandArg
from ._data_source import custom_group_welcome
from nonebot.adapters.onebot.v11.permission import GROUP
from configs.config import Config
from services.log import logger


__zx_plugin_name__ = "自定义进群欢迎消息 [Admin]"
__plugin_usage__ = """
usage：
    指令：
        自定义进群欢迎消息 ?[文本] ?[图片]
        示例：自定义进群欢迎消息 欢迎新人！[图片]
        Note：可以通过[at]来确认是否艾特新成员
        示例：自定义进群欢迎消息 欢迎你[at]
""".strip()
__plugin_des__ = '简易的自定义群欢迎消息'
__plugin_cmd__ = ['自定义群欢迎消息 ?[文本] ?[图片]']
__plugin_version__ = 0.1
__plugin_author__ = 'HibiKier'
__plugin_settings__ = {
    "admin_level": Config.get_config("admin_bot_manage", "SET_GROUP_WELCOME_MESSAGE_LEVEL"),
}

custom_welcome = on_command(
    "自定义进群欢迎消息",
    aliases={"自定义欢迎消息", "自定义群欢迎消息", "设置群欢迎消息"},
    permission=GROUP,
    priority=5,
    block=True,
)


@custom_welcome.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    try:
        msg = arg.extract_plain_text().strip()
        img = get_message_img(event.json())
        if not msg and not img:
            await custom_welcome.finish(__plugin_usage__)
        await custom_welcome.send(
            await custom_group_welcome(msg, img, event.user_id, event.group_id),
            at_sender=True,
        )
        logger.info(f"USER {event.user_id} GROUP {event.group_id} 自定义群欢迎消息：{msg}")
    except Exception as e:
        logger.error(f"自定义进群欢迎消息发生错误 {type(e)}：{e}")
        await custom_welcome.send("发生了一些未知错误...")
