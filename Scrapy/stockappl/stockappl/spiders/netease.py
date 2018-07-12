# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from stockappl.getcode import GET_CODE
from stockappl.items import StockapplItem


class NeteaseSpider(scrapy.Spider):
    name = 'netease'
    allowed_domains = ['money.163.com']
    start_url = 'http://quotes.money.163.com/f10/gsxw_{code},{index}.html'


    def start_requests(self):
        code = GET_CODE()
        for stock_code in list(code):
            CODE = stock_code[2:]
            print("0000000000000000000000000")
            print(CODE)
            for stock_index in range(0, 10):
                yield Request(url=self.start_url.format(code=CODE, index=stock_index), callback=lambda response, sz_code=stock_code: self.parse_stock(response, sz_code), dont_filter=True)

        pass

    def parse_stock(self, response, sz_code):
        title = response.xpath('//td[@class="td_text"]/a/text()').extract()
        url = response.xpath('//td[@class="td_text"]/a/@href').extract()
        date = response.xpath('//td[@class="align_c"]/text()').extract()

        for x, y, z in zip(title, url, date):
            yield Request(y, callback=lambda response, TITLE=x, DATE=z, CODE=sz_code: self.getNews(response, TITLE, DATE, CODE), dont_filter=True)
        pass

    def getNews(self, response, TITLE, DATE, CODE):
        # print(TITLE)
        # print(DATE)
        # print(CODE)
        news = response.xpath('//div[@class="post_text"]/p/text()').extract()
        str = "".join(news)
        #print(str)

        item = StockapplItem()
        item['symbol'] = CODE
        item['title'] = TITLE
        item['datetime'] = DATE
        item['news'] = str
        yield item
        pass
