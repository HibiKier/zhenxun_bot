#coding:utf-8
import aiohttp
from .config import DRAW_PATH
from asyncio.exceptions import TimeoutError
from bs4 import BeautifulSoup
import asyncio
from .util import download_img
from urllib.parse import unquote
from services.log import logger
from .util import remove_prohibited_str
import bs4
import re
try:
    import ujson as json
except ModuleNotFoundError:
    import json


headers = {'User-Agent': '"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"'}


async def update_info(url: str, game_name: str, info_list: list = None) -> 'dict, int':
    try:
        with open(DRAW_PATH + f'{game_name}.json', 'r', encoding='utf8') as f:
            data = json.load(f)
    except (ValueError, FileNotFoundError):
        data = {}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=7) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                _tbody = get_tbody(soup, game_name, url)
                trs = _tbody.find_all('tr')
                att_dict, start_index, index = init_attr(game_name)
                if game_name == 'guardian':
                    start_index = 1
                if game_name == 'azur':
                    start_index = 0
                for th in trs[0].find_all('th')[start_index:]:
                    text = th.text
                    if text[-1] == '\n':
                        text = text[:-1]
                    att_dict[text] = index
                    index += 1
                for tr in trs[1:]:
                    member_dict = {}
                    tds = tr.find_all('td')
                    if not info_list:
                        info_list = att_dict.keys()
                    for key in info_list:
                        key, attr = parse_key(key, game_name)
                        td = tds[att_dict[key]]
                        last_tag = unquote(_find_last_tag(td, attr, game_name), 'utf-8')
                        member_dict[key] = last_tag
                        member_dict = intermediate_check(member_dict, key, game_name, td)
                    avatar_img = await _modify_avatar_url(session, game_name, member_dict["名称"])
                    member_dict['头像'] = avatar_img if avatar_img else member_dict['头像']
                    member_dict, name = replace_update_name(member_dict, game_name)
                    await download_img(member_dict['头像'], game_name, name)
                    data[name] = member_dict
                    logger.info(f'{name} is update...')
            data = await _last_check(data, game_name, session)
    except TimeoutError:
        logger.warning(f'更新 {game_name} 超时...')
        return {}, 999
    with open(DRAW_PATH + f'{game_name}.json', 'w', encoding='utf8') as wf:
        wf.write(json.dumps(data, ensure_ascii=False, indent=4))
    return data, 200


def _find_last_tag(element: bs4.element.Tag, attr: str, game_name: str) -> str:
    last_tag = []
    for des in element.descendants:
        last_tag.append(des)
    if len(last_tag) == 1 and last_tag[0] == '\n':
        last_tag = ''
    elif last_tag[-1] == '\n':
        last_tag = last_tag[-2]
    else:
        last_tag = last_tag[-1]
    if attr and str(last_tag):
        last_tag = last_tag[attr]
    elif str(last_tag).find('<img') != -1:
        if last_tag.get('srcset'):
            last_tag = str(last_tag.get('srcset')).strip().split(' ')[-2].strip()
        else:
            last_tag = last_tag['src']
    else:
        last_tag = str(last_tag)
    if str(last_tag) and str(last_tag)[-1] == '\n':
        last_tag = str(last_tag)[:-1]

    if game_name not in ['pretty', 'pretty_card', 'guardian'] and last_tag.find('http') == -1:
        last_tag = last_tag.split('.')[0]

    return last_tag


# 获取大图（小图快爬）
async def _modify_avatar_url(session: aiohttp.ClientSession, game_name: str, char_name: str):
    # if game_name == 'prts':
    #     async with session.get(f'https://wiki.biligame.com/arknights/{char_name}', timeout=7) as res:
    #         soup = BeautifulSoup(await res.text(), 'lxml')
    #         try:
    #             img_url = str(soup.find('img', {'class': 'img-bg'})['srcset']).split(' ')[-2]
    #         except KeyError:
    #             img_url = str(soup.find('img', {'class': 'img-bg'})['src'])
    #         return img_url
    if game_name == 'genshin':
        return None
    if game_name == 'pretty_card':
        async with session.get(f'https://wiki.biligame.com/umamusume/{char_name}', timeout=7) as res:
            soup = BeautifulSoup(await res.text(), 'lxml')
            img_url = soup.find('div', {'class': 'support_card-left'}).find('div').find('img').get('src')
            return img_url
    if game_name == 'guardian':
        # 未上传图片太多，换成像素图
        # async with session.get(f'https://wiki.biligame.com/gt/{char_name}', timeout=7) as res:
        #     soup = BeautifulSoup(await res.text(), 'lxml')
        #     soup = soup.find('table', {'class': 'wikitable'}).find('tbody').find('tr')
        #     try:
        #         img_url = str(soup.find('img', {'class': 'img-kk'})['srcset']).split(' ')[-2]
        #     except KeyError:
        #         img_url = str(soup.find('img', {'class': 'img-kk'})['src'])
        #     except TypeError:
        #         logger.info(f'{char_name} 图片还未上传，跳过...')
        #         img_url = ''
        #     return img_url
        return None


