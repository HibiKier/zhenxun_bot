from configs.config import NICKNAME
from typing import List
from configs.path_config import IMAGE_PATH
from services.log import logger
from utils.utils import cn2py
from pathlib import Path
import aiofiles
import aiohttp
import os


async def upload_image_to_local(
    img_list: List[str], path: str, user_id: int, group_id: int = 0
) -> str:
    _path = path
    path = Path(IMAGE_PATH) / cn2py(path)
    path.mkdir(parents=True, exist_ok=True)
    img_id = len(os.listdir(path))
    failed_list = []
    success_id = ""
    async with aiohttp.ClientSession() as session:
        for img_url in img_list:
            try:
                async with session.get(img_url, timeout=7) as response:
                    if response.status == 200:
                        async with aiofiles.open(path / f"{img_id}.jpg", "wb") as f:
                            await f.write(await response.read())
                            success_id += str(img_id) + "，"
                            img_id += 1
                    else:
                        failed_list.append(img_url)
                        logger.warning(f"图片：{img_url} 下载失败....")
            except TimeoutError as e:
                logger.warning(f"图片：{img_url} 下载超时....e:{e}")
                if img_url not in failed_list:
                    failed_list.append(img_url)
    failed_result = ""
    for img in failed_list:
        failed_result += str(img) + "\n"
    logger.info(
        f"USER {user_id}  GROUP {group_id}"
        f" 上传图片至 {_path} 共 {len(img_list)} 张，失败 {len(failed_list)} 张，id={success_id[:-1]}"
    )
    if failed_list:
        return (
            f"这次一共为 {_path}库 添加了 {len(img_list) - len(failed_list)} 张图片\n"
            f"依次的Id为：{success_id[:-1]}\n上传失败：{failed_result[:-1]}\n{NICKNAME}感谢您对图库的扩充!WW"
        )
    else:
        return f"这次一共为 {_path}库 添加了 {len(img_list)} 张图片\n依次的Id为：" \
               f"{success_id[:-1]}\n{NICKNAME}感谢您对图库的扩充!WW"
