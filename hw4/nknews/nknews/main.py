from scrapy import cmdline
cmdline.execute("scrapy crawl news -o news2.json -s FEED_EXPORT_ENCODING=UTF-8".split())