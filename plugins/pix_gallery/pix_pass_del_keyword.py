from nonebot import on_command
from utils.utils import is_number
from utils.message_builder import at
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg, Command
from nonebot.permission import SUPERUSER
from ._data_source import remove_image
from ._model.pixiv_keyword_user import PixivKeywordUser
from ._model.pixiv import Pixiv
from typing import Tuple


__zx_plugin_name__ = "PIX关键词/UID/PID删除管理 [Superuser]"
__plugin_usage__ = """
usage：
    PIX关键词/UID/PID删除管理操作
    指令：
        通过pix关键词 [关键词/pid/uid]
        取消pix关键词 [关键词/pid/uid]
        删除pix关键词 [关键词/pid/uid]
        删除pix图片 *[pid]
        示例：通过pix关键词萝莉
        示例：通过pix关键词uid:123456
        示例：通过pix关键词pid:123456
        示例：删除pix图片4223442
""".strip()
__plugin_des__ = "PIX关键词/UID/PID删除管理"
__plugin_cmd__ = [
    "通过pix关键词 [关键词/pid/uid]",
    "取消pix关键词 [关键词/pid/uid]",
    "删除pix关键词 [关键词/pid/uid]",
    "删除pix图片 *[pid]",
]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


pass_keyword = on_command(
    "通过pix关键词",
    aliases={"通过pix关键字", "取消pix关键词", "取消pix关键字"},
    permission=SUPERUSER,
    priority=1,
    block=True,
)

del_keyword = on_command(
    "删除pix关键词", aliases={"删除pix关键字"}, permission=SUPERUSER, priority=1, block=True
)

del_pic = on_command("删除pix图片", permission=SUPERUSER, priority=1, block=True)


@del_keyword.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if not msg:
        await del_keyword.finish("好好输入要删除什么关键字啊笨蛋！")
    if is_number(msg):
        msg = f"uid:{msg}"
    if msg.lower().startswith("pid"):
        msg = "pid:" + msg.replace("pid", "").replace(":", "")
    if await PixivKeywordUser.delete_keyword(msg):
        await del_keyword.send(f"删除搜图关键词/UID：{msg} 成功...")
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 删除了pixiv搜图关键词:" + msg
        )
    else:
        await del_keyword.send(f"未查询到搜索关键词/UID/PID：{msg}，删除失败！")


@del_pic.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    pid_arr = arg.extract_plain_text().strip()
    if pid_arr:
        msg = ""
        black_pid = ""
        flag = False
        pid_arr = pid_arr.split()
        if pid_arr[-1] in ["-black", "-b"]:
            flag = True
            pid_arr = pid_arr[:-1]
        for pid in pid_arr:
            img_p = None
            if "p" in pid or "ugoira" in pid:
                if "p" in pid:
                    img_p = pid.split("p")[-1]
                    pid = pid.replace("_", "")
                    pid = pid[: pid.find("p")]
                elif "ugoira" in pid:
                    img_p = pid.split("ugoira")[-1]
                    pid = pid.replace("_", "")
                    pid = pid[: pid.find("ugoira")]
            if is_number(pid):
                if await Pixiv.query_images(pid=int(pid), r18=2):
                    if await remove_image(int(pid), img_p):
                        msg += f'{pid}{f"_p{img_p}" if img_p else ""}，'
                        if flag:
                            if await PixivKeywordUser.add_keyword(
                                114514,
                                114514,
                                f"black:{pid}{f'_p{img_p}' if img_p else ''}",
                                bot.config.superusers,
                            ):
                                black_pid += f'{pid}{f"_p{img_p}" if img_p else ""}，'
                        logger.info(
                            f"(USER {event.user_id}, GROUP "
                            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                            f" 删除了PIX图片 PID:{pid}{f'_p{img_p}' if img_p else ''}"
                        )
                    else:
                        await del_pic.send(
                            f"PIX:删除pid：{pid}{f'_p{img_p}' if img_p else ''} 失败.."
                        )
                else:
                    await del_pic.send(
                        f"PIX:图片pix：{pid}{f'_p{img_p}' if img_p else ''} 不存在...无法删除.."
                    )
            else:
                await del_pic.send(f"PID必须为数字！pid：{pid}", at_sender=True)
        await del_pic.send(f"PIX:成功删除图片：{msg[:-1]}")
        if flag:
            await del_pic.send(f"成功图片PID加入黑名单：{black_pid[:-1]}")
    else:
        await del_pic.send("虚空删除？")


@pass_keyword.handle()
async def _(bot: Bot, event: MessageEvent, cmd: Tuple[str, ...] = Command(), arg: Message = CommandArg()):
    tmp = {"group": {}, "private": {}}
    msg = arg.extract_plain_text().strip()
    if not msg:
        await pass_keyword.finish("通过虚空的关键词/UID？离谱...")
    msg = msg.split()
    flag = cmd[0][:2] == "通过"
    for x in msg:
        if x.lower().startswith("uid"):
            x = x.replace("uid", "").replace(":", "")
            x = f"uid:{x}"
        elif x.lower().startswith("pid"):
            x = x.replace("pid", "").replace(":", "")
            x = f"pid:{x}"
        if x.lower().find("pid") != -1 or x.lower().find("uid") != -1:
            if not is_number(x[4:]):
                await pass_keyword.send(f"UID/PID：{x} 非全数字，跳过该关键词...")
                continue
        user_id, group_id = await PixivKeywordUser.set_keyword_pass(x, flag)
        if not user_id:
            await pass_keyword.send(f"未找到关键词/UID：{x}，请检查关键词/UID是否存在...")
            continue
        if flag:
            if group_id == -1:
                if not tmp["private"].get(user_id):
                    tmp["private"][user_id] = {"keyword": [x]}
                else:
                    tmp["private"][user_id]["keyword"].append(x)
            else:
                if not tmp["group"].get(group_id):
                    tmp["group"][group_id] = {}
                if not tmp["group"][group_id].get(user_id):
                    tmp["group"][group_id][user_id] = {"keyword": [x]}
                else:
                    tmp["group"][group_id][user_id]["keyword"].append(x)
    msg = " ".join(msg)
    await pass_keyword.send(f'已成功{cmd[0][:2]}搜图关键词：{msg}....')
    for user in tmp["private"]:
        x = "，".join(tmp["private"][user]["keyword"])
        await bot.send_private_msg(
            user_id=user, message=f"你的关键词/UID/PID {x} 已被管理员通过，将在下一次进行更新..."
        )
    for group in tmp["group"]:
        for user in tmp["group"][group]:
            x = "，".join(tmp["group"][group][user]["keyword"])
            await bot.send_group_msg(
                group_id=group,
                message=Message(f"{at(user)}你的关键词/UID/PID {x} 已被管理员通过，将在下一次进行更新..."),
            )
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 通过了pixiv搜图关键词/UID:" + msg
    )
