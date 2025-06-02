from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

class SeleniumMiddleware:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # enable if running headless
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def process_request(self, request, spider):
        self.driver.get(request.url)

        # Wait for a specific element or condition to confirm the page is fully loaded
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "nepseticker"))
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
