from nonebot import on_message
from services.log import logger
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.typing import T_State
from util.utils import get_message_json, get_local_proxy
import json
from util.user_agent import get_user_agent
from nonebot.adapters.cqhttp.permission import GROUP
from bilibili_api import video
from util.init_result import image
from models.group_remind import GroupRemind
from nonebot.adapters.cqhttp.exception import ActionFailed
import time
import aiohttp
from bilibili_api import settings
if get_local_proxy():
    settings.proxy = get_local_proxy()


parse_bilibili_json = on_message(priority=1, permission=GROUP, block=False)


@parse_bilibili_json.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if await GroupRemind.get_status(event.group_id, 'blpar') and get_message_json(event.json()):
        data = json.loads(get_message_json(event.json())['data'])
        if data:
            if data.get('desc') == '哔哩哔哩':
                async with aiohttp.ClientSession(headers=get_user_agent()) as session:
                    async with session.get(data['meta']['detail_1']['qqdocurl'], proxy=get_local_proxy(), timeout=7) as response:
                        url = str(response.url).split("?")[0]
                        bvid = url.split('/')[-1]
                        vd_info = await video.Video(bvid=bvid).get_info()
                aid = vd_info['aid']
                title = vd_info['title']
                author = vd_info['owner']['name']
                reply = vd_info['stat']['reply']    # 回复
                favorite = vd_info['stat']['favorite']  # 收藏
                coin = vd_info['stat']['coin']      # 投币
                # like = vd_info['stat']['like']      # 点赞
                # danmu = vd_info['stat']['danmaku']  # 弹幕
                date = time.strftime("%Y-%m-%d", time.localtime(vd_info['ctime']))
                try:
                    await parse_bilibili_json.send(
                        image(vd_info["pic"]) +
                        f'\nav{aid}\n标题：{title}\n'
                        f'UP：{author}\n'
                        f'上传日期：{date}\n'
                        f'回复：{reply}，收藏：{favorite}，投币：{coin}\n'
                        f'{url}'
                    )
                except ActionFailed:
                    logger.warning(f'{event.group_id} 发送bilibili解析失败')
                logger.info(f'USER {event.user_id} GROUP {event.group_id} 解析bilibili转发 {url}')















