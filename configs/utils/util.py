from pathlib import Path
from configs.utils.init_config import init_config
try:
    import ujson as json
except ModuleNotFoundError:
    import json


data: dict = {}


def get_config_data():
    global data
    if not data:
        try:
            base_config = json.load(open(Path() / "config.json", 'r', encoding='utf8'))
            plugins2cmd_config = json.load(open(Path() / 'configs' / 'plugins2cmd_config.json', 'r', encoding='utf8'))
            other_config = json.load(open(Path() / 'configs' / 'other_config.json', 'r', encoding='utf8'))
            for key in base_config.keys():
                data.update(base_config[key])
            for key in plugins2cmd_config.keys():
                data.update(plugins2cmd_config[key])
            for key in other_config.keys():
                data.update(other_config[key])
        except FileNotFoundError:
            # logger.warning('配置文件不存在，生成默认配置....请填写数据库等必要数据后再次启动bot...')
            init_config()
            raise FileNotFoundError('配置文件不存在，生成默认配置....请填写数据库等必要数据后再次启动bot...')
        except ValueError:
            # logger.error('配置文件错误....')
            raise ValueError('配置文件错误....')
    return data



