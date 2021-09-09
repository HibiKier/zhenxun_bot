from pathlib import Path
try:
    import ujson as json
except ModuleNotFoundError:
    import json


def init_config(plugins2info_dict, plugins2cd_dict, plugins2exists_dict, DATA_PATH):
    plugins2info_file = Path(DATA_PATH) / 'configs' / 'plugins2info.json'
    plugins2info_file.parent.mkdir(exist_ok=True, parents=True)

    if plugins2info_file.exists():
        with open(plugins2info_file, 'r', encoding='utf8') as f:
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
    return plugins2info_dict, plugins2cd_dict, plugins2exists_dict


