# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouzzItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    phone = scrapy.Field()
    location = scrapy.Field()
    website_url = scrapy.Field()
    url = scrapy.Field()
    sub_url = scrapy.Field()
    review_count = scrapy.Field()
    contact = scrapy.Field()
    #desc = scrapy.Field()
    professional_info = scrapy.Field()
    typical_job_cost = scrapy.Field()
    email = scrapy.Field()
