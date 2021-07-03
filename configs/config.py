from .utils.util import get_config_data
from typing import List, Union
from services.service_config import TL_M_KEY, SYSTEM_PROXY, ALAPI_M_TOKEN
try:
    import ujson as json
except ModuleNotFoundError:
    import json


# 是否使用配置文件
USE_CONFIG_FILE = False


# API KEY（必要）
LOLICON_KEY: str = ""  # lolicon（不需要了，可不填）
RSSHUBAPP: str = "https://rsshub.app/"  # rsshub
ALAPI_TOKEN: str = ""   # ALAPI
# 图灵
TL_KEY: List[str] = []

# 数据库（必要）
# 如果填写了bind就不需要再填写后面的字段了#）
# 示例："bind": "postgresql://user:password@127.0.0.1:5432/database"
bind: str = ''
sql_name: str = 'postgresql'
user: str = ''
password: str = ''
address: str = ''
port: str = ''
database: str = ''


# 公开图库列表
IMAGE_DIR_LIST: List[str] = ["色图", "美图", "萝莉", "壁纸"]

# 对被ban用户发送的消息
BAN_RESULT: str = "才不会给你发消息."


# 插件配置
MAXINFO_REIMU: int = 7      # 上车(reimu)功能查找目的地的最大数
COUNT_PER_DAY_REIMU: int = 5    # 每日上车(reimu)次数限制
MAXINFO_BT: int = 10        # bt功能单次查找最大数
MAXINFO_PRIVATE_ANIME: int = 20     # 私聊搜索动漫返回的最大数量
MAXINFO_GROUP_ANIME: int = 5       # 群搜索动漫返回的最大数量
MAX_FIND_IMG_COUNT: int = 3      # 识图最大返回数
MAX_SETU_R_COUNT: int = 5       # 每日色图r次数限制

# 各种卡池的开关
PRTS_FLAG = True       # 明日方舟
GENSHIN_FLAG = True    # 原神
PRETTY_FLAG = True      # 赛马娘
GUARDIAN_FLAG = True   # 坎公骑冠剑
PCR_FLAG = True        # 公主连结
AZUR_FLAG = True       # 碧蓝航线
FGO_FLAG = True        # 命运-冠位指定（FGO）
ONMYOJI_FLAG = True    # 阴阳师

PCR_TAI = True         # pcr是否开启台服卡池
SEMAPHORE = 5          # 限制碧蓝航线和FGO并发数

ADMIN_DEFAULT_AUTH: int = 5  # 默认群管理员权限

MAX_SIGN_GOLD: int = 200     # 签到好感度加成额外获得的最大金币数

INITIAL_SETU_PROBABILITY: float = 0.7   # 色图概率
FUDU_PROBABILITY: float = 0.7          # 复读概率

INITIAL_OPEN_CASE_COUNT: int = 20    # 初始开箱次数
MUTE_DEFAULT_COUNT: int = 10      # 刷屏禁言默认检测次数
MUTE_DEFAULT_TIME: int = 7       # 刷屏检测默认规定时间

MUTE_DEFAULT_DURATION: int = 10  # 刷屏检测默禁言时长（分钟）

# 注：即在 MALICIOUS_CHECK_TIME 时间内触发相同命令 MALICIOUS_BAN_COUNT 将被 ban MALICIOUS_BAN_TIME 分钟
MALICIOUS_BAN_TIME: int = 30    # 恶意命令触发检测触发后ban的时长（分钟）
MALICIOUS_BAN_COUNT: int = 8     # 恶意命令触发检测最大触发次数
MALICIOUS_CHECK_TIME: int = 5     # 恶意命令触发检测规定时间内（秒）

# LEVEL
DELETE_IMG_LEVEL: int = 7           # 删除图片权限
MOVE_IMG_LEVEL: int = 7             # 移动图片权限
UPLOAD_LEVEL: int = 6               # 上传图片权限
BAN_LEVEL: int = 5                  # BAN权限
OC_LEVEL: int = 2                   # 开关群功能权限
MUTE_LEVEL: int = 5                 # 更改禁言设置权限
MEMBER_ACTIVITY_LEVEL = 5           # 群员活跃检测设置权限

# 需要为哪些群更新最新版gocq吗？（上传最新版gocq）
# 示例：[434995955, 239483248]
UPDATE_GOCQ_GROUP: List[int] = []

# 代理
system_proxy: Union[str, None] = None
buff_proxy: Union[str, None] = None

# 是否存储色图
DOWNLOAD_SETU: bool = True
# 是否自动同意好友添加
AUTO_ADD_FRIEND: bool = True

# 群管理员功能 与 对应权限
admin_plugins_auth = {
    'admin_bot_manage': OC_LEVEL,
    'ban': BAN_LEVEL,
    'delete_img': DELETE_IMG_LEVEL,
    'move_img': MOVE_IMG_LEVEL,
    'upload_img': UPLOAD_LEVEL,
    'admin_help': 1,
    'mute': MUTE_LEVEL,
    'member_activity_handle': MEMBER_ACTIVITY_LEVEL
}


