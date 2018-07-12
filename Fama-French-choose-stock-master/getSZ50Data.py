# coding:utf-8
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import pymysql.cursors
#功能：获取市场在2013-2016的收盘价
#报文头部
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.1708.400 QQBrowser/9.5.9635.400'
}


#爬取数据
def spider(year,season):
    #字符化处理
    yearStr = str(year)
    seasonStr = str(season)
    url = 'http://quotes.money.163.com/trade/lsjysj_zhishu_000016.html?year=' + yearStr + '&season=' + seasonStr
    #print(url)

    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'lxml')

    table = soup.findAll('table', {'class': 'table_bg001 border_box limit_sale'})[0]
    rows = table.findAll('tr')
    # print(rows[:0:-1])
    #返回一个季度的交易数据
    return rows[:0:-1]

#------------将获取的html提取并格式化
def Format(rows):
    #print(stockCode)
    for row in rows:
        csvRow = []
        for cell in row.findAll('td'):
            csvRow.append(cell.get_text().replace(',', ''))

        # print(csvRow[1])
        toMysql(csvRow)

#------------------------将获得的指数数据存放到数据库
def toMysql(rows):

    # 数据库的链接
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='',
                           db='testdata',
                           charset='utf8mb4')

    try:
        #获取会话指针
        with conn.cursor() as cursor:
            #创建sql语句
            sql = "insert into `sz50data`(`date`,`close`) values(%s,%s)"

            #执行sql语句
            cursor.execute(sql,(rows[0],rows[4]))
            #提交
            conn.commit()
            #print('sql commit ok')
    finally:
        conn.close()

#获取指定股票指定日期的每日行情
def getSZ50Data(beginYear, endYear):
    for year in range(beginYear, endYear+1):
        for season in range(1,5):
            rows = spider(year, season)
            if(rows != []):
                Format(rows)

                print('上证50-',year,'-',season,'done')
    print('ok')

def main():

    #获取上证50指数数据
    getSZ50Data(2013,2017)



# ps:删除数据库某个表的所有数据并将ID置1 TURNCATE TABLE 表名
if __name__ == '__main__':
    main()
