from utils.utils import get_bot
from bs4 import BeautifulSoup
from utils.http_utils import AsyncHttpx
import asyncio
import platform
import os

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


url = "https://github.com/Mrs4s/go-cqhttp/releases"


async def download_gocq_lasted(path: str):
    text = (await AsyncHttpx.get(url)).text
    soup = BeautifulSoup(text, "lxml")
    a = soup.find("div", {"class": "release-header"}).find("a")
    title = a.text
    _url = a.get("href")
    for file in os.listdir(path):
        if file.endswith(".zip"):
            if (
                file == title + "-windows-amd64.zip"
                or file == title + "_windows_amd64.zip"
            ):
                return "gocqhttp没有更新！"
    for file in os.listdir(path):
        os.remove(path + file)
    text = (await AsyncHttpx.get("https://github.com" + _url)).text
    update_info = ""
    soup = BeautifulSoup(text, "lxml")
    info_div = soup.find("div", {"class": "markdown-body"})
    for p in info_div.find_all("p"):
        update_info += p.text.replace("<br>", "\n") + "\n"
    div_all = soup.select(
        "div.d-flex.flex-justify-between.flex-items-center.py-1.py-md-2.Box-body.px-2"
    )
    for div in div_all:
        if (
            div.find("a").find("span").text == title + "-windows-amd64.zip"
            or div.find("a").find("span").text == title + "-linux-arm64.tar.gz"
            or div.find("a").find("span").text == "go-cqhttp_windows_amd64.zip"
            or div.find("a").find("span").text == "go-cqhttp_linux_arm64.tar.gz"
        ):
            file_url = div.find("a").get("href")
            if div.find("a").find("span").text.find("windows") == -1:
                tag = "-linux-arm64.tar.gz"
            else:
                tag = "-windows-amd64.zip"
            await AsyncHttpx.download_file(
                "https://github.com" + file_url, path + title + tag
            )
    return update_info


async def upload_gocq_lasted(path, name, group_id):
    bot = get_bot()
    folder_id = 0
    for folder in (await bot.get_group_root_files(group_id=group_id))["folders"]:
        if folder["folder_name"] == "gocq":
            folder_id = folder["folder_id"]
    if not folder_id:
        await bot.send_group_msg(group_id=group_id, message=f"请创建gocq文件夹后重试！")
        for file in os.listdir(path):
            os.remove(path + file)
    else:
        await bot.upload_group_file(
            group_id=group_id, folder=folder_id, file=path + name, name=name
        )


# asyncio.get_event_loop().run_until_complete(download_gocq_lasted())
