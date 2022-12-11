from typing import Optional, List, Any, Union, Dict
from pydantic import BaseModel


class Item(BaseModel):
    plugin_name: str
    sta: int


class PluginList(BaseModel):
    plugin_type: str
    icon: str
    logo: str
    items: List[Item]
