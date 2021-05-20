from .data_source import rd, help_message, st, en
from .madness import ti, li
from .create import Investigator
from .san_check import sc

from nonebot.plugin import on_startswith
from nonebot.adapters.cqhttp import Bot, Event

rdhelp = on_startswith("骰子娘帮助", priority=2)
stcommand = on_startswith(".st", priority=2)
encommand = on_startswith(".en", priority=2)
ticommand = on_startswith(".ti", priority=2)
licommand = on_startswith(".li", priority=2)
coc = on_startswith(".coc", priority=2)
sccommand = on_startswith(".sc", priority=2)
rdcommand = on_startswith(".r", priority=3)


@rdhelp.handle()
async def rdhelphandler(bot: Bot):
    await rdhelp.finish(help_message())


@stcommand.handle()
async def stcommandhandler(bot: Bot):
    await rdhelp.finish(st())


@encommand.handle()
async def enhandler(bot: Bot, event: Event):
    args = str(event.get_message())[3:].strip()
    await encommand.finish(en(args))


@rdcommand.handle()
async def rdcommandhandler(bot: Bot, event: Event):
    args = str(event.get_message())[2:].strip()
    uid = event.get_session_id()
    if args and not("." in args):
        rrd = rd(args)
        if type(rrd) == str:
            await rdcommand.finish(rrd)
        elif type(rrd) == list:
            await bot.send_private_msg(user_id=uid, message=rrd[0])


@coc.handle()
async def cochandler(bot: Bot, event: Event):
    args = str(event.get_message())[4:].strip()
    try:
        args = int(args)
    except:
        args = 20
    inv = Investigator()
    inv.age_change(args)
    await coc.finish(inv.output())


@ticommand.handle()
async def ticommandhandler(bot: Bot):
    await ticommand.finish(ti())


@licommand.handle()
async def licommandhandler(bot: Bot):
    await licommand.finish(li())


@sccommand.handle()
async def schandler(bot: Bot, event: Event):
    args = str(event.get_message())[3:].strip()
    await sccommand.finish(sc(args.lower()))
