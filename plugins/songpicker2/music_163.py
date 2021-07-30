import aiohttp
import json
from utils.utils import get_local_proxy
from configs.config import ALAPI_TOKEN
from asyncio.exceptions import TimeoutError


class dataApi:
    """
    从网易云音乐接口直接获取数据（实验性）
    """

    headers = {"referer": "http://music.163.com"}
    cookies = {"appver": "2.0.2"}

    async def search(self, songName: str):
        """
        搜索接口，用于由歌曲名查找id
        """
        async with aiohttp.ClientSession(
            headers=self.headers, cookies=self.cookies
        ) as session:
            async with session.post(
                f"http://music.163.com/api/search/get/",
                data={"s": songName, "limit": 5, "type": 1, "offset": 0},
            ) as r:
                if r.status != 200:
                    return None
                r = await r.text()
                return json.loads(r)

    async def getSongInfo(self, songId: int):
        """
        获取歌曲信息
        """
        async with aiohttp.ClientSession(
            headers=self.headers, cookies=self.cookies
        ) as session:
            async with session.post(
                f"http://music.163.com/api/song/detail/?id={songId}&ids=%5B{songId}%5D",
            ) as r:
                if r.status != 200:
                    return None
                r = await r.text()
                return json.loads(r)


class dataGet(dataApi):
    """
    从dataApi获取数据，并做简单处理
    """

    api = dataApi()

    async def songIds(self, songName: str, amount=5) -> list:
        """
        根据用户输入的songName 获取候选songId列表 [默认songId数量：5]
        """
        songIds = list()
        r = await self.api.search(songName=songName)
        if r is None:
            raise WrongDataError
        idRange = (
            amount if amount < len(r["result"]["songs"]) else len(r["result"]["songs"])
        )
        for i in range(idRange):
            songIds.append(r["result"]["songs"][i]["id"])
        return songIds

    async def songInfo(self, songId: int):
        """
        根据传递的songId，获取歌曲名、歌手、专辑等信息，作为dict返回
        """
        songInfo = dict()
        r = await self.api.getSongInfo(songId)
        if r is None:
            raise WrongDataError
        if r["code"] == -460:
            return "网易云网络繁忙！"
        songInfo["songName"] = r["songs"][0]["name"]

        songArtists = list()
        for ars in r["songs"][0]["artists"]:
            songArtists.append(ars["name"])
        songArtistsStr = "、".join(songArtists)
        songInfo["songArtists"] = songArtistsStr

        songInfo["songAlbum"] = r["songs"][0]["album"]["name"]

        return songInfo


class dataProcess:
    """
    将获取的数据处理为用户能看懂的形式
    """

    @staticmethod
    async def mergeSongInfo(songInfos: list) -> str:
        """
        将歌曲信息list处理为字符串，供用户点歌
        传递进的歌曲信息list含有多个歌曲信息dict
        """
        songInfoMessage = "请输入欲点播歌曲的序号：\n"
        numId = 0
        for songInfo in songInfos:
            songInfoMessage += f"{numId}："
            songInfoMessage += songInfo["songName"]
            songInfoMessage += "-"
            songInfoMessage += songInfo["songArtists"]
            songInfoMessage += " 专辑："
            songInfoMessage += songInfo["songAlbum"]
            songInfoMessage += "\n"
            numId += 1
        return songInfoMessage

    @staticmethod
    async def mergeSongComments(songComments: dict) -> str:
        songCommentsMessage = "\n".join(
            ["%s： %s" % (key, value) for (key, value) in songComments.items()]
        )
        return songCommentsMessage


class Error(Exception):
    """
    谁知道网易的接口会出什么幺蛾子
    """

    pass


class WrongDataError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
        self.message += "\n未从网易接口获取到有效的数据！"


async def get_music_id(keyword: str):
    url = f"https://v2.alapi.cn/api/music/search"
    params = {"token": ALAPI_TOKEN, "keyword": keyword}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url, proxy=get_local_proxy(), timeout=2, params=params
            ) as response:
                data = await response.json()
                if data["code"] == 200:
                    data = data["data"]["songs"]
                    return data["id"], 200
                else:
                    return f'访问失败...code：{data["code"]}', 999
        except TimeoutError:
            return "超时了...", 999
