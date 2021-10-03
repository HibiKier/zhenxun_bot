from nonebot import on_command
from .data_source import from_anime_get_info
from services.log import logger
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from configs.config import MAXINFO_GROUP_ANIME, MAXINFO_PRIVATE_ANIME
from utils.utils import get_message_text


__zx_plugin_name__ = "搜番"
__plugin_usage__ = f"""
usage：
    搜索动漫资源
    普通的搜番群内使用此功能只返还 {MAXINFO_GROUP_ANIME} 个结果，私聊返还 {MAXINFO_PRIVATE_ANIME} 个结果（绝不能打扰老色批们看色图！）
    指令：
        搜番  [番剧名称或者关键词]
        示例：搜番 刀剑神域
""".strip()
__plugin_des__ = "找不到想看的动漫吗？"
__plugin_cmd__ = ["搜番  [番剧名称或者关键词]"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["搜番"],
}
__plugin_block_limit__ = {
    "rst": "搜索还未完成，不要重复触发！"
}

search_anime = on_command("搜番", aliases={"搜动漫"}, priority=5, block=True)


@search_anime.args_parser
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if not msg:
        await search_anime.reject("番名番名番名呢？", at_sender=True)
    state["anime"] = msg


@search_anime.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if get_message_text(event.json()):
        state["anime"] = get_message_text(event.json())


@search_anime.got("anime", prompt="是不是少了番名？")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    key_word = state["anime"]
    await search_anime.send(f"开始搜番 {key_word}", at_sender=True)
    anime_report = await from_anime_get_info(
        key_word,
        MAXINFO_GROUP_ANIME
        if isinstance(event, GroupMessageEvent)
        else MAXINFO_PRIVATE_ANIME,
    )
    if anime_report:
        await search_anime.send(anime_report)
        logger.info(
            f"USER {event.user_id} GROUP"
            f" {event.group_id if isinstance(event, GroupMessageEvent) else 'private'} 搜索番剧 {key_word} 成功"
        )
    else:
        logger.warning(f"未找到番剧 {key_word}")
        await search_anime.send(f"未找到番剧 {key_word}（也有可能是超时，再尝试一下？）")
