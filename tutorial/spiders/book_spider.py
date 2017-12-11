import scrapy
from tutorial.items import TutorialItem


class BookSpider(scrapy.spiders.Spider):
    name = "book"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://dmoztools.net/Computers/Programming/Languages/Python/Books/",
        "http://dmoztools.net/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        for sel in response.css("#site-list-content div.site-item div.title-and-desc"):
            item = TutorialItem()
            item['name'] = sel.css("div.site-title::text").extract()
            item['link'] = sel.css('a::attr(href)').extract()
            item['desc'] = sel.css('div.site-descr::text').extract()

            yield item
