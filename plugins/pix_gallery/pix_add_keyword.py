from nonebot import on_command
from utils.utils import is_number
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg, Command
from typing import Tuple
from ._data_source import uid_pid_exists
from ._model.pixiv_keyword_user import PixivKeywordUser
from ._model.pixiv import Pixiv
from nonebot.permission import SUPERUSER

__zx_plugin_name__ = "PIX关键词/UID/PID添加管理 [Superuser]"
__plugin_usage__ = """
usage：
    PIX关键词/UID/PID添加管理操作
    指令：
        添加pix关键词 [Tag]: 添加一个pix搜索收录Tag
        添加pixuid [uid]: 添加一个pix搜索收录uid
        添加pixpid [pid]: 添加一个pix收录pid
""".strip()
__plugin_des__ = "PIX关键词/UID/PID添加管理"
__plugin_cmd__ = ["添加pix关键词 [Tag]", "添加pixuid [uid]", "添加pixpid [pid]"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


add_keyword = on_command("添加pix关键词", aliases={"添加pix关键字"}, priority=1, block=True)

add_black_pid = on_command("添加pix黑名单", permission=SUPERUSER, priority=1, block=True)

# 超级用户可以通过字符 -f 来强制收录不检查是否存在
add_uid_pid = on_command(
    "添加pixuid",
    aliases={
        "添加pixpid",
    },
    priority=1,
    block=True,
)


@add_keyword.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    group_id = -1
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
    if msg:
        if await PixivKeywordUser.add_keyword(
            event.user_id, group_id, msg, bot.config.superusers
        ):
            await add_keyword.send(
                f"已成功添加pixiv搜图关键词：{msg}，请等待管理员通过该关键词！", at_sender=True
            )
            logger.info(
                f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                f" 添加了pixiv搜图关键词:" + msg
            )
        else:
            await add_keyword.finish(f"该关键词 {msg} 已存在...")
    else:
        await add_keyword.finish(f"虚空关键词？.？.？.？")


@add_uid_pid.handle()
async def _(bot: Bot, event: MessageEvent, cmd: Tuple[str, ...] = Command(), arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    exists_flag = True
    if msg.find("-f") != -1 and str(event.user_id) in bot.config.superusers:
        exists_flag = False
        msg = msg.replace("-f", "").strip()
    if msg:
        for msg in msg.split():
            if not is_number(msg):
                await add_uid_pid.finish("UID只能是数字的说...", at_sender=True)
            if cmd[0].lower().endswith("uid"):
                msg = f"uid:{msg}"
            else:
                msg = f"pid:{msg}"
                if await Pixiv.check_exists(int(msg[4:]), "p0"):
                    await add_uid_pid.finish(f"该PID：{msg[4:]}已存在...", at_sender=True)
            if not await uid_pid_exists(msg) and exists_flag:
                await add_uid_pid.finish("画师或作品不存在或搜索正在CD，请稍等...", at_sender=True)
            group_id = -1
            if isinstance(event, GroupMessageEvent):
                group_id = event.group_id
            if await PixivKeywordUser.add_keyword(
                event.user_id, group_id, msg, bot.config.superusers
            ):
                await add_uid_pid.send(
                    f"已成功添加pixiv搜图UID/PID：{msg[4:]}，请等待管理员通过！", at_sender=True
                )
            else:
                await add_uid_pid.finish(f"该UID/PID：{msg[4:]} 已存在...")
    else:
        await add_uid_pid.finish("湮灭吧！虚空的UID！")


@add_black_pid.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    pid = arg.extract_plain_text().strip()
    img_p = ""
    if "p" in pid:
        img_p = pid.split("p")[-1]
        pid = pid.replace("_", "")
        pid = pid[: pid.find("p")]
    if not is_number(pid):
        await add_black_pid.finish("PID必须全部是数字！", at_sender=True)
    if await PixivKeywordUser.add_keyword(
        114514,
        114514,
        f"black:{pid}{f'_p{img_p}' if img_p else ''}",
        bot.config.superusers,
    ):
        await add_black_pid.send(f"已添加PID：{pid} 至黑名单中...")
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 添加了pixiv搜图黑名单 PID:{pid}"
        )
    else:
        await add_black_pid.send(f"PID：{pid} 已添加黑名单中，添加失败...")
