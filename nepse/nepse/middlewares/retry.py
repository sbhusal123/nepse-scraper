from scrapy.downloadermiddlewares.retry import RetryMiddleware
from twisted.internet.error import TimeoutError, TCPTimedOutError, ConnectionRefusedError, ConnectError

from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError
from playwright._impl._errors import Error as PlayWrightError

from scrapy.downloadermiddlewares.retry import get_retry_request

from rotating_proxies.middlewares import RotatingProxyMiddleware


class CustomRetryOnExceptionMiddleware(RetryMiddleware):
    EXCEPTIONS_TO_RETRY = (
        TimeoutError,
        TCPTimedOutError,
        ConnectionRefusedError,
        ConnectError,
        PlaywrightTimeoutError,
        PlayWrightError
    )

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            spider.logger.warning(f"Retrying {request.url} due to exception: {exception}")

            self.priority_adjust = -1
            
            max_retry_times = request.meta.get("max_retry_times", self.max_retry_times)
            return get_retry_request(
                request=request,
                reason=exception,
                spider=spider,
                max_retry_times=max_retry_times,
                priority_adjust=-1,
            )

        return None
