from pathlib import Path

from zhenxun.configs.path_config import TEMP_PATH

DEFAULT_GITHUB_URL = "https://github.com/HibiKier/zhenxun_bot/tree/main"
RELEASE_URL = "https://api.github.com/repos/HibiKier/zhenxun_bot/releases/latest"

VERSION_FILE_STRING = "__version__"
VERSION_FILE = Path() / VERSION_FILE_STRING

PYPROJECT_FILE_STRING = "pyproject.toml"
PYPROJECT_FILE = Path() / PYPROJECT_FILE_STRING
PYPROJECT_LOCK_FILE_STRING = "poetry.lock"
PYPROJECT_LOCK_FILE = Path() / PYPROJECT_LOCK_FILE_STRING
REQ_TXT_FILE_STRING = "requirements.txt"
REQ_TXT_FILE = Path() / REQ_TXT_FILE_STRING

BASE_PATH_STRING = "zhenxun"
BASE_PATH = Path() / BASE_PATH_STRING

TMP_PATH = TEMP_PATH / "auto_update"

BACKUP_PATH = Path() / "backup"

DOWNLOAD_GZ_FILE_STRING = "download_latest_file.tar.gz"
DOWNLOAD_ZIP_FILE_STRING = "download_latest_file.zip"
DOWNLOAD_GZ_FILE = TMP_PATH / DOWNLOAD_GZ_FILE_STRING
DOWNLOAD_ZIP_FILE = TMP_PATH / DOWNLOAD_ZIP_FILE_STRING

REPLACE_FOLDERS = [
    "builtin_plugins",
    "services",
    "utils",
    "models",
    "configs",
]
