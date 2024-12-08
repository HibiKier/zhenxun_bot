from playwright.async_api import Error as PlaywrightError
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


class NotFoundError(Exception):
    """
    未发现
    """

    pass


class GroupInfoNotFound(Exception):
    """
    群组未找到
    """

    pass


class EmptyError(Exception):
    """
    空错误
    """

    pass


class UserAndGroupIsNone(Exception):
    """
    用户和群组为空
    """

    pass


class InsufficientGold(Exception):
    """
    金币不足
    """

    pass


class NotFindSuperuser(Exception):
    """
    未找到超级用户
    """

    pass


class GoodsNotFound(Exception):
    """
    或找到道具
    """

    pass


class PlaywrightRenderError(Exception):
    """Playwright 渲染基础异常类"""

    pass


class TemplateRenderError(PlaywrightRenderError):
    """模板渲染异常

    Attributes:
        message: 异常信息
        template_path: 模板路径
        template_name: 模板名称
        error: PlaywrightError | PlaywrightTimeoutError
        context: 额外上下文信息
    """

    def __init__(
        self,
        message: str,
        *,
        template_path: str,
        template_name: str,
        error: PlaywrightError | PlaywrightTimeoutError,
        context: dict | None = None,
    ):
        self.template_path = template_path
        self.template_name = template_name
        self.original_error = error
        self.context = context or {}
        message = (
            f"Failed to render template '{template_name}' at '{template_path}'\n"
            f"Original error: {error!s}\n"
            f"Context: {context}"
        )
        super().__init__(message)
