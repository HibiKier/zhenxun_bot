from nonebot import on_regex
from nonebot.rule import to_me
from pathlib import Path


__zx_plugin_name__ = "关于"
__plugin_usage__ = """
usage：
    想要更加了解真寻吗
    指令：
        关于
""".strip()
__plugin_des__ = "想要更加了解真寻吗"
__plugin_cmd__ = ["关于"]
__plugin_version__ = 0.1
__plugin_type__ = ("其他",)
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 1,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["关于"],
}


about = on_regex("^关于$", priority=5, block=True, rule=to_me())


@about.handle()
async def _():
    ver_file = Path() / '__version__'
    version = None
    if ver_file.exists():
        with open(ver_file, 'r', encoding='utf8') as f:
            version = f.read().split(':')[-1].strip()
    msg = f"""
『绪山真寻Bot』
版本：{version}
简介：基于Nonebot2与go-cqhttp开发，是一个非常可爱的Bot呀，希望与大家要好好相处
项目地址：https://github.com/HibiKier/zhenxun_bot
文档地址：https://hibikier.github.io/zhenxun_bot/
    """.strip()
    await about.send(msg)
