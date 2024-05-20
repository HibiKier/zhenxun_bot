from pathlib import Path
from typing import Tuple

import nonebot

from zhenxun.configs.config import Config

Config.add_plugin_config(
    "hibiapi",
    "HIBIAPI",
    "https://api.obfs.dev",
    help="如果没有自建或其他hibiapi请不要修改",
    default_value="https://api.obfs.dev",
)
Config.add_plugin_config("pixiv", "PIXIV_NGINX_URL", "i.pximg.cf", help="Pixiv反向代理")
Config.add_plugin_config(
    "pix",
    "PIX_IMAGE_SIZE",
    "master",
    help="PIX图库下载的画质 可能的值：original：原图，master：缩略图（加快发送速度）",
    default_value="master",
)
Config.add_plugin_config(
    "pix",
    "SEARCH_HIBIAPI_BOOKMARKS",
    5000,
    help="最低收藏，PIX使用HIBIAPI搜索图片时达到最低收藏才会添加至图库",
    default_value=5000,
    type=int,
)
Config.add_plugin_config(
    "pix",
    "WITHDRAW_PIX_MESSAGE",
    (0, 1),
    help="自动撤回，参1：延迟撤回色图时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
    default_value=(0, 1),
    type=Tuple[int, int],
)
Config.add_plugin_config(
    "pix",
    "PIX_OMEGA_PIXIV_RATIO",
    (10, 0),
    help="PIX图库 与 额外图库OmegaPixivIllusts 混合搜索的比例 参1：PIX图库 参2：OmegaPixivIllusts扩展图库（没有此图库请设置为0）",
    default_value=(10, 0),
    type=Tuple[int, int],
)
Config.add_plugin_config(
    "pix", "TIMEOUT", 10, help="下载图片超时限制（秒）", default_value=10, type=int
)

Config.add_plugin_config(
    "pix",
    "SHOW_INFO",
    True,
    help="是否显示图片的基本信息，如PID等",
    default_value=True,
    type=bool,
)

Config.set_name("pix", "PIX图库")

nonebot.load_plugins(str(Path(__file__).parent.resolve()))
