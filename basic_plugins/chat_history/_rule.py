from nonebot.adapters.onebot.v11 import Event, MessageEvent
from configs.config import Config


def rule(event: Event) -> bool:
    return Config.get_config("chat_history", "FLAG") and isinstance(event, MessageEvent)