# 数据最后处理（是否需要额外数据或处理数据）
async def _last_check(data: dict, game_name: str, session: aiohttp.ClientSession):
    # if game_name == 'prts':
    #     url = 'https://wiki.biligame.com/arknights/'
    #     tasks = []
    #     for key in data.keys():
    #         tasks.append(asyncio.ensure_future(_async_update_prts_extra_info(url, key, session)))
    #     asyResult = await asyncio.gather(*tasks)
    #     for x in asyResult:
    #         for key in x.keys():
    #             data[key]['获取途径'] = x[key]['获取途径']
    if game_name == 'genshin':
        for key in data.keys():
            async with session.get(f'https://wiki.biligame.com/ys/{key}', timeout=7) as res:
                soup = BeautifulSoup(await res.text(), 'lxml')
                _trs = ''
                for table in soup.find_all('table', {'class': 'wikitable'}):
                    if str(table).find('常驻/限定') != -1:
                        _trs = table.find('tbody').find_all('tr')
                        break
                for tr in _trs:
                    data[key]['常驻/限定'] = '未知'
                    if str(tr).find('限定UP') != -1:
                        data[key]['常驻/限定'] = '限定UP'
                        logger.info(f'原神获取额外数据 {key}...{data[key]["常驻/限定"]}')
                        break
                    elif str(tr).find('常驻UP') != -1:
                        data[key]['常驻/限定'] = '常驻UP'
                        logger.info(f'原神获取额外数据 {key}...{data[key]["常驻/限定"]}')
                        break
    if game_name == 'pretty':
        for keys in data.keys():
            for key in data[keys].keys():
                r = re.search(r'.*?40px-(.*)图标.png', str(data[keys][key]))
                if r:
                    data[keys][key] = r.group(1)
                    logger.info(f'赛马娘额外修改数据...{keys}[{key}]=> {r.group(1)}')
    if game_name == 'guardian':
        for keys in data.keys():
            for key in data[keys].keys():
                r = re.search(r'.*?-star_(.*).png', str(data[keys][key]))
                if r:
                    data[keys][key] = r.group(1)
                    logger.info(f'坎公骑士剑额外修改数据...{keys}[{key}] => {r.group(1)}')
    return data


# 对抓取每行数据是否需要额外处理？
def intermediate_check(member_dict: dict, key: str, game_name: str, td: bs4.element.Tag):
    if game_name == 'prts':
        if key == '获取途径':
            msg = re.search('<td.*?>([\\s\\S]*)</td>', str(td)).group(1).strip()
            msg = msg[:-1] if msg[-1] == '\n' else msg
            if msg.find('<a') != -1:
                for a in td.find_all('a'):
                    msg = msg.replace(str(a), a.text)
            member_dict['获取途径'] = msg.split('<br/>')
    if game_name == 'pretty':
        if key == '初始星级':
            member_dict['初始星级'] = len(td.find_all('img'))
    if game_name == 'guardian':
        if key == '头像':
            member_dict['星级'] = str(td.find('span').find('img')['alt'])[-5]
            try:
                member_dict['头像'] = str(td.find('img')['srcset']).split(' ')[0]
            except KeyError:
                member_dict['头像'] = str(td.find('img')['src'])
    return member_dict


def init_attr(game_name: str):
    att_dict = {'头像': 0, '名称': 1}
    start_index = 2
    index = 2
    if game_name == 'guardian':
        att_dict = {'头像': 0, '名称': 0}
        start_index = 1
        index = 1
    return att_dict, start_index, index


# 解析key
def parse_key(key: str, game_name):
    attr = ''
    if game_name == 'genshin_arms':
        if key.find('.') != -1:
            key = key.split('.')
            attr = key[-1]
            key = key[0]
    return key, attr


# 拿到名称
def replace_update_name(member_dict: dict, game_name: str):
    name = member_dict['名称']
    if game_name == 'pretty_card':
        name = member_dict['中文名']
        name = remove_prohibited_str(name)
        member_dict['中文名'] = name
    else:
        name = remove_prohibited_str(name)
        member_dict['名称'] = name
    return member_dict, name


# 拿到tbody，不同游戏tbody可能不同
def get_tbody(soup: bs4.BeautifulSoup, game_name: str, url: str):
    max_count = 0
    _tbody = None
    if game_name == 'guardian_arms':
        if url[-2:] == '盾牌':
            div = soup.find('div', {'class': 'resp-tabs-container'}).find_all('div', {'class': 'resp-tab-content'})[1]
            _tbody = div.find('tbody')
        else:
            div = soup.find('div', {'class': 'resp-tabs-container'}).find_all('div', {'class': 'resp-tab-content'})[0]
            _tbody = div.find('table', {'id': 'CardSelectTr'}).find('tbody')
    else:
        for tbody in soup.find_all('tbody'):
            if len(tbody.find_all('tr')) > max_count:
                _tbody = tbody
                max_count = len(tbody.find_all('tr'))
    return _tbody


# async def _async_update_prts_extra_info(url: str, key: str, session: aiohttp.ClientSession):
#     for i in range(10):
#         try:
#             async with session.get(f'https://wiki.biligame.com/arknights/{key}', timeout=7) as res:
#                 soup = BeautifulSoup(await res.text(), 'lxml')
#                 obtain = str(soup.find('table', {'class': 'wikitable'}).find('tbody').find_all('td')[-1])
#                 obtain = re.search(r'<td.*?>([\s\S]*)</.*?', obtain).group(1)
#                 obtain = obtain[:-1] if obtain[-1] == '\n' else obtain
#                 if obtain.find('<br/>'):
#                     obtain = obtain.split('<br/>')
#                 elif obtain.find('<br>'):
#                     obtain = obtain.split('<br>')
#                 for i in range(len(obtain)):
#                     if obtain[i].find('<a') != -1:
#                         text = ''
#                         for msg in obtain[i].split('</a>'):
#                             r = re.search('>(.*)', msg)
#                             if r:
#                                 text += r.group(1) + ' '
#                         obtain[i] = obtain[i].split('<a')[0] + text[:-1] + obtain[i].split('</a>')[-1]
#                 logger.info(f'明日方舟获取额外信息 {key}...{obtain}')
#                 x = {key: {}}
#                 x[key]['获取途径'] = obtain
#                 return x
#         except TimeoutError:
#             logger.warning(f'访问{url}{key} 第 {i}次 超时...已再次访问')
#     return {}

