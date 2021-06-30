from configs.path_config import IMAGE_PATH, TXT_PATH
import os
from utils.user_agent import get_user_agent
from services.log import logger
from datetime import datetime
from utils.img_utils import rar_imgs, get_img_hash
from utils.utils import get_bot, get_local_proxy
from asyncio.exceptions import TimeoutError
import aiofiles
import aiohttp
from aiohttp.client_exceptions import ClientConnectorError

try:
    import ujson as json
except ModuleNotFoundError:
    import json


async def update_setu_img():
    async with aiohttp.ClientSession(headers=get_user_agent()) as session:
        for file_name in ['setu_url.json', 'setu_r18_url.json']:
            if file_name == 'setu_url.json':
                json_name = 'setu_data.json'
                path = '_setu/'
                rar_path = 'setu_rar/'
            else:
                json_name = 'r18_setu_data.json'
                path = '_r18/'
                rar_path = 'r18_rar/'
            if not os.path.exists(IMAGE_PATH + path):
                os.mkdir(IMAGE_PATH + path)
            if not os.path.exists(IMAGE_PATH + rar_path):
                os.mkdir(IMAGE_PATH + rar_path)
            try:
                data = json.load(open(TXT_PATH + json_name, encoding='utf8'))
                if not data:
                    data = {}
            except (FileNotFoundError, TypeError):
                data = {}
            _success = 0
            _similar = 0
            try:
                with open(TXT_PATH + file_name, 'r', encoding='utf8') as f:
                    txt_data = json.load(f)
                if not txt_data:
                    continue
            except (FileNotFoundError, ValueError):
                continue
            total = len(txt_data)
            urls = [data[x]['img_url'] for x in data.keys()]
            for pid in txt_data.keys():
                index = str(len(os.listdir(IMAGE_PATH + path)))
                url = txt_data[pid]["img_url"].replace('img-master', 'img-original').replace('_master1200', '')
                if url in urls or txt_data[pid]["img_url"] in urls:
                    continue
                logger.info(f'开始更新 index:{index} --> {url}')
                for _ in range(3):
                    try:
                        async with session.get(url, proxy=get_local_proxy(), timeout=15) as response:
                            if response.status == 200:
                                async with aiofiles.open(IMAGE_PATH + rar_path + index + ".jpg", 'wb') as f:
                                    await f.write(await response.read())
                                    _success += 1
                            else:
                                logger.info(f'{url} 不存在，使用更新原url')
                                url = txt_data[pid]["img_url"]
                                async with session.get(txt_data[pid]["img_url"], proxy=get_local_proxy(),
                                                       timeout=15) as response:
                                    if response.status == 200:
                                        async with aiofiles.open(IMAGE_PATH + rar_path + index + ".jpg", 'wb') as f:
                                            await f.write(await response.read())
                                            _success += 1
                        try:
                            if os.path.getsize(IMAGE_PATH + rar_path + str(index) + ".jpg") > 1024 * 1024 * 1.5:
                                rar_imgs(
                                    rar_path,
                                    path,
                                    in_file_name=index,
                                    out_file_name=index
                                )
                            else:
                                logger.info('不需要压缩，移动图片 ' + IMAGE_PATH + rar_path + index + ".jpg --> "
                                            + IMAGE_PATH + path + index + ".jpg")
                                os.rename(IMAGE_PATH + rar_path + index + ".jpg",
                                          IMAGE_PATH + path + index + ".jpg")
                        except FileNotFoundError:
                            logger.warning(f'文件 {index}.jpg 不存在，跳过...')
                            _success -= 1
                            continue
                        img_hash = str(get_img_hash(f'{IMAGE_PATH}{path}{index}.jpg'))
                        if img_hash in [data[x]['img_hash'] for x in data.keys()]:
                            logger.info(f'index:{index} 与 '
                                        f'{[data[x]["img_hash"] for x in data.keys()].index(img_hash)} 存在重复，删除')
                            os.remove(IMAGE_PATH + path + index + ".jpg")
                            _similar += 1
                        else:
                            data[index] = {
                                'title': txt_data[pid]['title'],
                                'author': txt_data[pid]['author'],
                                'pid': txt_data[pid]['pid'],
                                'img_hash': img_hash,
                                'img_url': url,
                                'tags': txt_data[pid]['tags'],
                            }
                        break
                    except (TimeoutError, ClientConnectorError) as e:
                        logger.warning(f'{url} 更新失败 ..{type(e)}：{e}')
                        continue
                    except Exception as e:
                        await get_bot().send_private_msg(
                            user_id=int(list(get_bot().config.superusers)[0]),
                            message=f'更新 {index}.jpg 色图错误 {type(e)}: {e}'
                        )
                        _success -= 1
                        logger.error(f'更新色图 {index}.jpg 错误 {type(e)}: {e}')
                        continue
            with open(TXT_PATH + json_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            open(TXT_PATH + file_name, 'w')
            logger.info(
                f'{str(datetime.now()).split(".")[0]} 更新 {file_name.split(".")[0]}完成，预计更新 {total} 张，'
                f'实际更新 {_success} 张，相似 {_similar} 张，实际存入 {_success - _similar} 张')
            await get_bot().send_private_msg(
                user_id=int(list(get_bot().config.superusers)[0]),
                message=f'{str(datetime.now()).split(".")[0]} 更新{file_name.split(".")[0]}完成，预计更新 {total} 张，'
                        f'实际更新 {_success} 张，相似 {_similar} 张，实际存入 {_success - _similar} 张'
            )
