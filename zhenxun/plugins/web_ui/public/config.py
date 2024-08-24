from datetime import datetime
from pydantic import BaseModel
from zhenxun.configs.path_config import DATA_PATH, TEMP_PATH


class PublicData(BaseModel):
    etag: str
    update_time: datetime


COMMAND_NAME = "webui_update_assets"

WEBUI_DATA_PATH = DATA_PATH / "web_ui"
PUBLIC_PATH = WEBUI_DATA_PATH / "public"
TMP_PATH = TEMP_PATH / "web_ui"

GITHUB_API_COMMITS = "https://api.github.com/repos/HibiKier/zhenxun_bot_webui/commits"
WEBUI_ASSETS_DOWNLOAD_URL = (
    "https://github.com/HibiKier/zhenxun_bot_webui/archive/refs/heads/dist.zip"
)
