from nonebot.adapters.onebot.v11.permission import GROUP
from configs.path_config import TEMP_PATH
from utils.image_utils import get_img_hash
import random
from utils.message_builder import image
from nonebot import on_message
from utils.utils import get_message_img, get_message_text
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from configs.config import Config
from utils.http_utils import AsyncHttpx
from services.log import logger


__zx_plugin_name__ = "复读"
__plugin_usage__ = """
usage：
    重复3次相同的消息时会复读
""".strip()
__plugin_des__ = "群友的本质是什么？是复读机哒！"
__plugin_type__ = ("其他",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_task__ = {"fudu": "复读"}
__plugin_configs__ = {
    "FUDU_PROBABILITY": {"value": 0.7, "help": "复读概率", "default_value": 0.7}
}
Config.add_plugin_config(
    "_task",
    "DEFAULT_FUDU",
    True,
    help_="被动 复读 进群默认开关状态",
    default_value=True,
)


class Fudu:
    def __init__(self):
        self.data = {}

    def append(self, key, content):
        self._create(key)
        self.data[key]["data"].append(content)

    def clear(self, key):
        self._create(key)
        self.data[key]["data"] = []
        self.data[key]["is_repeater"] = False

    def size(self, key) -> int:
        self._create(key)
        return len(self.data[key]["data"])

    def check(self, key, content) -> bool:
        self._create(key)
        return self.data[key]["data"][0] == content

    def get(self, key):
        self._create(key)
        return self.data[key]["data"][0]

    def is_repeater(self, key):
        self._create(key)
        return self.data[key]["is_repeater"]

    def set_repeater(self, key):
        self._create(key)
        self.data[key]["is_repeater"] = True

    def _create(self, key):
        if self.data.get(key) is None:
            self.data[key] = {"is_repeater": False, "data": []}


_fudu_list = Fudu()


fudu = on_message(permission=GROUP, priority=9)


@fudu.handle()
async def _(event: GroupMessageEvent):
    if event.is_tome():
        return
    if get_message_text(event.json()):
        if get_message_text(event.json()).find("@可爱的小真寻") != -1:
            await fudu.finish("复制粘贴的虚空艾特？", at_sender=True)
    img = get_message_img(event.json())
    msg = get_message_text(event.json())
    if not img and not msg:
        return
    if img:
        img_hash = await get_fudu_img_hash(img[0], event.group_id)
    else:
        img_hash = ""
    add_msg = msg + "|-|" + img_hash
    if _fudu_list.size(event.group_id) == 0:
        _fudu_list.append(event.group_id, add_msg)
    elif _fudu_list.check(event.group_id, add_msg):
        _fudu_list.append(event.group_id, add_msg)
    else:
        _fudu_list.clear(event.group_id)
        _fudu_list.append(event.group_id, add_msg)
    if _fudu_list.size(event.group_id) > 2:
        if random.random() < Config.get_config(
            "fudu", "FUDU_PROBABILITY"
        ) and not _fudu_list.is_repeater(event.group_id):
            if random.random() < 0.2:
                await fudu.finish("[[_task|fudu]]打断施法！")
            _fudu_list.set_repeater(event.group_id)
            if img and msg:
                rst = msg + image(f"compare_{event.group_id}_img.jpg", "temp")
            elif img:
                rst = image(f"compare_{event.group_id}_img.jpg", "temp")
            elif msg:
                rst = msg
            else:
                rst = ""
            if rst:
                if rst.endswith("打断施法！"):
                    rst = "打断" + rst
                await fudu.send("[[_task|fudu]]" + rst)


async def get_fudu_img_hash(url, group_id):
    try:
        if await AsyncHttpx.download_file(
            url, TEMP_PATH / f"compare_{group_id}_img.jpg"
        ):
            img_hash = get_img_hash(TEMP_PATH / f"compare_{group_id}_img.jpg")
            return str(img_hash)
        else:
            logger.warning(f"复读下载图片失败...")
    except Exception as e:
        logger.warning(f"复读读取图片Hash出错 {type(e)}：{e}")
    return ""
