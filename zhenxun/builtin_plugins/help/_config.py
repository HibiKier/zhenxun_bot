from zhenxun.configs.config import Config
from zhenxun.configs.path_config import DATA_PATH, IMAGE_PATH

GROUP_HELP_PATH = DATA_PATH / "group_help"
GROUP_HELP_PATH.mkdir(exist_ok=True, parents=True)
for f in GROUP_HELP_PATH.iterdir():
    f.unlink()

SIMPLE_HELP_IMAGE = IMAGE_PATH / "SIMPLE_HELP.png"
if SIMPLE_HELP_IMAGE.exists():
    SIMPLE_HELP_IMAGE.unlink()

SIMPLE_DETAIL_HELP_IMAGE = IMAGE_PATH / "SIMPLE_DETAIL_HELP.png"
if SIMPLE_DETAIL_HELP_IMAGE.exists():
    SIMPLE_DETAIL_HELP_IMAGE.unlink()

base_config = Config.get("help")
