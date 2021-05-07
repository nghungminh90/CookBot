from scrapy import cmdline
cmdline.execute("scrapy crawl cookpad --set FEED_EXPORT_ENCODING=utf-8 --output=cookpad.json".split());