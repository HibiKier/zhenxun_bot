import os
import random

from nonebot import on_notice
from nonebot.adapters.onebot.v11 import PokeNotifyEvent
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.plugin import PluginMetadata

from zhenxun.configs.path_config import IMAGE_PATH, RECORD_PATH
from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.ban_console import BanConsole
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.utils import CountLimiter

__plugin_meta__ = PluginMetadata(
    name="戳一戳",
    description="戳一戳发送语音美图萝莉图不美哉？",
    usage="""
    戳一戳随机掉落语音或美图萝莉图
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        menu_type="其他",
        plugin_type=PluginType.DEPENDANT,
    ).dict(),
)

REPLY_MESSAGE = [
    "lsp你再戳？",
    "连个可爱美少女都要戳的肥宅真恶心啊。",
    "你再戳！",
    "？再戳试试？",
    "别戳了别戳了再戳就坏了555",
    "我爪巴爪巴，球球别再戳了",
    "你戳你🐎呢？！",
    "那...那里...那里不能戳...绝对...",
    "(。´・ω・)ん?",
    "有事恁叫我，别天天一个劲戳戳戳！",
    "欸很烦欸！你戳🔨呢",
    "?",
    "再戳一下试试？",
    "???",
    "正在关闭对您的所有服务...关闭成功",
    "啊呜，太舒服刚刚竟然睡着了。什么事？",
    "正在定位您的真实地址...定位成功。轰炸机已起飞",
]


_clmt = CountLimiter(3)

poke_ = on_notice(priority=5, block=False)


@poke_.handle()
async def _(event: PokeNotifyEvent):
    uid = str(event.user_id) if event.user_id else None
    gid = str(event.group_id) if event.group_id else None
    if event.self_id == event.target_id:
        _clmt.increase(event.user_id)
        if _clmt.check(event.user_id) or random.random() < 0.3:
            rst = ""
            if random.random() < 0.15:
                await BanConsole.ban(uid, gid, 1, 60)
                rst = "气死我了！"
            await poke_.finish(rst + random.choice(REPLY_MESSAGE), at_sender=True)
        rand = random.random()
        path = random.choice(["luoli", "meitu"])
        if rand <= 0.3 and len(os.listdir(IMAGE_PATH / "image_management" / path)) > 0:
            index = random.randint(
                0, len(os.listdir(IMAGE_PATH / "image_management" / path)) - 1
            )
            await MessageUtils.build_message(
                [
                    f"id: {index}",
                    IMAGE_PATH / "image_management" / path / f"{index}.jpg",
                ]
            ).send()
            logger.info(f"USER {event.user_id} 戳了戳我")
        elif 0.3 < rand < 0.6:
            voice = random.choice(os.listdir(RECORD_PATH / "dinggong"))
            result = MessageSegment.record(RECORD_PATH / "dinggong" / voice)
            await poke_.send(result)
            await poke_.send(voice.split("_")[1])
            logger.info(
                f'USER {event.user_id} 戳了戳我 回复: {result} \n {voice.split("_")[1]}',
                "戳一戳",
            )
        else:
            await poke_.send(MessageSegment("poke", {"qq": event.user_id}))
