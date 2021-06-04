from .data_source import dataGet, dataProcess
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot import on_command


dataget = dataGet()

songpicker = on_command("点歌", priority=5, block=True)


@songpicker.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    # if args.isdigit():
    #     if "songName" in state:
    #         state["songNum"] = int(args)
    if args:
        state["songName"] = args


@songpicker.got("songName", prompt="歌名是？")
async def handle_songName(bot: Bot, event: Event, state: T_State):
    songName = state["songName"]
    songIdList = await dataget.songIds(songName=songName)
    if not songIdList:
        await songpicker.reject("没有找到这首歌，请发送其它歌名！")
    songInfoList = list()
    for songId in songIdList:
        songInfoDict = await dataget.songInfo(songId)
        if songInfoDict == '网易云网络繁忙！':
            await songpicker.finish('网易云网络繁忙！')
        songInfoList.append(songInfoDict)
    # songInfoMessage = await dataProcess.mergeSongInfo(songInfoList)
    # await songpicker.send(songInfoMessage)
    state["songIdList"] = songIdList


@songpicker.got("songName")
async def handle_songNum(bot: Bot, event: Event, state: T_State):
    songIdList = state["songIdList"]
    # songNum = state["songNum"]
    songNum = 0
    # 处理重选
    # if not songNum.isdigit():
    #     await songpicker.finish()
    # else:
    #     songNum = int(songNum)
    #
    # if songNum >= len(songIdList) or songNum < 0:
    #     await songpicker.reject("数字序号错误")

    selectedSongId = songIdList[int(songNum)]

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

    # songCommentsDict = await dataget.songComments(songId=selectedSongId)
    # songCommentsMessage = await dataProcess.mergeSongComments(songCommentsDict)
    # commentContent = [
    #     {
    #         "type": "text",
    #         "data": {
    #             "text": "下面为您播送热评：\n"
    #         }
    #     },
    #     {
    #         "type": "text",
    #         "data": {
    #             "text": songCommentsMessage
    #         }
    #     }
    # ]
    #
    # await songpicker.send(commentContent)