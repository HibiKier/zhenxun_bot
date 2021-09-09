from typing import List, Optional, Tuple
from services.service_config import TL_M_KEY, SYSTEM_M_PROXY, ALAPI_M_TOKEN
from .path_config import DATA_PATH
from pathlib import Path

try:
    import ujson as json
except ModuleNotFoundError:
    import json


# 是否使用配置文件
# 使用配置文件在每次启动时 plugins2info_dict, plugins2cd_dict, plugins2exists_dict 将从本地读取
# 除了 plugins2info_dict 新增内容键值会写入 plugins2info_file
# 其他修改或新增在 configs.config.py中对 plugins2info_dict, plugins2cd_dict, plugins2exists_dict 的配置无效
# 目录：data/configs/
USE_CONFIG_FILE: bool = False

# 回复消息名称
NICKNAME: str = "小真寻"

# API KEY（必要）
RSSHUBAPP: str = "https://rsshub.app"  # rsshub
ALAPI_TOKEN: str = ""  # ALAPI  https://admin.alapi.cn/user/login
HIBIAPI: str = "https://api.obfs.dev"
# 图灵
TL_KEY: List[str] = []

# 数据库（必要）
# 如果填写了bind就不需要再填写后面的字段了#）
# 示例："bind": "postgresql://user:password@127.0.0.1:5432/database"
bind: str = ""  # 数据库连接链接
sql_name: str = "postgresql"
user: str = ""  # 数据用户名
password: str = ""  # 数据库密码
address: str = ""  # 数据库地址
port: str = ""  # 数据库端口
database: str = ""  # 数据库名称

# 代理
SYSTEM_PROXY: Optional[str] = None  # 全局代理
BUFF_PROXY: Optional[str] = None  # Buff代理

# 公开图库列表
IMAGE_DIR_LIST: List[str] = ["美图", "萝莉", "壁纸"]

# 对被ban用户发送的消息
BAN_RESULT: str = "才不会给你发消息."

# PIX图库下载的画质 可能的值：original：原图，master：缩略图（加快发送速度）
PIX_IMAGE_SIZE: str = "master"


# 插件配置
MAXINFO_REIMU: int = 7  # 上车(reimu)功能查找目的地的最大数
COUNT_PER_DAY_REIMU: int = 5  # 每日上车(reimu)次数限制
MAXINFO_BT: int = 10  # bt功能单次查找最大数
MAXINFO_PRIVATE_ANIME: int = 20  # 私聊搜索动漫返回的最大数量
MAXINFO_GROUP_ANIME: int = 5  # 群搜索动漫返回的最大数量
MAX_FIND_IMG_COUNT: int = 3  # 识图最大返回数
# 参1：延迟撤回色图时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)
WITHDRAW_SETU_TIME: Tuple[int, int] = (90, 1)
# 参1：延迟撤回PIX图片时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)
WITHDRAW_PIX_TIME: Tuple[int, int] = (0, 1)

# PIX图库 与 额外图库OmegaPixivIllusts 混合搜索的比例 参1：PIX图库 参2：OmegaPixivIllusts扩展图库（没有此图库请设置为0）
PIX_OMEGA_PIXIV_RATIO: Tuple[int, int] = (2, 8)

# 各种卡池的开关
PRTS_FLAG = True  # 明日方舟
GENSHIN_FLAG = True  # 原神
PRETTY_FLAG = True  # 赛马娘
GUARDIAN_FLAG = True  # 坎公骑冠剑
PCR_FLAG = True  # 公主连结
AZUR_FLAG = True  # 碧蓝航线
FGO_FLAG = True  # 命运-冠位指定（FGO）
ONMYOJI_FLAG = True  # 阴阳师

PCR_TAI = True  # pcr是否开启台服卡池
SEMAPHORE = 5  # 限制碧蓝航线和FGO并发数

ADMIN_DEFAULT_AUTH: int = 5  # 默认群管理员权限

MAX_SIGN_GOLD: int = 200  # 签到好感度加成额外获得的最大金币数
MAX_RUSSIAN_BET_GOLD: int = 1000  # 俄罗斯轮盘最大赌注金额

INITIAL_SETU_PROBABILITY: float = 0.7  # 色图概率
FUDU_PROBABILITY: float = 0.7  # 复读概率

