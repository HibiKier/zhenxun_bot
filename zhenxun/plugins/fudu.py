import random

from nonebot import on_message
from nonebot.adapters import Event
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Image as alcImg
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_saa import Image, MessageFactory, Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import NICKNAME, Config
from zhenxun.configs.path_config import TEMP_PATH
from zhenxun.configs.utils import PluginExtraData, RegisterConfig, Task
from zhenxun.models.task_info import TaskInfo
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.image_utils import get_download_image_hash, get_img_hash
from zhenxun.utils.rules import ensure_group

__plugin_meta__ = PluginMetadata(
    name="复读",
    description="群友的本质是什么？是复读机哒！",
    usage="""
    usage：
        重复3次相同的消息时会复读
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        menu_type="其他",
        plugin_type=PluginType.HIDDEN,
        tasks=[Task(module="fudu", name="复读")],
        configs=[
            RegisterConfig(
                key="FUDU_PROBABILITY",
                value=0.7,
                help="复读概率",
                default_value=0.7,
                type=float,
            ),
            RegisterConfig(
                module="_task",
                key="DEFAULT_FUDU",
                value=True,
                help="被动 复读 进群默认开关状态",
                default_value=True,
                type=bool,
            ),
        ],
    ).dict(),
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


_manage = Fudu()


_matcher = on_message(rule=ensure_group, priority=999)


@_matcher.handle()
async def _(message: UniMsg, event: Event, session: EventSession):
    task = await TaskInfo.get_or_none(module="fudu")
    if task and not task.status:
        return
    if event.is_tome():
        return
    group_id = session.id2 or ""
    plain_text = message.extract_plain_text()
    image_list = []
    for m in message:
        if isinstance(m, alcImg):
            if m.url:
                image_list.append(m.url)
    if not plain_text and not image_list:
        return
    if plain_text and plain_text.startswith(f"@可爱的{NICKNAME}"):
        await Text("复制粘贴的虚空艾特？").send(reply=True)
    if image_list:
        img_hash = await get_download_image_hash(image_list[0], group_id)
    else:
        img_hash = ""
    add_msg = plain_text + "|-|" + img_hash
    if _manage.size(group_id) == 0:
        _manage.append(group_id, add_msg)
    elif _manage.check(group_id, add_msg):
        _manage.append(group_id, add_msg)
    else:
        _manage.clear(group_id)
        _manage.append(group_id, add_msg)
    if _manage.size(group_id) > 2:
        if random.random() < Config.get_config(
            "fudu", "FUDU_PROBABILITY"
        ) and not _manage.is_repeater(group_id):
            if random.random() < 0.2:
                if plain_text.endswith("打断施法！"):
                    await Text("打断" + plain_text).finish()
                else:
                    await Text("打断施法！").finish()
            _manage.set_repeater(group_id)
            rst = None
            if image_list and plain_text:
                rst = MessageFactory(
                    [Text(plain_text), Image(TEMP_PATH / f"compare_{group_id}_img.jpg")]
                )
            elif image_list:
                rst = Image(TEMP_PATH / f"compare_{group_id}_img.jpg")
            elif plain_text:
                rst = Text(plain_text)
            if rst:
                await rst.finish()
