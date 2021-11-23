import asyncio
import nonebot
import os
from services.log import logger
from .pcr_handle import update_pcr_info, init_pcr_data
from .azur_handle import update_azur_info, init_azur_data
from .prts_handle import update_prts_info, init_prts_data
from .pretty_handle import update_pretty_info, init_pretty_data
from .guardian_handle import update_guardian_info, init_guardian_data
from .genshin_handle import update_genshin_info, init_genshin_data
from .fgo_handle import update_fgo_info, init_fgo_data
from .onmyoji_handle import update_onmyoji_info, init_onmyoji_data
from .config import DRAW_PATH, PRTS_FLAG, PRETTY_FLAG, GUARDIAN_FLAG, PCR_FLAG, AZUR_FLAG, GENSHIN_FLAG, FGO_FLAG, \
    ONMYOJI_FLAG


driver: nonebot.Driver = nonebot.get_driver()


@driver.on_startup
async def async_update_game():
    tasks = []
    init_lst = [init_pcr_data, init_pretty_data, init_azur_data, init_prts_data, init_genshin_data, init_guardian_data,
                init_fgo_data, init_onmyoji_data]
    if PRTS_FLAG and not os.path.exists(DRAW_PATH + 'prts.json'):
        tasks.append(asyncio.ensure_future(update_prts_info()))
        init_lst.remove(init_prts_data)

    if PRETTY_FLAG and (not os.path.exists(DRAW_PATH + 'pretty.json') or
                        not os.path.exists(DRAW_PATH + 'pretty_card.json')):
        tasks.append(asyncio.ensure_future(update_pretty_info()))
        init_lst.remove(init_pretty_data)

    if GUARDIAN_FLAG and not os.path.exists(DRAW_PATH + 'guardian.json'):
        tasks.append(asyncio.ensure_future(update_guardian_info()))

    if PCR_FLAG and not os.path.exists(DRAW_PATH + 'pcr.json'):
        tasks.append(asyncio.ensure_future(update_pcr_info()))
        init_lst.remove(init_pcr_data)

    if GENSHIN_FLAG and (not os.path.exists(DRAW_PATH + 'genshin.json') or
                         not os.path.exists(DRAW_PATH + 'genshin_arms.json')):
        tasks.append(asyncio.ensure_future(update_genshin_info()))
        init_lst.remove(init_genshin_data)

    if AZUR_FLAG and not os.path.exists(DRAW_PATH + 'azur.json'):
        tasks.append(asyncio.ensure_future(update_azur_info()))
        init_lst.remove(init_azur_data)

    if FGO_FLAG and (not os.path.exists(DRAW_PATH + 'fgo.json') or
                     not os.path.exists(DRAW_PATH + 'fgo_card.json')):
        tasks.append(asyncio.ensure_future(update_fgo_info()))
        init_lst.remove(init_fgo_data)

    if ONMYOJI_FLAG and not os.path.exists(DRAW_PATH + 'onmyoji.json'):
        tasks.append(asyncio.ensure_future(update_onmyoji_info()))
        init_lst.remove(init_onmyoji_data)

    try:
        await asyncio.gather(*tasks)
        for func in init_lst:
            await func()
    except asyncio.exceptions.CancelledError:
        logger.info('更新异常：CancelledError，再次更新...')
        await async_update_game()





