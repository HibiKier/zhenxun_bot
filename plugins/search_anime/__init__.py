from nonebot import on_command
from .data_source import from_anime_get_info
from services.log import logger
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
from configs.config import MAXINFO_GROUP_ANIME, MAXINFO_PRIVATE_ANIME
from utils.utils import get_message_text, get_message_type, UserExistLimiter


__plugin_name__ = '搜番'
__plugin_usage__ = r"""
在群内使用此功能只返还5个结果，私聊返还 20 个结果（绝不能打扰老色批们看色图！）
搜索动漫资源
搜番  [番剧名称或者关键词]
搜番 Aria
""".strip()
_ulmt = UserExistLimiter()

search_anime = on_command('搜番', aliases={'搜动漫'}, priority=5, block=True)


@search_anime.args_parser
async def _(bot: Bot, event: Event, state: T_State):
    msg = get_message_text(event.json())
    if not msg:
        await search_anime.reject('番名番名番名呢？', at_sender=True)
    state['anime'] = msg


@search_anime.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if _ulmt.check(event.user_id):
        await search_anime.finish('您有动漫正在搜索，请稍等...', at_sender=True)
    _ulmt.set_True(event.user_id)
    if get_message_text(event.json()):
        state['anime'] = get_message_text(event.json())


@search_anime.got('anime', prompt='是不是少了番名？')
async def _(bot: Bot, event: Event, state: T_State):
    key_word = state['anime']
    await search_anime.send(f'开始搜番 {key_word}', at_sender=True)
    anime_report = await from_anime_get_info(key_word, MAXINFO_GROUP_ANIME if get_message_type(event.json()) in ['group', 'discuss'] else MAXINFO_PRIVATE_ANIME)
    if anime_report:
        await search_anime.send(anime_report)
        logger.info(f"USER {event.user_id} GROUP"
                    f" {event.group_id if event.message_type != 'private' else 'private'} 搜索番剧 {key_word} 成功")
    else:
        logger.warning(f"未找到番剧 {key_word}")
        await search_anime.send(f"未找到番剧 {key_word}（也有可能是超时，再尝试一下？）")
    _ulmt.set_False(event.user_id)



