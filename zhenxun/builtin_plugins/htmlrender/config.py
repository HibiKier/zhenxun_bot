from pydantic import BaseModel, Field
from nonebot import get_driver, get_plugin_config


class Config(BaseModel):
    htmlrender_browser: str | None = Field(default="chromium")
    htmlrender_download_host: str | None = Field(default=None)
    htmlrender_proxy_host: str | None = Field(default=None)
    htmlrender_browser_channel: str | None = Field(default=None)
    htmlrender_browser_executable_path: str | None = Field(default=None)
    htmlrender_connect_over_cdp: str | None = Field(default=None)


global_config = get_driver().config
plugin_config = get_plugin_config(Config)
