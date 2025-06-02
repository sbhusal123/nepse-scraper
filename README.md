# Nepse Crawler

Crawls [nepalstock](https://nepalstock.com/)

**Tools:**
- Scrapy for scraping
- Selenium for web broswer.




## Setup:

**Python Environment Setup:**
- Python Version: ``3.12.3``
- Setup virtual env: ``python3 -m venv env``
- Install packages: ``pip install -r requirements.txt``


## Runing Spider:

``cd nepse && scrapy crawl stockprice -o out.json``

This gives: ``out.json`` file inside `/nepse` directory.

## Sample Data:

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
