from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, PrivateMessageEvent
from nonebot.rule import to_me
from util.utils import get_message_text
from models.group_member_info import GroupInfoUser
from models.friend_user import FriendUser
import random
from models.ban_user import BanUser
from services.log import logger

nickname = on_command('nickname',
                      aliases={'以后叫我', '以后请叫我', '称呼我', '以后请称呼我', '以后称呼我', '叫我', '请叫我'},
                      rule=to_me(), priority=5, block=True)

my_nickname = on_command('my_name', aliases={'我叫什么', '我是谁', '我的名字'}, rule=to_me(), priority=5, block=True)


cancel_nickname = on_command('取消昵称', rule=to_me(), priority=5, block=True)


@nickname.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if not msg:
        await nickname.finish('叫你空白？叫你虚空？叫你无名？？', at_sender=True)
    if len(msg) > 10:
        await nickname.finish('昵称可不能超过10个字！', at_sender=True)
    if await GroupInfoUser.set_group_member_nickname(event.user_id, event.group_id, msg):
        if len(msg) < 5:
            if random.random() < 0.5:
                msg = "~".join(msg)
        await nickname.send(random.choice([
            '好啦好啦，我知道啦，{}，以后就这么叫你吧',
            '嗯嗯，小真寻记住你的昵称了哦，{}',
            '好突然，突然要叫你昵称什么的...{}..',
            '小真寻会好好记住的{}的，放心吧',
            '好..好.，那窝以后就叫你{}了.'
        ]).format(msg))
        logger.info(f'USER {event.user_id} GROUP {event.group_id} 设置群昵称 {msg}')
    else:
        await nickname.send('设置昵称失败，请更新群组成员信息！', at_sender=True)
        logger.warning(f'USER {event.user_id} GROUP {event.group_id} 设置群昵称 {msg} 失败')


@nickname.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if not msg:
        await nickname.finish('叫你空白？叫你虚空？叫你无名？？', at_sender=True)
    if len(msg) > 10:
        await nickname.finish('不要超过10个字！', at_sender=True)
    if await FriendUser.set_friend_nickname(event.user_id, msg):
        await nickname.send(random.choice([
            '好啦好啦，我知道啦，{}，以后就这么叫你吧',
            '嗯嗯，小真寻记住你的昵称了哦，{}',
            '好突然，突然要叫你昵称什么的...{}..',
            '小真寻会好好记住的{}的，放心吧',
            '好..好.，那窝以后就叫你{}了.'
        ]).format(msg))
        logger.info(f'USER {event.user_id} 设置昵称 {msg}')
    else:
        await nickname.send('设置昵称失败了，明天再来试一试！或联系管理员更新好友！', at_sender=True)
        logger.warning(f'USER {event.user_id} 设置昵称 {msg} 失败')


@my_nickname.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    try:
        nickname = await GroupInfoUser.get_group_member_nickname(event.user_id, event.group_id)
    except AttributeError:
        nickname = ''
    if nickname:
        await my_nickname.send(random.choice([
            '我肯定记得你啊，你是{}啊',
            '我不会忘记你的，你也不要忘记我！{}',
            '哼哼，真寻记忆力可是很好的，{}',
            '嗯？你是失忆了嘛...{}..',
            '不要小看真寻的记忆力啊！笨蛋{}！QAQ',
            '哎？{}..怎么了吗..突然这样问..'
        ]).format(nickname))
    else:
        try:
            nickname = (await GroupInfoUser.select_member_info(event.user_id, event.group_id)).user_name
        except AttributeError:
            nickname = event.user_id
            await my_nickname.finish(random.choice([
                '对不起，我只记得一串神秘代码..{}\n【群管理快更新群组成员信息！】'
            ]).format(nickname))
        await my_nickname.send(random.choice([
            '没..没有昵称嘛，{}',
            '啊，你是{}啊，我想叫你的昵称！',
            '是{}啊，有什么事吗？',
            '你是{}？'
        ]).format(nickname))


@my_nickname.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    nickname = await FriendUser.get_friend_nickname(event.user_id)
    if nickname:
        await my_nickname.send(random.choice([
            '我肯定记得你啊，你是{}啊',
            '我不会忘记你的，你也不要忘记我！{}',
            '哼哼，真寻记忆力可是很好的，{}',
            '嗯？你是失忆了嘛...{}..',
            '不要小看真寻的记忆力啊！笨蛋{}！QAQ',
            '哎？{}..怎么了吗..突然这样问..'
        ]).format(nickname))
    else:
        nickname = await FriendUser.get_user_name(event.user_id)
        if nickname:
            await my_nickname.send(random.choice([
                '没..没有昵称嘛，{}',
                '啊，你是{}啊，我想叫你的昵称！',
                '是{}啊，有什么事吗？',
                '你是{}？'
            ]).format(nickname))
        else:
            nickname = event.user_id
            await my_nickname.finish(random.choice([
                '对不起，我只记得一串神秘代码..{}\n【火速联系管理员更新好友列表！】'
            ]).format(nickname))


@cancel_nickname.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    nickname = await GroupInfoUser.get_group_member_nickname(event.user_id, event.group_id)
    if nickname:
        await cancel_nickname.send(random.choice([
            '呜..真寻睡一觉就会忘记的..和梦一样..{}',
            '窝知道了..{}..',
            '是真寻哪里做的不好嘛..好吧..晚安{}',
            '呃，{}，下次我绝对绝对绝对不会再忘记你！',
            '可..可恶！{}！太可恶了！呜'
        ]).format(nickname))
        await GroupInfoUser.set_group_member_nickname(event.user_id, event.group_id, '')
        await BanUser.ban(event.user_id, 9, 60)
    else:
        await cancel_nickname.send('你在做梦吗？你没有昵称啊', at_sender=True)


@cancel_nickname.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    nickname = await FriendUser.get_user_name(event.user_id)
    if nickname:
        await cancel_nickname.send(random.choice([
            '呜..真寻睡一觉就会忘记的..和梦一样..{}',
            '窝知道了..{}..',
            '是真寻哪里做的不好嘛..好吧..晚安{}',
            '呃，{}，下次我绝对绝对绝对不会再忘记你！',
            '可..可恶！{}！太可恶了！呜'
        ]).format(nickname))
        await FriendUser.get_user_name(event.user_id)
        await BanUser.ban(event.user_id, 9, 60)
    else:
        await cancel_nickname.send('你在做梦吗？你没有昵称啊', at_sender=True)











