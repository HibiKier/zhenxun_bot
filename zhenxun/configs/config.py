import random
from pathlib import Path

import nonebot
from pydantic import BaseModel

from .utils import ConfigsManager


class BotSetting(BaseModel):

    self_nickname: str = ""
    """回复时NICKNAME"""
    system_proxy: str | None = None
    """系统代理"""
    db_url: str = ""
    """数据库链接"""
    platform_superusers: dict[str, list[str]] = {}
    """平台超级用户"""

    def get_superuser(self, platform: str) -> str:
        """获取超级用户

        参数:
            platform: 对应平台

        返回:
            str | None: 超级用户id
        """
        if self.platform_superusers:
            if platform_superuser := self.platform_superusers.get(platform):
                return random.choice(platform_superuser)
        return ""


Config = ConfigsManager(Path() / "data" / "configs" / "plugins2config.yaml")

BotConfig = nonebot.get_plugin_config(BotSetting)
