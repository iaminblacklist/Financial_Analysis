# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from stockappl.getcode import GET_CODE
from stockappl.items import StockapplItem



import re
from bs4 import  BeautifulSoup,BeautifulStoneSoup
import chardet

class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['finance.sina.com.cn']
    #start_urls = ['http://finance.sina.com.cn/']
    start_url = "http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol={code}&Page={index}"
    #start_url = "http://finance.sina.com.cn"
    #start_url = "http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz000823&Page=1"



    def start_requests(self):
        #sina_url = '{url}sz300207&Page=1'.format(url=self.start_url)
        #sina_url = '{url}'.format(url=self.start_url) + code + '&Page=' + index
        code = GET_CODE()
        for stock_code in list(code):
            for stock_index in range(1, 10):
                yield Request(url=self.start_url.format(code=stock_code, index=stock_index), callback=lambda response, CODE=stock_code: self.parse_stock(response, CODE), dont_filter=True)


    def parse_stock(self, response, CODE):
        data = response.text
        soup = BeautifulSoup(data, "html5lib")
        paper_name = soup.html.body.select('div .datelist')[0].ul.find_all('a')
        tableData = []
        for e in paper_name:
            b = e.previous_sibling
            a = re.search(r'\d{4}(\-)\d{1,2}(\-)\d{1,2}', b)

            tableData.append({
                'symbol': CODE,
                'title': e.string,
                'url': e['href'],
                'datetime': a.group()
            })

            yield Request(url=e['href'], callback=lambda response, news_code=CODE, news_title=e.string, news_date=a.group(): self.getNews(response, news_code, news_title, news_date), dont_filter=True)

        #print(response.text)
        pass

    def getNews(self, response, newcode, newtitle, newdate):
        news = response.body
        htmlchardet = chardet.detect(news)
        print(htmlchardet["encoding"])

        # fopen1 = urlopen(newsurl).info()
        # print(fopen1)
        if htmlchardet["encoding"] == "Windows-1254":
            htmlchardet["encoding"] = "utf-8"

        if htmlchardet["encoding"] == "ascii":
            htmlchardet["encoding"] = "GB2312"

        # res = requests.get(newsurl)
        # res.encoding = htmlchardet["encoding"]
        soup = BeautifulSoup(response.text, 'html.parser', from_encoding=htmlchardet["encoding"])
        # ,  from_encoding='gb2312'
        try:
            print(soup.title.text)
        except (AttributeError, UnicodeEncodeError, TypeError) as e:
            pass

        newtext = []

        tt = soup.find_all('p')
        for t in tt:
            # print(t.text)
            newtext.append(t.text)

        news = ''.join(newtext)

        item = StockapplItem()
        item['symbol'] = newcode
        item['title'] = newtitle
        item['datetime'] = newdate
        item['news'] = news

        yield item
        #print(item)


        # f = open(newcode + '_' + newdate + '.txt', 'wt', encoding="utf-8")
        # try:
        #     f.write(news)
        # except (AttributeError, UnicodeEncodeError, TypeError) as e:
        #     pass
        #
        #
        # f.close()
        #pass