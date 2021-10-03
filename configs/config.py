from typing import List, Optional, Tuple
from services.service_config import TL_M_KEY, SYSTEM_M_PROXY, ALAPI_M_TOKEN
try:
    import ujson as json
except ModuleNotFoundError:
    import json


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
WITHDRAW_SETU_TIME: Tuple[int, int] = (0, 1)
# 参1：延迟撤回PIX图片时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)
WITHDRAW_PIX_TIME: Tuple[int, int] = (0, 1)

# PIX图库 与 额外图库OmegaPixivIllusts 混合搜索的比例 参1：PIX图库 参2：OmegaPixivIllusts扩展图库（没有此图库请设置为0）
PIX_OMEGA_PIXIV_RATIO: Tuple[int, int] = (10, 0)

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
MALICIOUS_BAN_COUNT: int = 6  # 恶意命令触发检测最大触发次数
MALICIOUS_CHECK_TIME: int = 5  # 恶意命令触发检测规定时间内（秒）

# LEVEL
DELETE_IMG_LEVEL: int = 7  # 删除图片权限
MOVE_IMG_LEVEL: int = 7  # 移动图片权限
UPLOAD_IMG_LEVEL: int = 6  # 上传图片权限
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


if TL_M_KEY:
    TL_KEY = TL_M_KEY
if SYSTEM_M_PROXY:
    SYSTEM_PROXY = SYSTEM_M_PROXY
if ALAPI_M_TOKEN:
    ALAPI_TOKEN = ALAPI_M_TOKEN


HIBIAPI = HIBIAPI[:-1] if HIBIAPI[-1] == "/" else HIBIAPI
RSSHUBAPP = RSSHUBAPP[:-1] if RSSHUBAPP[-1] == "/" else RSSHUBAPP



