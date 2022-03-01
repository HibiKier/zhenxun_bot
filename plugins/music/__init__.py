from .music_163 import get_song_id, get_song_info
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg
from nonebot.typing import T_State
from services.log import logger
from nonebot import on_command
from utils.message_builder import music


__zx_plugin_name__ = "点歌"
__plugin_usage__ = """
usage：
    在线点歌
    指令：
        点歌 [歌名]
""".strip()
__plugin_des__ = "为你点播了一首曾经的歌"
__plugin_cmd__ = ["点歌 [歌名]"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["点歌"],
}


music_handler = on_command("点歌", priority=5, block=True)


@music_handler.handle()
async def handle_first_receive(state: T_State, arg: Message = CommandArg()):
    if args := arg.extract_plain_text().strip():
        state["song_name"] = args


@music_handler.got("song_name", prompt="歌名是？")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    song = state["song_name"]
    song_id = await get_song_id(song)
    if not song_id:
        await music_handler.finish("没有找到这首歌！", at_sender=True)
    await music_handler.send(music("163", song_id))
    logger.info(
        f"(USER {event.user_id}, GROUP "
        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 点歌 :{song}"
    )




