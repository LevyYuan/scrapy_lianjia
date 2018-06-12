### scrapy_lianjia
基于Scrapy框架/ 使用charles进行数据抓包/ 使用scrapy_redis实现增量式和分布式爬取/ 使用MongoDb进行数据存储/ 使用crontab在每天凌晨定时执行爬虫任务/ 每日爬取数据量5w+
项目难度在于请求头的authorization参数进行了js加密。解决方法：分析微信小程序接口，逆向解析js加密参数，使用python语法生成加密参数
