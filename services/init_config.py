# import nonebot
from pathlib import Path
try:
    import ujson as json
except ModuleNotFoundError:
    import json

# driver: nonebot.Driver = nonebot.get_driver()

base_config = Path() / 'config.json'
plugins_cmd_config = Path() / 'configs' / 'plugins2cmd_config.json'
other_config = Path() / 'configs' / 'other_config.json'


def init_config():
    if not base_config.exists():
        base_config.parent.mkdir(parents=True, exist_ok=True)
        config_dict = {
            'apikey': {
                'LOLICON_KEY': '',
                'TL_KEY': [],
            },
            'sql': {
                'bind': '',
                'sql_name': '',
                'user': '',
                'password': '',
                'address': '',
                'port': '',
                'database': '',
            },
            'path': {
                'IMAGE_PATH': '',
                'VOICE_PATH': '',
                'TXT_PATH': '',
                'LOG_PATH': '',
                'DATA_PATH': '',
                'DRAW_PATH': '',
                'TEMP_PATH': '',
            },
            'proxy': {
                'system_proxy': '',
                'buff_proxy': ''
            },
            'rsshub': {
                'RSSHUBAPP': 'https://docs.rsshub.app/',
            },
            'apikey': {
                'LOLICON_KEY': '',
                'TL_KEY': [],
            },
            'rsshub': {
                'RSSHUBAPP': 'https://docs.rsshub.app/',
            },
            'sql': {
                'bind': '',
                'sql_name': '',
                'user': '',
                'password': '',
                'address': '',
                'port': '',
                'database': '',
            },
            'level': {
                'DELETE_IMG_LEVEL': 7,
                'MOVE_IMG_LEVEL': 7,
                'UPLOAD_LEVEL': 6,
                'BAN_LEVEL': 5,
                'OC_LEVEL': 2,
                'MUTE_LEVEL': 5,
            },
        }
        with open(base_config, 'w', encoding='utf8') as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)
    if not plugins_cmd_config.exists():
        plugins_cmd_config.parent.mkdir(parents=True, exist_ok=True)
        config_dict = {
            'base_config': {
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
        }
        with open(plugins_cmd_config, 'w', encoding='utf8') as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)
    if not other_config.exists():
        other_config.parent.mkdir(parents=True, exist_ok=True)
        config_dict = {
            'base': {
                'IMAGE_DIR_LIST': ["色图", "美图", "萝莉", "壁纸"],
                'BAN_RESULT': "才不会给你发消息.",
            },
            'bool': {
                'AUTO_ADD_FRIEND': True,
                'DOWNLOAD_SETU': True,
            },
            'probability': {
                'INITIAL_SETU_PROBABILITY': 0.7,
                'FUDU_PROBABILITY': 0.7,
            },
            'max_count': {
                'MAXINFO_REIMU': 7,
                'COUNT_PER_DAY_REIMU': 5,
                'MAXINFO_BT': 10,
                'MAXINFO_PRIVATE_ANIME': 20,
                'MAXINFO_GROUP_ANIME': 5,
                'MAX_FIND_IMG_COUNT': 3,
                'MAX_SIGN_GOLD': 200,
            },
            'malicious_ban': {
                'MALICIOUS_BAN_TIME': 30,
                'MALICIOUS_BAN_COUNT': 4,
                'MALICIOUS_CHECK_TIME': 5,
            },
            'open_case': {
                'INITIAL_OPEN_CASE_COUNT': 20,
            },
            'mute': {
                'MUTE_DEFAULT_COUNT': 10,
                'MUTE_DEFAULT_TIME': 7,
                'MUTE_DEFAULT_DURATION': 10,
            },
            'other': {
                'UPDATE_GOCQ_GROUP': [],
                'ADMIN_DEFAULT_AUTH': 5,
            },
            'auth': {
                'admin_plugins_auth': {
                    "admin_bot_manage": 2,
                    "ban": 5,
                    "delete_img": 7,
                    "move_img": 7,
                    "upload_img": 6,
                    "admin_help": 1,
                    "mute": 5
                }
            },
        }
        with open(other_config, 'w', encoding='utf8') as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)



