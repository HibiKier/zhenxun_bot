from typing import Optional
from .group_manager import GroupManager
from pathlib import Path
from .data_source import init
from .data_class import StaticData

# 群管理
group_manager: Optional[GroupManager] = GroupManager(
    Path() / "data" / "manager" / "group_manager.json"
)

withdraw_message_id_manager: Optional[StaticData] = StaticData(None)

init(group_manager)