INITIAL_OPEN_CASE_COUNT: int = 20  # 初始开箱次数
MUTE_DEFAULT_COUNT: int = 10  # 刷屏禁言默认检测次数
MUTE_DEFAULT_TIME: int = 7  # 刷屏检测默认规定时间
MUTE_DEFAULT_DURATION: int = 10  # 刷屏检测默禁言时长（分钟）

CHECK_NOTICE_INFO_CD = 300  # 群检测，个人权限检测等各种检测提示信息cd

# 注：即在 MALICIOUS_CHECK_TIME 时间内触发相同命令 MALICIOUS_BAN_COUNT 将被ban MALICIOUS_BAN_TIME 分钟
MALICIOUS_BAN_TIME: int = 30  # 恶意命令触发检测触发后ban的时长（分钟）
MALICIOUS_BAN_COUNT: int = 3  # 恶意命令触发检测最大触发次数
MALICIOUS_CHECK_TIME: int = 5  # 恶意命令触发检测规定时间内（秒）

# LEVEL
DELETE_IMG_LEVEL: int = 7  # 删除图片权限
MOVE_IMG_LEVEL: int = 7  # 移动图片权限
UPLOAD_LEVEL: int = 6  # 上传图片权限
BAN_LEVEL: int = 5  # BAN权限
OC_LEVEL: int = 2  # 开关群功能权限
MUTE_LEVEL: int = 5  # 更改禁言设置权限
MEMBER_ACTIVITY_LEVEL = 5  # 群员活跃检测设置权限
GROUP_BILIBILI_SUB_LEVEL = 5  # 群内bilibili订阅需要的权限

DEFAULT_GROUP_LEVEL = 5  # 默认群等级

# 是否开启HIBIAPI搜图功能（该功能会搜索群友提交的xp）
HIBIAPI_FLAG: bool = True
# HIBIAPI搜图图片的最低收藏
HIBIAPI_BOOKMARKS: int = 5000

# 需要为哪些群更新最新版gocq吗？（上传最新版gocq）
# 示例：[434995955, 239483248]
UPDATE_GOCQ_GROUP: List[int] = []

# 是否存储色图
DOWNLOAD_SETU: bool = True
# 仅仅使用本地色图
ONLY_USE_LOCAL_SETU: bool = False
# 是否自动同意好友添加
AUTO_ADD_FRIEND: bool = True
# 当含有ALAPI_TOKEN时是否检测文本合规，开启检测会减慢回复速度
ALAPI_AI_CHECK: bool = True
# 导入商店自带的三个商品
IMPORT_DEFAULT_SHOP_GOODS: bool = True
# 真寻是否自动更新
AUTO_UPDATE_ZHENXUN: bool = True

# 群管理员功能 与 对应权限
admin_plugins_auth = {
    "custom_welcome_message": OC_LEVEL,
    "group_notification_state": OC_LEVEL,
    "switch_rule": OC_LEVEL,
    "update_group_member_info": OC_LEVEL,
    "ban": BAN_LEVEL,
    "delete_img": DELETE_IMG_LEVEL,
    "move_img": MOVE_IMG_LEVEL,
    "upload_img": UPLOAD_LEVEL,
    "admin_help": 1,
    "mute": MUTE_LEVEL,
    "member_activity_handle": MEMBER_ACTIVITY_LEVEL,
}

# 需要cd的功能（方便管理）[秒]
# 自定义的功能需要cd也可以在此配置
# key：模块名称
# cd：cd 时长（秒）
# status：此限制的开关状态
# check_type：'private'/'group'/'all'，限制私聊/群聊/全部
# limit_type：监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
#                                     示例：'user'：用户N秒内触发1次，'group'：群N秒内触发1次
# rst：回复的话，可以添加[at]，[uname]，[nickname]来对应艾特，用户群名称，昵称系统昵称
# rst 为 "" 或 None 时则不回复
# rst示例："[uname]你冲的太快了，[nickname]先生，请稍后再冲[at]"
# rst回复："老色批你冲的太快了，欧尼酱先生，请稍后再冲@老色批"
#      用户昵称↑     昵称系统的昵称↑          艾特用户↑
plugins2cd_dict = {
    "open_cases": {
        "cd": 5,
        "status": True,
        "check_type": "all",
        "limit_type": "user",
        "rst": "着什么急啊，慢慢来！",
    },
    "send_setu": {
        "cd": 5,
        "status": True,
        "check_type": "all",
        "limit_type": "user",
        "rst": "您冲得太快了，请稍候再冲",
    },
    "sign_in": {
        "cd": 5,
        "status": True,
        "check_type": "group",
        "limit_type": "user",
        "rst": None,
    }
}

