# Scrapy settings for nepse project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

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
CONCURRENT_ITEMS = 5
CONCURRENT_REQUESTS = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 5
# -------------------------------------------------------------------------------------


# Selenium Config:
# -------------------------------------------------------------------------------------
# DOWNLOADER_MIDDLEWARES = {
#       'nepse.middlewares.selenium_middleware.SeleniumMiddleware': 543,
#       'nepse.middlewares.retry_middleware.Retry404Middleware': 540,
# }

# SELENIUM_MAX_SESSIONS = 10
# SELENIUM_HEADLESS = True

# -------------------------------------------------------------------------------------

# Random User Agent: https://pypi.org/project/scrapy-user-agents/
# Rotating Proxy: https://github.com/TeamHG-Memex/scrapy-rotating-proxies
# scrapy-proxies: https://github.com/aivarsk/scrapy-proxies
# -------------------------------------------------------------------------------------

# 
DOWNLOADER_MIDDLEWARES = {
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    'nepse.middlewares.retry.CustomRetryOnExceptionMiddleware': 555,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,    
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

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

import os
PROXY_LIST = os.path.join(os.getcwd() + '/proxy_list.txt')

# Proxy mode
# 0 = Every requests have different proxy
# 1 = Take only one proxy from the list and assign it to every requests
# 2 = Put a custom proxy to use in the settings
PROXY_MODE = 0
# -------------------------------------------------------------------------------------



# Playwright Config
# -------------------------------------------------------------------------------------

# Custom Download Handler at: nepse.downloaders.playwright.<>
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

PLAYWRIGHT_BROWSER_TYPE = "chromium"

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# 
PLAYWRIGHT_CONTEXTS = {
    "default": {
        
    }
}
# -------------------------------------------------------------------------------------

STATS_DUMP = True


# How long should request be waited by scrapy request response cycle
DOWNLOAD_TIMEOUT = 10


# Retry Timeouts
# -------------------------------------------------------------------------------------

RETRY_ENABLED = True
RETRY_TIMES = 10

# Optional: Backoff between retries
# Retry Time Backoff => RETRY_BACKOFF_BASE * (num_of_retry - 1 ) + random
RETRY_BACKOFF_BASE = 10  # exponential backoff base
RETRY_BACKOFF_MAX = 30  # if retry queue time > 30, keep it
# -------------------------------------------------------------------------------------


# Throtling
# -------------------------------------------------------------------------------------

# Enable disable throtling
AUTOTHROTTLE_ENABLED = True

# The initial download delay
AUTOTHROTTLE_START_DELAY = 5

# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60

# The average number of requests Scrapy should be sending in parallel to
# each remote server: affected by concurrency limit
AUTOTHROTTLE_TARGET_CONCURRENCY = 50.0

# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# -------------------------------------------------------------------------------------

