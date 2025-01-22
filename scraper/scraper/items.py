# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def stock_value(response):
    stock = response.xpath('//table[1]/tr[6]/td/text()').re_first(r'\d+')
    return stock

class BookItem(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    
    # table
    upc = scrapy.Field()
    product_type = scrapy.Field()
    stock = scrapy.Field()
    
    
    
    