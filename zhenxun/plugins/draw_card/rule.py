from nonebot.internal.rule import Rule

from zhenxun.configs.config import Config


def rule(game) -> Rule:
    async def _rule() -> bool:
        return Config.get_config("draw_card", game.config_name, True)

    return Rule(_rule)
