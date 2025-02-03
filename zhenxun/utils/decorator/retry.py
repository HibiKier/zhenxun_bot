from httpx import ConnectError, HTTPStatusError, TimeoutException
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed


class Retry:
    @staticmethod
    def api():
        """接口调用重试"""
        return retry(
            reraise=True,
            stop=stop_after_attempt(3),
            wait=wait_fixed(1),
            retry=retry_if_exception_type(
                (TimeoutException, ConnectError, HTTPStatusError)
            ),
        )
