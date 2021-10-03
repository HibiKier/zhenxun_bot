from .music_163 import get_song_id, get_song_info
from nonebot.adapters.cqhttp import Bot, Event, GroupMessageEvent
from nonebot.typing import T_State
from services.log import logger
from nonebot import on_command


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


songpicker = on_command("点歌", priority=5, block=True)


@songpicker.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["song_name"] = args


@songpicker.got("song_name", prompt="歌名是？")
async def _(bot: Bot, event: Event, state: T_State):
    song = state["song_name"]
    song_id = await get_song_id(song)
    if not song_id:
        await songpicker.finish("没有找到这首歌！", at_sender=True)
    for _ in range(3):
        song_content = [{"type": "music", "data": {"type": 163, "id": song_id}}]
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 点歌 :{song}"
        )
        await songpicker.finish(song_content)
    else:
        await songpicker.finish("网易云繁忙...")




