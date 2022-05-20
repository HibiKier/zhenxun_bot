from typing import Optional

from pydantic import Extra, BaseModel


class Config(BaseModel, extra=Extra.ignore):
    superusers: set
    debug: Optional[bool] = False
    setu_cd: int = 60
    setu_send_info_message: Optional[bool] = True
    setu_send_custom_message_path: Optional[str] = None
    setu_save: Optional[str] = None
    setu_path: Optional[str] = None
    setu_proxy: Optional[str] = None
    setu_dav_url: Optional[str] = None
    setu_dav_username: Optional[str] = None
    setu_dav_password: Optional[str] = None
    setu_withdraw: Optional[int] = None
    setu_reverse_proxy: str = "i.pixiv.re"
    setu_size: str = "regular"
    setu_api_url: str = "https://api.lolicon.app/setu/v2"
    setu_max: int = 30
