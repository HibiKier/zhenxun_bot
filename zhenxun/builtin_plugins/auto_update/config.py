from pathlib import Path

from zhenxun.configs.path_config import TEMP_PATH

DEV_URL = "https://ghproxy.cc/https://github.com/HibiKier/zhenxun_bot/archive/refs/heads/dev.zip"
MAIN_URL = "https://ghproxy.cc/https://github.com/HibiKier/zhenxun_bot/archive/refs/heads/main.zip"
RELEASE_URL = "https://api.github.com/repos/HibiKier/zhenxun_bot/releases/latest"


VERSION_FILE = Path() / "__version__"

PYPROJECT_FILE = Path() / "pyproject.toml"
PYPROJECT_LOCK_FILE = Path() / "poetry.lock"

BASE_PATH = Path() / "zhenxun"

TMP_PATH = TEMP_PATH / "auto_update"

BACKUP_PATH = Path() / "backup"

DOWNLOAD_GZ_FILE = TMP_PATH / "download_latest_file.tar.gz"
DOWNLOAD_ZIP_FILE = TMP_PATH / "download_latest_file.zip"

REPLACE_FOLDERS = ["builtin_plugins", "plugins", "services", "utils", "models"]
