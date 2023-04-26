from typing import List

from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    memes_command_start: List[str] = []
    memes_command_force_whitespace: bool = True
    memes_disabled_list: List[str] = []
    memes_check_resources_on_startup: bool = True
    memes_prompt_params_error: bool = False
    memes_use_sender_when_no_image: bool = False
    memes_use_default_when_no_text: bool = False


memes_config = Config.parse_obj(get_driver().config.dict())
