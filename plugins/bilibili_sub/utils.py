from utils.image_utils import BuildImage
from configs.path_config import IMAGE_PATH
from utils.http_utils import AsyncHttpx, get_user_agent
# from bilibili_api import user
from bilireq.user import get_user_info
from httpx import AsyncClient
from io import BytesIO


BORDER_PATH = IMAGE_PATH / "border"
BORDER_PATH.mkdir(parents=True, exist_ok=True)
BASE_URL = "https://api.bilibili.com"

async def get_pic(url: str) -> bytes:
    """
    获取图像
    :param url: 图像链接
    :return: 图像二进制
    """
    return (await AsyncHttpx.get(url, timeout=10)).content


async def create_live_des_image(uid: int, title: str, cover: str, tags: str, des: str):
    """
    生成主播简介图片
    :param uid: 主播 uid
    :param title: 直播间标题
    :param cover: 直播封面
    :param tags: 直播标签
    :param des: 直播简介
    :return:
    """

    user_info = await get_user_info(uid)
    name = user_info["name"]
    sex = user_info["sex"]
    face = user_info["face"]
    sign = user_info["sign"]
    ava = BuildImage(100, 100, background=BytesIO(await get_pic(face)))
    ava.circle()
    cover = BuildImage(470, 265, background=BytesIO(await get_pic(cover)))


def _create_live_des_image(
    title: str,
    cover: BuildImage,
    tags: str,
    des: str,
    user_name: str,
    sex: str,
    sign: str,
    ava: BuildImage,
):
    """
    生成主播简介图片
    :param title: 直播间标题
    :param cover: 直播封面
    :param tags: 直播标签
    :param des: 直播简介
    :param user_name: 主播名称
    :param sex: 主播性别
    :param sign: 主播签名
    :param ava: 主播头像
    :return:
    """
    border = BORDER_PATH / "0.png"
    border_img = None
    if border.exists():
        border_img = BuildImage(1772, 2657, background=border)
    bk = BuildImage(1772, 2657, font_size=30)
    bk.paste(cover, (0, 100), center_type="by_width")


async def get_meta(media_id: int, auth=None, reqtype="both", **kwargs):
    """
    根据番剧 ID 获取番剧元数据信息，
    作为bilibili_api和bilireq的替代品。
    如果bilireq.bangumi更新了，可以转为调用bilireq.bangumi的get_meta方法，两者完全一致。
    """
    from bilireq.utils import get

    url = f"{BASE_URL}/pgc/review/user"
    params = {"media_id": media_id}
    raw_json = await get(url, raw=True, params=params, auth=auth, reqtype=reqtype, **kwargs)
    return raw_json['result']


async def get_videos(
    uid: int, tid: int = 0, pn: int = 1, keyword: str = "", order: str = "pubdate"
):
    """
    获取用户投该视频信息
    作为bilibili_api和bilireq的替代品。
    如果bilireq.user更新了，可以转为调用bilireq.user的get_videos方法，两者完全一致。

    :param uid: 用户 UID
    :param tid: 分区 ID
    :param pn: 页码
    :param keyword: 搜索关键词
    :param order: 排序方式，可以为 “pubdate(上传日期从新到旧), stow(收藏从多到少), click(播放量从多到少)”
    """
    from bilireq.utils import ResponseCodeError

    url = f"{BASE_URL}/x/space/arc/search"
    headers = get_user_agent()
    headers["Referer"] = f"https://space.bilibili.com/{uid}/video"
    async with AsyncClient() as client:
        r = await client.head(
            "https://www.bilibili.com",
            headers=headers,
        )
        params = {
            "mid": uid,
            "ps": 30,
            "tid": tid,
            "pn": pn,
            "keyword": keyword,
            "order": order,
        }
        raw_json = (
            await client.get(url, params=params, headers=headers, cookies=r.cookies)
        ).json()
        if raw_json["code"] != 0:
            raise ResponseCodeError(
                code=raw_json["code"],
                msg=raw_json["message"],
                data=raw_json.get("data", None),
            )
        return raw_json["data"]

async def get_user_card(mid, photo: bool = False, auth=None, reqtype="both", **kwargs):
    from bilireq.utils import get

    url = f"{BASE_URL}/x/web-interface/card"
    return (
        await get(
            url,
            params={"mid": mid, "photo": photo},
            auth=auth,
            reqtype=reqtype,
            **kwargs,
        )
    )["card"]
