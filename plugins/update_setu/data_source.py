from configs.path_config import IMAGE_PATH, TXT_PATH
import os
from util.user_agent import get_user_agent
from services.log import logger
from datetime import datetime
from util.img_utils import rar_imgs, get_img_hash
from util.utils import get_bot, get_local_proxy
from asyncio.exceptions import TimeoutError
import aiofiles
import aiohttp
try:
    import ujson as json
except ModuleNotFoundError:
    import json


async def update_setu_img():
    async with aiohttp.ClientSession(headers=get_user_agent()) as session:
        for file_name in ['setu_url.txt', 'setu_r18_url.txt']:
            if file_name == 'setu_url.txt':
                json_name = 'setu_img_hash.json'
                path = 'setu/'
            else:
                json_name = 'r18_setu_img_hash.json'
                path = 'r18/'
            try:
                data = json.load(open(TXT_PATH + json_name))
                if not data:
                    continue
            except (FileNotFoundError, TypeError):
                continue
            _success = 0
            _similar = 0
            try:
                with open(TXT_PATH + file_name, 'r') as f:
                    txt_data = f.read()
                if not txt_data:
                    continue
            except FileNotFoundError:
                continue
            urls = list(set(txt_data[:-1].split(',')))
            total = len(urls)
            for url in urls:
                index = str(len(os.listdir(IMAGE_PATH + path)))
                logger.info(f'开始更新 index:{index} --> {url}')
                for _ in range(3):
                    try:
                        async with session.get(url, proxy=get_local_proxy(), timeout=15) as response:
                            if response.status == 200:
                                async with aiofiles.open(IMAGE_PATH + 'rar/' + index + ".jpg", 'wb') as f:
                                    await f.write(await response.read())
                                    _success += 1
                            else:
                                logger.info(f'{url} 不存在，跳过更新')
                                break
                        if os.path.getsize(IMAGE_PATH + 'rar/' + str(index) + ".jpg") > 1024 * 1024 * 1.5:
                            rar_imgs(
                                'rar/',
                                path,
                                in_file_name=index,
                                out_file_name=index
                            )
                        else:
                            logger.info('不需要压缩，移动图片 ' + IMAGE_PATH + 'rar/' + index + ".jpg --> "
                                        + IMAGE_PATH + path + index + ".jpg")
                            os.rename(IMAGE_PATH + 'rar/' + index + ".jpg",
                                      IMAGE_PATH + path + index + ".jpg")
                        img_hash = str(get_img_hash(f'{IMAGE_PATH}{path}{index}.jpg'))
                        if img_hash in data.values():
                            logger.info(f'index:{index} 与 '
                                        f'{list(data.keys())[list(data.values()).index(img_hash)]} 存在重复，删除')
                            os.remove(IMAGE_PATH + path + index + ".jpg")
                            _similar += 1
                        data[index] = img_hash
                        break
                    except TimeoutError:
                        continue
            with open(TXT_PATH + json_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            open(TXT_PATH + file_name, 'w')
            logger.info(
                f'{str(datetime.now()).split(".")[0]} 更新 {file_name.split(".")[0]}完成，预计更新 {total} 张，实际更新 {_success} 张，相似 {_similar} 张，实际存入 {_success - _similar} 张')
            await get_bot().send_private_msg(
                user_id=775757368,
                message=f'{str(datetime.now()).split(".")[0]} 更新{file_name.split(".")[0]}完成，预计更新 {total} 张，实际更新 {_success} 张，相似 {_similar} 张，实际存入 {_success - _similar} 张'
            )
