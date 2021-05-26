from nonebot.rule import Rule
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State
from .config import GENSHIN_FLAG, PRTS_FLAG, PRETTY_FLAG, GUARDIAN_FLAG, PCR_FLAG


def is_switch(game_name: str) -> Rule:

    async def _is_switch(bot: Bot, event: MessageEvent, state: T_State) -> bool:
        if game_name == 'prts':
            return PRTS_FLAG
        if game_name == 'genshin':
            return GENSHIN_FLAG
        if game_name == 'pretty':
            return PRETTY_FLAG
        if game_name == 'guardian':
            return GUARDIAN_FLAG
        if game_name == 'pcr':
            return PCR_FLAG
        else:
            return False

    return Rule(_is_switch)













