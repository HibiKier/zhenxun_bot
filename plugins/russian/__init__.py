from nonebot import on_command
from nonebot.adapters.onebot.v11 import GROUP, Bot, GroupMessageEvent, Message
from nonebot.typing import T_State
from utils.utils import is_number, get_message_at
from nonebot.params import CommandArg, Command, ArgStr
from models.group_member_info import GroupInfoUser
from utils.message_builder import at, image
from .model import RussianUser
from models.bag_user import BagUser
from services.log import logger
from .data_source import rank
from configs.config import NICKNAME, Config
from typing import Tuple
import random
import asyncio
import time


__zx_plugin_name__ = "俄罗斯轮盘"
__plugin_usage__ = """
usage：
    又到了决斗时刻
    指令：
        装弹 [子弹数] ?[金额=200] ?[at]: 开启游戏，装填子弹，可选自定义金额，或邀请决斗对象
        接受对决: 接受当前存在的对决
        拒绝对决: 拒绝邀请的对决
        开枪: 开出未知的一枪
        结算: 强行结束当前比赛 (仅当一方未开枪超过30秒时可使用)
        我的战绩: 对，你的战绩
        胜场排行/败场排行/欧洲人排行/慈善家排行/最高连胜排行/最高连败排行: 各种排行榜
        示例：装弹 3 100 @sdd
        * 注：同一时间群内只能有一场对决 *
""".strip()
__plugin_des__ = "虽然是运气游戏，但这可是战场啊少年"
__plugin_cmd__ = [
    "装弹 [子弹数] ?[金额=200] ?[at]",
    "接受对决",
    "拒绝对决",
    "开枪",
    "结算",
    "我的战绩",
    "胜场排行/败场排行/欧洲人排行/慈善家排行/最高连胜排行/最高连败排行",
]
__plugin_type__ = ("群内小游戏", 1)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["俄罗斯轮盘", "装弹"],
}
__plugin_configs__ = {
    "MAX_RUSSIAN_BET_GOLD": {
        "value": 1000,
        "help": "俄罗斯轮盘最大赌注金额",
        "default_value": 1000,
    }
}

rs_player = {}

russian = on_command(
    "俄罗斯轮盘", aliases={"装弹", "俄罗斯转盘"}, permission=GROUP, priority=5, block=True
)

accept = on_command(
    "接受对决", aliases={"接受决斗", "接受挑战"}, permission=GROUP, priority=5, block=True
)

refuse = on_command(
    "拒绝对决", aliases={"拒绝决斗", "拒绝挑战"}, permission=GROUP, priority=5, block=True
)

shot = on_command(
    "开枪", aliases={"咔", "嘭", "嘣"}, permission=GROUP, priority=5, block=True
)

settlement = on_command("结算", permission=GROUP, priority=5, block=True)

record = on_command("我的战绩", permission=GROUP, priority=5, block=True)

russian_rank = on_command(
    "胜场排行",
    aliases={"胜利排行", "败场排行", "失败排行", "欧洲人排行", "慈善家排行", "最高连胜排行", "最高连败排行"},
    permission=GROUP,
    priority=5,
    block=True,
)


