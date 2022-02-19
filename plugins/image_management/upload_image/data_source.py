from configs.config import NICKNAME
from typing import List
from configs.path_config import IMAGE_PATH
from services.log import logger
from utils.utils import cn2py
from utils.http_utils import AsyncHttpx
import os


_path = IMAGE_PATH / "image_management"


async def upload_image_to_local(
    img_list: List[str], path_: str, user_id: int, group_id: int = 0
) -> str:
    _path_name = path_
    path = _path / cn2py(path_)
    if not path.exists() and (path.parent.parent / cn2py(path_)).exists():
        path = path.parent.parent / cn2py(path_)
    path.mkdir(parents=True, exist_ok=True)
    img_id = len(os.listdir(path))
    failed_list = []
    success_id = ""
    for img_url in img_list:
        if await AsyncHttpx.download_file(img_url, path / f"{img_id}.jpg"):
            success_id += str(img_id) + "，"
            img_id += 1
        else:
            failed_list.append(img_url)
    failed_result = ""
    for img in failed_list:
        failed_result += str(img) + "\n"
    logger.info(
        f"USER {user_id}  GROUP {group_id}"
        f" 上传图片至 {_path_name} 共 {len(img_list)} 张，失败 {len(failed_list)} 张，id={success_id[:-1]}"
    )
    if failed_list:
        return (
            f"这次一共为 {_path_name}库 添加了 {len(img_list) - len(failed_list)} 张图片\n"
            f"依次的Id为：{success_id[:-1]}\n上传失败：{failed_result[:-1]}\n{NICKNAME}感谢您对图库的扩充!WW"
        )
    else:
        return (
            f"这次一共为 {_path_name}库 添加了 {len(img_list)} 张图片\n依次的Id为："
            f"{success_id[:-1]}\n{NICKNAME}感谢您对图库的扩充!WW"
        )
