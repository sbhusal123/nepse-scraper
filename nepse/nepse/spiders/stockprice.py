import scrapy
from scrapy.shell import inspect_response

from bs4 import BeautifulSoup

from scrapy_playwright.page import PageMethod

from scrapy import signals

from nepse.utils import fetch_and_save_https_proxies

# Note these settings are impacted by : DOWNLOAD_TIMEOUT in settings

async def wait_initial_page(page):
    await page.wait_for_selector("ul#nepseticker > li:last-child", timeout=10000)

async def wait_company_page(page):
    await page.wait_for_selector("h1", timeout=10000)

class StockpriceSpider(scrapy.Spider):
    name = "stockprice"
    allowed_domains = ["nepalstock.com"]
    start_urls = ["https://nepalstock.com/"]

    def start_requests(self):
        fetch_and_save_https_proxies() 
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                        PageMethod(wait_initial_page),
                ],
                 "playwright_context": "default",
            },
            dont_filter=True
        )

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, "lxml")

        ul = soup.find('ul', id="nepseticker")
        label = ul.find('li')

        ul_links = label.find_all('a')

        for item in ul_links:
            link = f'https://nepalstock.com{item.attrs['href']}'
            yield scrapy.Request(
                url=link,
                callback=self.parse_data,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod(wait_company_page),
                    ],
                    "playwright_context": "default",
                },
                dont_filter=True
            )
    
    def parse_data(self, response):
        data = response.body
        soup = BeautifulSoup(data, "lxml")

        # Find the table
        table = soup.find("table", class_="table table-striped")

        # Prepare dictionary to hold extracted data
        data = {}
        data['company'] = soup.find('h1').text
        data["url"] = response.request.url

        for row in table.find_all("tr"):
            th = row.find("th")
            td = row.find("td")

            if th and td:
                key = th.get_text(strip=True)
                
                value = ' '.join(td.stripped_strings)
                
                data[key] = value
        
        yield data

