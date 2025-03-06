from pathlib import Path
from typing_extensions import Self

import nonebot
from pydantic import BaseModel, Field
import pytz
from pytz.tzinfo import BaseTzInfo

from zhenxun.utils.compat import model_validator

from .utils import ConfigsManager

__all__ = ["BotConfig", "Config"]


class BotSetting(BaseModel):
    self_nickname: str = ""
    """回复时NICKNAME"""
    system_proxy: str | None = None
    """系统代理"""
    db_url: str = ""
    """数据库链接"""
    platform_superusers: dict[str, list[str]] = Field(default_factory=dict)
    """平台超级用户"""
    qbot_id_data: dict[str, str] = Field(default_factory=dict)
    """官bot id:账号id"""
    time_zone: str = Field(default="Asia/Shanghai", description="时区")

    @model_validator(mode="after")
    def check_timezone(self) -> Self:
        try:
            pytz.timezone(self.time_zone)
        except pytz.UnknownTimeZoneError as e:
            raise ValueError(f"时区 {self.time_zone} 不存在") from e
        return self

    @property
    def timezone(self) -> BaseTzInfo:
        return pytz.timezone(self.time_zone)

    def get_qbot_uid(self, qbot_id: str) -> str | None:
        """获取官bot账号id

        参数:
            qbot_id: 官bot id

        返回:
            str: 账号id
        """
        return self.qbot_id_data.get(qbot_id)

    def get_superuser(self, platform: str) -> list[str]:
        """获取超级用户

        参数:
            platform: 对应平台

        返回:
            list[str]: 超级用户id
        """
        if self.platform_superusers:
            return self.platform_superusers.get(platform, [])
        return []

    def get_sql_type(self) -> str:
        """获取数据库类型

        返回:
            str: 数据库类型, postgres, mysql, sqlite
        """
        return self.db_url.split(":", 1)[0] if self.db_url else ""


Config = ConfigsManager(Path() / "data" / "configs" / "plugins2config.yaml")

BotConfig = nonebot.get_plugin_config(BotSetting)
