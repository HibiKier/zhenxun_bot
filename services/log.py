import logging
from datetime import datetime
from configs.path_config import LOG_PATH

# CRITICAL    50
# ERROR      40
# WARNING   30
# INFO        20
# DEBUG      10
# NOTSET     0

# _handler = logging.StreamHandler(sys.stdout)
# _handler.setFormatter(
#     logging.Formatter('[%(asctime)s %(name)s] %(levelname)s: %(message)s')
# )
logger = logging.getLogger('hibiki')
logger.setLevel(level=logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# print(LOG_PATH)
file_handler = logging.FileHandler(LOG_PATH + str((datetime.now()).date()) + '.log', mode='a', encoding='utf-8')
file_handler.setLevel(level=logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
