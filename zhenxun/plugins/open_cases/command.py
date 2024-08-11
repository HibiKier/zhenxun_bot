from nonebot.permission import SUPERUSER
from nonebot_plugin_alconna import Alconna, Args, Option, on_alconna, store_true

from zhenxun.utils.rules import ensure_group

_open_matcher = on_alconna(
    Alconna("开箱", Args["name?", str]), priority=5, block=True, rule=ensure_group
)

_reload_matcher = on_alconna(
    Alconna("重置开箱"), priority=5, block=True, permission=SUPERUSER, rule=ensure_group
)

_my_open_matcher = on_alconna(
    Alconna("我的开箱"),
    aliases={"开箱统计", "开箱查询", "查询开箱"},
    priority=5,
    block=True,
    rule=ensure_group,
)

_group_open_matcher = on_alconna(
    Alconna("群开箱统计"), priority=5, block=True, rule=ensure_group
)

_multiple_matcher = on_alconna(
    Alconna("multiple-open", Args["num", int]["name?", str]),
    priority=5,
    block=True,
    rule=ensure_group,
)

_multiple_matcher.shortcut(
    r"(?P<num>\d+)连开箱(?P<name>.*?)",
    command="multiple-open",
    arguments=["{num}", "{name}"],
    prefix=True,
)

_update_matcher = on_alconna(
    Alconna(
        "更新武器箱",
        Args["name?", str],
        Option("-s", action=store_true, help_text="是否必定更新所属箱子"),
    ),
    aliases={"更新皮肤"},
    priority=1,
    permission=SUPERUSER,
    block=True,
)

_update_image_matcher = on_alconna(
    Alconna("更新武器箱图片", Args["name?", str]),
    priority=1,
    permission=SUPERUSER,
    block=True,
)

_show_case_matcher = on_alconna(
    Alconna("查看武器箱", Args["name?", str]), priority=5, block=True
)

_knifes_matcher = on_alconna(
    Alconna("我的金色"), priority=5, block=True, rule=ensure_group
)

_show_skin_matcher = on_alconna(Alconna("查看皮肤"), priority=5, block=True)

_price_matcher = on_alconna(
    Alconna(
        "价格趋势", Args["name", str]["skin", str]["abrasion", str]["day?", int, 7]
    ),
    priority=5,
    block=True,
)
