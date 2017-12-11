# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
from scrapy import Request
from tutorial.items import RpmItem
from scrapy.pipelines.files import FilesPipeline


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class BaiduResultPipeline(object):
    def __init__(self):
        self.file = open('BaiduResultItems.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.encode())
        return item


class ZhihuUserMongoPipeline(object):
    collection_name = 'zhihu_user'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'spider')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].update({'url_token': item["url_token"]}, {'$set': item}, True)
        return item
