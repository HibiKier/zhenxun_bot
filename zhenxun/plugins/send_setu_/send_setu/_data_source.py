import os
import random
from pathlib import Path

from asyncpg import UniqueViolationError
from nonebot_plugin_alconna import UniMessage

from zhenxun.configs.config import BotConfig, Config
from zhenxun.configs.path_config import IMAGE_PATH, TEMP_PATH
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.image_utils import compressed_image
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.utils import change_img_md5, change_pixiv_image_links

from .._model import Setu

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6;"
    " rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Referer": "https://www.pixiv.net",
}

base_config = Config.get("send_setu")


class SetuManage:

    URL = "https://api.lolicon.app/setu/v2"
    save_data = []

    @classmethod
    async def get_setu(
        cls,
        *,
        local_id: int | None = None,
        num: int = 10,
        tags: list[str] | None = None,
        is_r18: bool = False,
    ) -> list[UniMessage] | str:
        """获取色图

        参数:
            local_id: 指定图片id
            num: 数量
            tags: 标签
            is_r18: 是否r18

        返回:
            list[MessageFactory] | str: 色图数据列表或消息

        """
        result_list = []
        if local_id:
            """本地id"""
            data_list = await cls.get_setu_list(local_id=local_id)
            if isinstance(data_list, str):
                return data_list
            file = await cls.get_image(data_list[0])
            if isinstance(file, str):
                return file
            return [cls.init_image_message(file, data_list[0])]
        if base_config.get("ONLY_USE_LOCAL_SETU"):
            """仅使用本地色图"""
            flag = False
            data_list = await cls.get_setu_list(tags=tags, is_r18=is_r18)
            if isinstance(data_list, str):
                return data_list
            cls.save_data = data_list
            if num > len(data_list):
                num = len(data_list)
                flag = True
            setu_list = random.sample(data_list, num)
            for setu in setu_list:
                base_path = None
                if setu.is_r18:
                    base_path = IMAGE_PATH / "_r18"
                else:
                    base_path = IMAGE_PATH / "_setu"
                file_path = base_path / f"{setu.local_id}.jpg"
                if not file_path.exists():
                    return f"本地色图Id: {setu.local_id} 不存在..."
                result_list.append(cls.init_image_message(file_path, setu))
            if flag:
                result_list.append(
                    MessageUtils.build_message("坏了，已经没图了，被榨干了！")
                )
            return result_list
        data_list = await cls.search_lolicon(tags, num, is_r18)
        if isinstance(data_list, str):
            """搜索失败, 从本地数据库中搜索"""
            data_list = await cls.get_setu_list(tags=tags, is_r18=is_r18)
            if isinstance(data_list, str):
                return data_list
        if not data_list:
            return "没找到符合条件的色图..."
        cls.save_data = data_list
        flag = False
        if num > len(data_list):
            num = len(data_list)
            flag = True
        for setu in data_list:
            file = await cls.get_image(setu)
            if isinstance(file, str):
                result_list.append(MessageUtils.build_message(file))
                continue
            result_list.append(cls.init_image_message(file, setu))
        if not result_list:
            return "没找到符合条件的色图..."
        if flag:
            result_list.append(
                MessageUtils.build_message("坏了，已经没图了，被榨干了！")
            )
        return result_list

    @classmethod
    def init_image_message(cls, file: Path, setu: Setu) -> UniMessage:
        """初始化图片发送消息

        参数:
            file: 图片路径
            setu: Setu

        返回:
            UniMessage: 发送消息内容
        """
        data_list = []
        if base_config.get("SHOW_INFO"):
            data_list.append(
                f"id：{setu.local_id or ''}\n"
                f"title：{setu.title}\n"
                f"author：{setu.author}\n"
                f"PID：{setu.pid}\n"
            )
        data_list.append(file)
        return MessageUtils.build_message(data_list)

    @classmethod
    async def get_setu_list(
        cls,
        *,
        local_id: int | None = None,
        tags: list[str] | None = None,
        is_r18: bool = False,
    ) -> list[Setu] | str:
        """获取数据库中的色图数据

        参数:
            local_id: 色图本地id.
            tags: 标签.
            is_r18: 是否r18.

        返回:
            list[Setu] | str: 色图数据列表或消息
        """
        image_list: list[Setu] = []
        if local_id:
            image_count = await Setu.filter(is_r18=is_r18).count() - 1
            if local_id < 0 or local_id > image_count:
                return f"超过当前上下限！({image_count})"
            image_list = [await Setu.query_image(local_id, r18=is_r18)]  # type: ignore
        elif tags:
            image_list = await Setu.query_image(tags=tags, r18=is_r18)  # type: ignore
        else:
            image_list = await Setu.query_image(r18=is_r18)  # type: ignore
        if not image_list:
            return "没找到符合条件的色图..."
        return image_list

    @classmethod
    def get_luo(cls, impression: float) -> UniMessage | None:
        """罗翔

        参数:
            impression: 好感度

        返回:
            MessageFactory | None: 返回数据
        """
        if initial_setu_probability := base_config.get("INITIAL_SETU_PROBABILITY"):
            probability = float(impression) + initial_setu_probability * 100
            if probability < random.randint(1, 101):
                return MessageUtils.build_message(
                    [
                        "我为什么要给你发这个？",
                        IMAGE_PATH
                        / "luoxiang"
                        / random.choice(os.listdir(IMAGE_PATH / "luoxiang")),
                        f"\n(快向{BotConfig.self_nickname}签到提升好感度吧！)",
                    ]
                )
        return None

    @classmethod
    async def get_image(cls, setu: Setu) -> str | Path:
        """下载图片

        参数:
            setu: Setu

        返回:
            str | Path: 图片路径或返回消息
        """
        url = change_pixiv_image_links(setu.img_url)
        index = setu.local_id if setu.local_id else random.randint(1, 100000)
        file_name = f"{index}_temp_setu.jpg"
        base_path = TEMP_PATH
        if setu.local_id:
            """本地图片存在直接返回"""
            file_name = f"{index}.jpg"
            if setu.is_r18:
                base_path = IMAGE_PATH / "_r18"
            else:
                base_path = IMAGE_PATH / "_setu"
            local_file = base_path / file_name
            if local_file.exists():
                return local_file
        file = base_path / file_name
        download_success = False
        for i in range(3):
            logger.debug(f"尝试在线下载第 {i+1} 次", "色图")
            try:
                if await AsyncHttpx.download_file(
                    url,
                    file,
                    timeout=base_config.get("TIMEOUT"),
                ):
                    download_success = True
                    if setu.local_id is not None:
                        if (
                            os.path.getsize(base_path / f"{index}.jpg")
                            > 1024 * 1024 * 1.5
                        ):
                            compressed_image(
                                base_path / f"{index}.jpg",
                            )
                    change_img_md5(file)
                    logger.info(f"下载 lolicon 图片 {url} 成功， id：{index}")
                    break
            except TimeoutError as e:
                logger.error(f"下载图片超时", "色图", e=e)
            except Exception as e:
                logger.error(f"下载图片错误", "色图", e=e)
        return file if download_success else "图片被小怪兽恰掉啦..!QAQ"

    @classmethod
    async def search_lolicon(
        cls, tags: list[str] | None, num: int, is_r18: bool
    ) -> list[Setu] | str:
        """搜索lolicon色图

        参数:
            tags: 标签
            num: 数量
            is_r18: 是否r18

        返回:
            list[Setu] | str: 色图数据或返回消息
        """
        params = {
            "r18": 1 if is_r18 else 0,  # 添加r18参数 0为否，1为是，2为混合
            "tag": tags,  # 若指定tag
            "num": 20,  # 一次返回的结果数量
            "size": ["original"],
        }
        for count in range(3):
            logger.debug(f"尝试获取图片URL第 {count+1} 次", "色图")
            try:
                response = await AsyncHttpx.get(
                    cls.URL, timeout=base_config.get("TIMEOUT"), params=params
                )
                if response.status_code == 200:
                    data = response.json()
                    if not data["error"]:
                        data = data["data"]
                        result_list = cls.__handle_data(data)
                        num = num if num < len(data) else len(data)
                        random_list = random.sample(result_list, num)
                        if not random_list:
                            return "没找到符合条件的色图..."
                        return random_list
                    else:
                        return "没找到符合条件的色图..."
            except TimeoutError as e:
                logger.error(f"获取图片URL超时", "色图", e=e)
            except Exception as e:
                logger.error(f"访问页面错误", "色图", e=e)
        return "我网线被人拔了..QAQ"

    @classmethod
    def __handle_data(cls, data: dict) -> list[Setu]:
        """lolicon数据处理

        参数:
            data: lolicon数据

        返回:
            list[Setu]: 整理的数据
        """
        result_list = []
        for i in range(len(data)):
            img_url = data[i]["urls"]["original"]
            img_url = change_pixiv_image_links(img_url)
            title = data[i]["title"]
            author = data[i]["author"]
            pid = data[i]["pid"]
            tags = []
            for j in range(len(data[i]["tags"])):
                tags.append(data[i]["tags"][j])
            # if command != "色图r":
            #     if "R-18" in tags:
            #         tags.remove("R-18")
            setu = Setu(
                title=title,
                author=author,
                pid=pid,
                img_url=img_url,
                tags=",".join(tags),
                is_r18="R-18" in tags,
            )
            result_list.append(setu)
        return result_list

    @classmethod
    async def save_to_database(cls):
        """存储色图数据到数据库

        参数:
            data_list: 色图数据列表
        """
        set_list = []
        exists_list = []
        for data in cls.save_data:
            if f"{data.pid}:{data.img_url}" not in exists_list:
                exists_list.append(f"{data.pid}:{data.img_url}")
                set_list.append(data)
        if set_list:
            create_list = []
            _cnt = 0
            _r18_cnt = 0
            for setu in set_list:
                try:
                    if not await Setu.exists(pid=setu.pid, img_url=setu.img_url):
                        idx = await Setu.filter(is_r18=setu.is_r18).count()
                        setu.local_id = idx + (_r18_cnt if setu.is_r18 else _cnt)
                        setu.img_hash = ""
                        if setu.is_r18:
                            _r18_cnt += 1
                        else:
                            _cnt += 1
                        create_list.append(setu)
                except UniqueViolationError:
                    pass
            cls.save_data = []
            if create_list:
                try:
                    await Setu.bulk_create(create_list, 10)
                    logger.debug(f"成功保存 {len(create_list)} 条色图数据")
                except Exception as e:
                    logger.error("存储色图数据错误...", e=e)
