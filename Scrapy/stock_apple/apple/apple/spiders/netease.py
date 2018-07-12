# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from apple.items import AppleItem



class NeteaseSpider(scrapy.Spider):
    name = 'netease'
    allowed_domains = ['money.163.com']
    start_url = 'http://quotes.money.163.com/usstock/AAPL_news.html?page={index}'


    def start_requests(self):
        for stock_index in range(0, 711):
            yield Request(url=self.start_url.format(index=stock_index), callback=self.parse_stock, dont_filter=True)



    def parse_stock(self, response):
        title = response.xpath('//dt/a/text()').extract()
        url = response.xpath('//dt/a/@href').extract()
        date = response.xpath('//div[@class="time icon_news_pills_time"]/span/text()').extract()
        # print(title)
        # print(url)
        # print(date)
        for x, y, z in zip(title, url, date):
            # print(x)
            # print(y)
            yield Request(y, callback=lambda response, TITLE=x, DATE=z: self.getApple(response, TITLE, DATE), dont_filter=True)

        pass


    def getApple(self, response, TITLE, DATE):
        news = response.xpath('//div[@class="post_text"]/p/text()').extract()
        str = "".join(news)
        # print(str)
        # print(DATE)

        item = AppleItem()
        item['title'] = TITLE
        item['news'] = str
        item['datetime'] = DATE
        yield item

        pass