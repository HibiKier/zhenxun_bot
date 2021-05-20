from .utils.util import get_config_data
try:
    import ujson as json
except ModuleNotFoundError:
    import json


# 是否使用配置文件
USE_CONFIG_FILE = False


# 公开图库列表
IMAGE_DIR_LIST = ["色图", "美图", "萝莉", "壁纸"]

# 对被ban用户发送的消息
BAN_RESULT = "才不会给你发消息."

MAXINFO_REIMU: int = 7      # 上车功能查找目的地的最大数
COUNT_PER_DAY_REIMU: int = 5    # 每日上车次数限制
MAXINFO_BT: int = 10        # bt功能单次查找最大数
MAXINFO_PRIVATE_ANIME: int = 20     # 私聊单词搜索动漫最大数
MAXINFO_GROUP_ANIME: int = 5       # 群单词搜索动漫最大数
MAX_FIND_IMG_COUNT = 3      # 识图最大返回数

ADMIN_DEFAULT_AUTH = 5  # 默认群管理员权限

MAX_SIGN_GOLD = 200     # 好感度加成额外获得的最大金币数

INITIAL_SETU_PROBABILITY = 0.7   # 色图概率
FUDU_PROBABILITY = 0.7          # 复读概率

INITIAL_OPEN_CASE_COUNT = 20    # 初始开箱次数
MUTE_DEFAULT_COUNT = 10      # 刷屏禁言默认检测次数
MUTE_DEFAULT_TIME = 7       # 刷屏检测默认规定时间

MUTE_DEFAULT_DURATION = 10  # 刷屏检测默禁言时长（分钟）

# 注：即在 MALICIOUS_BAN_COUNT 时间内触发相同命令 MALICIOUS_CHECK_TIME 将被ban MALICIOUS_BAN_TIME 分钟
MALICIOUS_BAN_TIME = 30    # 恶意命令触发检测触发后ban的时长（分钟）
MALICIOUS_BAN_COUNT = 4     # 恶意命令触发检测规定时间内（秒）
MALICIOUS_CHECK_TIME = 5     # 恶意命令触发检测最大触发次数

# LEVEL
DELETE_IMG_LEVEL: int = 7
MOVE_IMG_LEVEL: int = 7
UPLOAD_LEVEL: int = 6
BAN_LEVEL: int = 5
OC_LEVEL: int = 2
MUTE_LEVEL: int = 5

# 需要更新gocq吗？
UPDATE_GOCQ_GROUP = []


# 代理
system_proxy = 'http://127.0.0.1:7890'
buff_proxy = ''

# 是否存储色图
DOWNLOAD_SETU = True
# 是否使用本地色图
LOCAL_SETU = True
# 是否自动同意好友添加
AUTO_ADD_FRIEND = True


# API KEY
LOLICON_KEY: str = "336595836015174952daa2"  # lolicon
RSSHUBAPP: str = "https://docs.rsshub.app/"  # rsshub
# 图灵
TL_KEY = ["4474710fabbf4540bfaa569c192bb457", "6f4c0920d2ff4962b5cbd8148aef771b",
          "f5595738894042fb9fad88ecdc4acf41", "c24400595fed48f9a5c5bc3ff03a3267", "efab135b75d84b02a59115f5b571f277"]

# 数据库
bind = 'postgresql://hibiki:KEWang130123@hibiki0v0.cn:5432/hibikibot'
sql_name = ''
user = ''
password = ''
address = ''
port = ''
database = ''


plugins2name_dict = {
    'sign_in': ['签到'],
    'send_img': ['发送图片', '萝莉', '美图', '壁纸'],
    'send_setu': ['色图', '涩图', '瑟图', '查色图'],
    'white2black': ['黑白图', '黑白草图'],
    'coser': ['coser', 'cos'],
    'quotations': ['语录'],
    'jitang': ['鸡汤'],
    'send_dinggong_voice': ['骂我', '骂老子', '骂劳资'],
    'open_cases': ['开箱', '我的开箱', '群开箱统计', '我的金色'],
    'luxun': ['鲁迅说过', '鲁迅说'],
    'fake_msg': ['假消息'],
    'buy': ['购买', '购买道具'],
    'my_gold': ['我的金币'],
    'my_props': ['我的道具'],
    'shop_help': ['商店'],
    'nonebot_plugin_cocdicer': ['骰子娘'],
    'update_pic': ['图片', '操作图片', '修改图片'],
    'search_buff_skin_price': ['查询皮肤'],
    'weather': ['天气', '查询天气', '天气查询'],
    'yiqing': ['疫情', '疫情查询', '查询疫情'],
    'what_anime': ['识番'],
    'search_anime': ['搜番'],
    'songpicker2': ['点歌'],
    'epic': ['epic'],
    'pixiv': ['pixiv', 'p站排行', '搜图'],
    'poke': ['戳一戳'],
    'draw_card': ['游戏抽卡', '原神一井', '原神来一井', '方舟一井', '方舟来一井'],
    'ai': ['ai', 'Ai', 'AI', 'aI'],
    'one_friend': ['我有一个朋友', '我有一个朋友想问问'],
    'translate': ['翻译', '英翻', '翻英', '日翻', '翻日', '韩翻', '翻韩'],
    'nonebot_plugin_picsearcher': ['识图'],
    'almanac': ['原神黄历', '黄历'],
    'material_remind': ['今日素材', '天赋材料'],
    'qiu_qiu_translation': ['丘丘翻译', '丘丘一下', '丘丘语翻译'],
    'query_resource_points': ['原神资源查询', '原神资源列表'],
}


admin_plugins_auth = {
    'admin_bot_manage': OC_LEVEL,
    'ban': BAN_LEVEL,
    'delete_img': DELETE_IMG_LEVEL,
    'move_img': MOVE_IMG_LEVEL,
    'upload_img': UPLOAD_LEVEL,
    'admin_help': 1,
    'mute': MUTE_LEVEL,
}


if USE_CONFIG_FILE:
    config = get_config_data()
    if config:
        for key in config.keys():
            if isinstance(config[key], str):
                config[key] = config[key].strip()
            # if not configs[key] and key.find("PATH") == -1:
            #     configs[key] = None
        globals().update(config)





