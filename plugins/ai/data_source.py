from configs.config import TL_KEY, ALAPI_TOKEN
import aiohttp
import random
import os
from configs.path_config import IMAGE_PATH, DATA_PATH
from services.log import logger
from utils.init_result import image, face
from utils.utils import get_bot
import re

try:
    import ujson as json
except ModuleNotFoundError:
    import json

url = "http://openapi.tuling123.com/openapi/api/v2"

check_url = "https://v2.alapi.cn/api/censor/text"

index = 0

anime_data = json.load(open(DATA_PATH + 'anime.json', 'r', encoding='utf8'))


# 图灵AI
async def get_qqbot_chat_result(text: str, img_url: str, user_id: int, user_name: str) -> str:
    global index
    if index == 5:
        index = 0
    if len(text) < 6 and random.random() < 0.6:
        keys = anime_data.keys()
        for key in keys:
            if text.find(key) != -1:
                return random.choice(anime_data[key]).replace('你', user_name)
    try:
        if text:
            req = {
                "perception":
                    {
                        "inputText":
                            {
                                "text": text
                            },
                        "selfInfo":
                            {
                                "location":
                                    {
                                        "city": "陨石坑",
                                        "province": "火星",
                                        "street": "第5坑位"
                                    }
                            }
                    },
                "userInfo":
                    {
                        "apiKey": TL_KEY[index],
                        "userId": str(user_id)
                    }
            }
        elif img_url:
            req = {
                "reqType": 1,
                "perception":
                    {
                        "inputImage": {
                            "url": img_url
                        },
                        "selfInfo":
                            {
                                "location":
                                    {
                                        "city": "陨石坑",
                                        "province": "火星",
                                        "street": "第5坑位"
                                    }
                            }
                    },
                "userInfo":
                    {
                        "apiKey": TL_KEY[index],
                        "userId": str(user_id)
                    }
            }
    except IndexError:
        index = 0
        return no_result()
    async with aiohttp.ClientSession() as sess:
        async with sess.post(url, json=req) as response:
            if response.status != 200:
                return ''
            resp_payload = json.loads(await response.text())
            if resp_payload['intent']:
                if int(resp_payload['intent']['code']) in [4003]:
                    index += 1
                    # 该AI很屑！！！！！！！！！！！！
                    async with sess.get(f'http://api.qingyunke.com/api.php?key=free&appid=0&msg={text}') as res:
                        data = json.loads(await res.text())
                        if data['result'] == 0:
                            content = data['content']
                            if content.find('菲菲') != -1:
                                content = content.replace('菲菲', list(get_bot().config.nickname)[0])
                            if content.find('公众号') != -1:
                                content = ''
                            if content.find('{br}') != -1:
                                content = content.replace('{br}', '\n')
                            if content.find('提示') != -1:
                                content = content[:content.find('提示')]
                            while True:
                                r = re.search('{face:(.*)}', content)
                                if r:
                                    id_ = r.group(1)
                                    content = content.replace('{' + f'face:{id_}' + '}', str(face(id_)))
                                else:
                                    break
                            return content
            if resp_payload['results']:
                for result in resp_payload['results']:
                    if result['resultType'] == 'text':
                        text = result['values']['text']
                        if user_name:
                            text = text.replace('小朋友', user_name)
                            if len(user_name) < 5:
                                if random.random() < 0.5:
                                    user_name = "~".join(user_name) + '~'
                                    if random.random() < 0.2:
                                        if user_name.find('大人') == -1:
                                            user_name += '大~人~'
                            text = text.replace('小主人', user_name)
                        return text


def hello() -> str:
    result = random.choice((
        "哦豁？！",
        "你好！Ov<",
        f"库库库，呼唤{list(get_bot().config.nickname)[0]}做什么呢",
        "我在呢！",
        "呼呼，叫俺干嘛"
    ))
    img = random.choice(os.listdir(IMAGE_PATH + "zai/"))
    if img[-4:] == ".gif":
        result += image(img, "zai")
    else:
        result += image(img, "zai")
    return result


def no_result() -> str:
    return random.choice([
        '你在说啥子？',
        f'纯洁的{list(get_bot().config.nickname)[0]}没听懂',
        '下次再告诉你(下次一定)',
        '你觉得我听懂了吗？嗯？',
        '我！不！知！道！'
    ]) + image(
        random.choice(os.listdir(IMAGE_PATH + "noresult/")
                      ), "noresult")


async def check_text(text: str):
    if not ALAPI_TOKEN:
        return text
    params = {
        'token': ALAPI_TOKEN,
        'text': text
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=2, params=params) as response:
                data = await response.json()
                if data['code'] == 200:
                    if data['conclusion_type'] == 2:
                        return no_result()
        except Exception as e:
            logger.error(f'检测违规文本错误...e：{e}')
        return text
