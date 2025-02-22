from anyio import EndOfStream
from httpx import ConnectError, HTTPStatusError, TimeoutException
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed


class Retry:
    @staticmethod
    def api(
        retry_count: int = 3, wait: int = 1, exception: tuple[type[Exception], ...] = ()
    ):
        """接口调用重试"""
        base_exceptions = (
            TimeoutException,
            ConnectError,
            HTTPStatusError,
            EndOfStream,
            *exception,
        )
        return retry(
            reraise=True,
            stop=stop_after_attempt(retry_count),
            wait=wait_fixed(wait),
            retry=retry_if_exception_type(base_exceptions),
        )
