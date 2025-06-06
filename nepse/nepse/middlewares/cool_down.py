import asyncio
from scrapy import signals

class CooldownAfterRequestsMiddleware:
    def __init__(self):
        self.request_count = 0
        self.cooldown_threshold = 40
        self.cooldown_seconds = 10

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def spider_opened(self, spider):
        self.request_count = 0

    async def process_request(self, request, spider):
        self.request_count += 1

        print("\n\n")

        print("Request Count=>", self.request_count)

        print("\n\n")

        if self.request_count % self.cooldown_threshold == 0:
            spider.logger.info(f"Reached {self.request_count} requests, cooling down for {self.cooldown_seconds} seconds...")
            await asyncio.sleep(self.cooldown_seconds)

        # Continue processing the request immediately
        return None
