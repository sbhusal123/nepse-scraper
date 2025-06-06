start_hub:
	cd selenium_hub && make run
stop_hub:
	cd selenium_hub && make destroy
forward_port:
	cd selenium_hub && make forward_port
run_spider:
	cd nepse && scrapy crawl stockprice -s LOG_LEVEL=DEBUG -s LOG_FILE=scrapy.log -o out.json
update_proxies:
	cd nepse && python get_proxies.py
remove_caches:
	cd nepse && rm -rf out.json
	cd nepse && rm -rf scrapy.log
