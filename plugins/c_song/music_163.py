import aiohttp
import json


headers = {"referer": "http://music.163.com"}
cookies = {"appver": "2.0.2"}


async def search_song(song_name: str):
    async with aiohttp.ClientSession(
            headers=headers, cookies=cookies
    ) as session:
        async with session.post(
                f"http://music.163.com/api/search/get/",
                data={"s": song_name, "limit": 1, "type": 1, "offset": 0},
        ) as r:
            if r.status != 200:
                return None
            r = await r.text()
            return json.loads(r)


async def get_song_id(songName: str) -> int:
    """
    根据用户输入的songName 获取候选songId列表 [默认songId数量：5]
    """
    r = await search_song(songName)
    return r["result"]["songs"][0]["id"]


async def get_song_info(songId: int):
    """
    获取歌曲信息
    """
    async with aiohttp.ClientSession(
        headers=headers, cookies=cookies
    ) as session:
        async with session.post(
            f"http://music.163.com/api/song/detail/?id={songId}&ids=%5B{songId}%5D",
        ) as r:
            if r.status != 200:
                return None
            r = await r.text()
            return json.loads(r)



