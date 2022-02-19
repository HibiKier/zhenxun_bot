from nonebot import on_command, on_regex
from .query_resource import get_resource_type_list, query_resource, init, check_resource_exists
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from utils.utils import scheduler
from services.log import logger
from configs.config import NICKNAME
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
import re

try:
    import ujson as json
except ModuleNotFoundError:
    import json

__zx_plugin_name__ = "原神资源查询"
__plugin_usage__ = """
usage：
    不需要打开网页，就能帮你生成资源图片
    指令：
        原神资源查询 [资源名称]
        原神资源列表
        [资源名称]在哪
        哪有[资源名称]
""".strip()
__plugin_superuser_usage__ = """
usage：
    更新原神资源信息
    指令：
        更新原神资源信息
""".strip()
__plugin_des__ = "原神大地图资源速速查看"
__plugin_cmd__ = ["原神资源查询 [资源名称]", "原神资源列表", "[资源名称]在哪/哪有[资源名称]", "更新原神资源信息 [_superuser]"]
__plugin_type__ = ("原神相关",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["原神资源查询", "原神资源列表"],
}
__plugin_block_limit__ = {
    "rst": "您有资源正在查询！"
}

qr = on_command("原神资源查询", aliases={"原神资源查找"}, priority=5, block=True)
qr_lst = on_command("原神资源列表", priority=5, block=True)
rex_qr = on_regex(".*?(在哪|在哪里|哪有|哪里有).*?", priority=5, block=True)
update_info = on_command("更新原神资源信息", permission=SUPERUSER, priority=1, block=True)


@qr.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    resource_name = arg.extract_plain_text().strip()
    if check_resource_exists(resource_name):
        await qr.send("正在生成位置....")
        resource = await query_resource(resource_name)
        await qr.send(Message(resource), at_sender=True)
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 查询原神材料:" + resource_name
        )
    else:
        await qr.send(f"未查找到 {resource_name} 资源，可通过 “原神资源列表” 获取全部资源名称..")


@rex_qr.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if "在哪" in msg:
        rs = re.search("(.*)在哪.*?", msg)
        resource_name = rs.group(1) if rs else ""
    else:
        rs = re.search(".*?(哪有|哪里有)(.*)", msg)
        resource_name = rs.group(2) if rs else ""
    if check_resource_exists(resource_name):
        await qr.send("正在生成位置....")
        resource = await query_resource(resource_name)
        if resource:
            await rex_qr.send(Message(resource), at_sender=True)
            logger.info(
                f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                f" 查询原神材料:" + resource_name
            )


@qr_lst.handle()
async def _(bot: Bot, event: MessageEvent):
    txt = get_resource_type_list()
    txt_list = txt.split("\n")
    if isinstance(event, GroupMessageEvent):
        mes_list = []
        for txt in txt_list:
            data = {
                "type": "node",
                "data": {
                    "name": f"这里是{NICKNAME}酱",
                    "uin": f"{bot.self_id}",
                    "content": txt,
                },
            }
            mes_list.append(data)
        await bot.send_group_forward_msg(group_id=event.group_id, messages=mes_list)
    else:
        rst = ""
        for i in range(len(txt_list)):
            rst += txt_list[i] + "\n"
            if i % 5 == 0:
                if rst:
                    await qr_lst.send(rst)
                rst = ""


@update_info.handle()
async def _():
    await init(True)
    await update_info.send("更新原神资源信息完成...")


@scheduler.scheduled_job(
    "cron",
    hour=5,
    minute=1,
)
async def _():
    try:
        await init()
        logger.info(f"每日更新原神材料信息成功！")
    except Exception as e:
        logger.error(f"每日更新原神材料信息错误：{e}")
