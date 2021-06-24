from .music_163 import dataGet, dataProcess, get_music_id
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot import on_command

__plugin_name__ = '点歌'

__plugin_usage__ = '用法：点歌 [歌名]'

dataget = dataGet()

songpicker = on_command("点歌", priority=5, block=True)


@songpicker.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["songName"] = args


@songpicker.got("songName", prompt="歌名是？")
async def handle_songName(bot: Bot, event: Event, state: T_State):
    songName = state["songName"]
    songIdList = await dataget.songIds(songName=songName)
    if not songIdList:
        await songpicker.finish("没有找到这首歌！", at_sender=True)
    for _ in range(3):
        songInfoDict = await dataget.songInfo(songIdList[0])
        if songInfoDict != '网易云网络繁忙！':
            break
    else:
        await songpicker.finish("网易云繁忙...")
    state["songIdList"] = songIdList


@songpicker.got("songName")
async def handle_songNum(bot: Bot, event: Event, state: T_State):
    songIdList = state["songIdList"]
    selectedSongId = songIdList[0]
    songContent = [
        {
            "type": "music",
            "data": {
                "type": 163,
                "id": selectedSongId
            }
        }
    ]
    await songpicker.send(songContent)

