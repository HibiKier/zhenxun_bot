import requests
import re
# 向网站进行post请求 获取数据
def get_msg(ip):
    session=requests.session()
    url= 'http://dbcha.com/'
    domain = "_minecraft._tcp." + ip
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'
    }
    data1={
        'name': domain,
        'time': 'Srv',
    }
    login=session.post(url=url,headers=headers,data=data1)
    return login.text

# 对数据进行正则表达式提取 获取SRV解析记录
def get_srv(ip):
    srv_list = ""
    srv_search = re.compile(r'<td class="r">target</td><td class="l">(.*?)</td>')
    domain = str(srv_search.findall(str(get_msg(ip))))[2:-2:]
    srv_search = re.compile(r'<td class="r">port</td><td class="l">(.*?)</td>')
    port = str(srv_search.findall(str(get_msg(ip))))[2:-2:]
    if domain != "":
        srv_list = domain + ":" + port
        return srv_list
    else:
        return ip