from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.typing import T_State
from .config import draw_config


def is_switch(game_name: str) -> Rule:

    async def _is_switch(bot: Bot, event: MessageEvent, state: T_State) -> bool:
        if game_name == 'prts':
            return draw_config.PRTS_FLAG
        if game_name == 'genshin':
            return draw_config.GENSHIN_FLAG
        if game_name == 'pretty':
            return draw_config.PRETTY_FLAG
        if game_name == 'guardian':
            return draw_config.GUARDIAN_FLAG
        if game_name == 'pcr':
            return draw_config.PCR_FLAG
        if game_name == 'azur':
            return draw_config.AZUR_FLAG
        if game_name == 'fgo':
            return draw_config.FGO_FLAG
        if game_name == 'onmyoji':
            return draw_config.ONMYOJI_FLAG
        else:
            return False

    return Rule(_is_switch)
