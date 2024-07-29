import aiohttp
from bilireq import live, video

from zhenxun.utils.user_agent import get_user_agent

from .get_image import get_image
from .information_container import InformationContainer


async def parse_bili_url(get_url: str, information_container: InformationContainer):
    """解析Bilibili链接，获取相关信息

    参数:
        get_url (str): 待解析的Bilibili链接
        information_container (InformationContainer): 信息容器

    返回:
        dict: 包含解析得到的信息的字典
    """
    response_url = ""

    # 去除链接末尾的斜杠
    if get_url[-1] == "/":
        get_url = get_url[:-1]

    # 发起HTTP请求，获取重定向后的链接
    async with aiohttp.ClientSession(headers=get_user_agent()) as session:
        async with session.get(
            get_url,
            timeout=7,
        ) as response:
            response_url = str(response.url).split("?")[0]

    # 去除重定向后链接末尾的斜杠
    if response_url[-1] == "/":
        response_url = response_url[:-1]

    # 根据不同类型的链接进行处理
    if response_url.startswith(
        ("https://www.bilibili.com/video", "https://m.bilibili.com/video/")
    ):
        vd_url = response_url
        vid = vd_url.split("/")[-1]
        vd_info = await video.get_video_base_info(vid)
        information_container.update({"vd_info": vd_info, "vd_url": vd_url})

    elif response_url.startswith("https://live.bilibili.com"):
        live_url = response_url
        liveid = live_url.split("/")[-1]
        live_info = await live.get_room_info_by_id(liveid)
        information_container.update({"live_info": live_info, "live_url": live_url})

    elif response_url.startswith("https://www.bilibili.com/read"):
        cv_url = response_url
        image_info = await get_image(cv_url)
        information_container.update({"image_info": image_info, "image_url": cv_url})

    elif response_url.startswith(
        ("https://www.bilibili.com/opus", "https://t.bilibili.com")
    ):
        opus_url = response_url
        image_info = await get_image(opus_url)
        information_container.update({"image_info": image_info, "image_url": opus_url})

    return information_container.get_information()
