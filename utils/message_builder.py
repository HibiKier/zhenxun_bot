from configs.path_config import IMAGE_PATH, VOICE_PATH
from nonebot.adapters.cqhttp.message import MessageSegment
from configs.config import NICKNAME
from services.log import logger
from typing import Union, List
from pathlib import Path
import os


def image(
    img_name: Union[str, Path] = None,
    path: str = None,
    abspath: str = None,
    b64: str = None,
) -> Union[MessageSegment, str]:
    """
    说明：
        生成一个 MessageSegment.image 消息
        生成顺序：绝对路径(abspath) > base64(b64) > img_name
    参数：
        :param img_name: 图片文件名称，默认在 resource/img 目录下
        :param path: 图片所在路径，默认在 resource/img 目录下
        :param abspath: 图片绝对路径
        :param b64: 图片base64
    """
    if abspath:
        return (
            MessageSegment.image("file:///" + abspath)
            if os.path.exists(abspath)
            else ""
        )
    elif isinstance(img_name, Path):
        if img_name.exists():
            return MessageSegment.image(f"file:///{img_name.absolute()}")
        logger.warning(f"图片 {img_name.absolute()}缺失...")
        return ""
    elif b64:
        return MessageSegment.image(b64 if "base64://" in b64 else "base64://" + b64)
    else:
        if "http" in img_name:
            return MessageSegment.image(img_name)
        if len(img_name.split(".")) == 1:
            img_name += ".jpg"
        file = (
            Path(IMAGE_PATH) / path / img_name if path else Path(IMAGE_PATH) / img_name
        )
        if file.exists():
            return MessageSegment.image(f"file:///{file.absolute()}")
        else:
            logger.warning(f"图片 {file.absolute()}缺失...")
            return ""


def at(qq: int) -> MessageSegment:
    """
    说明：
        生成一个 MessageSegment.at 消息
    参数：
        :param qq: qq号
    """
    return MessageSegment.at(qq)


def record(voice_name: str, path: str = None) -> MessageSegment or str:
    """
    说明：
        生成一个 MessageSegment.record 消息
    参数：
        :param voice_name: 音频文件名称，默认在 resource/voice 目录下
        :param path: 音频文件路径，默认在 resource/voice 目录下
    """
    if len(voice_name.split(".")) == 1:
        voice_name += ".mp3"
    file = (
        Path(VOICE_PATH) / path / voice_name if path else Path(VOICE_PATH) / voice_name
    )
    if "http" in voice_name:
        return MessageSegment.record(voice_name)
    if file.exists():
        result = MessageSegment.record(f"file:///{file.absolute()}")
        return result
    else:
        logger.warning(f"语音{file.absolute()}缺失...")
        return ""


def text(msg: str) -> MessageSegment:
    """
    说明：
        生成一个 MessageSegment.text 消息
    参数：
        :param msg: 消息文本
    """
    return MessageSegment.text(msg)


def contact_user(qq: int) -> MessageSegment:
    """
    说明：
        生成一个 MessageSegment.contact_user 消息
    参数：
        :param qq: qq号
    """
    return MessageSegment.contact_user(qq)


def share(
    url: str, title: str, content: str = None, image_url: str = None
) -> MessageSegment:
    """
    说明：
        生成一个 MessageSegment.share 消息
    参数：
        :param url: 自定义分享的链接
        :param title: 自定义分享的包体
        :param content: 自定义分享的内容
        :param image_url: 自定义分享的展示图片
    """
    return MessageSegment.share(url, title, content, image_url)


def xml(data: str) -> MessageSegment:
    """
    说明：
        生成一个 MessageSegment.xml 消息
    参数：
        :param data: 数据文本
    """
    return MessageSegment.xml(data)


def json(data: str) -> MessageSegment:
    """
    说明：
        生成一个 MessageSegment.json 消息
    参数：
        :param data: 消息数据
    """
    return MessageSegment.json(data)


def face(id_: int) -> MessageSegment:
    """
    说明：
        生成一个 MessageSegment.face 消息
    参数：
        :param id_: 表情id
    """
    return MessageSegment.face(id_)


def poke(qq: int) -> MessageSegment:
    """
    说明：
        生成一个 MessageSegment.poke 消息
    参数：
        :param qq: qq号
    """
    return MessageSegment("poke", {"qq": qq})


def custom_forward_msg(
    msg_list: List[str], uin: Union[int, str], name: str = f"这里是{NICKNAME}"
) -> List[dict]:
    """
    生成自定义合并消息
    :param msg_list: 消息列表
    :param uin: 发送者 QQ
    :param name: 自定义名称
    """
    uin = int(uin)
    mes_list = []
    for _message in msg_list:
        data = {
            "type": "node",
            "data": {
                "name": name,
                "uin": f"{uin}",
                "content": _message,
            },
        }
        mes_list.append(data)
    return mes_list
