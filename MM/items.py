# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MmItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    site = scrapy.Field()
    source = scrapy.Field()
    pubtime = scrapy.Field()
    fetchtime = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    # resource = scrapy.Field()
    discription = scrapy.Field()
    rawcontent = scrapy.Field()
    keywords = scrapy.Field()
    searchwords = scrapy.Field()
    MD5 = scrapy.Field()
    public_opinion = scrapy.Field()