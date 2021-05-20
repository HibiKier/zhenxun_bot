from util.user_agent import get_user_agent
import aiohttp
from lxml import etree
from lxml.etree import Element
from configs.config import MAXINFO_BT
from urllib import parse
from html import unescape
from util.utils import get_local_proxy, is_number
import time
import platform
if platform.system() == 'Windows':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


url = 'https://www.btmet.com/search.php'


async def get_bt_info(keyword: str, args: str, r18: str = '1') -> str:
    cookiesDit = {
        'r18': r18
    }
    s_time = time.time()
    params = get_params(keyword, args)
    async with aiohttp.ClientSession(headers=get_user_agent(), cookies=cookiesDit) as session:
        async with session.get(url, proxy=get_local_proxy(), params=params, timeout=30) as response:
            html = etree.HTML(await response.text())
            print(response.url)
            num = html.xpath('//div[@id="wall"]//span/b/text()')[0]
            print(num)
            if num.find(",") != -1:
                num = num.split(',')[0]
            if num == '0':
                return "没有找到记录"

            div_all = html.xpath('//div[@class="search-item"]')[1:]
            div_all = div_all[:MAXINFO_BT] if len(div_all) > MAXINFO_BT else div_all
            line_list = [await get_item_line(div) for div in div_all]
            clist = []
            for line in line_list:
                if line.strip() != '':
                    clist.append(line)

    return f"搜索 {keyword} 结果（共 {int(int(num.text) / 10) if int(num) % 10 == 0 else int(int(num) / 10) + 1} " \
           f"页）（耗时 {int(time.time() - s_time)} 秒）：\n" + "\n\n".join(clist)


async def get_item_line(div: Element) -> str:
    try:
        magent = div.xpath('./div[2]/a/@href')[0]
        size = div.xpath('./div[@class="f_left"]/div[@class="item-bar"]/span/b/font/text()')[0]
        type = div.xpath('./div[@class="f_left"]/div[@class="item-bar"]/span[@class="cpill blue-pill"]/text()')[0].strip()

        title_doc = div.xpath('.//a[@class="smashTitle"]//text()')[0]
        title_code = title_doc[title_doc.find('("') + 2: title_doc.find('")')]
        title_xml_code = parse.unquote(title_code)
        title_xml = etree.HTML(unescape(title_xml_code))
        title = title_xml.xpath('string(.)')
    except Exception:
        return ''
    return "【{}】| {}\n【{}】| {}".format(type, title, size, magent)


# https://www.btmet.com/search.php?q=%E9%92%A2%E9%93%81%E4%BE%A0&c=5&o=0&l=&p=2
def get_params(keyword: str, args: str) -> dict:
    params = {
        'q': keyword,
        'c': '',
        'l': '',
        'o': 0,
        'p': ''
    }
    if not args:
        return params
    args = args.split(" ")
    for arg in args:
        if '-U' == arg.upper():
            params['o'] = 1
        if '-S' == arg.upper():
            params['o'] = 2
        if '-H' == arg.upper():
            params['o'] = 3
        if '-V' == arg.upper():
            params['c'] = 1
        if '-P' == arg.upper():
            params['c'] = 2
        if '-A' == arg.upper():
            params['c'] = 5
        if is_number(arg):
            params['p'] = arg
    return params


# print(asyncio.get_event_loop().run_until_complete(get_bt_info('钢铁侠', '')))


