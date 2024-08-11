import asyncio
import traceback
from dataclasses import dataclass
from typing import Any

import nonebot
from cn2an import cn2an
from nonebot import on_keyword, on_message, on_regex
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import RegexGroup
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_Handler
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginExtraData
from zhenxun.utils.message import MessageUtils

from .handles.azur_handle import AzurHandle
from .handles.ba_handle import BaHandle
from .handles.base_handle import BaseHandle
from .handles.fgo_handle import FgoHandle
from .handles.genshin_handle import GenshinHandle
from .handles.guardian_handle import GuardianHandle
from .handles.onmyoji_handle import OnmyojiHandle
from .handles.pcr_handle import PcrHandle
from .handles.pretty_handle import PrettyHandle
from .handles.prts_handle import PrtsHandle
from .rule import rule

__plugin_meta__ = PluginMetadata(
    name="游戏抽卡",
    description="就算是模拟抽卡也不能改变自己是个非酋",
    usage="""
    usage：
        模拟赛马娘，原神，明日方舟，坎公骑冠剑，公主连结(国/台)，碧蓝航线，FGO，阴阳师，碧蓝档案进行抽卡
        指令：
            原神[1-180]抽: 原神常驻池
            原神角色[1-180]抽: 原神角色UP池子
            原神角色2池[1-180]抽: 原神角色UP池子
            原神武器[1-180]抽: 原神武器UP池子
            重置原神抽卡: 清空当前卡池的抽卡次数[即从0开始计算UP概率]
            方舟[1-300]抽: 方舟卡池，当有当期UP时指向UP池
            赛马娘[1-200]抽: 赛马娘卡池，当有当期UP时指向UP池
            坎公骑冠剑[1-300]抽: 坎公骑冠剑卡池，当有当期UP时指向UP池
            pcr/公主连接[1-300]抽: 公主连接卡池
            碧蓝航线/碧蓝[重型/轻型/特型/活动][1-300]抽: 碧蓝航线重型/轻型/特型/活动卡池
            fgo[1-300]抽: fgo卡池 (已失效)
            阴阳师[1-300]抽: 阴阳师卡池
            ba/碧蓝档案[1-200]抽：碧蓝档案卡池
        * 以上指令可以通过 XX一井 来指定最大抽取数量 *
        * 示例：原神一井 *
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        menu_type="抽卡相关",
        superuser_help="""
        更新方舟信息
        重载方舟卡池
        更新原神信息
        重载原神卡池
        更新赛马娘信息
        重载赛马娘卡池
        更新坎公骑冠剑信息
        更新碧蓝航线信息
        更新fgo信息
        更新阴阳师信息
        """,
    ).dict(),
)

_hidden = on_message(rule=lambda: False)


@dataclass
class Game:
    keywords: set[str]
    handle: BaseHandle
    flag: bool
    config_name: str
    max_count: int = 300  # 一次最大抽卡数
    reload_time: int | None = None  # 重载UP池时间（小时）
    has_other_pool: bool = False


games = (
    Game(
        {"azur", "碧蓝航线"},
        AzurHandle(),
        Config.get_config("draw_card", "AZUR_FLAG", True),
        "AZUR_FLAG",
    ),
    Game(
        {"fgo", "命运冠位指定"},
        FgoHandle(),
        Config.get_config("draw_card", "FGO_FLAG", True),
        "FGO_FLAG",
    ),
    Game(
        {"genshin", "原神"},
        GenshinHandle(),
        Config.get_config("draw_card", "GENSHIN_FLAG", True),
        "GENSHIN_FLAG",
        max_count=180,
        reload_time=18,
        has_other_pool=True,
    ),
    Game(
        {"guardian", "坎公骑冠剑"},
        GuardianHandle(),
        Config.get_config("draw_card", "GUARDIAN_FLAG", True),
        "GUARDIAN_FLAG",
        reload_time=4,
    ),
    Game(
        {"onmyoji", "阴阳师"},
        OnmyojiHandle(),
        Config.get_config("draw_card", "ONMYOJI_FLAG", True),
        "ONMYOJI_FLAG",
    ),
    Game(
        {"pcr", "公主连结", "公主连接", "公主链接", "公主焊接"},
        PcrHandle(),
        Config.get_config("draw_card", "PCR_FLAG", True),
        "PCR_FLAG",
    ),
    Game(
        {"pretty", "马娘", "赛马娘"},
        PrettyHandle(),
        Config.get_config("draw_card", "PRETTY_FLAG", True),
        "PRETTY_FLAG",
        max_count=200,
        reload_time=4,
    ),
    Game(
        {"prts", "方舟", "明日方舟"},
        PrtsHandle(),
        Config.get_config("draw_card", "PRTS_FLAG", True),
        "PRTS_FLAG",
        reload_time=4,
    ),
    Game(
        {"ba", "碧蓝档案"},
        BaHandle(),
        Config.get_config("draw_card", "BA_FLAG", True),
        "BA_FLAG",
    ),
)


def create_matchers():
    def draw_handler(game: Game) -> T_Handler:
        async def handler(
            session: EventSession,
            args: tuple[Any, ...] = RegexGroup(),
        ):
            pool_name, pool_type_, num, unit = args
            if num == "单":
                num = 1
            else:
                try:
                    num = int(cn2an(num, mode="smart"))
                except ValueError:
                    await MessageUtils.build_message("必！须！是！数！字！").finish(
                        reply_to=True
                    )
            if unit == "井":
                num *= game.max_count
            if num < 1:
                await MessageUtils.build_message("虚空抽卡？？？").finish(reply_to=True)
            elif num > game.max_count:
                await MessageUtils.build_message(
                    "一井都满不足不了你嘛！快爬开！"
                ).finish(reply_to=True)
            pool_name = (
                pool_name.replace("池", "")
                .replace("武器", "arms")
                .replace("角色", "char")
                .replace("卡牌", "card")
                .replace("卡", "card")
            )
            try:
                if pool_type_ in ["2池", "二池"]:
                    pool_name = pool_name + "1"
                res = await game.handle.draw(
                    num, pool_name=pool_name, user_id=session.id1
                )
                logger.info(
                    f"游戏抽卡 类型: {list(game.keywords)[1]} 卡池: {pool_name} 数量: {num}",
                    "游戏抽卡",
                    session=session,
                )
            except:
                logger.warning(traceback.format_exc())
                await MessageUtils.build_message("出错了...").finish(reply_to=True)
            await res.send()

        return handler

    def update_handler(game: Game) -> T_Handler:
        async def handler(matcher: Matcher):
            await game.handle.update_info()
            await matcher.finish("更新完成！")

        return handler

    def reload_handler(game: Game) -> T_Handler:
        async def handler(matcher: Matcher):
            res = await game.handle.reload_pool()
            if res:
                await res.send()

        return handler

    def reset_handler(game: Game) -> T_Handler:
        async def handler(matcher: Matcher, session: EventSession):
            if not session.id1:
                await MessageUtils.build_message("获取用户id失败...").finish()
            if game.handle.reset_count(session.id1):
                await MessageUtils.build_message("重置成功！").send()

        return handler

    def scheduled_job(game: Game) -> T_Handler:
        async def handler():
            await game.handle.reload_pool()

        return handler

    for game in games:
        pool_pattern = r"([^\s单0-9零一二三四五六七八九百十]{0,3})"
        num_pattern = r"(单|[0-9零一二三四五六七八九百十]{1,3})"
        unit_pattern = r"([抽|井|连])"
        pool_type = "()"
        if game.has_other_pool:
            pool_type = r"([2二]池)?"
        draw_regex = r".*?(?:{})\s*{}\s*{}\s*{}\s*{}".format(
            "|".join(game.keywords), pool_pattern, pool_type, num_pattern, unit_pattern
        )
        update_keywords = {f"更新{keyword}信息" for keyword in game.keywords}
        reload_keywords = {f"重载{keyword}卡池" for keyword in game.keywords}
        reset_keywords = {f"重置{keyword}抽卡" for keyword in game.keywords}
        on_regex(draw_regex, priority=5, block=True, rule=rule(game)).append_handler(
            draw_handler(game)
        )
        on_keyword(
            update_keywords, priority=1, block=True, permission=SUPERUSER
        ).append_handler(update_handler(game))
        on_keyword(
            reload_keywords, priority=1, block=True, permission=SUPERUSER
        ).append_handler(reload_handler(game))
        on_keyword(reset_keywords, priority=5, block=True).append_handler(
            reset_handler(game)
        )
        if game.reload_time:
            scheduler.add_job(
                scheduled_job(game), trigger="cron", hour=game.reload_time, minute=1
            )


create_matchers()


# 更新资源
@scheduler.scheduled_job(
    "cron",
    hour=4,
    minute=1,
)
async def _():
    tasks = []
    for game in games:
        if game.flag:
            tasks.append(asyncio.ensure_future(game.handle.update_info()))
    await asyncio.gather(*tasks)


driver = nonebot.get_driver()


@driver.on_startup
async def _():
    tasks = []
    for game in games:
        if game.flag:
            game.handle.init_data()
            if not game.handle.data_exists():
                tasks.append(asyncio.ensure_future(game.handle.update_info()))
    await asyncio.gather(*tasks)
