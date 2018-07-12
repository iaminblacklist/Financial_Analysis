# coding:utf-8
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import pymysql.cursors
#功能：获取指定股票日期的每日收盘价
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.1708.400 QQBrowser/9.5.9635.400'
}

#爬取财务数据
def spiderStockFinance(stockCode):

    url = 'http://quotes.money.163.com/f10/zycwzb_'+stockCode+'.html#01c02'
    #print(url)

    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'lxml')

    table = soup.findAll('table', {'class': 'table_bg001 border_box limit_sale scr_table'})[0]
    rows = table.findAll('tr')
    #rowsData=[]

    #rowsData = rowsData[rows[0:1],rows[9:10],rows[17:18]]
    #print(rows[0:1])
    #print(rowsData)#净利润和净资产
    #返回某股票的财务报表

    return rows[0:]

def Format(rows,stockCode):

    for row in rows[0:1]:
        csvRow1 = []
        for cell in row.findAll('th'):
            csvRow1.append(cell.get_text().replace(',', ''))
    for row in rows[18:19]:
        csvRow2 = []
        for cell in row.findAll('td'):
            csvRow2.append(cell.get_text().replace(',', ''))
    #print(csvRow2)
    #print(csvRow3)
    toMysql(csvRow1[1:17],csvRow2[1:17],stockCode)


def toMysql(rows1,rows2,stockCode):
    #获取数据库的链接
    stockCodeStr = str(stockCode)
    #print(stockCode)
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user = 'root',
                           password = '1378215200zad',
                           db = 'testdata',
                           charset = 'utf8mb4')
    #print('conn ok')
    try:
        #获取会话指针
        with conn.cursor() as cursor:
            #创建sql语句
            sql = "insert into `finance`(`code`,`date`,`assets`) values(%s,%s,%s)"

            #执行sql语句
            for i in range(0,len(rows1)):
                cursor.execute(sql,(stockCodeStr,rows1[i],rows2[i]))
            #提交
                conn.commit()
        print(stockCodeStr+' commit ok')
    finally:
        conn.close()

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
    for i in range(0,49):
        #print(i)
        rows =spiderStockFinance(stocklist[i])
        Format(rows,stocklist[i])

if __name__ == '__main__':
    main()
