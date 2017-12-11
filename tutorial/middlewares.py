# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import scrapy
import requests
import string
import os


class TutorialSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleare(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://127.0.0.1:9743'
        return None


BASE_DOWNLOAD_PATH = "/Users/kyy/data/rpm"


def check_file(url):
    path = BASE_DOWNLOAD_PATH + "/" + ("/".join(url.split("/")[-2:]))
    print(path)
    return os.path.exists(path)


def down_file(url):
    if check_file(url) is True:
        print("文件已经存在：%s" % url)
        return

    path_file = BASE_DOWNLOAD_PATH + "/" + ("/".join(url.split("/")[-2:]))
    path = "/".join(path_file.split("/")[0:-1])
    if os.path.exists(path) is False:
        os.makedirs(path)

    # open(path_file + ".tmp", "w+").close()
    r = requests.get(url, stream=True, timeout=5)
    with open(path_file, "wb") as file:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    if os.path.exists(path_file + ".tmp") is True:
        os.remove(path_file + ".tmp")


class RpmDownloader(object):
    def process_request(self, request, spider):
        if request.url.endswith(".rpm"):
            down_file(request.url)
            return scrapy.http.HtmlResponse(url="", body="",
                                            encoding='utf8')
        return None


down_file(
    "http://ftp.loongnix.org/os/loongnix/1.0/os/Packages/p/p0f-3.07b-3.fc21.loongson.mips64el.rpm")
