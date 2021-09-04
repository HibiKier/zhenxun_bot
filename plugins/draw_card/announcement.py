import aiohttp
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from .config import DRAW_PATH
from pathlib import Path
from asyncio.exceptions import TimeoutError
from services.log import logger
try:
    import ujson as json
except ModuleNotFoundError:
    import json

headers = {'User-Agent': '"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"'}

prts_up_char = Path(DRAW_PATH + "/draw_card_up/prts_up_char.json")
genshin_up_char = Path(DRAW_PATH + "/draw_card_up/genshin_up_char.json")
pretty_up_char = Path(DRAW_PATH + "/draw_card_up/pretty_up_char.json")
guardian_up_char = Path(DRAW_PATH + "/draw_card_up/guardian_up_char.json")

prts_url = "https://ak.hypergryph.com/news.html"
genshin_url = "https://wiki.biligame.com/ys/%E7%A5%88%E6%84%BF"
pretty_url = "https://wiki.biligame.com/umamusume/%E5%85%AC%E5%91%8A"
guardian_url = "https://wiki.biligame.com/gt/%E9%A6%96%E9%A1%B5"


# 是否过时
def is_expired(data: dict):
    try:
        times = data['time'].split('-')
        for i in range(len(times)):
            times[i] = str(datetime.now().year) + '-' + times[i].split('日')[0].strip().replace('月', '-')
        start_date = datetime.strptime(times[0], '%Y-%m-%d').date()
        end_date = datetime.strptime(times[1], '%Y-%m-%d').date()
        now = datetime.now().date()
    except ValueError:
        return False
    return start_date <= now <= end_date


