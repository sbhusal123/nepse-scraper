from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SeleniumMiddleware:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

        selenium_hub_url = "http://localhost:4444/wd/hub"

        self.driver = webdriver.Remote(
            command_executor=selenium_hub_url,
            options=chrome_options
        )

    def process_request(self, request, spider):
        self.driver.get(request.url)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
        except Exception as e:
            spider.logger.warning(f"Timeout waiting for page to load: {e}")

        body = self.driver.page_source

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )
