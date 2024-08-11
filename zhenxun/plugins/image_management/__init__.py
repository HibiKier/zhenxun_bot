from pathlib import Path
from typing import List, Tuple

import nonebot

from zhenxun.configs.config import Config
from zhenxun.configs.path_config import IMAGE_PATH

Config.add_plugin_config(
    "image_management",
    "IMAGE_DIR_LIST",
    ["美图", "萝莉", "壁纸"],
    help="公开图库列表，可自定义添加 [如果含有send_setu插件，请不要添加色图库]",
    default_value=[],
    type=List[str],
)

Config.add_plugin_config(
    "image_management",
    "WITHDRAW_IMAGE_MESSAGE",
    (0, 1),
    help="自动撤回，参1：延迟撤回发送图库图片的时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
    default_value=(0, 1),
    type=Tuple[int, int],
)

Config.add_plugin_config(
    "image_management:delete_image",
    "DELETE_IMAGE_LEVEL",
    7,
    help="删除图库图片需要的管理员等级",
    default_value=7,
    type=int,
)

Config.add_plugin_config(
    "image_management:move_image",
    "MOVE_IMAGE_LEVEL",
    7,
    help="移动图库图片需要的管理员等级",
    default_value=7,
    type=int,
)

Config.add_plugin_config(
    "image_management:upload_image",
    "UPLOAD_IMAGE_LEVEL",
    6,
    help="上传图库图片需要的管理员等级",
    default_value=6,
    type=int,
)

Config.add_plugin_config(
    "image_management",
    "SHOW_ID",
    True,
    help="是否消息显示图片下标id",
    default_value=True,
    type=bool,
)

Config.set_name("image_management", "图库操作")


(IMAGE_PATH / "image_management").mkdir(parents=True, exist_ok=True)


nonebot.load_plugins(str(Path(__file__).parent.resolve()))
