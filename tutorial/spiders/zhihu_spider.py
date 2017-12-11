# -*- coding: utf-8 -*-
import scrapy
import json

import tutorial.items as items

FOLLOWEES = "https://www.zhihu.com/api/v4/members/{user}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={offset}&limit={limit}"
FOLLOWERS = "https://www.zhihu.com/api/v4/members/{user}/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={offset}&limit={limit}"
USER_DETAIL = "https://www.zhihu.com/api/v4/members/{user}?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics"


class ZhihuSpiderSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
            "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
        },
        "MONGO_URI": "127.0.0.1:27017",
        "MONGO_DATABASE": "spider",
        "ITEM_PIPELINES": {
            'tutorial.pipelines.ZhihuUserMongoPipeline': 100,
        }
    }

    start_user = "zhang-peng-cheng-67-42"

    def start_requests(self):
        yield scrapy.Request(USER_DETAIL.format(user=self.start_user),
                             callback=self.parse_user)

    def parse_user(self, response):
        result = json.loads(response.text)
        zhihu_user_item = items.ZhihuUserItem()
        # 这里循环判断获取的字段是否在自己定义的字段中，然后进行赋值
        for field in zhihu_user_item.fields:
            if field in result.keys():
                zhihu_user_item[field] = result.get(field)

        yield zhihu_user_item

        yield scrapy.Request(FOLLOWEES.format(user=result.get("url_token"), offset=0, limit=20),
                             callback=self.parse_follow)
        yield scrapy.Request(FOLLOWERS.format(user=result.get("url_token"), offset=0, limit=20),
                             callback=self.parse_follow)

    def parse_follow(self, response):
        print("====")
        print(response.text)
        results = json.loads(response.text)
        if "data" in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(USER_DETAIL.format(user=result.get("url_token")),
                                     callback=self.parse_user)

        if 'page' in results.keys() and results.get('is_end') == False:
            next_page = results.get('paging').get("next")
            yield scrapy.Request(next_page, self.parse_follow)
