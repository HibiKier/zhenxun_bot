from nonebot import on_command
from nonebot.permission import SUPERUSER
from models.level_user import LevelUser
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, GroupMessageEvent
from utils.utils import get_message_at, is_number
from services.log import logger
from utils.message_builder import at
from nonebot.params import Command, CommandArg
from typing import Tuple

__zx_plugin_name__ = "用户权限管理 [Superuser]"
__plugin_usage__ = """
usage：
    增删改用户的权限
    指令：
        添加权限 [at] [权限]
        添加权限 [qq] [group_id] [权限]
        删除权限 [at]
""".strip()
__plugin_des__ = "增删改用户的权限"
__plugin_cmd__ = [
    "添加权限 [at] [权限]",
    "添加权限 [qq] [group_id] [权限]",
    "删除权限 [at]",
]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


super_cmd = on_command(
    "添加管理",
    aliases={"删除管理", "添加权限", "删除权限"},
    priority=1,
    permission=SUPERUSER,
    block=True,
)


@super_cmd.handle()
async def _(
    bot: Bot,
    event: MessageEvent,
    cmd: Tuple[str, ...] = Command(),
    arg: Message = CommandArg(),
):
    group_id = event.group_id if isinstance(event, GroupMessageEvent) else -1
    level = None
    args = arg.extract_plain_text().strip().split()
    qq = get_message_at(event.json())
    flag = 2
    try:
        if qq:
            qq = qq[0]
            if cmd[0][:2] == "添加" and args and is_number(args[0]):
                level = int(args[0])
        else:
            if cmd[0][:2] == "添加":
                if (
                    len(args) > 2
                    and is_number(args[0])
                    and is_number(args[1])
                    and is_number(args[2])
                ):
                    qq = int(args[0])
                    group_id = int(args[1])
                    level = int(args[2])
            else:
                if len(args) > 1 and is_number(args[0]) and is_number(args[1]):
                    qq = int(args[0])
                    group_id = int(args[1])
            flag = 1
        level = -1 if cmd[0][:2] == "删除" else level
        if group_id == -1 or not level or not qq:
            raise IndexError()
    except IndexError:
        await super_cmd.finish(__plugin_usage__)
    try:
        if cmd[0][:2] == "添加":
            if await LevelUser.set_level(qq, group_id, level, 1):
                result = f"添加管理成功, 权限: {level}"
            else:
                result = f"管理已存在, 更新权限: {level}"
        else:
            if await LevelUser.delete_level(qq, event.group_id):
                result = "删除管理成功!"
            else:
                result = "该账号无管理权限!"
        if flag == 2:
            await super_cmd.send(result)
        elif flag == 1:
            await bot.send_group_msg(
                group_id=group_id,
                message=Message(
                    f"{at(qq)}管理员修改了你的权限"
                    f"\n--------\n你当前的权限等级：{level if level != -1 else 0}"
                ),
            )
            await super_cmd.send("修改成功")
    except Exception as e:
        await super_cmd.send("执行指令失败!")
        logger.error(f"执行指令失败 e：{e}")
