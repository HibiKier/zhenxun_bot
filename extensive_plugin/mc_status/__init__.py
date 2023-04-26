#!/usr/bin/python3
from typing import Type
from cgitb import handler 
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent,Message,Event,MessageSegment
from nonebot.params import ArgStr, CommandArg
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from utils.utils import get_message_text
from services.log import logger
from utils.message_builder import image
from .mc_status import mc_status_get
from .mc_status import mc_player_list_get
from .minecraft_srv import get_srv

__zx_plugin_name__ = "MC服务器状态查询"
__plugin_usage__ = """
usage：
    查询服务器状态
        mc <服务器地址>
    查询服务器玩家列表
        mcplayer <服务器地址>
    查询服务器srv解析
        mcsrv <服务器地址>
""".strip()
__plugin_des__ = "查询mc服务器状态 以图片的形式发出"
__plugin_cmd__ = ["mc "]
__plugin_version__ = 0.11
__plugin_author__ = "shenghuo2"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["mc ","mcplayer","mcsrv",],
}
__plugin_type__ = ('工具',)
__plugin_cd_limit__ = {
    "cd": 1,
    "rst": "冷静点，要坏掉惹！"
}
# 命令注册
mc_server_status_query = on_command("mc ", priority=5, block=True)
mc_player_list = on_command("mcplayer", priority=5, block=True)
mc_srv = on_command("mcsrv", priority=5, block=True)
# 状态查询
@mc_server_status_query.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["ip"] = args


@mc_server_status_query.got("ip", prompt="输入mc ip进行查询")
async def handle_city(bot: Bot, event: Event, state: T_State):
    ip = str(state["ip"])[3::]
    ip = get_srv(ip)
    img_base64 = mc_status_get(ip)
    img = MessageSegment.image(f'base64://{img_base64}')
    try:
        await mc_server_status_query.send(img)
    except Exception as e:
        error = ('错误明细是' + str(e.__class__.__name__) + str(e))
        await mc_server_status_query.finish(message = error)
# 列表查询
@mc_player_list.handle()
async def handle_mc_player_list(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["ip"] = args

@mc_player_list.got("ip", prompt="输入mcplayer ip进行查询")
async def got_mc_player_list(bot: Bot, event: Event, state: T_State):
    ip = str(state["ip"])[9::]
    ip = get_srv(ip)
    player_list = mc_player_list_get(ip)

    await mc_player_list.finish(message = player_list)

# srv查询
@mc_srv.handle()
async def handle_mc_srv(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["ip"] = args

@mc_srv.got("ip", prompt="输入mcsrv ip进行查询")
async def got_mc_srv(bot: Bot, event: Event, state: T_State):
    ip = str(state["ip"])[6::]
    # 对是否进行srv解析进行判断
    if (get_srv(ip) == ip):
        srv = "此IP没有进行srv解析"
    else:
        srv = "srv解析的结果为: " + get_srv(ip)

    await mc_srv.finish(message = srv)