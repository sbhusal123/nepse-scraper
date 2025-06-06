import threading
from queue import Queue
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumMiddleware:
    def __init__(self, max_sessions=5, headless=True):
        self.driver_pool = Queue(max_sessions)
        self.lock = threading.Lock()

        # Firefox profile to block assets loading
        profile = FirefoxProfile()

        # Firefox options
        firefox_options = Options()
        if headless:
            firefox_options.add_argument("--headless")
        firefox_options.add_argument("--disable-gpu")

        selenium_url = "http://localhost:4444/wd/hub"

        # Create pool of Firefox Remote WebDrivers
        for _ in range(max_sessions):
            driver = webdriver.Remote(
                command_executor=selenium_url,
                options=firefox_options
            )
            self.driver_pool.put(driver)

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls(
            max_sessions=crawler.settings.getint("SELENIUM_MAX_SESSIONS", 5),
            headless=crawler.settings.getbool("SELENIUM_HEADLESS", True)
        )

        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        if not request.meta.get("use_selenium"):
            return None

        driver = self.driver_pool.get()

        try:
            driver.get(request.url)

            # Wait until page load is complete
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )

            # Optional: wait for JS execution if you know a selector, e.g.
            # WebDriverWait(driver, 10).until(
            #     lambda d: d.find_element_by_css_selector('div.content')
            # )

            body = driver.page_source

            return HtmlResponse(
                url=driver.current_url,
                body=body,
                encoding='utf-8',
                request=request
            )
        finally:
            self.driver_pool.put(driver)

    def spider_closed(self):
        while not self.driver_pool.empty():
            driver = self.driver_pool.get()
            driver.quit()
