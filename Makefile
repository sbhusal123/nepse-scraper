start_hub:
	cd selenium_hub && make run
stop_hub:
	cd selenium_hub && make destroy
forward_port:
	cd selenium_hub && make forward_port
run_spider:
	cd nepse && scrapy crawl stockprice -o $(FILE)
