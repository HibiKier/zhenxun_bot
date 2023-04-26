import asyncio
import shlex
from typing import List

import httpx
from meme_generator.meme import Meme
from nonebot.log import logger

from .config import memes_config
from .exception import NetworkError


async def download_url(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url, timeout=20)
                resp.raise_for_status()
                return resp.content
            except Exception as e:
                logger.warning(f"Error downloading {url}, retry {i}/3: {e}")
                await asyncio.sleep(3)
    raise NetworkError(f"{url} 下载失败！")


def split_text(text: str) -> List[str]:
    try:
        return shlex.split(text)
    except:
        return text.split()


def meme_info(meme: Meme) -> str:
    keywords = "、".join([f'"{keyword}"' for keyword in meme.keywords])

    patterns = "、".join([f'"{pattern}"' for pattern in meme.patterns])

    image_num = f"{meme.params_type.min_images}"
    if meme.params_type.max_images > meme.params_type.min_images:
        image_num += f" ~ {meme.params_type.max_images}"

    text_num = f"{meme.params_type.min_texts}"
    if meme.params_type.max_texts > meme.params_type.min_texts:
        text_num += f" ~ {meme.params_type.max_texts}"

    default_texts = ", ".join([f'"{text}"' for text in meme.params_type.default_texts])

    if args := meme.params_type.args_type:
        parser = args.parser
        args_info = parser.format_help().split("\n\n")[-1]
        lines = []
        for line in args_info.splitlines():
            if line.lstrip().startswith("options") or line.lstrip().startswith(
                "-h, --help"
            ):
                continue
            lines.append(line)
        args_info = "\n".join(lines)
    else:
        args_info = ""

    return (
        f"表情名：{meme.key}\n"
        + f"关键词：{keywords}\n"
        + (f"正则表达式：{patterns}\n" if patterns else "")
        + f"需要图片数目：{image_num}\n"
        + f"需要文字数目：{text_num}\n"
        + (f"默认文字：[{default_texts}]\n" if default_texts else "")
        + (f"可选参数：\n{args_info}\n" if args_info else "")
    )


if memes_config.memes_check_resources_on_startup:
    from meme_generator.download import check_resources
    from nonebot import get_driver

    driver = get_driver()

    @driver.on_startup
    async def _():
        logger.info("正在检查资源文件...")
        asyncio.create_task(check_resources())
