from typing import List
from nonebot.adapters.onebot.v11 import MessageEvent
from ._config import SearchType


def parse_data(cmd: str, event: MessageEvent, superusers: List[str]):
    search_type = SearchType.TOTAL
    if cmd[:2] == "全局":
        if str(event.user_id) in superusers:
            if cmd[2] == '日':
                search_type = SearchType.DAY
            elif cmd[2] == '周':
                _type = SearchType.WEEK
            elif cmd[2] == '月':
                _type = SearchType.MONTH
        
