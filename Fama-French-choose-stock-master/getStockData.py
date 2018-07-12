# coding:utf-8
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import pymysql.cursors
#功能：获取指定股票日期的每日收盘价
#报文头部
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.1708.400 QQBrowser/9.5.9635.400'
}


#爬取数据
def spider(stockCode,year,season):
    #字符化处理
    stockCodeStr = str(stockCode)
    yearStr = str(year)
    seasonStr = str(season)
    url = 'http://quotes.money.163.com/trade/lsjysj_' + stockCodeStr + '.html?year=' + yearStr + '&season=' + seasonStr
    #print(url)

    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'lxml')

    table = soup.findAll('table', {'class': 'table_bg001'})[0]
    rows = table.findAll('tr')
    # print(rows[:0:-1])
    #返回一个季度的交易数据
    return rows[:0:-1]

#------------将获取的html提取并格式化
def Format(rows,stockCode,assets):
    #print(stockCode)
    for row in rows:
        csvRow = []
        for cell in row.findAll('td'):
            csvRow.append(cell.get_text().replace(',', ''))

        #print(csvRow[1])
        toMysql(csvRow,stockCode,assets)

#---------------从数据库获取指定股票的股本数据
def getCaptailStock(stockCode):
    # 数据库的链接
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='1378215200zad',
                           db='testdata',
                           charset='utf8mb4')
    try:
        # 获取会话指针
        with conn.cursor() as cursor:
            # 创建sql语句
            sql = "SELECT `id`, `code`, `capitalstock` FROM `capitalstock` WHERE `code`= %s"

            # 执行sql语句
            cursor.execute(sql, (stockCode))
            result = cursor.fetchall()
            return result[0][2]
            # 提交
        conn.commit()
    finally:
        conn.close()

#获得财务报表的净资产
def getAssets(stockCode,year,season):
    # 数据库的链接
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='1378215200zad',
                           db='testdata',
                           charset='utf8mb4')
    year = str(year)
    if (season == 1):
        date = year + '-03-31'
    if (season == 2):
        date = year + '-06-30'
    if (season == 3):
        date = year + '-09-30'
    if (season == 4):
        date = year + '-12-31'
    #print(date)
    #print(stockCode)
    try:
        # 获取会话指针
        with conn.cursor() as cursor:
            # 创建sql语句
            sql = "SELECT `id`, `code`, `date`, `assets` FROM `finance` WHERE `code` = %s AND `date`= %s"

            # 执行sql语句
            cursor.execute(sql, (stockCode,date))
            result = cursor.fetchall()
            #print(result)
            return result[0][3]
            # 提交
        conn.commit()
    finally:
        conn.close()
#------------------------将获得的股票数据存放到数据库
def toMysql(rows,stockCode,assets):

    # 数据库的链接
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='',
                           db='testdata',
                           charset='utf8mb4')

    captailStock = getCaptailStock(stockCode)
    captailStock = float(captailStock)
    rows[4] = float(rows[4])
    marketcap = rows[4]*captailStock
    bm = marketcap/assets
    try:
        #获取会话指针
        with conn.cursor() as cursor:
            #创建sql语句
            sql = "insert into `stockdata`(`code`,`date`,`close`,`marketcap`,`bm`) values(%s,%s,%s,%s,%s)"

            #执行sql语句
            cursor.execute(sql,(stockCode,rows[0],rows[4],marketcap,bm))
            #提交
            conn.commit()
            #print('sql commit ok')
    finally:
        conn.close()

#获取指定股票指定日期的每日行情
def getStockData(stockCode, beginYear, endYear):
    for year in range(beginYear, endYear+1):
        for season in range(1,5):
            rows = spider(stockCode, year, season)
            assets = getAssets(stockCode,year,season)
            if(rows != []):
                Format(rows,stockCode,assets)

                print(stockCode,'-',year,'-',season,'done')
    print('ok')

def main():
    #上证50成分股列表
    stocklist = ['600000', '600010', '600015', '600016', '600019',
                 '600028', '600030', '600031', '600036', '600048',
                 '600050', '600104', '600111', '600123', '600256',
                 '600348', '600362', '600383', '600489', '600518',
                 '600519', '600547', '600549', '600585', '600837',
                 '600887', '600999', '601006', '601088', '601166',
                 '601169', '601288', '601318', '601328',
                 '601336', '601398', '601601', '601628', '601668',
                 '601669', '601688', '601699', '601766', '601788',
                 '601818', '601857', '601899', '601901', '601989']
    #获取列表中所有股票的数据
    for i in range(0,49):
        getStockData(stocklist[i],2013,2016)



# ps:删除数据库某个表的所有数据并将ID置1 TURNCATE TABLE 表名
if __name__ == '__main__':
    main()
