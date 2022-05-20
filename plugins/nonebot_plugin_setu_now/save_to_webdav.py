from io import BytesIO

from nonebot import get_driver
from nonebot.log import logger
from webdav4.client import Client as dav_client

from configs.config import Config
from .models import Setu

setu_dav_url = Config.get_config("nonebot_plugin_setu_now", "SETU_DAV_URL")
setu_dav_username = Config.get_config("nonebot_plugin_setu_now", "SETU_DAV_USERNAME")
setu_dav_password = Config.get_config("nonebot_plugin_setu_now", "SETU_DAV_PASSWORD")
setu_path = Config.get_config("nonebot_plugin_setu_now", "SETU_PATH")

logger.info(
    "setu将会保存在 WebDAV 服务器中, URL: {}, UserName: {}, Path: {}".format(
        setu_dav_url, setu_dav_username, setu_path
    )
)


def upload_file(img: BytesIO, pid, p, r18, title, author):
    client = dav_client(
        setu_dav_url,  # type: ignore
        auth=(setu_dav_username, setu_dav_password),  # type: ignore
    )
    path = f"{setu_path}{'r18' if r18 else '' }/{pid}_{p}_{title}_{author}.jpg"
    client.upload_fileobj(img, to_path=path, overwrite=True)  # type: ignore
    logger.debug(f"WebDAV: {setu_dav_url} 图片已保存{path}")


def convert_file(bytes_file):
    file = BytesIO(bytes_file)
    return file


async def save_img(setu: Setu):
    upload_file(
        convert_file(setu.img), setu.pid, setu.p, setu.r18, setu.title, setu.author
    )
