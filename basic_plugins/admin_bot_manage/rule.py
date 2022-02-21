from nonebot.adapters.onebot.v11 import Event
from utils.manager import group_manager, plugins2settings_manager
from utils.utils import get_message_text
from services.log import logger

cmd = []


def switch_rule(event: Event) -> bool:
    """
    检测文本是否是关闭功能命令
    :param event: pass
    """
    global cmd
    try:
        if not cmd:
            cmd = ["关闭全部被动", "开启全部被动", "开启全部功能", "关闭全部功能"]
            _data = group_manager.get_task_data()
            for key in _data:
                cmd.append(f"开启{_data[key]}")
                cmd.append(f"关闭{_data[key]}")
                cmd.append(f"开启 {_data[key]}")
                cmd.append(f"关闭 {_data[key]}")
            _data = plugins2settings_manager.get_data()
            for key in _data:
                try:
                    for x in _data[key]["cmd"]:
                        cmd.append(f"开启{x}")
                        cmd.append(f"关闭{x}")
                        cmd.append(f"开启 {x}")
                        cmd.append(f"关闭 {x}")
                except KeyError:
                    pass
        msg = get_message_text(event.json()).split()
        msg = msg[0] if msg else ""
        return msg in cmd
    except Exception as e:
        logger.error(f"检测是否为功能开关命令发生错误 {type(e)}: {e}")
    return False
