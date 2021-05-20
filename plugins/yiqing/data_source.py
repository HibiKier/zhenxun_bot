from datetime import datetime
import aiohttp
from util.user_agent import get_user_agent
import json
import os
from configs.path_config import TXT_PATH
from util.utils import get_local_proxy


url = "https://api.yimian.xyz/coro/"


async def get_yiqing_data(province, city_=''):
    if not os.path.exists(TXT_PATH + "yiqing/"):
        os.mkdir(TXT_PATH + "yiqing/")
    if not os.path.exists(TXT_PATH + "yiqing/" + str(datetime.now().date()) + ".json"):
        async with aiohttp.ClientSession(headers=get_user_agent()) as session:
            async with session.get(url, proxy=get_local_proxy(), timeout=7) as response:
                datalist = await response.json()
        with open(TXT_PATH + "yiqing/" + str(datetime.now().date()) + ".json", 'w') as f:
            json.dump(datalist, f)
    datalist = json.load(open(TXT_PATH + "yiqing/" + str(datetime.now().date()) + ".json", 'r'))
    result = ''
    for data in datalist:
        if data['provinceShortName'] == province:
            if city_ == '':
                result = province + "疫情数据:\n现存确诊: " + \
                         str(data['currentConfirmedCount']) + "\n累计确诊: " + \
                         str(data['confirmedCount']) + "\n治愈: " + \
                         str(data['curedCount']) + "\n死亡: " + \
                         str(data['deadCount'])
                break
            else:
                for city in data['cities']:
                    if city['cityName'] == city_:
                        result = city_ + "疫情数据:\n现存确诊: " + \
                                 str(city['currentConfirmedCount']) + "\n累计确诊: " + str(city['confirmedCount']) +\
                                 "\n治愈: " + str(city['curedCount']) + "\n死亡: " + str(city['deadCount'])
                        break
    return result


def clear_data():
    for file in os.listdir(TXT_PATH + "yiqing/"):
        os.remove(TXT_PATH + "yiqing/" + file)


if __name__ == '__main__':
    print(get_yiqing_data("浙江", city_=''))

