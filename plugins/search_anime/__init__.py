from nonebot import on_command
from .data_source import from_anime_get_info
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from nonebot.typing import T_State
from configs.config import Config
from utils.message_builder import custom_forward_msg
from nonebot.params import CommandArg, ArgStr


__zx_plugin_name__ = "搜番"
__plugin_usage__ = f"""
usage：
    搜索动漫资源
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
__plugin_block_limit__ = {"rst": "搜索还未完成，不要重复触发！"}
__plugin_configs__ = {
    "SEARCH_ANIME_MAX_INFO": {"value": 20, "help": "搜索动漫返回的最大数量", "default_value": 20}
}

search_anime = on_command("搜番", aliases={"搜动漫"}, priority=5, block=True)


@search_anime.handle()
async def _(state: T_State, arg: Message = CommandArg()):
    if arg.extract_plain_text().strip():
        state["anime"] = arg.extract_plain_text().strip()


@search_anime.got("anime", prompt="是不是少了番名？")
async def _(bot: Bot, event: MessageEvent, state: T_State, key_word: str = ArgStr("anime")):
    await search_anime.send(f"开始搜番 {key_word}", at_sender=True)
    anime_report = await from_anime_get_info(
        key_word,
        Config.get_config("search_anime", "SEARCH_ANIME_MAX_INFO"),
    )
    if anime_report:
        if isinstance(event, GroupMessageEvent):
            mes_list = custom_forward_msg(anime_report, bot.self_id)
            await bot.send_group_forward_msg(group_id=event.group_id, messages=mes_list)
        else:
            await search_anime.send("\n\n".join(anime_report))
        logger.info(
            f"USER {event.user_id} GROUP"
            f" {event.group_id if isinstance(event, GroupMessageEvent) else 'private'} 搜索番剧 {key_word} 成功"
        )
    else:
        logger.warning(f"未找到番剧 {key_word}")
        await search_anime.send(f"未找到番剧 {key_word}（也有可能是超时，再尝试一下？）")
