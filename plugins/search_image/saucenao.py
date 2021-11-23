from utils.user_agent import get_user_agent
from utils.utils import get_local_proxy





async def get_saucenao_identify_result(url: str) -> Result.DictListResult:
    fetcher = HttpFetcher(timeout=10, flag='search_image_saucenao', headers=HEADERS)

    if not API_KEY:
        logger.opt(colors=True).warning(f'<r>Saucenao API KEY未配置</r>, <y>无法使用Saucenao API进行识图!</y>')
        return Result.DictListResult(error=True, info='Saucenao API KEY未配置', result=[])

    __payload = {'output_type': 2,
                 'api_key': API_KEY,
                 'testmode': 1,
                 'numres': 6,
                 'db': 999,
                 'url': url}
    saucenao_result = await fetcher.get_json(url=API_URL_SAUCENAO, params=__payload)
    if saucenao_result.error:
        logger.warning(f'get_saucenao_identify_result failed, Network error: {saucenao_result.info}')
        return Result.DictListResult(error=True, info=f'Network error: {saucenao_result.info}', result=[])

    __result_json = saucenao_result.result

    if __result_json['header']['status'] != 0:
        logger.error(f"get_saucenao_identify_result failed, DataSource error, "
                     f"status code: {__result_json['header']['status']}")
        return Result.DictListResult(
            error=True, info=f"DataSource error, status code: {__result_json['header']['status']}", result=[])

    __result = []
    for __item in __result_json['results']:
        try:
            if int(float(__item['header']['similarity'])) < 75:
                continue
            else:
                __result.append({'similarity': __item['header']['similarity'],
                                 'thumbnail': __item['header']['thumbnail'],
                                 'index_name': __item['header']['index_name'],
                                 'ext_urls': __item['data']['ext_urls']})
        except Exception as res_err:
            logger.warning(f"get_saucenao_identify_result failed: {repr(res_err)}, can not resolve results")
            continue
    return Result.DictListResult(error=False, info='Success', result=__result)