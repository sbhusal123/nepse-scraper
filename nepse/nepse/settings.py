# Scrapy settings for nepse project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from dotenv import load_dotenv
import os

load_dotenv()

JS_ENGINE = os.environ.get('JS_ENGINE', 'selenium')
HEADLESS = int(os.environ.get('HEADLESS', '0')) == 1

HUB_URL = os.environ.get('HUB_URL', 'http://localhost:4444/wd/hub')

BROWSER = os.environ.get('BROWSER', 'chrome')

MAX_BROWSER_SESSIONS = int(os.environ.get('MAX_BROWSER_SESSIONS', 5))

USE_PROXY = int(os.environ.get('USE_PROXY', '0')) == 1
ROTATE_USER_AGENT = int(os.environ.get('ROTATE_USER_AGENT', '0')) == 1

IS_SELENIUM = JS_ENGINE == 'selenium'
IS_PLAYWRIGHT = JS_ENGINE == 'playwright'
IS_SELENIUM_HUB = JS_ENGINE == 'selenium-hub'

BOT_NAME = "nepse"

SPIDER_MODULES = ["nepse.spiders"]
NEWSPIDER_MODULE = "nepse.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "nepse (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "nepse.middlewares.NepseSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "nepse.middlewares.NepseDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "nepse.pipelines.NepsePipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"


# Concurrency
# -------------------------------------------------------------------------------------
CONCURRENT_ITEMS = int(os.environ.get('CONCURRENT_ITEMS', 50))
CONCURRENT_REQUESTS = int(os.environ.get('CONCURRENT_REQUESTS', 20))
CONCURRENT_REQUESTS_PER_DOMAIN = int(os.environ.get('RETRY_TIMESCONCURRENT_REQUESTS_PER_DOMAIN', 5))
# -------------------------------------------------------------------------------------


# Selenium Config:
# -------------------------------------------------------------------------------------
# DOWNLOADER_MIDDLEWARES = {
#       'nepse.middlewares.selenium_middleware.SeleniumMiddleware': 543,
#       'nepse.middlewares.retry_middleware.Retry404Middleware': 540,
# }
SELENIUM_HEADLESS = HEADLESS

# -------------------------------------------------------------------------------------

# 

# Random User Agent: https://pypi.org/project/scrapy-user-agents/
# scrapy-proxies: https://github.com/aivarsk/scrapy-proxies
# -------------------------------------------------------------------------------------


DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,

    # Download Error Exception
    'nepse.middlewares.retry.CustomRetryOnExceptionMiddleware': 555,
}

if IS_SELENIUM_HUB:
    DOWNLOADER_MIDDLEWARES.update({
      'nepse.middlewares.selenium.SeleniumHubMiddleware': 543
    })

if IS_SELENIUM:
    DOWNLOADER_MIDDLEWARES.update({
      'nepse.middlewares.selenium.SeleniumStandaloneMiddleware': 543
    })    

if USE_PROXY:
    DOWNLOADER_MIDDLEWARES.update({
        'scrapy_proxies.RandomProxy': 100,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
        'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    })

if ROTATE_USER_AGENT:
    DOWNLOADER_MIDDLEWARES.update({
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    })

# -------------------------------------------------------------------------------------


# Retry failing req with proxy
# -------------------------------------------------------------------------------------
# Retry many times since proxies often fail
# RETRY_TIMES = 10
# Retry on most error codes since proxies fail for different reasons
# RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
# ...

PROXY_LIST = os.path.join(os.getcwd() + '/proxy_list.txt')
if not os.path.exists(PROXY_LIST):
    with open(PROXY_LIST, 'w') as f:
        pass

# Proxy mode
# 0 = Every requests have different proxy
# 1 = Take only one proxy from the list and assign it to every requests
# 2 = Put a custom proxy to use in the settings
PROXY_MODE = 0
# -------------------------------------------------------------------------------------



# Playwright Config
# -------------------------------------------------------------------------------------

# Custom Download Handler at: nepse.downloaders.playwright.<>

if IS_PLAYWRIGHT:
    DOWNLOADER_MIDDLEWARES.update({
        'nepse.middlewares.playwright.PlaywrightAutoMiddleware': 543
    })
    DOWNLOAD_HANDLERS = {
        "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    }

    PLAYWRIGHT_BROWSER_TYPE = "chromium"

    PLAYWRIGHT_LAUNCH_OPTIONS = {
        "headless": HEADLESS
    }

    # Add playwright context here
    PLAYWRIGHT_CONTEXTS = {
        "default": {
            
        }
    }    

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# -------------------------------------------------------------------------------------

STATS_DUMP = True


# How long should request be waited by scrapy request response cycle
DOWNLOAD_TIMEOUT = int(os.environ.get('DOWNLOAD_TIMEOUT', 10))


# Retry Timeouts
# -------------------------------------------------------------------------------------

RETRY_ENABLED = int(os.environ.get('RETRY_ENABLED', 1)) == 1
RETRY_TIMES = int(os.environ.get('RETRY_TIMES', 10))

RETRY_BACKOFF_BASE = int(os.environ.get('RETRY_BACKOFF_BASE', 5))
RETRY_BACKOFF_MAX = int(os.environ.get('RETRY_BACKOFF_MAX', 60))
# -------------------------------------------------------------------------------------


# Throtling
# -------------------------------------------------------------------------------------

# Enable disable throtling
AUTOTHROTTLE_ENABLED = int(os.environ.get('AUTOTHROTTLE_ENABLED', '1')) == 1

# The initial download delay
AUTOTHROTTLE_START_DELAY = 2

# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = int(os.environ.get('AUTOTHROTTLE_MAX_DELAY', '60'))

# The average number of requests Scrapy should be sending in parallel to
# each remote server: affected by concurrency limit
AUTOTHROTTLE_TARGET_CONCURRENCY = float(os.environ.get('AUTOTHROTTLE_TARGET_CONCURRENCY', '10'))
# -------------------------------------------------------------------------------------

