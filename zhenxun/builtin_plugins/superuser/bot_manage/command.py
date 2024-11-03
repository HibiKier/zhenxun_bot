from nonebot.permission import SUPERUSER
from arclet.alconna.action import store_true
from nonebot_plugin_alconna import on_alconna
from arclet.alconna import Args, Option, Alconna, Subcommand

bot_manage = on_alconna(
    Alconna(
        "bot_manage",
        Subcommand(
            "task",
            Option(
                "list",
                action=store_true,
                default=False,
                help_text="查看 bot_id 下的所有可用被动",
            ),
            Subcommand(
                "enable",
                Option(
                    "-a|--all",
                    action=store_true,
                    default=False,
                    help_text="可选开启全部",
                ),
                Args["feature_name?", str],
                Args["bot_id?", str],
            ),
            Subcommand(
                "disable",
                Option(
                    "-a|--all",
                    action=store_true,
                    default=False,
                    help_text="可选关闭全部",
                ),
                Args["feature_name?", str],
                Args["bot_id?", str],
            ),
        ),
        Subcommand(
            "plugin",
            Option(
                "list",
                action=store_true,
                default=False,
                help_text="查看 bot_id 下的所有可用插件",
            ),
            Subcommand(
                "enable",
                Option(
                    "-a|--all",
                    action=store_true,
                    default=False,
                    help_text="可选开启全部",
                ),
                Args["plugin_name?", str],
                Args["bot_id?", str],
            ),
            Subcommand(
                "disable",
                Option(
                    "-a|--all",
                    action=store_true,
                    default=False,
                    help_text="可选关闭全部",
                ),
                Args["plugin_name?", str],
                Args["bot_id?", str],
            ),
        ),
        Subcommand(
            "status",
            Subcommand(
                "tasks",
                Args["bot_id", str],
            ),
            Subcommand(
                "plugins",
                Args["bot_id", str],
            ),
            Subcommand(
                "bots",
                Args["bot_id", str],
            ),
        ),
        Subcommand(
            "full_function",
            Subcommand(
                "enable",
                Args["bot_id?", str],
            ),
            Subcommand(
                "disable",
                Args["bot_id?", str],
            ),
        ),
        Subcommand(
            "bot_switch",
            Subcommand(
                "enable",
                Args["bot_id?", str],
            ),
            Subcommand(
                "disable",
                Args["bot_id?", str],
            ),
        ),
    ),
    permission=SUPERUSER,
    priority=5,
    block=True,
)