@accept.handle()
async def _(event: GroupMessageEvent):
    global rs_player
    try:
        if rs_player[event.group_id][1] == 0:
            await accept.finish("目前没有发起对决，你接受个啥？速速装弹！", at_sender=True)
    except KeyError:
        await accept.finish("目前没有进行的决斗，请发送 装弹 开启决斗吧！", at_sender=True)
    if rs_player[event.group_id][2] != 0:
        if (
            rs_player[event.group_id][1] == event.user_id
            or rs_player[event.group_id][2] == event.user_id
        ):
            await accept.finish(f"你已经身处决斗之中了啊，给我认真一点啊！", at_sender=True)
        else:
            await accept.finish("已经有人接受对决了，你还是乖乖等待下一场吧！", at_sender=True)
    if rs_player[event.group_id][1] == event.user_id:
        await accept.finish("请不要自己枪毙自己！换人来接受对决...", at_sender=True)
    if (
        rs_player[event.group_id]["at"] != 0
        and rs_player[event.group_id]["at"] != event.user_id
    ):
        await accept.finish(
            Message(f'这场对决是邀请 {at(rs_player[event.group_id]["at"])}的，不要捣乱！'),
            at_sender=True,
        )
    if time.time() - rs_player[event.group_id]["time"] > 30:
        rs_player[event.group_id] = {}
        await accept.finish("这场对决邀请已经过时了，请重新发起决斗...", at_sender=True)

    user_money = await BagUser.get_gold(event.user_id, event.group_id)
    if user_money < rs_player[event.group_id]["money"]:
        if (
            rs_player[event.group_id]["at"] != 0
            and rs_player[event.group_id]["at"] == event.user_id
        ):
            rs_player[event.group_id] = {}
            await accept.finish("你的金币不足以接受这场对决！对决还未开始便结束了，请重新装弹！", at_sender=True)
        else:
            await accept.finish("你的金币不足以接受这场对决！", at_sender=True)

    player2_name = event.sender.card or event.sender.nickname

    rs_player[event.group_id][2] = event.user_id
    rs_player[event.group_id]["player2"] = player2_name
    rs_player[event.group_id]["time"] = time.time()

    await accept.send(
        Message(f"{player2_name}接受了对决！\n" f"请{at(rs_player[event.group_id][1])}先开枪！")
    )


@refuse.handle()
async def _(event: GroupMessageEvent):
    global rs_player
    try:
        if rs_player[event.group_id][1] == 0:
            await accept.finish("你要拒绝啥？明明都没有人发起对决的说！", at_sender=True)
    except KeyError:
        await refuse.finish("目前没有进行的决斗，请发送 装弹 开启决斗吧！", at_sender=True)
    if (
        rs_player[event.group_id]["at"] != 0
        and event.user_id != rs_player[event.group_id]["at"]
    ):
        await accept.finish("又不是找你决斗，你拒绝什么啊！气！", at_sender=True)
    if rs_player[event.group_id]["at"] == event.user_id:
        at_player_name = (
            await GroupInfoUser.get_member_info(event.user_id, event.group_id)
        ).user_name
        await accept.send(
            Message(f"{at(rs_player[event.group_id][1])}\n" f"{at_player_name}拒绝了你的对决！")
        )
        rs_player[event.group_id] = {}


@settlement.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    global rs_player
    if (
        not rs_player.get(event.group_id)
        or rs_player[event.group_id][1] == 0
        or rs_player[event.group_id][2] == 0
    ):
        await settlement.finish("比赛并没有开始...无法结算...", at_sender=True)
    if (
        event.user_id != rs_player[event.group_id][1]
        and event.user_id != rs_player[event.group_id][2]
    ):
        await settlement.finish("吃瓜群众不要捣乱！黄牌警告！", at_sender=True)
    if time.time() - rs_player[event.group_id]["time"] <= 30:
        await settlement.finish(
            f'{rs_player[event.group_id]["player1"]} 和'
            f' {rs_player[event.group_id]["player2"]} 比赛并未超时，请继续比赛...'
        )
    win_name = (
        rs_player[event.group_id]["player1"]
        if rs_player[event.group_id][2] == rs_player[event.group_id]["next"]
        else rs_player[event.group_id]["player2"]
    )
    await settlement.send(f"这场对决是 {win_name} 胜利了")
    await end_game(bot, event)


