from utils.image_utils import BuildImage
from configs.path_config import IMAGE_PATH
from utils.http_utils import AsyncHttpx
from bilibili_api import user
from io import BytesIO


BORDER_PATH = IMAGE_PATH / "border"
BORDER_PATH.mkdir(parents=True, exist_ok=True)


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
    u = user.User(uid)
    user_info = await u.get_user_info()
    name = user_info["name"]
    sex = user_info["sex"]
    face = user_info["face"]
    sign = user_info["sign"]
    ava = BuildImage(100, 100, background=BytesIO(await get_pic(face)))
    ava.circle()
    cover = BuildImage(470, 265, background=BytesIO(await get_pic(cover)))
    print()


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
