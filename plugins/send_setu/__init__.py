import random
from nonebot import on_command, on_regex
from nonebot.permission import SUPERUSER
from services.log import logger
from models.sigin_group_user import SignGroupUser
from util.utils import FreqLimiter, UserExistLimiter, is_number, get_message_text, get_message_imgs
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent, PrivateMessageEvent
from .data_source import get_setu, get_luoxiang, search_online_setu, get_setu_urls, \
    check_r18_and_keyword, find_img_index, delete_img, add_img
from nonebot.adapters.cqhttp.exception import ActionFailed
import re
from models.count_user import UserCount
from aiohttp.client_exceptions import ClientConnectorError
from configs.config import MAX_SETU_R_COUNT

__plugin_name__ = '色图'
__plugin_usage__ = f'''示例：
    1. 色图   （随机本地色图）
    2. 色图r   （随机在线十张r18涩图）
    3. 色图 666 （本地色图id）
    4. 色图 xx （在线搜索xx色图）
    5. 色图r xx   （搜索十张xx的r18涩图，注意空格）（仅私聊，每日限制5次）
    6. 来n张涩图  （本地涩图连发）（1<=n<=9）
    7. 来n张xx的涩图   （在线搜索xx涩图）（较慢，看网速）
注：【色图r每日提供{MAX_SETU_R_COUNT}次
    本地涩图没有r18！
    联网搜索会较慢！
    如果图片数量与数字不符，
    原因1：网络不好，网线被拔QAQ
    原因2：搜索到的总数小于数字
    原因3：图太色或者小错误了】'''

url = "https://api.lolicon.app/setu/"
_flmt = FreqLimiter(5)
_ulmt = UserExistLimiter()
path = "_setu/"


setu = on_command("色图", aliases={"涩图", "不够色", "来一发", "再来点"}, priority=5, block=True)
setu_reg = on_regex('(.*)[份|发|张|个|次|点](.*)[瑟|色|涩]图', priority=5, block=True)
find_setu = on_command("查色图", priority=5, block=True)
delete_setu = on_command('删除色图', aliases={'删除涩图'}, priority=5, block=True, permission=SUPERUSER)
upload_setu = on_command('上传色图', aliases={'上传涩图'}, priority=5, block=True, permission=SUPERUSER)


@setu.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    img_id = get_message_text(event.json())
    if img_id in ['帮助']:
        await setu.finish(__plugin_usage__)
    impression = (await SignGroupUser.ensure(event.user_id, event.group_id)).impression
    luox = get_luoxiang(impression)
    if luox:
        await setu.finish(luox)
    if not _flmt.check(event.user_id):
        await setu.finish('您冲得太快了，请稍候再冲', at_sender=True)
    _flmt.start_cd(event.user_id)
    if _ulmt.check(event.user_id):
        await setu.finish(f"您有色图正在处理，请稍等")
    _ulmt.set_True(event.user_id)
    setu_img, index = get_setu(img_id)
    if setu_img:
        try:
            await setu.send(setu_img)
        except:
            _ulmt.set_False(event.user_id)
            await setu.finish('这张图色过头了，我自己看看就行了！', at_sender=True)
        logger.info(
            f"USER {event.user_id} GROUP {event.group_id} 发送色图 {index}.jpg 成功")
    else:
        msg = img_id
        if list(bot.config.nickname)[0].find(msg) != -1:
            _ulmt.set_False(event.user_id)
            await setu.finish('咳咳咳，虽然我很可爱，但是我木有自己的色图~~~有的话记得发我一份呀')
        keyword, r18, num = await check_r18_and_keyword(msg, event.user_id)
        if r18 == 1:
            _ulmt.set_False(event.user_id)
            await setu.finish(random.choice([
                "这种不好意思的东西怎么可能给这么多人看啦",
                "羞羞脸！给我滚出克私聊！",
                "变态变态变态变态大变态！"
            ]))
        try:
            urls, text_list, code = await get_setu_urls(keyword, num, r18=r18)
        except ClientConnectorError:
            _ulmt.set_False(event.user_id)
            await setu.finish('网络失败了..别担心！正在靠运气上网！', at_sender=True)
        else:
            if code == 200:
                for i in range(num):
                    try:
                        setu_img, index = await search_online_setu(urls[i])
                        await setu.send(text_list[i] + setu_img)
                        logger.info(
                            f"USER {event.user_id} GROUP {event.group_id}"
                            f" 发送在线色图 {keyword}.jpg 成功")
                    except Exception as e:
                        logger.error(f'色图发送错误 e：{e}')
                        await setu.send('图片下载惜败！', at_sender=True)
            else:
                await setu.send(urls)
    _ulmt.set_False(event.user_id)


