#!/usr/bin/python3
from nonebot import on_command ,on_message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent,Message,Event,MessageSegment
from nonebot.params import ArgStr, CommandArg
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from utils.utils import get_message_text
from services.log import logger
from utils.message_builder import image
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from datetime import datetime

__zx_plugin_name__ = "生活小工具合集"
__plugin_usage__ = """
QQ机器人工具集
    --shenghuo2
usage：
    使用注意这个命令有没有空格
    
    #四级考试
        显示最近的四级考试倒计时日期
""".strip()
__plugin_des__ = "工具汇总"
__plugin_cmd__ = ["#四级考试"]
__plugin_version__ = 0.01
__plugin_author__ = "shenghuo2"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["#四级考试"],
}
__plugin_type__ = ('工具',)
__plugin_cd_limit__ = {
    "cd": 2,
    "rst": "冷静点，要坏掉惹！"
}
# 命令注册
ip_query_command = on_command("#IP", priority=5, block=True)
gen_flag_command = on_command("#flag", priority=5, block=True)

def CET4():
    today = datetime.today()
    if today > datetime(today.year, 6, 10):

        future = datetime.strptime(f'{today.year}-12-10 09:00:00','%Y-%m-%d %H:%M:%S')
    else:
        future = datetime.strptime(f'{today.year}-06-10 09:00:00','%Y-%m-%d %H:%M:%S')
    #当前时间
    now=datetime.now()
    #时间差
    delta = future-now
    hour = delta.seconds/60/60
    minute = (delta.seconds -hour*60*60)/60
    seconds=delta.seconds-hour*60*60 - minute*60
    print_now=now.strftime('%Y-%m-%d %H:%M:%S')

    return (f"现在是北京时间: ,{print_now}\n距离英语四级笔试考试还有：{delta.days}天")



# 四级考试时间计算
CET4_command = on_command("#四级考试", priority=5, block=True)

@CET4_command.handle()
async def handle_CET4_command(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["#四级考试"] = args


@CET4_command.got("#四级考试", prompt="输入#四级考试")
async def got_CET4_command(bot: Bot, event: Event, state: T_State):
    msg = CET4()
    await CET4_command.finish(message = msg)

