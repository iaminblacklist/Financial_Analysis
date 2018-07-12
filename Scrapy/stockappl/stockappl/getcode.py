import os

#STOCK_CODE = ['sz300207']

def GET_CODE():
    f = open('stockappl/stock_code.txt')
    STOCK_CODE = []
    for line in f.readlines():
        line = line.replace('\n', '')
        STOCK_CODE.append(line)
    f.close()
    return STOCK_CODE



# if __name__ == '__main__':
#     f = open('stock_code.txt')
#     STOCK_CODE = []
#     for line in f.readlines():
#         # print(line,end = '')
#         line = line.replace('\n', '')
#         STOCK_CODE.append(line)
#     print(STOCK_CODE)
#     f.close()
