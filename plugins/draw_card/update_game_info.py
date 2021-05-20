#coding:utf-8
import aiohttp
from configs.path_config import DRAW_PATH
from asyncio.exceptions import TimeoutError
from services.log import logger
from bs4 import BeautifulSoup
from .util import download_img
from urllib.parse import unquote
import bs4
from util.user_agent import get_user_agent
import re
try:
    import ujson as json
except ModuleNotFoundError:
    import json


async def update_info(url: str, game_name: str, info_list: list = None) -> 'dict, int':
    try:
        with open(DRAW_PATH + f'/draw_card_config/{game_name}.json', 'r', encoding='utf8') as f:
            data = json.load(f)
    except (ValueError, FileNotFoundError):
        data = {}
    try:
        async with aiohttp.ClientSession(headers=get_user_agent()) as session:
            async with session.get(url, timeout=7) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                max_count = 0
                _tbody = None
                for tbody in soup.find_all('tbody'):
                    if len(tbody.find_all('tr')) > max_count:
                        _tbody = tbody
                        max_count = len(tbody.find_all('tr'))
                trs = _tbody.find_all('tr')
                att_dict = {'头像': 0, '名称': 1}
                index = 2
                for th in trs[0].find_all('th')[2:]:
                    text = th.text
                    if text[-1] == '\n':
                        text = text[:-1]
                    att_dict[text] = index
                    index += 1
                for tr in trs[1:]:
                    member_dict = {}
                    k_name = ''
                    tds = tr.find_all('td')
                    if not info_list:
                        info_list = att_dict.keys()
                    for key in info_list:
                        attr = ''
                        if key.find('.') != -1:
                            key = key.split('.')
                            attr = key[-1]
                            key = key[0]
                        td = tds[att_dict[key]]
                        last_tag = unquote(_find_last_tag(td, attr), 'utf-8')
                        if game_name.find('pretty') == -1 and last_tag.find('http') == -1:
                            last_tag = last_tag.split('.')[0]
                        if key == '名称':
                            k_name = last_tag
                        member_dict[key] = last_tag
                        if game_name == 'pretty' and key == '初始星级':
                            member_dict['初始星级'] = len(td.find_all('img'))
                    avatar_img = await _modify_avatar_url(session, game_name, member_dict["名称"])
                    if avatar_img:
                        member_dict['头像'] = avatar_img
                    name = member_dict['名称']
                    if game_name == 'pretty_card':
                        name = member_dict['中文名']
                    await download_img(member_dict['头像'], game_name, name)
                    if k_name:
                        data[k_name] = member_dict
                    logger.info(f'{k_name} is update...')
            data = await _last_check(data, game_name, session)
    except TimeoutError:
        return {}, 999
    with open(DRAW_PATH + f'/draw_card_config/{game_name}.json', 'w', encoding='utf8') as wf:
        wf.write(json.dumps(data, ensure_ascii=False, indent=4))
    return data, 200


def _find_last_tag(element: bs4.element.Tag, attr: str) -> str:
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
    return last_tag


# 获取大图（小图快爬）
async def _modify_avatar_url(session: aiohttp.ClientSession, game_name: str, char_name: str):
    if game_name == 'prts':
        async with session.get(f'https://wiki.biligame.com/arknights/{char_name}', timeout=7) as res:
            soup = BeautifulSoup(await res.text(), 'lxml')
            try:
                img_url = str(soup.find('img', {'class': 'img-bg'})['srcset']).split(' ')[-2]
            except KeyError:
                img_url = str(soup.find('img', {'class': 'img-bg'})['src'])
            return img_url
    if game_name == 'genshin':
        return None
    if game_name == 'pretty_card':
        async with session.get(f'https://wiki.biligame.com/umamusume/{char_name}', timeout=7) as res:
            soup = BeautifulSoup(await res.text(), 'lxml')
            img_url = soup.find('div', {'class': 'support_card-left'}).find('div').find('img').get('src')
            return img_url


# 数据最后处理（是否需要额外数据）
async def _last_check(data: dict, game_name: str, session: aiohttp.ClientSession):
    if game_name == 'prts':
        for key in data.keys():
            async with session.get(f'https://wiki.biligame.com/arknights/{key}', timeout=7) as res:
                soup = BeautifulSoup(await res.text(), 'lxml')
                obtain = str(soup.find('table', {'class': 'wikitable'}).find('tbody').find_all('td')[-1])
                obtain = re.search(r'<td.*?>([\s\S]*)</.*?', obtain).group(1)
                obtain = obtain[:-1] if obtain[-1] == '\n' else obtain
                if obtain.find('<br/>'):
                    obtain = obtain.split('<br/>')
                elif obtain.find('<br>'):
                    obtain = obtain.split('<br>')
                data[key]['获取途径'] = obtain
    # if game_name == 'genshin':
    #     for key in data.keys():
    #         async with session.get(f'https://wiki.biligame.com/ys/{key}', timeout=7) as res:
    #             soup = BeautifulSoup(await res.text(), 'lxml')
    #             trs = soup.find('div', {'class': 'poke-bg'}).find('table').find('tbody').find_all('tr')
    #             for tr in trs:
    #                 if tr.find('th').text.find('常驻/限定') != -1:
    #                     data[key]['常驻/限定'] = tr.find('td').text
    #                     break
    if game_name == 'pretty':
        for keys in data.keys():
            for key in data[keys].keys():
                # print(f'key --> {data[keys][key]}')
                r = re.search(r'.*?40px-(.*)图标.png', str(data[keys][key]))
                if r:
                    data[keys][key] = r.group(1)
    return data




# ul = soup.find('div', {'class': 'savelist_bot'}).find('ul')


