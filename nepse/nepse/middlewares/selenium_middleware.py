import threading
from queue import Queue
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

import threading

from scrapy import signals
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class SeleniumHubMiddleware:
    def __init__(self, settings):
        self.max_sessions = settings.getint('MAX_BROWSER_SESSIONS')
        self.headless = settings.getint('HEADLESS')
        self.driver_pool = Queue(self.max_sessions)
        self.lock = threading.Lock()

        self.browser = settings.get('BROWSER')
        self.selenium_url = settings.get('HUB_URL')

        mode = "remote Selenium hub" if self.selenium_url else "local standalone"
        print(f"Using {mode} with browser={self.browser} and max_sessions={self.max_sessions}")

        for _ in range(self.max_sessions):
            driver = self._create_driver()
            self.driver_pool.put(driver)

    def _create_driver(self):
        if self.browser == 'firefox':
            options = FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--disable-gpu")

        elif self.browser == 'chrome':
            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        else:
            raise ValueError(f"Unsupported browser: {self.browser}")

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls(crawler.settings)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        driver = self.driver_pool.get()
        try:
            driver.get(request.url)

            wait_for = request.meta.get("wait_for")
            if wait_for:
                WebDriverWait(driver, 10).until(
                    lambda d: d.find_element("css selector", wait_for)
                )

            body = driver.page_source

            return HtmlResponse(
                url=driver.current_url,
                body=body,
                encoding='utf-8',
                request=request
            )
        finally:
            self.driver_pool.put(driver)

    def spider_closed(self, spider):
        while not self.driver_pool.empty():
            driver = self.driver_pool.get()
            driver.quit()

    def process_request(self, request, spider):
        if not request.meta.get("use_selenium"):
            return None

        driver = self.driver_pool.get()
        try:
            driver.get(request.url)

            wait_for = request.meta.get("wait_for")
            if wait_for:
                WebDriverWait(driver, 10).until(
                    lambda d: d.find_element("css selector", wait_for)
                )

            body = driver.page_source

            return HtmlResponse(
                url=driver.current_url,
                body=body,
                encoding='utf-8',
                request=request
            )
        finally:
            self.driver_pool.put(driver)

    def spider_closed(self, spider):
        while not self.driver_pool.empty():
            driver = self.driver_pool.get()
            driver.quit()




class SeleniumStandaloneMiddleware:
    def __init__(self, settings):
        self.max_sessions = settings.getint('MAX_BROWSER_SESSIONS')
        self.headless = settings.getint('HEADLESS')
        self.driver_pool = Queue(self.max_sessions)
        self.lock = threading.Lock()

        self.browser = settings.get('BROWSER')
        self.selenium_url = settings.get('HUB_URL')

        self.driver_pool = Queue(self.max_sessions)
        self.lock = threading.Lock()

        print("[SeleniumStandaloneMiddleware] Initializing with", self.max_sessions, "local sessions")

        for _ in range(self.max_sessions):
            driver = self._create_driver()
            self.driver_pool.put(driver)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        driver = self.driver_pool.get()

        try:
            driver.get(request.url)

            wait_for = request.meta.get("wait_for")
            if wait_for:
                WebDriverWait(driver, 10).until(
                    lambda d: d.find_element("css selector", wait_for)
                )

            body = driver.page_source
            return HtmlResponse(
                url=driver.current_url,
                body=body,
                encoding='utf-8',
                request=request
            )
        finally:
            self.driver_pool.put(driver)

    def spider_closed(self, spider):
        while not self.driver_pool.empty():
            driver = self.driver_pool.get()
            driver.quit()

    def _create_driver(self):
        if self.browser == 'firefox':
            options = FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--disable-gpu")

            return webdriver.Firefox(options=options)

        elif self.browser == 'chrome':
            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            return webdriver.Chrome(options=options)

        else:
            raise ValueError(f"Unsupported browser: {self.browser}")