@setu.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    img_id = get_message_text(event.json())
    if img_id in ['帮助']:
        await setu.finish(__plugin_usage__)
    if not _flmt.check(event.user_id):
        await setu.finish('您冲得太快了，请稍候再冲', at_sender=True)
    _flmt.start_cd(event.user_id)
    if _ulmt.check(event.user_id):
        await setu.finish(f"您有色图正在处理，请稍等")
    _ulmt.set_True(event.user_id)
    setu_img, index = get_setu(img_id)
    if setu_img:
        await setu.send(setu_img)
        logger.info(
            f"USER {event.user_id} GROUP private 发送色图 {index}.jpg 成功")
    else:
        msg = img_id
        if list(bot.config.nickname)[0].find(msg) != -1:
            _ulmt.set_False(event.user_id)
            await setu.finish('咳咳咳，虽然我很可爱，但是我木有自己的色图~~~有的话记得发我一份呀')
        keyword, r18, num = await check_r18_and_keyword(msg, event.user_id)
        if r18 == 1:
            if await UserCount.check_count(event.user_id, 'setu_r18', MAX_SETU_R_COUNT):
                _ulmt.set_False(event.user_id)
                await setu.finish('要节制啊，请明天再来...\n【每日提供5次】', at_sender=True)
            else:
                await UserCount.add_count(event.user_id, 'setu_r18', count=1)
        try:
            urls, text_list, code = await get_setu_urls(keyword, num, r18=r18)
        except ClientConnectorError:
            await UserCount.add_count(event.user_id, 'setu_r18', count=-1)
            await setu.finish('网络失败了..别担心！这次搜索不算数喔', at_sender=True)
        else:
            count = 0
            if code == 200:
                for i in range(num):
                    try:
                        setu_img, index = await search_online_setu(urls[i])
                        await setu.send(text_list[i] + setu_img)
                        logger.info(
                            f"USER {event.user_id} GROUP private"
                            f" 发送{'r18' if img_id == 'r' else ''}色图 {index}.jpg 成功")
                    except Exception as e:
                        logger.error(f'色图发送错误 e：{e}')
                        await setu.send('图片下载惜败！', at_sender=True)
                        count += 1
                    if count > 6:
                        await setu.send('检测到下载惜败的图片过多，这次就不算数了，果咩..', at_sender=True)
                        await UserCount.add_count(event.user_id, 'setu_r18', count=-1)
            else:
                if code == 401:
                    if r18 == 1:
                        await UserCount.add_count(event.user_id, 'setu_r18', count=-1)
                        await setu.send(urls + ' 色图r次数返还！')
                    else:
                        await setu.send(urls, at_sender=True)
                else:
                    if r18 == 1:
                        await setu.send('这次不是小真寻的戳！色图r次数返还！', at_sender=True)
                        await UserCount.add_count(event.user_id, 'setu_r18', count=-1)
                    else:
                        await setu.send(urls, at_sender=True)
    _ulmt.set_False(event.user_id)


num_key = {
    '一': 1,
    '二': 2,
    '两': 2,
    '双': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9
}


