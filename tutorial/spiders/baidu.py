# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import BaiduResultItem


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']

    def start_requests(self):
        yield scrapy.Request('https://www.baidu.com/s?wd=%s' % self.key)

    def parse(self, response):
        for rs in response.css("#content_left div.result"):
            item = BaiduResultItem()
            item["title"] = "".join(rs.css("h3.t a::text").extract())
            item["desc"] = "".join(rs.css("div.c-abstract::text").extract())
            yield item
