# Nepse Crawler

Crawls [nepalstock](https://nepalstock.com/)

**Tools:**
- Scrapy
- Setup With: Playwright / Selenium Grid / Selenium Standalone


## Selenium Hub Setup:

[Kubernetes Setup](./selenium_hub/README.md)

- 

**Commands:**
- Start Hub: ``make start_hub``
- Stop / Destroy Hub: ``make stop_hub``
- Forward Port To Host: ``make forward_port`` exposes hub connect port.

# Other setup:

- Download selenium webdriver if using selenium.

**Playwright**
```
playwright install chrome
```


## Crawler Setup:

**Python Environment Setup:**
- Python Version: ``3.12.3``
- Setup virtual env: ``python3 -m venv env``
- Install packages: ``pip install -r requirements.txt``

