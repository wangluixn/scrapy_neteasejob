# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WangyinewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    productName = scrapy.Field()
    postTypeFullName = scrapy.Field()
    description = scrapy.Field()
    recruitNum = scrapy.Field()
    reqEducationName = scrapy.Field()
    reqWorkYearsName = scrapy.Field()
    requirement = scrapy.Field()
    firstPostTypeName = scrapy.Field()
    workPlaceNameList = scrapy.Field()
    table_fields = scrapy.Field()  # 字段名称
    table_name = scrapy.Field()  # 插入表的名称



