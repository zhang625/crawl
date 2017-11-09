# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from  securitites.items  import SecurititesItem
import logging

class SecurititesPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MANGODB_PORT']
        db_name = settings['MANGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        db = client[db_name]
        self.post = db[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        logging.info('进入lines')
        if isinstance(item, SecurititesItem):
            try:
                postItem = dict(item)
                self.post.insert(postItem)
            except Exception:
                pass
        return item