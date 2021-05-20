from configs.path_config import IMAGE_PATH, VOICE_PATH
from nonebot.adapters.cqhttp.message import MessageSegment
import os
from services.log import logger


def image(img_name: str = None, path: str = '', abspath: str = None, b64: str = None):
    if abspath:
        if os.path.exists(abspath):
            return MessageSegment.image("file:///" + abspath)
        else:
            return ''
    elif b64:
        if b64.find('base64://') != -1:
            return MessageSegment.image(b64)
        else:
            return MessageSegment.image('base64://' + b64)
    else:
        img_name = str(img_name)
        if img_name.find('http') == -1:
            if len(img_name.split('.')) == 1:
                img_name += '.jpg'
            if os.path.exists(IMAGE_PATH + path + '/' + img_name):
                return MessageSegment.image("file:///" + IMAGE_PATH + path + '/' + img_name)
            else:
                logger.warning(f"图片 {path}/{img_name}缺失.")
                return ''
        else:
            return MessageSegment.image(img_name)


def at(qq):
    return MessageSegment.at(qq)


def record(voice_name='', path=''):
    if len(voice_name.split('.')) == 1:
        voice_name += '.mp3'
    if path == "":
        name = VOICE_PATH + "{}.".format(voice_name)
    else:
        name = VOICE_PATH + "{}/{}".format(path, voice_name)
    if voice_name.find('http') == -1:
        if os.path.exists(name):
            result = MessageSegment.record("file:///" + name)
            return result
        else:
            logger.warning(f"语音{path}/{voice_name}缺失...")
            return ""
    else:
        return MessageSegment.record(voice_name)


def text(msg):
    return MessageSegment.text(msg)


def contact_user(qq):
    return MessageSegment.contact_user(qq)


def share(url, title, content='', image_url=''):
    return MessageSegment.share(url, title, content, image_url)


def xml(data):
    return MessageSegment.xml(data)


def json(data):
    return MessageSegment.json(data)


def face(id_):
    return MessageSegment.face(id_)


def poke(qq):
    return MessageSegment('poke', {"qq": qq})


def forward():
    return MessageSegment.forward()

# if __name__ == '__main__':
#     print(get_record_result("dadada", "", type="amr"))
