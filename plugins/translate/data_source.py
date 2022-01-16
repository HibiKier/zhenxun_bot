from utils.http_utils import AsyncHttpx

url = f"http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"


async def translate_msg(language_type, msg):
    data = {
        "type": parse_language(language_type),
        "i": msg,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true",
    }
    data = (await AsyncHttpx.post(url, data=data)).json()
    if data["errorCode"] == 0:
        return f'原文：{msg}\n翻译{data["translateResult"][0][0]["tgt"]}'
    return "翻译惜败.."


# ZH_CN2EN 中文　»　英语
# ZH_CN2JA 中文　»　日语
# ZH_CN2KR 中文　»　韩语
# ZH_CN2FR 中文　»　法语
# ZH_CN2RU 中文　»　俄语
# ZH_CN2SP 中文　»　西语
# EN2ZH_CN 英语　»　中文
# JA2ZH_CN 日语　»　中文
# KR2ZH_CN 韩语　»　中文
# FR2ZH_CN 法语　»　中文
# RU2ZH_CN 俄语　»　中文
# SP2ZH_CN 西语　»　中文


def parse_language(language_type):
    if language_type == "英翻":
        return "EN2ZH_CN"
    if language_type == "日翻":
        return "JA2ZH_CN"
    if language_type == "韩翻":
        return "KR2ZH_CN"
    # if language_type == '法翻':
    #     return 'FR2ZH_CN'
    # if language_type == '俄翻':
    #     return 'RU2ZH_CN'
    if language_type == "翻英":
        return "ZH_CN2EN"
    if language_type == "翻日":
        return "ZH_CN2JA"
    if language_type == "翻韩":
        return "ZH_CN2KR"
    # if language_type == '翻法':
    #     return 'ZH_CN2FR'
    # if language_type == '翻俄':
    #     return 'ZH_CN2RU'
