import time
from hashlib import md5

from zhenxun.configs.config import Config
from zhenxun.utils.http_utils import AsyncHttpx

URL = "http://api.fanyi.baidu.com/api/trans/vip/translate"


language = {
    "自动": "auto",
    "粤语": "yue",
    "韩语": "kor",
    "泰语": "th",
    "葡萄牙语": "pt",
    "希腊语": "el",
    "保加利亚语": "bul",
    "芬兰语": "fin",
    "斯洛文尼亚语": "slo",
    "繁体中文": "cht",
    "中文": "zh",
    "文言文": "wyw",
    "法语": "fra",
    "阿拉伯语": "ara",
    "德语": "de",
    "荷兰语": "nl",
    "爱沙尼亚语": "est",
    "捷克语": "cs",
    "瑞典语": "swe",
    "越南语": "vie",
    "英语": "en",
    "日语": "jp",
    "西班牙语": "spa",
    "俄语": "ru",
    "意大利语": "it",
    "波兰语": "pl",
    "丹麦语": "dan",
    "罗马尼亚语": "rom",
    "匈牙利语": "hu",
}


async def translate_message(word: str, form: str, to: str) -> str:
    """翻译

    参数:
        word (str): 翻译文字
        form (str): 源语言
        to (str): 目标语言

    返回:
        str: 翻译后的文字
    """
    if form in language:
        form = language[form]
    if to in language:
        to = language[to]
    salt = str(time.time())
    app_id = Config.get_config("translate", "APPID")
    secret_key = Config.get_config("translate", "SECRET_KEY")
    sign = app_id + word + salt + secret_key  # type: ignore
    md5_ = md5()
    md5_.update(sign.encode("utf-8"))
    sign = md5_.hexdigest()
    params = {
        "q": word,
        "from": form,
        "to": to,
        "appid": app_id,
        "salt": salt,
        "sign": sign,
    }
    url = URL + "?"
    for key, value in params.items():
        url += f"{key}={value}&"
    url = url[:-1]
    resp = await AsyncHttpx.get(url)
    data = resp.json()
    if data.get("error_code"):
        return data.get("error_msg")
    if trans_result := data.get("trans_result"):
        return trans_result[0]["dst"]
    return "没有找到翻译捏..."