# 用户调用阻塞（方便管理）
# 即 当用户调用此功能还未结束时
# 用发送消息阻止用户重复调用此命令直到该命令结束
# 参数同上 plugin2cd_dict
plugins2exists_dict = {
    "send_setu": {
        "status": False,
        "check_type": "all",
        "limit_type": "user",
        "rst": "您有色图正在处理，请稍等.....",
    },
    "pixiv": {
        "status": True,
        "check_type": "all",
        "limit_type": "user",
        "rst": "P站排行榜或搜图正在搜索，请不要重复触发命令...",
    },
    "pix": {
        "status": True,
        "check_type": "all",
        "limit_type": "user",
        "rst": "您有PIX图片正在处理，请稍等...",
    }
}

# 模块与对应命令和对应群权限
# 用于生成帮助图片 和 开关功能
# key：模块名称
# level：需要的群等级
# default_status：加入群时功能的默认开关状态
# cmd：关闭[cmd] 都会触发命令 关闭对应功能，cmd列表第一个词为统计的功能名称
plugins2info_dict = {
    "sign_in": {"level": 5, "default_status": True, "cmd": ["签到"]},
    "send_img": {
        "level": 5,
        "default_status": True,
        "cmd": ["发送图片", "发图", "萝莉", "美图", "壁纸"],
    },
    "send_setu": {"level": 9, "default_status": True, "cmd": ["色图", "涩图", "瑟图", "查色图"]},
    "white2black": {"level": 5, "default_status": True, "cmd": ["黑白图", "黑白草图"]},
    "coser": {"level": 9, "default_status": True, "cmd": ["coser", "cos"]},
    "quotations": {"level": 5, "default_status": True, "cmd": ["语录"]},
    "jitang": {"level": 5, "default_status": True, "cmd": ["鸡汤"]},
    "send_dinggong_voice": {
        "level": 5,
        "default_status": True,
        "cmd": ["骂我", "骂老子", "骂劳资"],
    },
    "open_cases": {
        "level": 5,
        "default_status": True,
        "cmd": ["开箱", "我的开箱", "群开箱统计", "我的金色"],
    },
    "luxun": {"level": 5, "default_status": True, "cmd": ["鲁迅说", "鲁迅说过"]},
    "fake_msg": {"level": 5, "default_status": True, "cmd": ["假消息"]},
    "buy": {"level": 5, "default_status": True, "cmd": ["购买", "购买道具"]},
    "my_gold": {"level": 5, "default_status": True, "cmd": ["我的金币"]},
    "my_props": {"level": 5, "default_status": True, "cmd": ["我的道具"]},
    "shop_handle": {"level": 5, "default_status": True, "cmd": ["商店"]},
    "update_pic": {"level": 5, "default_status": True, "cmd": ["图片", "操作图片", "修改图片"]},
    "search_buff_skin_price": {"level": 5, "default_status": True, "cmd": ["查询皮肤"]},
    "weather": {"level": 5, "default_status": True, "cmd": ["天气", "查询天气", "天气查询"]},
    "yiqing": {"level": 5, "default_status": True, "cmd": ["疫情", "疫情查询", "查询疫情"]},
    "what_anime": {"level": 5, "default_status": True, "cmd": ["识番"]},
    "search_anime": {"level": 5, "default_status": True, "cmd": ["搜番"]},
    "songpicker2": {"level": 5, "default_status": True, "cmd": ["点歌"]},
    "epic": {"level": 5, "default_status": True, "cmd": ["epic"]},
    "pixiv": {"level": 9, "default_status": True, "cmd": ["pixiv", "p站排行", "搜图"]},
    "poke": {"level": 5, "default_status": True, "cmd": ["戳一戳", "拍一拍"]},
    "draw_card": {
        "level": 5,
        "default_status": True,
        "cmd": [
            "抽卡",
            "游戏抽卡",
        ],
    },
    "ai": {"level": 5, "default_status": True, "cmd": ["ai", "Ai", "AI", "aI"]},
    "one_friend": {"level": 5, "default_status": True, "cmd": ["我有一个朋友", "我有一个朋友想问问"]},
    "translate": {
        "level": 5,
        "default_status": True,
        "cmd": ["翻译", "英翻", "翻英", "日翻", "翻日", "韩翻", "翻韩"],
    },
    "nonebot_plugin_picsearcher": {"level": 5, "default_status": True, "cmd": ["识图"]},
    "almanac": {"level": 5, "default_status": True, "cmd": ["原神黄历", "黄历"]},
    "material_remind": {"level": 5, "default_status": True, "cmd": ["今日素材", "天赋材料"]},
    "qiu_qiu_translation": {
        "level": 5,
        "default_status": True,
        "cmd": ["丘丘翻译", "丘丘一下", "丘丘语翻译"],
    },
    "query_resource_points": {
        "level": 5,
        "default_status": True,
        "cmd": ["原神资源查询", "原神资源列表"],
    },
    "russian": {"level": 5, "default_status": True, "cmd": ["俄罗斯轮盘", "俄罗斯转盘", "装弹"]},
    "gold_redbag": {"level": 5, "default_status": True, "cmd": ["塞红包", "红包", "抢红包"]},
    "poetry": {"level": 5, "default_status": True, "cmd": ["念诗", "来首诗", "念首诗"]},
    "comments_163": {
        "level": 5,
        "default_status": True,
        "cmd": ["到点了", "12点了", "网易云热评", "网易云评论"],
    },
    "cover": {"level": 5, "default_status": True, "cmd": ["b封面", "B封面"]},
    "pid_search": {"level": 9, "default_status": True, "cmd": ["p搜", "P搜"]},
    "pix": {
        "level": 5,
        "default_status": True,
        "cmd": ["pix", "PIX", "pIX", "Pix", "PIx"],
    },
    "wbtop": {"level": 5, "default_status": True, "cmd": ["微博热搜", "微博", "wbtop"]},
    "update_info": {"level": 5, "default_status": True, "cmd": ["更新信息", "更新日志"]},
}

