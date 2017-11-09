# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SecurititesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    plate = scrapy.Field()
    link = scrapy.Field()
    uuid = scrapy.Field()
    name = scrapy.Field()
    nowPrice = scrapy.Field()
    volume = scrapy.Field()
    code_mgsy = scrapy.Field()
    code_mgjzc = scrapy.Field()
    code_PE = scrapy.Field()
    code_PB = scrapy.Field()
    code_business = scrapy.Field()
    code_concept = scrapy.Field()
    pass
