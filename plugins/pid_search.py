from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, GroupMessageEvent
from nonebot.typing import T_State

from configs.config import Config
from utils.utils import is_number, change_pixiv_image_links
from utils.message_builder import image
from services.log import logger
from asyncio.exceptions import TimeoutError
from configs.path_config import IMAGE_PATH
from utils.manager import withdraw_message_manager
from utils.http_utils import AsyncHttpx
from nonebot.params import CommandArg, Arg


__zx_plugin_name__ = "pid搜索"
__plugin_usage__ = """
usage：
    通过 pid 搜索图片
    指令：
        p搜 [pid]
""".strip()
__plugin_des__ = "通过 pid 搜索图片"
__plugin_cmd__ = ["p搜 [pid]"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["p搜"],
}

pid_search = on_command("p搜", aliases={"pixiv搜", "P搜"}, priority=5, block=True)


@pid_search.handle()
async def _h(event: MessageEvent, state: T_State, arg: Message = CommandArg()):
    pid = arg.extract_plain_text().strip()
    if pid:
        state["pid"] = pid


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6;"
    " rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Referer": "https://www.pixiv.net",
}


@pid_search.got("pid", prompt="需要查询的图片PID是？")
async def _g(event: MessageEvent, state: T_State, pid: str = Arg("pid")):
    url = Config.get_config("hibiapi", "HIBIAPI") + "/api/pixiv/"
    if pid in ["取消", "算了"]:
        await pid_search.finish("已取消操作...")
    if not is_number(pid):
        await pid_search.reject_arg("pid", "笨蛋，重新输入数！字！")
    for _ in range(3):
        try:
            data = (
                await AsyncHttpx.get(
                    url,
                    params={"id": pid},
                    timeout=5,
                )
            ).json()
        except TimeoutError:
            pass
        except Exception as e:
            await pid_search.finish(f"发生了一些错误..{type(e)}：{e}")
        else:
            if data.get("error"):
                await pid_search.finish(data["error"]["user_message"], at_sender=True)
            data = data["illust"]
            if not data["width"] and not data["height"]:
                await pid_search.finish(f"没有搜索到 PID：{pid} 的图片", at_sender=True)
            pid = data["id"]
            title = data["title"]
            author = data["user"]["name"]
            author_id = data["user"]["id"]
            image_list = []
            try:
                image_list.append(data["meta_single_page"]["original_image_url"])
            except KeyError:
                for image_url in data["meta_pages"]:
                    image_list.append(image_url["image_urls"]["original"])
            for i, img_url in enumerate(image_list):
                img_url = change_pixiv_image_links(img_url)
                if not await AsyncHttpx.download_file(
                    img_url,
                    IMAGE_PATH / "temp" / f"pid_search_{event.user_id}_{i}.png",
                    headers=headers,
                ):
                    await pid_search.send("图片下载失败了....", at_sender=True)
                tmp = ""
                if isinstance(event, GroupMessageEvent):
                    tmp = "\n【注】将在30后撤回......"
                msg_id = await pid_search.send(
                    Message(
                        f"title：{title}\n"
                        f"pid：{pid}\n"
                        f"author：{author}\n"
                        f"author_id：{author_id}\n"
                        f'{image(f"pid_search_{event.user_id}_{i}.png", "temp")}'
                        f"{tmp}"
                    )
                )
                logger.info(
                    f"(USER {event.user_id}, "
                    f"GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                    f" 查询图片 PID：{pid}"
                )
                if isinstance(event, GroupMessageEvent):
                    withdraw_message_manager.append((msg_id, 30))
            break
    else:
        await pid_search.finish("图片下载失败了....", at_sender=True)
