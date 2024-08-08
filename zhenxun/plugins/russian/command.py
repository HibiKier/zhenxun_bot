from nonebot_plugin_alconna import Alconna, Args
from nonebot_plugin_alconna import At as alcAt
from nonebot_plugin_alconna import on_alconna

from zhenxun.utils.rules import ensure_group

_russian_matcher = on_alconna(
    Alconna(
        "俄罗斯轮盘",
        Args["money", int]["num?", str]["at_user?", alcAt],
    ),
    aliases={"装弹", "俄罗斯转盘"},
    rule=ensure_group,
    priority=5,
    block=True,
)

_accept_matcher = on_alconna(
    Alconna("接受对决"),
    aliases={"接受决斗", "接受挑战"},
    rule=ensure_group,
    priority=5,
    block=True,
)

_refuse_matcher = on_alconna(
    Alconna("拒绝对决"),
    aliases={"拒绝决斗", "拒绝挑战"},
    rule=ensure_group,
    priority=5,
    block=True,
)

_shoot_matcher = on_alconna(
    Alconna("开枪"),
    aliases={"咔", "嘭", "嘣"},
    rule=ensure_group,
    priority=5,
    block=True,
)

_settlement_matcher = on_alconna(
    Alconna("结算"),
    rule=ensure_group,
    priority=5,
    block=True,
)

_record_matcher = on_alconna(
    Alconna("我的战绩"),
    rule=ensure_group,
    priority=5,
    block=True,
)

_rank_matcher = on_alconna(
    Alconna(
        "russian-rank",
        Args["rank_type", ["win", "lose", "a", "b", "max_win", "max_lose"]][
            "num?", int, 10
        ],
    ),
    rule=ensure_group,
    priority=5,
    block=True,
)

_rank_matcher.shortcut(
    r"轮盘胜场排行(?P<num>\d*)",
    command="russian-rank",
    arguments=["win", "{num}"],
    prefix=True,
)

_rank_matcher.shortcut(
    r"轮盘败场排行(?P<num>\d*)",
    command="russian-rank",
    arguments=["lose", "{num}"],
    prefix=True,
)

_rank_matcher.shortcut(
    r"轮盘欧洲人排行(?P<num>\d*)",
    command="russian-rank",
    arguments=["a", "{num}"],
    prefix=True,
)

_rank_matcher.shortcut(
    r"轮盘慈善家排行(?P<num>\d*)",
    command="russian-rank",
    arguments=["b", "{num}"],
    prefix=True,
)

_rank_matcher.shortcut(
    r"轮盘最高连胜排行(?P<num>\d*)",
    command="russian-rank",
    arguments=["max_win", "{num}"],
    prefix=True,
)

_rank_matcher.shortcut(
    r"轮盘最高连败排行(?P<num>\d*)",
    command="russian-rank",
    arguments=["max_lose", "{num}"],
    prefix=True,
)
