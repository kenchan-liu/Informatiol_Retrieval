from scrapy import cmdline
cmdline.execute("scrapy crawl links -o nurls.json".split())