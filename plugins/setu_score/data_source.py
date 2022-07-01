import time
from services.log import logger
from utils.langconv import *
from utils.http_utils import AsyncHttpx
from configs.config import Config

API_KEY = Config.get_config("setu_score", "API_KEY")
SECRET_KEY = Config.get_config("setu_score", "SECRET_KEY")


async def get_setu_score(setu: str) -> "str,int":
    s_time = time.time()

    if not API_KEY:
        return "缺失API_KEY！", 500
    if not SECRET_KEY:
        return "缺失SECRET_KEY！", 500
    params = {"imgUrl": setu}
    try:
        host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}'
        response = await AsyncHttpx.get(host)
        access_token = response.json()["access_token"]
        request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined"
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        resp = await AsyncHttpx.post(request_url, data=params, headers=headers)
        resp_json = resp.json()
        logger.info(resp_json)
        if "error_code" in resp_json:
            err_code = resp_json['error_code']
            err_msg = resp_json['error_msg']
            logger.warning(f"错误代码{err_code},错误原因{err_msg}")
            return f"发生了点错误", 500
        if "data" not in resp_json:
            logger.warning(f"请检查策略组中疑似区间是否拉满")
            return f"请检查策略组中疑似区间是否拉满", 500
        data = resp_json["data"]
        porn_0 = 0
        porn_1 = 0
        porn_2 = 0
        for c in data:
            # 由于百度的图片审核经常给出极低分,所以不合规项置信度*500后为分数
            if c['type'] == 1 and c['subType'] == 0:
                porn_0 = int(c['probability'] * 500)
            elif c['type'] == 1 and c['subType'] == 1:
                porn_1 = int(c['probability'] * 500)
            elif c['type'] == 1 and c['subType'] == 10:
                porn_2 = int(c['probability'] * 500)
        return f"{max(porn_0, porn_1, porn_2)}", 200
    except Exception as e:
        logger.error(f"色图评分发生错误 {type(e)}：{e}")
        return "发生了奇怪的错误，那就没办法了，再试一次？", 500
