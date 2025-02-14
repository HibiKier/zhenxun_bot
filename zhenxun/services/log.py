from datetime import datetime, timedelta
from typing import Any, overload

import nonebot
from nonebot import require

require("nonebot_plugin_session")
from loguru import logger as logger_
from nonebot.log import default_filter, default_format
from nonebot_plugin_session import Session
from nonebot_plugin_uninfo import Session as uninfoSession

from zhenxun.configs.path_config import LOG_PATH

driver = nonebot.get_driver()

log_level = driver.config.log_level or "INFO"

logger_.add(
    LOG_PATH / f"{datetime.now().date()}.log",
    level=log_level,
    rotation="00:00",
    format=default_format,
    filter=default_filter,
    retention=timedelta(days=30),
)

logger_.add(
    LOG_PATH / f"error_{datetime.now().date()}.log",
    level="ERROR",
    rotation="00:00",
    format=default_format,
    filter=default_filter,
    retention=timedelta(days=30),
)


class logger:
    TEMPLATE_A = "Adapter[{}] {}"
    TEMPLATE_B = "Adapter[{}] [<u><c>{}</c></u>]: {}"
    TEMPLATE_C = "Adapter[{}] 用户[<u><e>{}</e></u>] 触发 [<u><c>{}</c></u>]: {}"
    TEMPLATE_D = "Adapter[{}] 群聊[<u><e>{}</e></u>] 用户[<u><e>{}</e></u>] 触发"
    " [<u><c>{}</c></u>]: {}"
    TEMPLATE_E = "Adapter[{}] 群聊[<u><e>{}</e></u>] 用户[<u><e>{}</e></u>] 触发"
    " [<u><c>{}</c></u>] [Target](<u><e>{}</e></u>): {}"

    TEMPLATE_ADAPTER = "Adapter[<m>{}</m>] "
    TEMPLATE_USER = "用户[<u><e>{}</e></u>] "
    TEMPLATE_GROUP = "群聊[<u><e>{}</e></u>] "
    TEMPLATE_COMMAND = "CMD[<u><c>{}</c></u>] "
    TEMPLATE_PLATFORM = "平台[<u><m>{}</m></u>] "
    TEMPLATE_TARGET = "[Target]([<u><e>{}</e></u>]) "

    SUCCESS_TEMPLATE = "[<u><c>{}</c></u>]: {} | 参数[{}] 返回: [<y>{}</y>]"

    WARNING_TEMPLATE = "[<u><y>{}</y></u>]: {}"

    ERROR_TEMPLATE = "[<u><r>{}</r></u>]: {}"

    @overload
    @classmethod
    def info(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: int | str | None = None,
        group_id: int | str | None = None,
        adapter: str | None = None,
        target: Any = None,
        platform: str | None = None,
    ): ...

    @overload
    @classmethod
    def info(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: Session | None = None,
        target: Any = None,
        platform: str | None = None,
    ): ...

    @overload
    @classmethod
    def info(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: uninfoSession | None = None,
        target: Any = None,
        platform: str | None = None,
    ): ...

    @classmethod
    def info(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: int | str | Session | uninfoSession | None = None,
        group_id: int | str | None = None,
        adapter: str | None = None,
        target: Any = None,
        platform: str | None = None,
    ):
        user_id: str | None = session  # type: ignore
        if isinstance(session, Session):
            user_id = session.id1
            adapter = session.bot_type
            if session.id3:
                group_id = f"{session.id3}:{session.id2}"
            elif session.id2:
                group_id = f"{session.id2}"
            platform = platform or session.platform
        elif isinstance(session, uninfoSession):
            user_id = session.user.id
            adapter = session.adapter
            if session.group:
                group_id = session.group.id
            platform = session.basic["scope"]
        template = cls.__parser_template(
            info, command, user_id, group_id, adapter, target, platform
        )
        try:
            logger_.opt(colors=True).info(template)
        except Exception:
            logger_.info(template)

    @classmethod
    def success(
        cls,
        info: str,
        command: str,
        param: dict[str, Any] | None = None,
        result: str = "",
    ):
        param_str = ""
        if param:
            param_str = ",".join([f"<m>{k}</m>:<g>{v}</g>" for k, v in param.items()])
        logger_.opt(colors=True).success(
            cls.SUCCESS_TEMPLATE.format(command, info, param_str, result)
        )

    @overload
    @classmethod
    def warning(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: int | str | None = None,
        group_id: int | str | None = None,
        adapter: str | None = None,
        target: Any = None,
        platform: str | None = None,
        e: Exception | None = None,
    ): ...

    @overload
    @classmethod
    def warning(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: Session | None = None,
        adapter: str | None = None,
        target: Any = None,
        platform: str | None = None,
        e: Exception | None = None,
    ): ...

    @overload
    @classmethod
    def warning(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: uninfoSession | None = None,
        adapter: str | None = None,
        target: Any = None,
        platform: str | None = None,
        e: Exception | None = None,
    ): ...

    @classmethod
    def warning(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: int | str | Session | uninfoSession | None = None,
        group_id: int | str | None = None,
        adapter: str | None = None,
        target: Any = None,
        platform: str | None = None,
        e: Exception | None = None,
    ):
        user_id: str | None = session  # type: ignore
        if isinstance(session, Session):
            user_id = session.id1
            adapter = session.bot_type
            if session.id3:
                group_id = f"{session.id3}:{session.id2}"
            elif session.id2:
                group_id = f"{session.id2}"
            platform = platform or session.platform
        elif isinstance(session, uninfoSession):
            user_id = session.user.id
            adapter = session.adapter
            if session.group:
                group_id = session.group.id
            platform = session.basic["scope"]
        template = cls.__parser_template(
            info, command, user_id, group_id, adapter, target, platform
        )
        if e:
            template += f" || 错误<r>{type(e)}: {e}</r>"
        try:
            logger_.opt(colors=True).warning(template)
        except Exception as e:
            logger_.warning(template)

    @overload
    @classmethod
    def error(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: int | str | None = None,
        group_id: int | str | None = None,
        adapter: str | None = None,
        target: Any = None,
        platform: str | None = None,
        e: Exception | None = None,
    ): ...

    @overload
    @classmethod
    def error(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: Session | None = None,
        target: Any = None,
        platform: str | None = None,
        e: Exception | None = None,
    ): ...

    @overload
    @classmethod
    def error(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: uninfoSession | None = None,
        target: Any = None,
        platform: str | None = None,
        e: Exception | None = None,
    ): ...

    @classmethod
    def error(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: int | str | Session | uninfoSession | None = None,
        group_id: int | str | None = None,
        adapter: str | None = None,
        target: Any = None,
        platform: str | None = None,
        e: Exception | None = None,
    ):
        user_id: str | None = session  # type: ignore
        if isinstance(session, Session):
            user_id = session.id1
            adapter = session.bot_type
            if session.id3:
                group_id = f"{session.id3}:{session.id2}"
            elif session.id2:
                group_id = f"{session.id2}"
            platform = platform or session.platform
        elif isinstance(session, uninfoSession):
            user_id = session.user.id
            adapter = session.adapter
            if session.group:
                group_id = session.group.id
            platform = session.basic["scope"]
        template = cls.__parser_template(
            info, command, user_id, group_id, adapter, target, platform
        )
        if e:
            template += f" || 错误 <r>{type(e)}: {e}</r>"
        try:
            logger_.opt(colors=True).error(template)
        except Exception as e:
            logger_.error(template)

    @overload
    @classmethod
    def debug(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: int | str | None = None,
        group_id: int | str | None = None,
        adapter: str | None = None,
        target: Any = None,
        platform: str | None = None,
        e: Exception | None = None,
    ): ...

    @overload
    @classmethod
    def debug(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: Session | None = None,
        target: Any = None,
        platform: str | None = None,
        e: Exception | None = None,
    ): ...

    @overload
    @classmethod
    def debug(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: uninfoSession | None = None,
        target: Any = None,
        platform: str | None = None,
        e: Exception | None = None,
    ): ...

    @classmethod
    def debug(
        cls,
        info: str,
        command: str | None = None,
        *,
        session: int | str | Session | uninfoSession | None = None,
        group_id: int | str | None = None,
        adapter: str | None = None,
        target: Any = None,
        platform: str | None = None,
        e: Exception | None = None,
    ):
        user_id: str | None = session  # type: ignore
        if isinstance(session, Session):
            user_id = session.id1
            adapter = session.bot_type
            if session.id3:
                group_id = f"{session.id3}:{session.id2}"
            elif session.id2:
                group_id = f"{session.id2}"
            platform = platform or session.platform
        elif isinstance(session, uninfoSession):
            user_id = session.user.id
            adapter = session.adapter
            if session.group:
                group_id = session.group.id
            platform = session.basic["scope"]
        template = cls.__parser_template(
            info, command, user_id, group_id, adapter, target, platform
        )
        if e:
            template += f" || 错误 <r>{type(e)}: {e}</r>"
        try:
            logger_.opt(colors=True).debug(template)
        except Exception as e:
            logger_.debug(template)

    @classmethod
    def __parser_template(
        cls,
        info: str,
        command: str | None = None,
        user_id: int | str | None = None,
        group_id: int | str | None = None,
        adapter: str | None = None,
        target: Any = None,
        platform: str | None = None,
    ) -> str:
        arg_list = []
        template = ""
        if adapter is not None:
            template += cls.TEMPLATE_ADAPTER
            arg_list.append(adapter)
        if platform is not None:
            template += cls.TEMPLATE_PLATFORM
            arg_list.append(platform)
        if group_id is not None:
            template += cls.TEMPLATE_GROUP
            arg_list.append(group_id)
        if user_id is not None:
            template += cls.TEMPLATE_USER
            arg_list.append(user_id)
        if command is not None:
            template += cls.TEMPLATE_COMMAND
            arg_list.append(command)
        if target is not None:
            template += cls.TEMPLATE_TARGET
            arg_list.append(target)
        arg_list.append(info)
        template += "{}"
        return template.format(*arg_list)
