import asyncio
import nonebot
from nonebot.log import logger
from .pcr_handle import update_pcr_info, init_pcr_data
from .azur_handle import update_azur_info, init_azur_data
from .prts_handle import update_prts_info, init_prts_data
from .pretty_handle import update_pretty_info, init_pretty_data
from .guardian_handle import update_guardian_info, init_guardian_data
from .genshin_handle import update_genshin_info, init_genshin_data
from .fgo_handle import update_fgo_info, init_fgo_data
from .onmyoji_handle import update_onmyoji_info, init_onmyoji_data
from .config import draw_config, DRAW_DATA_PATH


driver = nonebot.get_driver()


@driver.on_startup
async def async_update_game():
    tasks = []
    init_lst = [init_pcr_data, init_pretty_data, init_azur_data, init_prts_data, init_genshin_data, init_guardian_data,
                init_fgo_data, init_onmyoji_data]
    if draw_config.PRTS_FLAG and not (DRAW_DATA_PATH / 'prts.json').exists():
        tasks.append(asyncio.ensure_future(update_prts_info()))
        init_lst.remove(init_prts_data)

    if draw_config.PRETTY_FLAG and (not (DRAW_DATA_PATH / 'pretty.json').exists() or
                        not (DRAW_DATA_PATH / 'pretty_card.json').exists()):
        tasks.append(asyncio.ensure_future(update_pretty_info()))
        init_lst.remove(init_pretty_data)

    if draw_config.GUARDIAN_FLAG and not (DRAW_DATA_PATH / 'guardian.json').exists():
        tasks.append(asyncio.ensure_future(update_guardian_info()))
        init_lst.remove(init_guardian_data)

    if draw_config.PCR_FLAG and not (DRAW_DATA_PATH / 'pcr.json').exists():
        tasks.append(asyncio.ensure_future(update_pcr_info()))
        init_lst.remove(init_pcr_data)

    if draw_config.GENSHIN_FLAG and (not (DRAW_DATA_PATH / 'genshin.json').exists() or
                         not (DRAW_DATA_PATH / 'genshin_arms.json').exists()):
        tasks.append(asyncio.ensure_future(update_genshin_info()))
        init_lst.remove(init_genshin_data)

    if draw_config.AZUR_FLAG and not (DRAW_DATA_PATH / 'azur.json').exists():
        tasks.append(asyncio.ensure_future(update_azur_info()))
        init_lst.remove(init_azur_data)

    if draw_config.FGO_FLAG and (not (DRAW_DATA_PATH / 'fgo.json').exists() or
                     not (DRAW_DATA_PATH / 'fgo_card.json').exists()):
        tasks.append(asyncio.ensure_future(update_fgo_info()))
        init_lst.remove(init_fgo_data)

    if draw_config.ONMYOJI_FLAG and not (DRAW_DATA_PATH / 'onmyoji.json').exists():
        tasks.append(asyncio.ensure_future(update_onmyoji_info()))
        init_lst.remove(init_onmyoji_data)
    try:
        await asyncio.gather(*tasks)
        for func in init_lst:
            await func()
    except asyncio.exceptions.CancelledError:
        logger.warning('更新异常：CancelledError，再次更新...')
        await async_update_game()
