import aiohttp
from .config import DRAW_PATH, SEMAPHORE
from asyncio.exceptions import TimeoutError
from .util import download_img
from bs4 import BeautifulSoup
from .util import remove_prohibited_str
from services.log import logger
import asyncio
try:
    import ujson as json
except ModuleNotFoundError:
    import json


headers = {'User-Agent': '"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"'}


async def update_requests_info(game_name: str):
    try:
        with open(DRAW_PATH + f'{game_name}.json', 'r', encoding='utf8') as f:
            data = json.load(f)
    except (ValueError, FileNotFoundError):
        data = {}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            if game_name in ['fgo', 'fgo_card']:
                if game_name == 'fgo':
                    url = 'http://fgo.vgtime.com/servant/ajax?card=&wd=&ids=&sort=12777&o=desc&pn='
                else:
                    url = 'http://fgo.vgtime.com/equipment/ajax?wd=&ids=&sort=12958&o=desc&pn='
                for i in range(9999):
                    async with session.get(f'{url}{i}', timeout=7) as response:
                        fgo_data = json.loads(await response.text())
                        if int(fgo_data['nums']) == 0:
                            break
                        for x in fgo_data['data']:
                            x['name'] = remove_prohibited_str(x['name'])
                            key = x['name']
                            data = add_to_data(data, x, game_name)
                            await download_img(data[key]['头像'], game_name, key)
                            logger.info(f'{key} is update...')
            if game_name == 'onmyoji':
                url = 'https://yys.res.netease.com/pc/zt/20161108171335/js/app/all_shishen.json?v74='
                async with session.get(f'{url}', timeout=7) as response:
                    onmyoji_data = await response.json()
                    for x in onmyoji_data:
                        x['name'] = remove_prohibited_str(x['name'])
                        key = x['name']
                        data = add_to_data(data, x, game_name)
                        logger.info(f'{key} is update...')
            data = await _last_check(data, game_name, session)
    except TimeoutError:
        logger.warning(f'更新 {game_name} 超时...')
        return {}, 999
    with open(DRAW_PATH + f'{game_name}.json', 'w', encoding='utf8') as wf:
        json.dump(data, wf, ensure_ascii=False, indent=4)
    return data, 200


# 添加到字典
def add_to_data(data: dict, x: dict, game_name: str) -> dict:
    member_dict = {}
    if game_name == 'fgo':
        member_dict = {
            'id': x['id'],
            'card_id': x['charid'],
            '头像': x['icon'],
            '名称': x['name'],
            '职阶': x['classes'],
            '星级': x['star'],
            'hp': x['lvmax4hp'],
            'atk': x['lvmax4atk'],
            'card_quick': x['cardquick'],
            'card_arts': x['cardarts'],
            'card_buster': x['cardbuster'],
            '宝具': x['tprop'],
        }
    if game_name == 'fgo_card':
        member_dict = {
            'id': x['id'],
            'card_id': x['equipid'],
            '头像': x['icon'],
            '名称': x['name'],
            '星级': x['star'],
            'hp': x['lvmax_hp'],
            'atk': x['lvmax_atk'],
            'skill_e': x['skill_e'].split('<br />')[: -1],
        }
    if game_name == 'onmyoji':
        member_dict = {
            'id': x['id'],
            '名称': x['name'],
            '星级': x['level'],
        }
    data[member_dict['名称']] = member_dict
    return data


# 获取额外数据
async def _last_check(data: dict, game_name: str, session: aiohttp.ClientSession) -> dict:
    if game_name == 'fgo':
        url = 'http://fgo.vgtime.com/servant/'
        tasks = []
        semaphore = asyncio.Semaphore(SEMAPHORE)
        for key in data.keys():
            tasks.append(asyncio.ensure_future(_async_update_fgo_extra_info(url, key, data[key]['id'], session, semaphore)))
        asyResult = await asyncio.gather(*tasks)
        for x in asyResult:
            for key in x.keys():
                data[key]['入手方式'] = x[key]['入手方式']
    if game_name == 'onmyoji':
        url = 'https://yys.163.com/shishen/{}.html'
        for key in data.keys():
            async with session.get(f'{url.format(data[key]["id"])}', timeout=7) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                data[key]['头像'] = "https:" + soup.find('div', {'class': 'pic_wrap'}).find('img')['src']
                await download_img(data[key]['头像'], game_name, key)
    return data


async def _async_update_fgo_extra_info(url: str, key: str, _id: str, session: aiohttp.ClientSession, semaphore):
    # 防止访问超时
    async with semaphore:
        for i in range(10):
            try:
                async with session.get(f'{url}{_id}', timeout=7) as response:
                    soup = BeautifulSoup(await response.text(), 'lxml')
                    obtain = soup.find('table', {'class': 'uk-table uk-codex-table'}).find_all('td')[-1].text
                    if obtain.find('限时活动免费获取 活动结束后无法获得') != -1:
                        obtain = ['活动获取']
                    elif obtain.find('非限时UP无法获得') != -1:
                        obtain = ['限时召唤']
                    else:
                        if obtain.find('&') != -1:
                            obtain = obtain.strip().split('&')
                        else:
                            obtain = obtain.strip().split(' ')
                    logger.info(f'Fgo获取额外信息 {key}....{obtain}')
                    x = {key: {}}
                    x[key]['入手方式'] = obtain
                    return x
            except TimeoutError:
                logger.warning(f'访问{url}{_id} 第 {i}次 超时...已再次访问')
    return {}






