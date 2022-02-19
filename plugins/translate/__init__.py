from nonebot import on_command
from nonebot.params import CommandArg
from services.log import logger
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from nonebot.typing import T_State
from .data_source import translate_msg


__zx_plugin_name__ = "翻译"
__plugin_usage__ = """
usage：
    出国旅游小助手
    指令：
        英翻 [英文]
        翻英 [中文]
        日翻 [日文]
        翻日 [中文]
        韩翻 [韩文]
        翻韩 [中文]
""".strip()
__plugin_des__ = "出国旅游好助手"
__plugin_cmd__ = ["英翻 [英文]", "翻英 [中文]", "日翻 [日文]", "翻日 [中文]", "韩翻 [韩文]", "翻韩 [中文]"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["翻译"],
}


translate = on_command(
    "translate", aliases={"英翻", "翻英", "日翻", "翻日", "韩翻", "翻韩"}, priority=5, block=True
)


@translate.handle()
async def _(state: T_State, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if msg:
        state["msg"] = msg


@translate.got("msg", prompt="你要翻译的消息是啥？")
async def _(event: MessageEvent, state: T_State):
    msg = state["msg"]
    if len(msg) > 150:
        await translate.finish("翻译过长！请不要超过150字", at_sender=True)
    await translate.send(await translate_msg(state["_prefix"]["raw_command"], msg))
    logger.info(
        f"(USER {event.user_id}, GROUP "
        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 使用翻译：{msg}"
    )
