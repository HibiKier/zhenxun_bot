from pathlib import Path
from typing import List, Union

from configs.config import NICKNAME
from configs.path_config import IMAGE_PATH, RECORD_PATH
from nonebot.adapters.onebot.v11.message import MessageSegment, Message
from services.log import logger


def image(
        file: Union[str, Path, bytes] = None,
        path: str = None,
        b64: str = None,
) -> Union[MessageSegment, str]:
    """
    说明:
        生成一个 MessageSegment.image 消息
        生成顺序：绝对路径(abspath) > base64(b64) > img_name
    参数:
        :param file: 图片文件名称，默认在 resource/img 目录下
        :param path: 图片所在路径，默认在 resource/img 目录下
        :param b64: 图片base64
    """
    if isinstance(file, Path):
        if file.exists():
            return MessageSegment.image(file)
        logger.warning(f"图片 {file.absolute()}缺失...")
        return ""
    elif isinstance(file, bytes):
        return MessageSegment.image(file)
    elif b64:
        return MessageSegment.image(b64 if "base64://" in b64 else "base64://" + b64)
    else:
        if file.startswith("http"):
            return MessageSegment.image(file)
        if len(file.split(".")) == 1:
            file += ".jpg"
        if (file := IMAGE_PATH / path / file if path else IMAGE_PATH / file).exists():
            return MessageSegment.image(file)
        else:
            logger.warning(f"图片 {file} 缺失...")
            return ""


def at(qq: Union[int, str]) -> MessageSegment:
    """
    说明:
        生成一个 MessageSegment.at 消息
    参数:
        :param qq: qq号
    """
    return MessageSegment.at(qq)


def record(voice_name: str, path: str = None) -> MessageSegment or str:
    """
    说明:
        生成一个 MessageSegment.record 消息
    参数:
        :param voice_name: 音频文件名称，默认在 resource/voice 目录下
        :param path: 音频文件路径，默认在 resource/voice 目录下
    """
    if len(voice_name.split(".")) == 1:
        voice_name += ".mp3"
    file = (
        Path(RECORD_PATH) / path / voice_name
        if path
        else Path(RECORD_PATH) / voice_name
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
    说明:
        生成一个 MessageSegment.text 消息
    参数:
        :param msg: 消息文本
    """
    return MessageSegment.text(msg)


def contact_user(qq: int) -> MessageSegment:
    """
    说明:
        生成一个 MessageSegment.contact_user 消息
    参数:
        :param qq: qq号
    """
    return MessageSegment.contact_user(qq)


def share(
        url: str, title: str, content: str = None, image_url: str = None
) -> MessageSegment:
    """
    说明:
        生成一个 MessageSegment.share 消息
    参数:
        :param url: 自定义分享的链接
        :param title: 自定义分享的包体
        :param content: 自定义分享的内容
        :param image_url: 自定义分享的展示图片
    """
    return MessageSegment.share(url, title, content, image_url)


def xml(data: str) -> MessageSegment:
    """
    说明:
        生成一个 MessageSegment.xml 消息
    参数:
        :param data: 数据文本
    """
    return MessageSegment.xml(data)


def json(data: str) -> MessageSegment:
    """
    说明:
        生成一个 MessageSegment.json 消息
    参数:
        :param data: 消息数据
    """
    return MessageSegment.json(data)


def face(id_: int) -> MessageSegment:
    """
    说明:
        生成一个 MessageSegment.face 消息
    参数:
        :param id_: 表情id
    """
    return MessageSegment.face(id_)


def poke(qq: int) -> MessageSegment:
    """
    说明:
        生成一个 MessageSegment.poke 消息
    参数:
        :param qq: qq号
    """
    return MessageSegment("poke", {"qq": qq})


def music(type_: str, id_: int) -> MessageSegment:
    return MessageSegment.music(type_, id_)


def custom_forward_msg(
        msg_list: List[Union[str, Message]], uin: Union[int, str], name: str = f"这里是{NICKNAME}"
) -> List[dict]:
    """
    说明:
        生成自定义合并消息
    参数:
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


class MessageBuilder:
    """
    MessageSegment构建工具
    """

    def __init__(self, msg: Union[str, MessageSegment, Message]):
        if msg:
            if isinstance(msg, str):
                self._msg = text(msg)
            else:
                self._msg = msg
        else:
            self._msg = text("")

    def text(self, msg: str):
        return MessageBuilder(self._msg + text(msg))

    def image(
        self,
        file: Union[str, Path, bytes] = None,
        path: str = None,
        b64: str = None,
    ):
        return MessageBuilder(self._msg + image(file, path, b64))

    def at(self, qq: int):
        return MessageBuilder(self._msg + at(qq))

    def face(self, id_: int):
        return MessageBuilder(self._msg + face(id_))