@russian.handle()
async def _(
    bot: Bot, event: GroupMessageEvent, state: T_State, arg: Message = CommandArg()
):
    global rs_player
    msg = arg.extract_plain_text().strip()
    try:
        if (
            rs_player[event.group_id][1]
            and not rs_player[event.group_id][2]
            and time.time() - rs_player[event.group_id]["time"] <= 30
        ):
            await russian.finish(
                f'现在是 {rs_player[event.group_id]["player1"]} 发起的对决\n请等待比赛结束后再开始下一轮...'
            )
        if (
            rs_player[event.group_id][1]
            and rs_player[event.group_id][2]
            and time.time() - rs_player[event.group_id]["time"] <= 30
        ):
            await russian.finish(
                f'{rs_player[event.group_id]["player1"]} 和'
                f' {rs_player[event.group_id]["player2"]}的对决还未结束！'
            )
        if (
            rs_player[event.group_id][1]
            and rs_player[event.group_id][2]
            and time.time() - rs_player[event.group_id]["time"] > 30
        ):
            await russian.send("决斗已过时，强行结算...")
            await end_game(bot, event)
        if (
            not rs_player[event.group_id][2]
            and time.time() - rs_player[event.group_id]["time"] > 30
        ):
            rs_player[event.group_id][1] = 0
            rs_player[event.group_id][2] = 0
            rs_player[event.group_id]["at"] = 0
    except KeyError:
        pass
    if msg:
        msg = msg.split()
        if len(msg) == 1:
            msg = msg[0]
            if is_number(msg) and not (int(msg) < 1 or int(msg) > 6):
                state["bullet_num"] = int(msg)
        else:
            money = msg[1].strip()
            msg = msg[0].strip()
            if is_number(msg) and not (int(msg) < 1 or int(msg) > 6):
                state["bullet_num"] = int(msg)
            if is_number(money) and 0 < int(money) <= Config.get_config(
                "russian", "MAX_RUSSIAN_BET_GOLD"
            ):
                state["money"] = int(money)
            else:
                state["money"] = 200
                await russian.send(
                    f"赌注金额超过限制（{Config.get_config('russian', 'MAX_RUSSIAN_BET_GOLD')}），已改为200（默认）"
                )
    state["at"] = get_message_at(event.json())


@russian.got("bullet_num", prompt="请输入装填子弹的数量！(最多6颗)")
async def _(
    event: GroupMessageEvent, state: T_State, bullet_num: str = ArgStr("bullet_num")
):
    global rs_player
    if bullet_num in ["取消", "算了"]:
        await russian.finish("已取消操作...")
    try:
        if rs_player[event.group_id][1] != 0:
            await russian.finish("决斗已开始...", at_sender=True)
    except KeyError:
        pass
    if not is_number(bullet_num):
        await russian.reject_arg("bullet_num", "输入子弹数量必须是数字啊喂！")
    bullet_num = int(bullet_num)
    if bullet_num < 1 or bullet_num > 6:
        await russian.reject_arg("bullet_num", "子弹数量必须大于0小于7！")
    at_ = state["at"] if state.get("at") else []
    money = state["money"] if state.get("money") else 200
    user_money = await BagUser.get_gold(event.user_id, event.group_id)
    if bullet_num < 0 or bullet_num > 6:
        await russian.reject("子弹数量必须大于0小于7！速速重新装弹！")
    if money > Config.get_config("russian", "MAX_RUSSIAN_BET_GOLD"):
        await russian.finish(
            f"太多了！单次金额不能超过{Config.get_config('russian', 'MAX_RUSSIAN_BET_GOLD')}！",
            at_sender=True,
        )
    if money > user_money:
        await russian.finish("你没有足够的钱支撑起这场挑战", at_sender=True)

    player1_name = event.sender.card or event.sender.nickname

    if at_:
        at_ = at_[0]
        try:
            at_player_name = (
                await GroupInfoUser.get_member_info(at_, event.group_id)
            ).user_name
        except AttributeError:
            at_player_name = at(at_)
        msg = f"{player1_name} 向 {at(at_)} 发起了决斗！请 {at_player_name} 在30秒内回复‘接受对决’ or ‘拒绝对决’，超时此次决斗作废！"
    else:
        at_ = 0
        msg = "若30秒内无人接受挑战则此次对决作废【首次游玩请发送 ’俄罗斯轮盘帮助‘ 来查看命令】"

    rs_player[event.group_id] = {
        1: event.user_id,
        "player1": player1_name,
        2: 0,
        "player2": "",
        "at": at_,
        "next": event.user_id,
        "money": money,
        "bullet": random_bullet(bullet_num),
        "bullet_num": bullet_num,
        "null_bullet_num": 7 - bullet_num,
        "index": 0,
        "time": time.time(),
    }

    await russian.send(
        Message(
            ("咔 " * bullet_num)[:-1] + f"，装填完毕\n挑战金额：{money}\n"
            f"第一枪的概率为：{str(float(bullet_num) / 7.0 * 100)[:5]}%\n"
            f"{msg}"
        )
    )


