from configs.path_config import IMAGE_PATH, TXT_PATH
import os
import random
from util.init_result import image
from configs.config import LOLICON_KEY
import aiohttp
import aiofiles
from services.log import logger
from util.img_utils import get_img_hash
from util.utils import get_local_proxy, is_number
from asyncio.exceptions import TimeoutError
from models.count_user import UserCount
from configs.config import DOWNLOAD_SETU
try:
    import ujson as json
except ModuleNotFoundError:
    import json


url = "https://api.lolicon.app/setu/"
path = 'setu/'


async def get_setu_urls(keyword: str, num: int = 1, r18: int = 0):
    # print(keyword)
    if r18 == 1:
        file_name = 'setu_r18_url.txt'
    else:
        file_name = 'setu_url.txt'
    try:
        with open(TXT_PATH + file_name, 'r') as f:
            txt_data = f.read()
    except FileNotFoundError:
        txt_data = ''
    params = {
        "apikey": LOLICON_KEY,  # 添加apikey
        'r18': r18,  # 添加r18参数 0为否，1为是，2为混合
        'keyword': keyword,  # 若指定关键字，将会返回从插画标题、作者、标签中模糊搜索的结果
        'num': num,  # 一次返回的结果数量，范围为1到10，不提供 APIKEY 时固定为1
        'size1200': 1,  # 是否使用 master_1200 缩略图，以节省流量或提升加载速度
        }
    urls = []
    text_list = []
    for count in range(3):
        print(f'get_setu_url: count --> {count}')
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, proxy=get_local_proxy(), timeout=5, params=params) as response:
                    if response.status == 429:
                        return '调用达到上限，明日赶早呀~', '', 429
                    if response.status == 404:
                        return "网站裂开了...", '', 998
                    if response.status == 200:
                        data = await response.json()
                        if data['code'] == 0:
                            # print(len(data['data']))
                            for i in range(len(data['data'])):
                                img_url = data['data'][i]['url']
                                title = data['data'][i]['title']
                                author = data['data'][i]['author']
                                pid = data['data'][i]['pid']
                                urls.append(img_url)
                                text_list.append(f'title：{title}\nauthor：{author}\nPID：{pid}')
                                img_url = str(img_url).replace('img-master', 'img-original').replace('_master1200', '')
                                txt_data += img_url + ','
                            with open(TXT_PATH + file_name, 'w') as f:
                                f.write(txt_data)
                            return urls, text_list, 200
                        else:
                            return "没找到符合条件的色图...", '', 401
            except TimeoutError:
                pass
    return '我网线被人拔了..QAQ', '', 999


async def search_online_setu(url: str):
    async with aiohttp.ClientSession() as session:
        for i in range(3):
            print(f'search_online_setu --> {i}')
            try:
                async with session.get(url, proxy=get_local_proxy(), timeout=7) as res:
                    if res.status == 200:
                        index = str(random.randint(1, 100000))
                        async with aiofiles.open(IMAGE_PATH + 'temp/' + index + "_temp_setu.jpg", 'wb') as f:
                            try:
                                await f.write(await res.read())
                            except TimeoutError:
                                # return '\n这图没下载过来~（网太差？）', -1, False
                                continue
                        logger.info(f"下载 lolicon图片 {url} 成功， id：{index}")
                        return image(f'{index}_temp_setu.jpg', 'temp'), index
                    else:
                        logger.warning(f"访问 lolicon图片 {url} 失败 status：{res.status}")
                        # return '\n这图好难下载啊！QAQ', -1, False
            except TimeoutError:
                pass
        return '\n图片被小怪兽恰掉啦..!QAQ', -1


def get_setu(index: str):
    length = len(os.listdir(IMAGE_PATH + path))
    if length == 0:
        return None, None
    if not index:
        index = random.randint(0, length - 1)
    if is_number(index):
        if int(index) > length or int(index) < 0:
            return f"超过当前上下限！({length - 1})", 999
        else:
            return f'id：{index}' + image(f'{index}.jpg', 'setu'), index
    return None, None


def get_luoxiang(impression):
    probability = impression + 70
    if probability < random.randint(1, 101):
        return "我为什么要给你发这个？" + image(random.choice(os.listdir(IMAGE_PATH + "luoxiang/")), 'luoxiang') + \
               "\n(快向小真寻签到提升好感度吧！)"
    return None


async def check_r18_and_keyword(msg: str, user_id) -> 'str, int, int':
    msg_list = msg.split(' ')
    num = 1
    r18 = 0
    keyword = ''
    if len(msg_list) == 1:
        if msg_list[0].strip().lower() in ['r', 'r18']:
            r18 = 1
            num = 10
        else:
            keyword = msg_list[0]
    elif len(msg_list) == 2:
        keyword = msg_list[1].strip()
        if msg_list[0].strip().lower() in ['r', 'r18']:
            r18 = 1
            num = 10
    else:
        keyword = msg[0]
    if r18 == 1:
        await UserCount.add_user(user_id)
    return keyword, r18, num


# def delete_img(index):
#     if os.path.exists(IMAGE_PATH + path + f"{index}.jpg"):
#         img_hash = str(get_img_hash(IMAGE_PATH + f"setu/{index}.jpg"))
#         tp = list(setu_hash_dict.keys())[list(setu_hash_dict.values()).index(img_hash)]
#         logger.info(f"色图 {index}.jpg 与 {tp}.jpg 相似， 删除....")
#         os.remove(IMAGE_PATH + path + f"{index}.jpg")


async def find_img_index(img_url, user_id):
    try:
        setu_hash_dict = json.load(open(TXT_PATH + 'setu_img_hash.json'))
    except (FileNotFoundError, ValueError):
        setu_hash_dict = {}
    async with aiohttp.ClientSession() as session:
        async with session.get(img_url, proxy=get_local_proxy(), timeout=5) as res:
            async with aiofiles.open(IMAGE_PATH + f"temp/{user_id}_find_setu_index.jpg", 'wb') as f:
                await f.write(await res.read())
    img_hash = str(get_img_hash(IMAGE_PATH + f"temp/{user_id}_find_setu_index.jpg"))
    try:
        tp = list(setu_hash_dict.keys())[list(setu_hash_dict.values()).index(img_hash)]
        return "id --> " + str(tp)
    except ValueError:
        return "该图不在色图库中！"


