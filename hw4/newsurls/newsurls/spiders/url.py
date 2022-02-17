import scrapy

import re
import os
from lxml import etree

from newsurls.items import urlsItem

#path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class URLnews(scrapy.Spider):
    name = 'links'
    temp = []
    for i in range(1,800):
        temp.append("http://news.nankai.edu.cn/mtnk/system/count//0006000/000000000000/000/000/c0006000000000000000_000000{}.shtml".format(i))
    temp.append("http://news.nankai.edu.cn/ywsd/index.shtml")
    start_urls = temp
    def parse(self,response):
        item = urlsItem()
        sel = scrapy.Selector(response)
        find = response.xpath("/html/body/div/table[3]/tbody/tr/td[1]/table[2]/tbody/tr/td")
        t = find.xpath("//a/@href").extract()
        t = t[11:-6]
        t.remove('http://news.nankai.edu.cn/wx/index.shtml')
        item['links'] = t
        yield item
        
