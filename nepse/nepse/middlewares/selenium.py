import threading
from queue import Queue
from selenium import webdriver

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from .mixins import SeleniumRequestMixins

import threading


class SeleniumHubMiddleware(SeleniumRequestMixins):

    def __init__(self, settings):
        self.max_sessions = settings.getint('MAX_BROWSER_SESSIONS')
        self.headless = settings.getbool('HEADLESS')
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

            return webdriver.Remote(
                command_executor=self.selenium_url,
                options=options
            )

        elif self.browser == 'chrome':
            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            return webdriver.Remote(
                command_executor=self.selenium_url,
                options=options
            )
        else:
            raise ValueError(f"Unsupported browser: {self.browser}")


class SeleniumStandaloneMiddleware(SeleniumRequestMixins):

    def __init__(self, settings):

        self.max_sessions = settings.getint('MAX_BROWSER_SESSIONS')
        self.headless = settings.getint('HEADLESS')
        self.browser = settings.get('BROWSER')

        self.driver_pool = Queue(self.max_sessions)
        self.lock = threading.Lock()

        print("[SeleniumStandaloneMiddleware] Initializing with", self.max_sessions, "local sessions")

        for _ in range(self.max_sessions):
            driver = self._create_driver()
            self.driver_pool.put(driver)


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
