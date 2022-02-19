from nonebot import on_command
from utils.message_builder import image
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from ._data_source import gen_keyword_pic, get_keyword_num
from ._model.pixiv_keyword_user import PixivKeywordUser
from nonebot.params import CommandArg
import asyncio


__zx_plugin_name__ = "查看pix图库"
__plugin_usage__ = """
usage：
    查看pix图库
    指令：
        查看pix图库 ?[tags]: 查看指定tag图片数量，为空时查看整个图库
""".strip()
__plugin_des__ = "让我看看管理员私藏了多少货"
__plugin_cmd__ = ["查看pix图库 ?[tags]"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查看pix图库"],
}


my_keyword = on_command("我的pix关键词", aliases={"我的pix关键字"}, priority=1, block=True)

show_keyword = on_command("显示pix关键词", aliases={"显示pix关键字"}, priority=1, block=True)

show_pix = on_command("查看pix图库", priority=1, block=True)


@my_keyword.handle()
async def _(event: MessageEvent):
    data = await PixivKeywordUser.get_all_user_dict()
    if data.get(event.user_id) is None or not data[event.user_id]["keyword"]:
        await my_keyword.finish("您目前没有提供任何Pixiv搜图关键字...", at_sender=True)
    await my_keyword.send(
        f"您目前提供的如下关键字：\n\t" + "，".join(data[event.user_id]["keyword"])
    )


@show_keyword.handle()
async def _(bot: Bot, event: MessageEvent):
    _pass_keyword, not_pass_keyword = await PixivKeywordUser.get_current_keyword()
    if _pass_keyword or not_pass_keyword:
        await show_keyword.send(
            image(
                b64=await asyncio.get_event_loop().run_in_executor(
                    None,
                    gen_keyword_pic,
                    _pass_keyword,
                    not_pass_keyword,
                    str(event.user_id) in bot.config.superusers,
                )
            )
        )
    else:
        if str(event.user_id) in bot.config.superusers:
            await show_keyword.finish(f"目前没有已收录或待收录的搜索关键词...")
        else:
            await show_keyword.finish(f"目前没有已收录的搜索关键词...")


@show_pix.handle()
async def _(arg: Message = CommandArg()):
    keyword = arg.extract_plain_text().strip()
    count, r18_count, count_, setu_count, r18_count_ = await get_keyword_num(keyword)
    await show_pix.send(
        f"PIX图库：{keyword}\n"
        f"总数：{count + r18_count}\n"
        f"美图：{count}\n"
        f"R18：{r18_count}\n"
        f"---------------\n"
        f"Omega图库：{keyword}\n"
        f"总数：{count_ + setu_count + r18_count_}\n"
        f"美图：{count_}\n"
        f"色图：{setu_count}\n"
        f"R18：{r18_count_}"
    )
