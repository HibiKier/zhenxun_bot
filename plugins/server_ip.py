from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, PrivateMessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from nonebot.rule import to_me

__plugin_name__ = '服务器'
__plugin_usage__ = '用法： 无'


server_ip = on_command("服务器", aliases={'ip'}, rule=to_me(), priority=5, block=True)


@server_ip.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    await server_ip.finish("|* 请不要发给其他人！ *|\n"
                           "\t***********\n"
                           "|* 请不要发给其他人！ *|\n"
                           "csgo ~号键控制台输入 connect ip 进入服务器\n"
                           "然后再公屏输入 !diy 来使用皮肤（英文感叹号，注意）\n"
                           "【说不定可以凑到内战噢，欢迎~{娱乐为主，别骂人球球了}】", at_sender=True)


# @server_ip.handle()
# async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
#     if event.group_id == ***********:
#         await server_ip.finish("嗨呀！当前服务器地址是:"
#                                "\ncsgo:***********")
#     elif event.group_id == ***********:
#         await server_ip.finish("嗨呀！当前服务器地址是:*********** !diy")
#     else:
#         await server_ip.finish("不好意思呀，小真寻不能为你使用此功能，因为服务器IP是真寻的小秘密呀！", at_sender=True)





