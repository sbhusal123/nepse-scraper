import time
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from scrapy.exceptions import IgnoreRequest
import logging


# TODO: retry by rotating user agent and proxy

class Retry404Middleware(RetryMiddleware):
    def __init__(self, settings):
        super().__init__(settings)
        self.retry_http_codes = set(settings.getlist('RETRY_HTTP_CODES'))
        self.retry_http_codes.add(404)
        self.delay_on_404 = settings.getfloat('RETRY_404_DELAY', 10)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        if response.status == 404 and request.meta.get('dont_retry') is not True:
            spider.logger.warning(f"Got 404. Retrying {request.url} after {self.delay_on_404}s delay...")
            time.sleep(self.delay_on_404)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response

        return super().process_response(request, response, spider)