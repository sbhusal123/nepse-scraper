from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait

class SeleniumRequestMixins:

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
                    lambda d: len(d.find_elements(By.CSS_SELECTOR, wait_for)) > 0
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
