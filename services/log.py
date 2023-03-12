from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from loguru import logger as logger_
from nonebot.log import default_filter, default_format

from configs.path_config import LOG_PATH

logger_.add(
    LOG_PATH / f"{datetime.now().date()}.log",
    level="INFO",
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

    TEMPLATE_A = "{}"
    TEMPLATE_B = "[<u><c>{}</c></u>]: {}"
    TEMPLATE_C = "用户[<u><e>{}</e></u>] 触发 [<u><c>{}</c></u>]: {}"
    TEMPLATE_D = "群聊[<u><e>{}</e></u>] 用户[<u><e>{}</e></u>] 触发 [<u><c>{}</c></u>]: {}"
    TEMPLATE_E = "群聊[<u><e>{}</e></u>] 用户[<u><e>{}</e></u>] 触发 [<u><c>{}</c></u>] [Target](<u><e>{}</e></u>): {}"

    TEMPLATE_USER = "用户[<u><e>{}</e></u>] "
    TEMPLATE_GROUP = "群聊[<u><e>{}</e></u>] "
    TEMPLATE_COMMAND = "CMD[<u><c>{}</c></u>] "
    TEMPLATE_TARGET = "[Target]([<u><e>{}</e></u>]) "

    SUCCESS_TEMPLATE = "[<u><c>{}</c></u>]: {} | 参数[{}] 返回: [<y>{}</y>]"

    WARNING_TEMPLATE = "[<u><y>{}</y></u>]: {}"

    ERROR_TEMPLATE = "[<u><r>{}</r></u>]: {}"

    @classmethod
    def info(
        cls,
        info: str,
        command: Optional[str] = None,
        user_id: Optional[Union[int, str]] = None,
        group_id: Optional[Union[int, str]] = None,
        target: Optional[Any] = None,
    ):
        template = cls.__parser_template(info, command, user_id, group_id, target)
        logger_.opt(colors=True).info(template)

    @classmethod
    def success(
        cls,
        info: str,
        command: str,
        param: Optional[Dict[str, Any]] = None,
        result: Optional[str] = "",
    ):
        param_str = ""
        if param:
            param_str = ",".join([f"<m>{k}</m>:<g>{v}</g>" for k, v in param.items()])
        logger_.opt(colors=True).success(
            cls.SUCCESS_TEMPLATE.format(command, info, param_str, result)
        )

    @classmethod
    def warning(
        cls,
        info: str,
        command: Optional[str] = None,
        user_id: Optional[Union[int, str]] = None,
        group_id: Optional[Union[int, str]] = None,
        target: Optional[Any] = None,
        e: Optional[Exception] = None,
    ):
        template = cls.__parser_template(info, command, user_id, group_id, target)
        if e:
            template += f" || 错误<r>{type(e)}: {e}</r>"
        logger_.opt(colors=True).warning(template)

    @classmethod
    def error(
        cls,
        info: str,
        command: Optional[str] = None,
        user_id: Optional[Union[int, str]] = None,
        group_id: Optional[Union[int, str]] = None,
        target: Optional[Any] = None,
        e: Optional[Exception] = None,
    ):
        template = cls.__parser_template(info, command, user_id, group_id, target)
        if e:
            template += f" || 错误 <r>{type(e)}: {e}</r>"
        logger_.opt(colors=True).error(template)

    @classmethod
    def debug(
        cls,
        info: str,
        command: Optional[str] = None,
        user_id: Optional[Union[int, str]] = None,
        group_id: Optional[Union[int, str]] = None,
        target: Optional[Any] = None,
        e: Optional[Exception] = None,
    ):
        template = cls.__parser_template(info, command, user_id, group_id, target)
        if e:
            template += f" || 错误 <r>{type(e)}: {e}</r>"
        logger_.opt(colors=True).debug(template)

    @classmethod
    def __parser_template(
        cls,
        info: str,
        command: Optional[str] = None,
        user_id: Optional[Union[int, str]] = None,
        group_id: Optional[Union[int, str]] = None,
        target: Optional[Any] = None,
    ) -> str:
        arg_list = []
        template = ""
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
