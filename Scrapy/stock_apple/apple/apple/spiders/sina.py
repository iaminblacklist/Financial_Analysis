# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from apple.items import AppleItem
import re



class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['finance.sina.com.cn']
    start_url = 'http://biz.finance.sina.com.cn/usstock/usstock_news.php?pageIndex={index}&symbol=AAPL&type=1'


    def start_requests(self):
        for stock_index in range(1, 100):
            yield Request(url=self.start_url.format(index=stock_index), callback=self.parse_stock, dont_filter=True)



    def parse_stock(self, response):
        title = response.xpath('//a[@type-stastics="cj"]/text()').extract()
        url = response.xpath('//a[@type-stastics="cj"]/@href').extract()
        date = response.xpath('//span[@class="xb_list_r"]/text()').extract()
        date = date[9:17]
        print("0000000000000000000000000000000000000")
        print(date)
        print(title)
        # print(url)
        for x, y, z in zip(title, url, date):
            # print(x)
            # print(y)
            yield Request(y, callback=lambda response, TITLE=x, DATE=z: self.getApple(response, TITLE, DATE), dont_filter=True)

        pass

    def getApple(self, response, TITLE, DATE):
        # t = response.xpath('//h1[@class="main-title"]/text()').extract()
        # print(TITLE)
        news = response.xpath('//p/text()').extract()
        str = "".join(news)
        # print(str)
        # print(TITLE)
        # print(DATE)

        item = AppleItem()
        item['title'] = TITLE
        item['news'] = str
        item['datetime'] = DATE
        yield item

        pass

