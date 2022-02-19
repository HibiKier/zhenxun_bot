from nonebot.adapters.onebot.v11 import Message
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from services.db_context import db
from nonebot.params import CommandArg
from services.log import logger

__zx_plugin_name__ = "执行sql [Superuser]"
__plugin_usage__ = """
usage：
    执行一段sql语句
    指令：
        exec [sql语句]
""".strip()
__plugin_des__ = "执行一段sql语句"
__plugin_cmd__ = [
    "exec [sql语句]",
]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


exec_ = on_command("exec", rule=to_me(), permission=SUPERUSER, priority=1, block=True)


@exec_.handle()
async def _(arg: Message = CommandArg()):
    sql = arg.extract_plain_text().strip()
    async with db.transaction():
        try:
            query = db.text(sql)
            await db.first(query)
            await exec_.send("执行 sql 语句成功.")
        except Exception as e:
            await exec_.send(f"执行 sql 语句失败 {type(e)}：{e}")
            logger.error(f"执行 sql 语句失败 {type(e)}：{e}")