@shot.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    global rs_player
    try:
        if time.time() - rs_player[event.group_id]["time"] > 30:
            if rs_player[event.group_id][2] == 0:
                rs_player[event.group_id][1] = 0
                await shot.finish("这场对决已经过时了，请重新装弹吧！", at_sender=True)
            else:
                await shot.send("决斗已过时，强行结算...")
                await end_game(bot, event)
                return
    except KeyError:
        await shot.finish("目前没有进行的决斗，请发送 装弹 开启决斗吧！", at_sender=True)
    if rs_player[event.group_id][1] == 0:
        await shot.finish("没有对决，也还没装弹呢，请先输入 装弹 吧！", at_sender=True)
    if (
        rs_player[event.group_id][1] == event.user_id
        and rs_player[event.group_id][2] == 0
    ):
        await shot.finish("baka，你是要枪毙自己嘛笨蛋！", at_sender=True)
    if rs_player[event.group_id][2] == 0:
        await shot.finish("请这位勇士先发送 接受对决 来站上擂台...", at_sender=True)
    player1_name = rs_player[event.group_id]["player1"]
    player2_name = rs_player[event.group_id]["player2"]
    if rs_player[event.group_id]["next"] != event.user_id:
        if (
            event.user_id != rs_player[event.group_id][1]
            and event.user_id != rs_player[event.group_id][2]
        ):
            await shot.finish(
                random.choice(
                    [
                        f"不要打扰 {player1_name} 和 {player2_name} 的决斗啊！",
                        f"给我好好做好一个观众！不然{NICKNAME}就要生气了",
                        f"不要捣乱啊baka{(await GroupInfoUser.get_member_info(event.user_id, event.group_id)).user_name}！",
                    ]
                ),
                at_sender=True,
            )
        await shot.finish(
            f"你的左轮不是连发的！该 "
            f'{(await GroupInfoUser.get_member_info(int(rs_player[event.group_id]["next"]), event.group_id)).user_name} 开枪了'
        )
    if rs_player[event.group_id]["bullet"][rs_player[event.group_id]["index"]] != 1:
        await shot.send(
            Message(
                random.choice(
                    [
                        "呼呼，没有爆裂的声响，你活了下来",
                        "虽然黑洞洞的枪口很恐怖，但好在没有子弹射出来，你活下来了",
                        '"咔"，你没死，看来运气不错',
                    ]
                )
                + f"\n下一枪中弹的概率"
                f'：{str(float((rs_player[event.group_id]["bullet_num"])) / float(rs_player[event.group_id]["null_bullet_num"] - 1 + rs_player[event.group_id]["bullet_num"]) * 100)[:5]}%\n'
                f"轮到 {at(rs_player[event.group_id][1] if event.user_id == rs_player[event.group_id][2] else rs_player[event.group_id][2])}了"
            )
        )
        rs_player[event.group_id]["null_bullet_num"] -= 1
        rs_player[event.group_id]["next"] = (
            rs_player[event.group_id][1]
            if event.user_id == rs_player[event.group_id][2]
            else rs_player[event.group_id][2]
        )
        rs_player[event.group_id]["time"] = time.time()
        rs_player[event.group_id]["index"] += 1
    else:
        await shot.send(
            random.choice(
                [
                    '"嘭！"，你直接去世了',
                    "眼前一黑，你直接穿越到了异世界...(死亡)",
                    "终究还是你先走一步...",
                ]
            )
            + f'\n第 {rs_player[event.group_id]["index"] + 1} 发子弹送走了你...',
            at_sender=True,
        )
        win_name = (
            player1_name
            if event.user_id == rs_player[event.group_id][2]
            else player2_name
        )
        await asyncio.sleep(0.5)
        await shot.send(f"这场对决是 {win_name} 胜利了")
        await end_game(bot, event)


