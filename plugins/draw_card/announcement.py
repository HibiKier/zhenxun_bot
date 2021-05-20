import aiohttp
from bs4 import BeautifulSoup
import re
from datetime import datetime
from pathlib import Path
from configs.path_config import DRAW_PATH
from util.user_agent import get_user_agent

try:
    import ujson as json
except ModuleNotFoundError:
    import json

up_char_file = Path(DRAW_PATH) / "draw_card_up" / "prts_up_char.json"

prts_url = "https://wiki.biligame.com/arknights/%E6%96%B0%E9%97%BB%E5%85%AC%E5%91%8A"


def _get_up_char(r: str, text: str):
    pr = re.search(r, text)
    chars = pr.group(1)
    probability = pr.group(2)
    chars = chars.replace('[限定]', '').replace('[', '').replace(']', '')
    probability = probability.replace('【', '')
    return chars, probability


class PrtsAnnouncement:

    @staticmethod
    async def get_announcement_text():
        async with aiohttp.ClientSession(headers=get_user_agent()) as session:
            async with session.get(prts_url, timeout=7) as res:
                soup = BeautifulSoup(await res.text(), 'lxml')
                trs = soup.find('table').find('tbody').find_all('tr')
                for tr in trs:
                    a = tr.find_all('td')[-1].find('a')
                    if a.text.find('寻访') != -1:
                        url = a.get('href')
                        break
            async with session.get(f'https://wiki.biligame.com/{url}', timeout=7) as res:
                return await res.text(), a.text[:-4]

    @staticmethod
    async def update_up_char():
        up_char_file.parent.mkdir(parents=True, exist_ok=True)
        data = {'up_char': {'6': {}, '5': {}, '4': {}}, 'title': '', 'time': ''}
        text, title = await PrtsAnnouncement.get_announcement_text()
        soup = BeautifulSoup(text, 'lxml')
        data['title'] = title
        context = soup.find('div', {'id': 'mw-content-text'}).find('div')
        data['pool_img'] = str(context.find('div', {'class': 'center'}).find('div').find('a').
                               find('img').get('srcset')).split(' ')[-2]
        # print(context.find_all('p'))
        for p in context.find_all('p')[1:]:
            if p.text.find('活动时间') != -1:
                pr = re.search(r'.*?活动时间：(.*)', p.text)
                data['time'] = pr.group(1)
            elif p.text.find('★★★★★★') != -1:
                chars, probability = _get_up_char(r'.*?★★★★★★：(.*?)（.*?出率的?(.*?)%.*?）.*?', p.text)
                slt = '/'
                if chars.find('\\') != -1:
                    slt = '\\'
                for char in chars.split(slt):
                    data['up_char']['6'][char.strip()] = probability.strip()
            elif p.text.find('★★★★★') != -1:
                chars, probability = _get_up_char(r'.*?★★★★★：(.*?)（.*?出率的?(.*?)%.*?）.*?', p.text)
                slt = '/'
                if chars.find('\\') != -1:
                    slt = '\\'
                for char in chars.split(slt):
                    data['up_char']['5'][char.strip()] = probability.strip()
            elif p.text.find('★★★★') != -1:
                chars, probability = _get_up_char(r'.*?★★★★：(.*?)（.*?出率的?(.*?)%.*?）.*?', p.text)
                slt = '/'
                if chars.find('\\') != -1:
                    slt = '\\'
                for char in chars.split(slt):
                    data['up_char']['4'][char.strip()] = probability.strip()
                break
            pr = re.search(r'.*?★：(.*?)（在(.*?)★.*?以(.*?)倍权值.*?）.*?', p.text)
            if pr:
                char = pr.group(1)
                star = pr.group(2)
                weight = pr.group(3)
                char = char.replace('[限定]', '').replace('[', '').replace(']', '')
                data['up_char'][star][char.strip()] = f'权{weight}'
        # data['time'] = '03月09日16:00 - 05月23日03:59'
        if not is_expired(data):
            data['title'] = ''
        else:
            with open(up_char_file, 'w', encoding='utf8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        if not up_char_file.exists():
            with open(up_char_file, 'w', encoding='utf8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            with open(up_char_file, 'r', encoding='utf8') as f:
                old_data = json.load(f)
            if is_expired(old_data):
                return old_data
            else:
                with open(up_char_file, 'w', encoding='utf8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
        return data


# 是否过时
def is_expired(data: dict):
    times = data['time'].split('-')
    for i in range(len(times)):
        times[i] = str(datetime.now().year) + '-' + times[i].split('日')[0].strip().replace('月', '-')
    start_date = datetime.strptime(times[0], '%Y-%m-%d').date()
    end_date = datetime.strptime(times[1], '%Y-%m-%d').date()
    now = datetime.now().date()
    return start_date < now < end_date

# ad = Announcement('https://wiki.biligame.com/arknights/%E6%96%B0%E9%97%BB%E5%85%AC%E5%91%8A')
# asyncio.get_event_loop().run_until_complete(check_up_char('prts'))
