from typing import Optional
from .group_manager import GroupManager
from pathlib import Path
from .withdraw_message_manager import WithdrawMessageManager
from .plugins2cd_manager import Plugins2cdManager
from .plugins2block_manager import Plugins2blockManager
from .plugins2settings_manager import Plugins2settingsManager
from .admin_manager import AdminManager
from configs.path_config import DATA_PATH
from nonebot import Driver
import nonebot

driver: Driver = nonebot.get_driver()

# 群功能开关 | 群被动技能 | 群权限  管理
group_manager: Optional[GroupManager] = GroupManager(
    Path(DATA_PATH) / "manager" / "group_manager.json"
)
# 撤回消息管理
withdraw_message_manager: Optional[WithdrawMessageManager] = WithdrawMessageManager()

# 插件基本设置管理
plugins2settings_manager: Optional[Plugins2settingsManager] = Plugins2settingsManager(
    Path(DATA_PATH) / "configs" / "plugins2settings.yaml"
)

# 插件命令 cd 管理
plugins2cd_manager: Optional[Plugins2cdManager] = Plugins2cdManager(
    Path(DATA_PATH) / "configs" / "plugins2cd.yaml"
)

# 插件命令 阻塞 管理
plugins2block_manager: Optional[Plugins2blockManager] = Plugins2blockManager(
    Path(DATA_PATH) / "configs" / "plugins2block.yaml"
)

# 管理员命令管理器
admin_manager = AdminManager()

