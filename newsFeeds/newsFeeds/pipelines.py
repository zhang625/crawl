# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from newsFeeds.items import NewsfeedsItem
import datetime
from scrapy import log


class NewsfeedsPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MANGODB_PORT']
        db_name = settings['MANGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        db = client[db_name]
        nowTime = datetime.datetime.now()
        nowTimeStr = '%s%s%s' % (nowTime.year, nowTime.month, nowTime.day)
        self.post = db[settings['MONGODB_DOCNAME']]
        self.postPull = {'newsTime': nowTimeStr, 'itemPull': []}

    # @classmethod
    def close_spider(self, spider):
        self.post.insert(self.postPull)
        sel = self.post.find_one({"newsTime": self.postPull['newsTime']})
        if sel and len(sel['itemPull']) > 0:
            log.msg('重复数据', level=log.INFO)
            pass
        elif sel and len(sel['itemPull']) == 0:
            log.msg('空数组,删除后递归', level=log.INFO)
            self.post.remove(sel['id'])
            return self.close_spider(spider)
        elif len(self.postPull['itemPull']) > 0:
            log.msg('开始储存', level=log.INFO)
            self.post.insert(self.postPull)
        else:
            log.msg('空数据', level=log.INFO)

    def process_item(self, item, spider):
        if isinstance(item, NewsfeedsItem):
            try:
                postItem = dict(item)
                self.postPull['itemPull'].append(postItem)
            except Exception:
                pass
        return item
