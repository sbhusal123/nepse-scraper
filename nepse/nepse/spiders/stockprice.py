import scrapy
from scrapy.shell import inspect_response

from bs4 import BeautifulSoup

from nepse.utils import fetch_and_save_https_proxies

class StockpriceSpider(scrapy.Spider):
    name = "stockprice"
    allowed_domains = ["nepalstock.com"]
    start_urls = ["https://nepalstock.com/"]

    def start_requests(self):
        # fetch_and_save_https_proxies() 
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            dont_filter=True,
            meta={
                "wait_for": "ul#nepseticker"
            }
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
                dont_filter=True,
                meta={
                    "wait_for": "html body app-root div main.main div.container app-company-details main.main div.container div.row div.col-lg-4.mb-3.mb-lg-0 div.box, h1"
                }                
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
