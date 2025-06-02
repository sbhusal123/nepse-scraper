# Nepse Crawler

Crawls [nepalstock](https://nepalstock.com/)

**Tools:**
- Scrapy for scraping
- Splash as a js rendering enginee


## Setup:

**Python Environment Setup:**
- Python Version: ``3.12.3``
- Setup virtual env: ``python3 -m venv env``
- Install packages: ``pip install -r requirements.txt``


## Runing Spider:

``cd nepse && scrapy crawl stockprice -o out.json``

This gives: ``out.json`` file inside `/nepse` directory.

