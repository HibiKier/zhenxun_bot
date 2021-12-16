from utils.http_utils import AsyncHttpx
import json


headers = {"referer": "http://music.163.com"}
cookies = {"appver": "2.0.2"}


async def search_song(song_name: str):
    """
    搜索歌曲
    :param song_name: 歌名
    """
    r = await AsyncHttpx.post(
        f"http://music.163.com/api/search/get/",
        data={"s": song_name, "limit": 1, "type": 1, "offset": 0},
    )
    if r.status_code != 200:
        return None
    return json.loads(r.text)


async def get_song_id(song_name: str) -> int:
    """ """
    r = await search_song(song_name)
    try:
        return r["result"]["songs"][0]["id"]
    except KeyError:
        return 0


async def get_song_info(songId: int):
    """
    获取歌曲信息
    """
    r = await AsyncHttpx.post(
        f"http://music.163.com/api/song/detail/?id={songId}&ids=%5B{songId}%5D",
    )
    if r.status_code != 200:
        return None
    return json.loads(r.text)
