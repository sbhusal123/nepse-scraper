# middlewares.py

from scrapy_playwright.page import PageMethod

class PlaywrightAutoMiddleware:

    def __init__(self, settings):
        self.use_playwright = settings.getbool('IS_PLAYWRIGHT', False)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if not self.use_playwright:
            return None

        wait_for = request.meta.get("wait_for")
        playwright_page_methods = []

        if wait_for:
            if isinstance(wait_for, str):
                selectors = [s.strip() for s in wait_for.split(',')]
            elif isinstance(wait_for, list):
                selectors = wait_for
            else:
                selectors = []

            for selector in selectors:
                playwright_page_methods.append(
                    PageMethod("wait_for_selector", selector, timeout=10000)
                )

        request.meta['playwright'] = True
        request.meta['playwright_page_methods'] = playwright_page_methods

        return None
