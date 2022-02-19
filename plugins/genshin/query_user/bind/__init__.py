from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from utils.utils import is_number
from .._models import Genshin
from services.log import logger
from nonebot.params import CommandArg, Command
from typing import Tuple


__zx_plugin_name__ = "原神绑定"
__plugin_usage__ = """
usage：
    绑定原神uid等数据，cookie极为重要，请谨慎绑定
    ** 如果对拥有者不熟悉，并不建议添加cookie **
    该项目只会对cookie用于”米游社签到“，“原神玩家查询”，“原神便笺查询”
    指令：
        原神绑定uid [uid]
        原神绑定米游社id [mys_id]
        原神绑定cookie [cookie] # 该绑定请私聊
        原神解绑
        示例：原神绑定uid 92342233
    如果不明白怎么获取cookie请输入“原神绑定cookie”。
""".strip()
__plugin_des__ = "绑定自己的原神uid等"
__plugin_cmd__ = ["原神绑定uid [uid]", "原神绑定米游社id [mys_id]", "原神绑定cookie [cookie]", "原神解绑"]
__plugin_type__ = ("原神相关",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["原神绑定"],
}

bind = on_command(
    "原神绑定uid", aliases={"原神绑定米游社id", "原神绑定cookie"}, priority=5, block=True
)

unbind = on_command("原神解绑", priority=5, block=True)


@bind.handle()
async def _(event: MessageEvent, cmd: Tuple[str, ...] = Command(), arg: Message = CommandArg()):
    cmd = cmd[0]
    msg = arg.extract_plain_text().strip()
    if cmd in ["原神绑定uid", "原神绑定米游社id"]:
        if not is_number(msg):
            await bind.finish("uid/id必须为纯数字！", at_senders=True)
        msg = int(msg)
    if cmd == "原神绑定uid":
        uid = await Genshin.get_user_uid(event.user_id)
        if uid:
            await bind.finish(f"您已绑定过uid：{uid}，如果希望更换uid，请先发送原神解绑")
        flag = await Genshin.add_uid(event.user_id, msg)
        if not flag:
            await bind.finish("添加失败，该uid可能已存在...")
        _x = f"已成功添加原神uid：{msg}"
    elif cmd == "原神绑定米游社id":
        uid = await Genshin.get_user_uid(event.user_id)
        if not uid:
            await bind.finish("请先绑定原神uid..")
        await Genshin.set_mys_id(uid, msg)
        _x = f"已成功为uid：{uid} 设置米游社id：{msg}"
    else:
        if not msg:
            await bind.finish(
                "私聊发送！！\n打开 https://bbs.mihoyo.com/ys/\n登录后按F12点击控制台输入document.cookie复制输出的内容即可"
            )
        if isinstance(event, GroupMessageEvent):
            await bind.finish("请立即撤回你的消息并私聊发送！")
        uid = await Genshin.get_user_uid(event.user_id)
        if not uid:
            await bind.finish("请先绑定原神uid..")
        if msg.startswith('"') or msg.startswith("'"):
            msg = msg[1:]
        if msg.endswith('"') or msg.endswith("'"):
            msg = msg[:-1]
        await Genshin.set_cookie(uid, msg)
        _x = f"已成功为uid：{uid} 设置cookie"
    if isinstance(event, GroupMessageEvent):
        await Genshin.set_bind_group(uid, event.group_id)
    await bind.send(_x)
    logger.info(
        f"(USER {event.user_id}, "
        f"GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" {cmd}：{msg}"
    )


@unbind.handle()
async def _(event: MessageEvent):
    if await Genshin.delete_user(event.user_id):
        await unbind.send("用户数据删除成功...")
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f"原神解绑"
        )
    else:
        await unbind.send("该用户数据不存在..")
