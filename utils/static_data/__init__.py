from typing import Optional
from .group_manager import GroupManager
from pathlib import Path
from .data_source import init

# 群权限
group_manager: Optional[GroupManager] = GroupManager(
    Path() / "data" / "manager" / "group_manager.json"
)

init(group_manager)
