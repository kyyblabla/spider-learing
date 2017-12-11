# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import BaiduResultItem


class BaiduSpider(scrapy.Spider):
    name = 'ip'
    allowed_domains = ['baidu.com']

    start_urls = ["https://www.baidu.com/s?wd=ip"]

    def parse(self, response):
        info = response.css("div#content_left div.op-ip-detail *::text").extract()
        print(info)