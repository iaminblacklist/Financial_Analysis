# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from bulletin.getcode import GET_CODE
from bulletin.items import BulletinItem
import re


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['finance.sina.com.cn']
    start_url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/{code}/page_type/ndbg.phtml'


    def start_requests(self):
        code = GET_CODE()
        for stock_code in list(code):
            yield Request(url=self.start_url.format(code=stock_code), callback=lambda response, CODE=stock_code: self.parse_stock(response, CODE), dont_filter=True)
        #yield Request(url='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/000049/page_type/ndbg.phtml', callback=self.parse_stock)



    def parse_stock(self, response, CODE):
        html = response.text
        target = r'&id=[_0-9_]{6,7}'
        target_list = re.findall(target, html)
        print(target_list)
        for each in target_list:
            target_url = 'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid=' + CODE + each
            yield Request(target_url, callback=lambda response, news_code=CODE: self.getBulletin(response, CODE), dont_filter=True)
        pass

    def getBulletin(self, response, CODE):
        title = response.xpath('//th[@style="text-align:center"]/text()').extract_first()
        text = response.xpath('//pre/text()').extract_first()

        item = BulletinItem()
        item['code'] = CODE
        item['title'] = title
        item['bulletin'] = text

        yield item
        #print(response.xpath('//th[@style="text-align:center"]/text()').extract_first())
        #print(response.xpath('//pre/text()').extract_first())
        #pass