# 模块与对应命令和对应群权限
# 用于生成帮助图片 和 开关功能 以及 群权限
plugins2info_dict = {
    'sign_in': {
        'level': 5,
        'cmd': ['签到']
    },
    'send_img': {
        'level': 5,
        'cmd': ['发送图片', '发图', '萝莉', '美图', '壁纸']
    },
    'send_setu': {
        'level': 9,
        'cmd': ['色图', '涩图', '瑟图', '查色图']
    },
    'white2black': {
        'level': 5,
        'cmd': ['黑白图', '黑白草图']
    },
    'coser': {
        'level': 9,
        'cmd': ['coser', 'cos']
    },
    'quotations': {
        'level': 5,
        'cmd': ['语录']
    },
    'jitang': {
        'level': 5,
        'cmd': ['鸡汤']
    },
    'send_dinggong_voice': {
        'level': 5,
        'cmd': ['骂我', '骂老子', '骂劳资']
    },
    'open_cases': {
        'level': 5,
        'cmd': ['开箱', '我的开箱', '群开箱统计', '我的金色']
    },
    'luxun': {
        'level': 5,
        'cmd': ['鲁迅说', '鲁迅说过']
    },
    'fake_msg': {
        'level': 5,
        'cmd': ['假消息']
    },
    'buy': {
        'level': 5,
        'cmd': ['购买', '购买道具']
    },
    'my_gold': {
        'level': 5,
        'cmd': ['我的金币']
    },
    'my_props': {
        'level': 5,
        'cmd': ['我的道具']
    },
    'shop_handle': {
        'level': 5,
        'cmd': ['商店']
    },
    'update_pic': {
        'level': 5,
        'cmd': ['图片', '操作图片', '修改图片']
    },
    'search_buff_skin_price': {
        'level': 5,
        'cmd': ['查询皮肤']
    },
    'weather': {
        'level': 5,
        'cmd': ['天气', '查询天气', '天气查询']
    },
    'yiqing': {
        'level': 5,
        'cmd': ['疫情', '疫情查询', '查询疫情']
    },
    'what_anime': {
        'level': 5,
        'cmd': ['识番']
    },
    'search_anime': {
        'level': 5,
        'cmd': ['搜番']
    },
    'songpicker2': {
        'level': 5,
        'cmd': ['点歌']
    },
    'epic': {
        'level': 5,
        'cmd': ['epic']
    },
    'pixiv': {
        'level': 9,
        'cmd': ['pixiv', 'p站排行', '搜图']
    },
    'poke': {
        'level': 5,
        'cmd': ['戳一戳', '拍一拍']
    },
    'draw_card': {
        'level': 5,
        'cmd': ['抽卡', '游戏抽卡', '原神抽卡', '方舟抽卡', '坎公骑冠剑抽卡', 'pcr抽卡', 'fgo抽卡', '碧蓝抽卡', '碧蓝航线抽卡', '阴阳师抽卡']
    },
    'ai': {
        'level': 5,
        'cmd': ['ai', 'Ai', 'AI', 'aI']
    },
    'one_friend': {
        'level': 5,
        'cmd': ['我有一个朋友', '我有一个朋友想问问']
    },
    'translate': {
        'level': 5,
        'cmd': ['翻译', '英翻', '翻英', '日翻', '翻日', '韩翻', '翻韩']
    },
    'nonebot_plugin_picsearcher': {
        'level': 5,
        'cmd': ['识图']
    },
    'almanac': {
        'level': 5,
        'cmd': ['原神黄历', '黄历']
    },
    'material_remind': {
        'level': 5,
        'cmd': ['今日素材', '天赋材料']
    },
    'qiu_qiu_translation': {
        'level': 5,
        'cmd': ['丘丘翻译', '丘丘一下', '丘丘语翻译']
    },
    'query_resource_points': {
        'level': 5,
        'cmd': ['原神资源查询', '原神资源列表']
    },
    'russian': {
        'level': 5,
        'cmd': ['俄罗斯轮盘', '俄罗斯转盘', '装弹']
    },
    'gold_redbag': {
        'level': 5,
        'cmd': ['塞红包', '红包', '抢红包']
    },
    'poetry': {
        'level': 5,
        'cmd': ['念诗', '来首诗', '念首诗']
    },
    'comments_163': {
        'level': 5,
        'cmd': ['到点了', '12点了', '网易云热评', '网易云评论']
    },
    'cover': {
        'level': 5,
        'cmd': ['b封面', 'B封面']
    },
    'pid_search': {
        'level': 9,
        'cmd': ['p搜', 'P搜']
    }
}

if TL_M_KEY:
    TL_KEY = TL_M_KEY
if SYSTEM_PROXY:
    system_proxy = SYSTEM_PROXY
if ALAPI_M_TOKEN:
    ALAPI_TOKEN = ALAPI_M_TOKEN

# 配置文件应用
if USE_CONFIG_FILE:
    config = get_config_data()
    if config:
        for key in config.keys():
            if isinstance(config[key], str):
                config[key] = config[key].strip()
            if key.find('proxy') != -1:
                if not config[key]:
                    config[key] = None
            # if not configs[key] and key.find("PATH") == -1:
            #     configs[key] = None
        globals().update(config)





