from configs.config import Config
from nonebot.internal.rule import Rule


def rule() -> Rule:
    async def _rule() -> bool:
        return Config.get_config("self_message", "STATUS")

    return Rule(_rule)
