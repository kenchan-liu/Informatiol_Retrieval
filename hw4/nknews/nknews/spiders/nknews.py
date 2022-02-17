import scrapy
import re
import os
from lxml import etree
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nknews.items import NknewsItem
import json
with open('F:\\Scrapy\\nknews\\nknews\\spiders\\urls2.json','r',encoding='utf-8')as fp:
    json_data = json.load(fp)
ret = []
for i in range(701):
    ret+=(json_data[i]['links'])
class NKnews(scrapy.Spider):
    name = 'news'
    start_urls = ret
    def parse(self,response):
        item = NknewsItem()
        sel = scrapy.Selector(response)
        news = sel.xpath("//html/body/div/table[3]")
        t = []
        item['content'] = response.xpath("//p/text()").extract()
        #item['content'] = news.xpath("//tbody/tr/td[1]/table[2]/tbody/tr[3]/text()").extract()
        item['links'] = news.xpath("//a/@href").extract()
        t.append(str(response)[5:-1])
        item['url'] = t
        yield item
        
