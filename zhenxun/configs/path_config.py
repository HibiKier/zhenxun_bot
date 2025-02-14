from pathlib import Path

# 图片路径
IMAGE_PATH = Path() / "resources" / "image"
# 语音路径
RECORD_PATH = Path() / "resources" / "record"
# 文本路径
TEXT_PATH = Path() / "resources" / "text"
# 日志路径
LOG_PATH = Path() / "log"
# 字体路径
FONT_PATH = Path() / "resources" / "font"
# 数据路径
DATA_PATH = Path() / "data"
# 临时数据路径
TEMP_PATH = Path() / "resources" / "temp"
# 网页模板路径
TEMPLATE_PATH = Path() / "resources" / "template"


IMAGE_PATH.mkdir(parents=True, exist_ok=True)
RECORD_PATH.mkdir(parents=True, exist_ok=True)
TEXT_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH.mkdir(parents=True, exist_ok=True)
FONT_PATH.mkdir(parents=True, exist_ok=True)
DATA_PATH.mkdir(parents=True, exist_ok=True)
TEMP_PATH.mkdir(parents=True, exist_ok=True)