if TL_M_KEY:
    TL_KEY = TL_M_KEY
if SYSTEM_M_PROXY:
    SYSTEM_PROXY = SYSTEM_M_PROXY
if ALAPI_M_TOKEN:
    ALAPI_TOKEN = ALAPI_M_TOKEN


HIBIAPI = HIBIAPI[:-1] if HIBIAPI[-1] == "/" else HIBIAPI
RSSHUBAPP = RSSHUBAPP[:-1] if RSSHUBAPP[-1] == "/" else RSSHUBAPP


if USE_CONFIG_FILE:
    # 读取配置文件
    plugins2info_file = Path(DATA_PATH) / 'configs' / 'plugins2info.json'
    plugins2info_file.parent.mkdir(exist_ok=True, parents=True)

    if plugins2info_file.exists():
        with open(plugins2info_file, 'r') as f:
            _data = json.load(f)
            for p in plugins2info_dict:
                if not _data.get(p):
                    _data[p] = plugins2info_dict[p]
        with open(plugins2info_file, 'w') as wf:
            json.dump(_data, wf, ensure_ascii=False, indent=4)
        plugins2info_dict = _data
    else:
        with open(plugins2info_file, 'w', encoding='utf8') as wf:
            json.dump(plugins2info_dict, wf, ensure_ascii=False, indent=4)

    plugins2cd_file = Path(DATA_PATH) / 'configs' / 'plugins2cd.json'
    if plugins2cd_file.exists():
        with open(plugins2cd_file, 'r', encoding='utf8') as f:
            plugins2cd_dict = json.load(f)
    else:
        with open(plugins2cd_file, 'w', encoding='utf8') as wf:
            json.dump(plugins2cd_dict, wf, ensure_ascii=False, indent=4)

    plugins2exists_file = Path(DATA_PATH) / 'configs' / 'plugins2exists.json'
    if plugins2exists_file.exists():
        with open(plugins2exists_file, 'r', encoding='utf8') as f:
            plugins2exists_dict = json.load(f)
    else:
        with open(plugins2exists_file, 'w', encoding='utf8') as wf:
            json.dump(plugins2exists_dict, wf, ensure_ascii=False, indent=4)


# 配置文件应用
# if USE_CONFIG_FILE:
#     config = get_config_data()
#     if config:
#         for key in config.keys():
#             if isinstance(config[key], str):
#                 config[key] = config[key].strip()
#             if key.find("proxy") != -1:
#                 if not config[key]:
#                     config[key] = None
#             # if not configs[key] and key.find("PATH") == -1:
#             #     configs[key] = None
#         globals().update(config)