@setu_reg.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if event.message_type == "group":
        impression = (await SignGroupUser.ensure(event.user_id, event.group_id)).impression
        luox = get_luoxiang(impression)
        if luox:
            await setu.finish(luox, at_sender=True)
    if _ulmt.check(event.user_id):
        await setu.finish(f"您有色图正在处理，请稍等")
    _ulmt.set_True(event.user_id)
    if not _flmt.check(event.user_id):
        _ulmt.set_False(event.user_id)
        await setu.finish('您冲得太快了，请稍候再冲', at_sender=True)
    _flmt.start_cd(event.user_id)
    msg = get_message_text(event.json())
    num = 1
    msg = re.search(r'(.*)[份|发|张|个|次|点](.*)[瑟|涩|色]图', msg)
    if msg:
        num = msg.group(1)
        keyword = msg.group(2)
        if keyword:
            if keyword[-1] == '的':
                keyword = keyword[:-1]
        if num:
            num = num[-1]
            if num_key.get(num):
                num = num_key[num]
            elif is_number(num):
                try:
                    num = int(num)
                except ValueError:
                    num = 1
            else:
                num = 1
    else:
        return
    # try:
    if not keyword:
        for _ in range(num):
            try:
                img, index = get_setu('')
                if not img:
                    break
                await setu_reg.send(img)
            except Exception as e:
                await setu_reg.send('有图太色了发不出来...')
            else:
                logger.info(
                    f"USER {event.user_id} GROUP {event.group_id if event.message_type != 'private' else 'private'}"
                    f" 发送 {index} 色图成功")
                _ulmt.set_False(event.user_id)
        else:
            _ulmt.set_False(event.user_id)
            return
    if list(bot.config.nickname)[0].find(keyword) != -1:
        await setu.finish('咳咳咳，虽然我很可爱，但是我木有自己的色图~~~有的话记得发我一份呀')
    urls, text_list, code = await get_setu_urls(keyword, num)
    if code == 200:
        for i in range(len(urls)):
            try:
                setu_img, index = await search_online_setu(urls[i])
                await setu_reg.send(text_list[i] + '\n' + setu_img)
            except ActionFailed as e:
                await setu_reg.send('这图太色了，会教坏小孩子的，不给看..')
            else:
                logger.info(
                    f"USER {event.user_id} GROUP {event.group_id if event.message_type != 'private' else 'private'}"
                    f" 发送 {keyword} {num}连 色图成功")
    else:
        _ulmt.set_False(event.user_id)
        await setu_reg.finish(urls, at_sender=True)
    _ulmt.set_False(event.user_id)


@find_setu.args_parser
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if str(event.message) == '取消':
        await find_setu.finish('取消了操作', at_sender=True)
    imgs = get_message_imgs(event.json())
    if not imgs:
        await find_setu.reject("不搞错了，俺要图！")
    state['img'] = imgs[0]


@find_setu.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if get_message_text(event.json()) in ['帮助']:
        await find_setu.finish('通过图片获取本地色图id\n\t示例：查色图(图片)')
    imgs = get_message_imgs(event.json())
    if imgs:
        state['img'] = imgs[0]


@find_setu.got('img', prompt="速速来图！")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    img = state['img']
    await find_setu.send(await find_img_index(img, event.user_id), at_sender=True)


@delete_setu.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    _id = get_message_text(event.json())
    if _id:
        flag, text = delete_img(int(_id))
        if flag:
            await delete_setu.finish(f'删除色图 id：{_id} 成功', at_sender=True)
        else:
            await delete_setu.finish(f'删除色图 id：{_id} 失败，{text}', at_sender=True)


@upload_setu.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    imgs = get_message_imgs(event.json())
    if imgs:
        lens, add_count = await add_img(imgs)
        if add_count == 0:
            await upload_setu.finish('上传的涩图已在色图库中，未成功上传，可以通过 查色图 来查看色图在图库中的id', at_sender=True)
        id_s = ''
        for i in range(add_count, 0, -1):
            id_s += f'{lens - add_count} '
        await upload_setu.finish(f"这次一共为 色图 库 添加了 {add_count} 张图片\n"
                                 f"依次的Id为：{id_s[:-1]}\n"
                                 f"小真寻感谢您对图库的扩充!WW", at_sender=True)
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
            f" 上传色图ID：{id_s[:-1]}")


