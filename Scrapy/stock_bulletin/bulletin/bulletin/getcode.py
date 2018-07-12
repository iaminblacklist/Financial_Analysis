def GET_CODE():
    f = open('bulletin/stock_code.txt')
    STOCK_CODE = []
    for line in f.readlines():
        line = line.replace('\n', '')
        STOCK_CODE.append(line)
    f.close()
    return STOCK_CODE
