# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Chictopia1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
    friends = scrapy.Field()
    following = scrapy.Field()
    followers = scrapy.Field()
    entry_url = scrapy.Field()