# 检查写入
def check_write(data: dict, up_char_file):
    if not is_expired(data['char']):
        for x in list(data.keys()):
            data[x]['title'] = ''
    else:
        with open(up_char_file, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    if not up_char_file.exists():
        with open(up_char_file, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    else:
        with open(up_char_file, 'r', encoding='utf8') as f:
            old_data = json.load(f)
        if is_expired(old_data['char']):
            return old_data
        else:
            with open(up_char_file, 'w', encoding='utf8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
    return data


class PrtsAnnouncement:

    def __init__(self):
        self.game_name = '明日方舟'

    async def _get_announcement_text(self):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(prts_url, timeout=7) as res:
                soup = BeautifulSoup(await res.text(), 'lxml')
                ol = soup.find('ol', {'class': 'articleList active', 'data-category-key': 'LATEST'})
                for li in ol:
                    itype = li.find('span', {'class': 'articleItemCate'}).text
                    if itype == '活动':
                        a = li.find('a')['href']
                        async with session.get(f'https://ak.hypergryph.com{a}', headers=headers, timeout=7) as res:
                            return await res.text()

    async def update_up_char(self):
        prts_up_char.parent.mkdir(parents=True, exist_ok=True)
        try:
            data = {'char': {'up_char': {'6': {}, '5': {}, '4': {}}, 'title': '', 'time': '', 'pool_img': ''}}
            text = await self._get_announcement_text()
            soup = BeautifulSoup(text, 'lxml')
            content = soup.find('div', {'class': 'article-content'})
            contents = [x for x in content.contents if x.text or str(x).find('img') != -1]
            start_index = -1
            end_index = -1
            for i in range(len(contents)):
                if str(contents[i]).startswith('<p>'):
                    r = re.search('(.*)(寻访|复刻).*?开启', contents[i].text)
                    if r:
                        if str(contents[i+3].text).find('★') != -1:
                            img = contents[i-1].find('img')
                            if img:
                                data['char']['pool_img'] = img['src']
                            start_index = i
                            for j in range(i, len(contents)):
                                if str(contents[j]).find('注意') != -1:
                                    end_index = j
                                    break
                            break
            contents = contents[start_index: end_index]
            title = contents[0].text
            data['char']['title'] = title[title.find('【'): title.find('】') + 1]
            data['char']['time'] = str(contents[1].text).split('：', maxsplit=1)[1]
            for p in contents[2:]:
                p = str(p.text)
                r = None
                if p.find('★') != -1:
                    if p.find('权值') == -1:
                        r = re.search(r'.*?：(.*)（占(.*)★.*?的(.*)%）', p)
                    else:
                        r = re.search(r'.*?：(.*)（在(.*)★.*?以(.*)倍权值.*?）', p)
                    star = r.group(2)
                if r:
                    chars = r.group(1)
                    if chars.find('/') != -1:
                        chars = chars.strip().split('/')
                    elif chars.find('\\') != -1:
                        chars = chars.strip().split('\\')
                    else:
                        chars = chars.split('\n')
                    chars = [x.replace('[限定]', '').strip() for x in chars]
                    probability = r.group(3)
                    probability = probability if int(probability) > 10 else f'权{probability}'
                    for char in chars:
                        if char.strip():
                            data['char']['up_char'][star][char.strip()] = probability
        except TimeoutError:
            logger.warning(f'更新明日方舟UP池信息超时...')
            if prts_up_char.exists():
                with open(prts_up_char, 'r', encoding='utf8') as f:
                    data = json.load(f)
        except Exception as e:
            logger.error(f'更新明日方舟未知错误 e：{e}')
            if prts_up_char.exists():
                with open(prts_up_char, 'r', encoding='utf8') as f:
                    data = json.load(f)
        return check_write(data, prts_up_char)


class GenshinAnnouncement:

    def __init__(self):
        self.game_name = '原神'

    async def _get_announcement_text(self):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(genshin_url, timeout=7) as res:
                return await res.text()

    async def update_up_char(self):
        genshin_up_char.parent.mkdir(exist_ok=True, parents=True)
        data = {
            'char': {'up_char': {'5': {}, '4': {}}, 'title': '', 'time': '', 'pool_img': ''},
            'arms': {'up_char': {'5': {}, '4': {}}, 'title': '', 'time': '', 'pool_img': ''}
        }
        text = await self._get_announcement_text()
        soup = BeautifulSoup(text, 'lxml')
        try:
            div = soup.find_all('div', {'class': 'row'})[1]
            tables = div.find_all('table', {'class': 'wikitable'})
            for table in tables:
                trs = table.find('tbody').find_all('tr')
                pool_img = trs[0].find('th').find('img')
                if pool_img['title'].find('角色活动') == -1:
                    itype = 'arms'
                else:
                    itype = 'char'
                try:
                    data[itype]['pool_img'] = str(pool_img['srcset']).split(' ')[0]
                except KeyError:
                    data[itype]['pool_img'] = pool_img['src']
                data[itype]['title'] = str(pool_img['title']).split(f'期{"角色" if itype == "char" else "武器"}')[0][:-3]
                data[itype]['time'] = trs[1].find('td').text
                if data[itype]['time'][-1] == '\n':
                    data[itype]['time'] = data[itype]['time'][:-1]
                if '版本更新后' in data[itype]['time']:
                    sp = data[itype]['time'].split('~')
                    end_time = datetime.strptime(sp[1].strip(), "%Y/%m/%d %H:%M:%S")
                    start_time = end_time - timedelta(days=20)
                    data[itype]['time'] = start_time.strftime('%Y/%m/%d') + ' ~ ' + end_time.strftime('%Y/%m/%d')
                tmp = ''
                for tm in data[itype]['time'].split('~'):
                    date_time_sp = tm.split('/')
                    date_time_sp[2] = date_time_sp[2].strip().replace(' ', '日 ')
                    tmp += date_time_sp[1] + '月' + date_time_sp[2] + ' - '
                data[itype]['time'] = tmp[:-2].strip()
                for a in trs[2].find('td').find_all('a'):
                    char_name = a['title']
                    data[itype]['up_char']['5'][char_name] = "50"
                for a in trs[3].find('td').find_all('a'):
                    char_name = a['title']
                    data[itype]['up_char']['4'][char_name] = "50"
        except TimeoutError:
            logger.warning(f'更新原神UP池信息超时...')
            if genshin_up_char.exists():
                with open(genshin_up_char, 'r', encoding='utf8') as f:
                    data = json.load(f)
        except Exception as e:
            logger.error(f'更新原神UP失败，疑似UP池已结束， e：{e}')
            if genshin_up_char.exists():
                with open(genshin_up_char, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    data['char']['title'] = ''
                    data['arms']['title'] = ''
                with open(genshin_up_char, 'w', encoding='utf8') as wf:
                    json.dump(data, wf, ensure_ascii=False, indent=4)
                return data
        return check_write(data, genshin_up_char)


class PrettyAnnouncement:

    def __init__(self):
        self.game_name = '赛马娘'

    async def _get_announcement_text(self):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(pretty_url, timeout=7) as res:
                soup = BeautifulSoup(await res.text(), 'lxml')
                divs = soup.find('div', {'id': 'mw-content-text'}).find('div').find_all('div')
                for div in divs:
                    a = div.find('a')
                    try:
                        title = a['title']
                    except (KeyError, TypeError):
                        continue
                    if title.find('新角色追加') != -1:
                        url = a['href']
                        break
            async with session.get(f'https://wiki.biligame.com/{url}', timeout=7) as res:
                return await res.text(), title[:-2]

    async def update_up_char(self):
        pretty_up_char.parent.mkdir(exist_ok=True, parents=True)
        data = {
            'char': {'up_char': {'3': {}, '2': {}, '1': {}}, 'title': '', 'time': '', 'pool_img': ''},
            'card': {'up_char': {'3': {}, '2': {}, '1': {}}, 'title': '', 'time': '', 'pool_img': ''}
        }
        try:
            text, title = await self._get_announcement_text()
            soup = BeautifulSoup(text, 'lxml')
            context = soup.find('div', {'class': 'toc-sticky'})
            if not context:
                context = soup.find('div', {'class': 'mw-parser-output'})
            data['char']['title'] = title
            data['card']['title'] = title
            r = re.search(r'(\d{1,2}/\d{1,2} \d{1,2}:\d{1,2} ～ \d{1,2}/\d{1,2} \d{1,2}:\d{1,2})', str(context.text))
            if r:
                time = str(r.group(1))
            else:
                logger.error('赛马娘UP无法找到活动日期....取消更新UP池子...')
                return check_write(data, pretty_up_char)
            time = time.replace('～', '-').replace('/', '月').split(' ')
            time = time[0] + '日 ' + time[1] + ' - ' + time[3] + '日 ' + time[4]
            data['char']['time'] = time
            data['card']['time'] = time
            for p in context.find_all('p'):
                if str(p).find('当期UP赛马娘') != -1 and str(p).find('■') != -1:
                    if not data['char']['pool_img']:
                        try:
                            data['char']['pool_img'] = p.find('img')['src']
                        except TypeError:
                            for center in context.find_all('center'):
                                try:
                                    img = center.find('img')
                                    if img and str(img['alt']).find('新马娘') != -1 and str(img['alt']).find('总览') == 1:
                                        data['char']['pool_img'] = img['src']
                                except (TypeError, KeyError):
                                    pass
                    r = re.findall(r'.*?当期UP赛马娘([\s\S]*)＜奖励内容＞.*?', str(p))
                    if r:
                        for x in r:
                            x = str(x).split('\n')
                            for msg in x:
                                if msg.find('★') != -1:
                                    msg = msg.replace('<br/>', '')
                                    char_name = msg[msg.find('['):].strip()
                                    if (star := len(msg[:msg.find('[')].strip())) == 3:
                                        data['char']['up_char']['3'][char_name] = '70'
                                    elif star == 2:
                                        data['char']['up_char']['2'][char_name] = '70'
                                    elif star == 1:
                                        data['char']['up_char']['1'][char_name] = '70'
                if str(p).find('（当期UP对象）') != -1 and str(p).find('赛马娘') == -1 and str(p).find('■') != -1:
                    # data['card']['pool_img'] = p.find('img')['src']
                    if not data['char']['pool_img']:
                        try:
                            data['char']['pool_img'] = p.find('img')['src']
                        except TypeError:
                            for center in context.find_all('center'):
                                try:
                                    img = center.find('img')
                                    if img and str(img['alt']).find('新卡') != -1 and str(img['alt']).find('总览') == 1:
                                        data['card']['pool_img'] = img['src']
                                except (TypeError, KeyError):
                                    pass
                    r = re.search(r'■全?新?支援卡（当期UP对象）([\s\S]*)</p>', str(p))
                    if r:
                        rmsg = r.group(1).strip()
                        rmsg = rmsg.split('<br/>')
                        rmsg = [x for x in rmsg if x]
                        for x in rmsg:
                            x = x.replace('\n', '').replace('・', '')
                            star = x[:x.find('[')].strip()
                            char_name = x[x.find('['):].strip()
                            if star == 'SSR':
                                data['card']['up_char']['3'][char_name] = '70'
                            if star == 'SR':
                                data['card']['up_char']['2'][char_name] = '70'
                            if star == 'R':
                                data['card']['up_char']['1'][char_name] = '70'
            # 日文->中文
            with open(DRAW_PATH + 'pretty_card.json', 'r', encoding='utf8') as f:
                all_data = json.load(f)
            for star in data['card']['up_char'].keys():
                for name in list(data['card']['up_char'][star].keys()):
                    char_name = name.split(']')[1].strip()
                    tp_name = name[name.find('['): name.find(']') + 1].strip().replace('[', '【').replace(']', '】')
                    for x in all_data.keys():
                        if all_data[x]['名称'].find(tp_name) != -1 and all_data[x]['关联角色'] == char_name:
                            data['card']['up_char'][star].pop(name)
                            data['card']['up_char'][star][all_data[x]['中文名']] = '70'
        except TimeoutError:
            logger.warning(f'更新赛马娘UP池信息超时...')
            if pretty_up_char.exists():
                with open(pretty_up_char, 'r', encoding='utf8') as f:
                    data = json.load(f)
        except Exception as e:
            logger.error(f'赛马娘up更新未知错误 {type(e)}：{e}')
            if pretty_up_char.exists():
                with open(pretty_up_char, 'r', encoding='utf8') as f:
                    data = json.load(f)
        return check_write(data, pretty_up_char)


class GuardianAnnouncement:

    def __init__(self):
        self.game_name = '坎公骑冠剑'

    async def _get_announcement_text(self):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(guardian_url, timeout=7) as res:
                return await res.text()

    async def update_up_char(self):
        data = {
            'char': {'up_char': {'3': {}}, 'title': '', 'time': '', 'pool_img': ''},
            'arms': {'up_char': {'5': {}}, 'title': '', 'time': '', 'pool_img': ''}
        }
        try:
            text = await self._get_announcement_text()
            soup = BeautifulSoup(text, 'lxml')
            context = soup.select('div.col-sm-3:nth-child(3) > div:nth-child(2) > div:nth-child(1) '
                                  '> div:nth-child(2) > div:nth-child(3) > font:nth-child(1)')[0]
            title = context.find('p').find('b').text
            tmp = title.split('，')
            time = ''
            for msg in tmp:
                r = re.search(r'[从|至](.*)(开始|结束)', msg)
                if r:
                    time += r.group(1).strip() + ' - '
            time = time[:-3]
            title = time.split(' - ')[0] + 'UP卡池'
            data['char']['title'] = title
            data['arms']['title'] = title
            data['char']['time'] = time
            data['arms']['time'] = time
            start_idx = -1
            end_idx = -1
            index = 0
            divs = context.find_all('div')
            for x in divs:
                if x.text == '角色':
                    start_idx = index
                if x.text == '武器':
                    end_idx = index
                    break
                index += 1
            for x in divs[start_idx + 1: end_idx]:
                name = x.find('p').find_all('a')[-1].text
                data['char']['up_char']['3'][name] = '0'
            for x in divs[end_idx + 1:]:
                name = x.find('p').find_all('a')[-1].text
                data['arms']['up_char']['5'][name] = '0'
        except TimeoutError:
            logger.warning(f'更新坎公骑冠剑UP池信息超时...')
            if guardian_up_char.exists():
                with open(guardian_up_char, 'r', encoding='utf8') as f:
                    data = json.load(f)
        except Exception as e:
            logger.error(f'坎公骑冠剑up更新未知错误 {type(e)}：{e}')
        return check_write(data, guardian_up_char)
