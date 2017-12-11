# -*- coding: utf-8 -*-
import scrapy
import string
from tutorial.items import RpmItem


class LoonginxSpider(scrapy.Spider):
    name = 'loonginx'
    allowed_domains = ['loongnix.org']
    base_url = 'http://ftp.loongnix.org/os/loongnix/1.0/os/Packages/p'

    start_urls = ['http://ftp.loongnix.org/os/loongnix/1.0/os/Packages/p']
    # start_urls = ['http://ftp.loongnix.org/os/loongnix/1.0/os/Packages/0/0xFFFF-0.3.9-11.fc21.loongson.mips64el.rpm']

    ps=""

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'tutorial.middlewares.RpmDownloader': 543,
        }
    }

    # def start_requests(self):
    #     for c in "023469" + string.ascii_lowercase:
    #         yield scrapy.Request(self.base_url + c, callback=self.parse)

    def parse(self, response):
        for a in response.css("table a::attr(href)"):
            href = a.extract()
            if href.endswith("rpm"):
                url = response.url + href.replace("/", "")
                print("get：%s" % url)
                yield scrapy.Request(url)
