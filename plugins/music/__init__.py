from .music_163 import get_song_id, get_song_info
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg,Arg
from nonebot.matcher import Matcher
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
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    #/Edited by U2yyy/使用matcher来set key值
    if args:
        matcher.set_arg("song_name",args)
        
@music_handler.got("song_name", prompt="歌名是？")
async def _(bot: Bot, event: MessageEvent, song_name: Message = Arg()):
    #/Edited by U2yyy/这里把set或者传入的key值转换为string类型值来供函数使用
    song = song_name.extract_plain_text().strip()
    song_id = await get_song_id(song)
    if not song_id:
        await music_handler.finish("没有找到这首歌！", at_sender=True)
    await music_handler.send(music("163", song_id))
    logger.info(
        f"(USER {event.user_id}, GROUP "
        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 点歌 :{song}"
    )




