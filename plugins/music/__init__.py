from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg,Arg
from nonebot.matcher import Matcher
from services.log import logger
from nonebot import on_command
import aiohttp

__zx_plugin_name__ = "点歌语音版"
__plugin_usage__ = """
usage：
    在线点歌，发送语音
        指令：
            来首 [歌名]
""".strip()
__plugin_des__ = "小真寻为你点歌"
__plugin_cmd__ = ["来首 [歌名]"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 1.0
__plugin_author__ = "U2yyy"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["来首"],
}
async def get_song_id(song_name: str) -> int:
    url = 'http://127.0.0.1:7002/kuwo/search/searchMusicBykeyWord?key='+song_name+''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            song_data = await res.json()
            if res.status != 200:
                return 0
            return song_data['data']['list'][0]['rid']   
            
async def get_song_url(song_id:int):
    #看机器人文档的时候看到有人用了类似于vue的{}插值用法，我没能实现，不知道是怎么完成的
    url = 'http://127.0.0.1:7002/kuwo/url?mid='+str(song_id)+'&type=music'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            song = await res.json()
            if song['code'] != 200:
                return None
            return song['data']['url']

music_handler = on_command("来首",aliases={"点歌"}, priority=5, block=True)

@music_handler.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    if args:
        matcher.set_arg("song_name",args)

@music_handler.got("song_name", prompt="歌名是？")
async def _(bot: Bot, event: MessageEvent, song_name: Message = Arg()):
    song = song_name.extract_plain_text().strip()
    song_id = await get_song_id(song)
    if not song_id:
        await music_handler.finish("没有找到这首歌！", at_sender=True)
    song_mp4 = await (get_song_url(song_id))
    if not song_mp4:
        await music_handler.finish("没有找到这首歌！", at_sender=True)
    await music_handler.send(Message('[CQ:record,file='+song_mp4+']'))
    logger.info(
        f"(USER {event.user_id}, GROUP "
        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 来首 :{song}"
        )
