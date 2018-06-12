# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest, Request
import json
from scrapy_08_爬取链家二手房.items import LianjiaItem

# 用于产生参数
import hashlib
import base64
from urllib.parse import urlparse, parse_qs

# 用于产生时间戳
import time


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['wechat.lianjia.com']
    start_urls = ['http://wechat.lianjia.com/']
    begin_url = 'https://wechat.lianjia.com/ershoufang/search?city_id=420100&condition=&query=&order=&offset={page}&limit=10&sign='

    # 产生authorization参数
    def get_authorization(self, page):
        app_id = "ljwxapp:"
        app_key = "6e8566e348447383e16fdd1b233dbb49"
        param = ""
        parse_param = parse_qs(urlparse(self.begin_url.format(page=page)).query, keep_blank_values=True)  # 解析url参数
        data = {key: value[-1] for key, value in parse_param.items()}  # 生成字典
        dict_keys = sorted(data.keys())  # 对key进行排序
        for key in dict_keys:  # 排序后拼接参数,key = value 模式
            param += str(key) + "=" + data[key]
        param = param + app_key  # 参数末尾添加app_key
        param_md5 = hashlib.md5(param.encode()).hexdigest()  # 对参数进行md5 加密
        authorization_source = app_id + param_md5  # 加密结果添加前缀app_id
        authorization = base64.b64encode(authorization_source.encode())  # 再次进行base64 编码
        return authorization.decode()

    # 产生毫秒级时间戳
    def get_timestamp(self):
        t = time.time()
        timestamp = int(round(t * 10000))
        return timestamp

    # 初始请求
    def start_requests(self):
        page = 0

        headers = {
            'lianjia-source': 'ljwxapp',
            'authorization': str(self.get_authorization(page)),
            'time-stamp': str(self.get_timestamp())
        }
        print(self.get_authorization(page))

        yield Request(
            self.begin_url.format(page=page),
            callback=self.parse_house,
            headers=headers,
            meta={'page': page}
        )

    # 分析二手房
    def parse_house(self, response):
        print(response.url)
        res = json.loads(response.text)
        # print(res)

        wrap = res['data']['list']
        for key, value in wrap.items():
            item = LianjiaItem()
            item['title'] = value['title']
            item['frame_type'] = value['frame_type']
            item['floor_level'] = value['floor_level']
            item['floor_total'] = value['floor_total']
            item['orientation'] = value['orientation']
            item['building_type'] = value['building_type']
            item['building_year'] = value['building_year']
            item['deal_property'] = value['deal_property']
            item['list_time'] = value['list_time']
            item['house_type'] = value['house_type']
            item['elevator'] = value['elevator']
            item['total_price'] = value['total_price']
            item['unit_price'] = value['unit_price']

        print(item)

        # 翻页
        page = response.meta.get('page') + 10
        headers = {
            'lianjia-source': 'ljwxapp',
            'authorization': str(self.get_authorization(page)),
            'time-stamp': str(self.get_timestamp())
        }

        yield Request(
            self.begin_url.format(page=page),
            callback=self.parse_house,
            headers=headers,
            meta={'page': page}
        )
