# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class LianjiaItem(Item):
    title = Field()
    frame_type = Field()
    floor_level = Field()
    floor_total = Field()
    orientation = Field()
    building_type = Field()
    building_year = Field()
    deal_property = Field()
    list_time = Field()
    house_type = Field()
    elevator = Field()
    total_price = Field()
    unit_price = Field()






