from nonebot.adapters.onebot.v11 import Message, Bot, MessageEvent
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from utils.message_builder import custom_forward_msg
from services.db_context import db
from nonebot.params import CommandArg
from services.log import logger

import asyncio

__zx_plugin_name__ = "执行sql [Superuser]"
__plugin_usage__ = """
usage：
    执行一段sql语句
    指令：
        exec [sql语句] ([查询页数，19条/页])
        查看所有表
""".strip()
__plugin_des__ = "执行一段sql语句"
__plugin_cmd__ = [
    "exec [sql语句]",
]
__plugin_version__ = 0.2
__plugin_author__ = "HibiKier"


exec_ = on_command("exec", rule=to_me(), permission=SUPERUSER, priority=1, block=True)
tables = on_command("查看所有表", rule=to_me(), permission=SUPERUSER, priority=1, block=True)


@exec_.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    sql = arg.extract_plain_text().strip()
    async with db.transaction():
        try:
            # 判断是否为SELECT语句
            if sql.lower().startswith("select"):
                # 分割语句
                try:
                    page = int(sql.split(" ")[-1]) - 1
                    sql_list = sql.split(" ")[:-1]
                except ValueError:
                    page = 0
                    sql_list = sql.split(" ")
                # 拼接语句
                sql = " ".join(sql_list)
                query = db.text(sql)
                res = await db.all(query)
                msg_list = [f"第{page+1}页查询结果："]
                # logger.info(res)
                # 获取所有字段
                keys = res[0].keys()
                # 每页10条
                for i in res[page * 10 : (page + 1) * 10]:
                    msg = ""
                    for key in keys:
                        msg += f"{key}: {i[key]}\n"
                    msg += f"第{page+1}页第{res.index(i)+1}条"
                    msg_list.append(msg)
                # 检查是私聊还是群聊
                try:
                    forward_msg_list = custom_forward_msg(msg_list, bot.self_id)
                    await bot.send_group_forward_msg(group_id=event.group_id, messages=forward_msg_list)
                except:
                    for msg in msg_list:
                        await exec_.send(msg)
                        await asyncio.sleep(0.2)
                return
            query = db.text(sql)
            await db.first(query)
            await exec_.send("执行 sql 语句成功.")
        except Exception as e:
            await exec_.send(f"执行 sql 语句失败 {type(e)}：{e}")
            logger.error(f"执行 sql 语句失败 {type(e)}：{e}")


@tables.handle()
async def _(bot: Bot, event: MessageEvent):
    # 获取所有表
    query = db.text("select tablename from pg_tables where schemaname = 'public'")
    res = await db.all(query)
    msg = "数据库中的所有表名：\n"
    for tablename in res:
        msg += str(tablename["tablename"]) + "\n"
    await tables.finish(msg)
