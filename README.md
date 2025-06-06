# Nepse Crawler

Crawls [nepalstock](https://nepalstock.com/)

**Tools:**
- Scrapy for scraping
- Selenium Hub Deployed On Kubernetes Cluster



## Selenium Hub Setup:

[Readme](./selenium_hub/README.md)

**Commands:**
- Start Hub: ``make start_hub``
- Stop / Destroy Hub: ``make stop_hub``
- Forward Port To Host: ``make forward_port`` exposes hub connect port.


## Crawler Setup:

**Python Environment Setup:**
- Python Version: ``3.12.3``
- Setup virtual env: ``python3 -m venv env``
- Install packages: ``pip install -r requirements.txt``


**Runing Spider:**

``cd nepse && scrapy crawl stockprice -o out.json``

This gives: ``out.json`` file inside `/nepse` directory.

**Sample Data:**

```json
{
    "company": "Aarambha Chautari Laghubitta Bittiya Sanstha Limited (ACLBSL)",
    "Instrument Type": "Equity ( EQ )", 
    "Listing Date": "Jan 1, 2019", 
    "Last Traded Price": "1,065.00 -10.19 (-0.95%)",
    "Total Traded Quantity": "806",
    "Total Trades": "24",
    "Previous Day Close Price": "1,075.19",
    "High Price / Low Price": "1,096.60 / 1,064.50", 
    "52 Week High / 52 Week Low": "1,491.00 / 894.10", 
    "Open Price": "1,096.60", 
    "Close Price*": "0", 
    "Total Listed Shares": "3,671,435",
    "Total Paid up Value": "367,143,488.00", 
    "Market Capitalization": "3,947,490,197.65"
},
```

[Sample Data](./nepse/data.data)


**Crawler Selenium Hub COnfiguration:**

[Selenium Middleware](./nepse/nepse/middlewares/selenium_middleware.py)

This middleware sends the request from Scrapy to Selenium and returns a HTML page back.

```python
# .....

class SeleniumMiddleware:
    def __init__(self):
        chrome_options = Options()

        # Uncomment to enable headless
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

        # HUB URL
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

```
