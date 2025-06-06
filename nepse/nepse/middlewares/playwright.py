# middlewares.py

from scrapy import signals
from scrapy_playwright.page import PageMethod

class PlaywrightAutoMiddleware:

    def __init__(self, settings):
        self.use_playwright = settings.get('IS_PLAYWRIGHT')

    @classmethod
    def from_crawler(cls, crawler):
        # You can access crawler.settings here if needed
        return cls(crawler.settings)

    def process_request(self, request, spider):
        request.meta["playwright"] = True

        selector = request.meta.get("wait_for")
        if selector:
            page_methods = request.meta.setdefault("playwright_page_methods", [])
            page_methods.append(PageMethod("wait_for", selector, timeout=10000))
        return None