async def end_game(bot: Bot, event: GroupMessageEvent):
    global rs_player
    player1_name = rs_player[event.group_id]["player1"]
    player2_name = rs_player[event.group_id]["player2"]
    if rs_player[event.group_id]["next"] == rs_player[event.group_id][1]:
        win_user_id = rs_player[event.group_id][2]
        lose_user_id = rs_player[event.group_id][1]
        win_name = player2_name
        lose_name = player1_name
    else:
        win_user_id = rs_player[event.group_id][1]
        lose_user_id = rs_player[event.group_id][2]
        win_name = player1_name
        lose_name = player2_name
    rand = random.randint(0, 5)
    money = rs_player[event.group_id]["money"]
    if money > 10:
        fee = int(money * float(rand) / 100)
        fee = 1 if fee < 1 and rand != 0 else fee
    else:
        fee = 0
    await RussianUser.add_count(win_user_id, event.group_id, "win")
    await RussianUser.add_count(lose_user_id, event.group_id, "lose")
    await RussianUser.money(win_user_id, event.group_id, "win", money - fee)
    await RussianUser.money(lose_user_id, event.group_id, "lose", money)
    await BagUser.add_gold(win_user_id, event.group_id, money - fee)
    await BagUser.spend_gold(lose_user_id, event.group_id, money)
    win_user = await RussianUser.ensure(win_user_id, event.group_id)
    lose_user = await RussianUser.ensure(lose_user_id, event.group_id)
    bullet_str = ""
    for x in rs_player[event.group_id]["bullet"]:
        bullet_str += "__ " if x == 0 else "| "
    logger.info(f"俄罗斯轮盘：胜者：{win_name} - 败者：{lose_name} - 金币：{money}")
    rs_player[event.group_id] = {}
    await bot.send(
        event,
        message=f"结算：\n"
        f"\t胜者：{win_name}\n"
        f"\t赢取金币：{money - fee}\n"
        f"\t累计胜场：{win_user.win_count}\n"
        f"\t累计赚取金币：{win_user.make_money}\n"
        f"-------------------\n"
        f"\t败者：{lose_name}\n"
        f"\t输掉金币：{money}\n"
        f"\t累计败场：{lose_user.fail_count}\n"
        f"\t累计输掉金币：{lose_user.lose_money}\n"
        f"-------------------\n"
        f"哼哼，{NICKNAME}从中收取了 {float(rand)}%({fee}金币) 作为手续费！\n"
        f"子弹排列：{bullet_str[:-1]}",
    )


@record.handle()
async def _(event: GroupMessageEvent):
    user = await RussianUser.ensure(event.user_id, event.group_id)
    await record.send(
        f"俄罗斯轮盘\n"
        f"总胜利场次：{user.win_count}\n"
        f"当前连胜：{user.winning_streak}\n"
        f"最高连胜：{user.max_winning_streak}\n"
        f"总失败场次：{user.fail_count}\n"
        f"当前连败：{user.losing_streak}\n"
        f"最高连败：{user.max_losing_streak}\n"
        f"赚取金币：{user.make_money}\n"
        f"输掉金币：{user.lose_money}",
        at_sender=True,
    )


@russian_rank.handle()
async def _(
    event: GroupMessageEvent,
    cmd: Tuple[str, ...] = Command(),
    arg: Message = CommandArg(),
):
    num = arg.extract_plain_text().strip()
    if is_number(num) and 51 > int(num) > 10:
        num = int(num)
    else:
        num = 10
    rank_image = None
    if cmd[0] in ["胜场排行", "胜利排行"]:
        rank_image = await rank(event.group_id, "win_rank", num)
    if cmd[0] in ["败场排行", "失败排行"]:
        rank_image = await rank(event.group_id, "lose_rank", num)
    if cmd[0] == "欧洲人排行":
        rank_image = await rank(event.group_id, "make_money", num)
    if cmd[0] == "慈善家排行":
        rank_image = await rank(event.group_id, "spend_money", num)
    if cmd[0] == "最高连胜排行":
        rank_image = await rank(event.group_id, "max_winning_streak", num)
    if cmd[0] == "最高连败排行":
        rank_image = await rank(event.group_id, "max_losing_streak", num)
    if rank_image:
        await russian_rank.send(image(b64=rank_image.pic2bs4()))


# 随机子弹排列
def random_bullet(num: int) -> list:
    bullet_lst = [0, 0, 0, 0, 0, 0, 0]
    for i in random.sample([0, 1, 2, 3, 4, 5, 6], num):
        bullet_lst[i] = 1
    return bullet_lst
