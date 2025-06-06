# Nepse Crawler

Crawls [nepalstock](https://nepalstock.com/)

**Tools:**
- Scrapy
- Setup With: Playwright / Selenium Grid / Selenium Standalone


# Setup

- Any one setup can be ran.

### Selenium Hub Setup:

[Kubernetes Setup](./selenium_hub/README.md)

> Uses chrome nodes with single hub



**Commands:**
- Start Hub: ``make start_hub``
- Stop / Destroy Hub: ``make stop_hub``
- Forward Port To Host: ``make forward_port`` exposes hub connect port.

### Standalone Selenium / Playwright Setup

**Selenium Standalone**
- Download selenium webdriver if using selenium.

**Playwright**
- Install playwright corresponding browser
```
playwright install chrome / firefox
```

## Setup

**Python Environment Setup:**
- Python Version: ``3.12.3``
- Setup virtual env: ``python3 -m venv env``
- Install packages: ``pip install -r requirements.txt``

## Environment Variables:


> **.env.example**

Create .env following the instructions in the comment.

```sh
# # Note that all values are string


# # Common Settings:
# # ------------------------------------------------------------------------------------

# # use selenium or playwright
# selenium / selenium-hub / playwright
# # Default: selenium
JS_ENGINE="selenium"

# # Concurrent sessions for seleniumgrid
# # For parallel usage of nodes accross grid
# # Depends on kubernetes config.
# # Default to 5
MAX_BROWSER_SESSIONS=10

# Which Browser to use
# chrome / firefox
BROWSER="chrome"


# # Headless
# # Default: 0
HEADLESS="0"

# Grid Hub URL
HUB_URL="http://localhost:4444/wd/hub"



# # Do you want to use proxy ?
# # Default: 0
USE_PROXY="1"

# # Want to rotate user agent:
# # Default: 0
ROTATE_USER_AGENT="1"

# # ------------------------------------------------------------------------------------


# # Retries:
# # ------------------------------------------------------------------------------------

# # Seconds to wait => RETRY_BACKOFF_BASE * (retry_times - 1) + random

# # enable retry
# # Default: 1
RETRY_ENABLED="1"

# # how many times to retry
# # Default: 10
RETRY_TIMES="10"

# # Backoff between retries
# # Default: 5
RETRY_BACKOFF_BASE="10"

# # Max seconds to wait to dispatch retry request
# # Default: 60
RETRY_BACKOFF_MAX="50"

# # Max no of time in sec for request time out
# # Default: 10
DOWNLOAD_TIMEOUT="5"
# # ------------------------------------------------------------------------------------

# # Throtling
# # ------------------------------------------------------------------------------------

# # Enabled by Default
# # Default: 1
AUTOTHROTTLE_ENABLED=1

# # The maximum download delay to be set in case of high latencies
# # Defaults to 60
AUTOTHROTTLE_MAX_DELAY=20


# # No of concurrent retry to retry for throtled resources
# # Default => 10
AUTOTHROTTLE_TARGET_CONCURRENCY=10
# # ------------------------------------------------------------------------------------


# # Concurrency
# # ------------------------------------------------------------------------------------
# # No of concurrent items to fetch
# # Default: 50
CONCURRENT_ITEMS=50

# # No of concurrent requests
# # Default: 20
CONCURRENT_REQUESTS=50

# # No of requets per domain
# # Default: 5
CONCURRENT_REQUESTS_PER_DOMAIN=20
# # ------------------------------------------------------------------------------------

```

## Runing Spider:
- ``make run_spider``
- ``remove_cache``
