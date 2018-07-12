# coding:utf-8
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
import statsmodels.api as sm
from statsmodels import regression
import pylab
pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']
pylab.mpl.rcParams['axes.unicode_minus'] = False
# ********************基础知识***************************
#--------------------用sqlalchemy创建引擎
# engine = create_engine('mysql://root:@localhost/testdata?charset=utf8')
#从数据库中读取表存为DataFrame
# df2 = pd.read_sql("SELECT `id`, `code`, `date`, `close`, `marketcap` FROM `stockdata` WHERE `date` = '2013-01-04'",engine,index_col='date')
# print(df2.sort('marketcap')['code'][:16])#小市值股票组合
# print(df2.sort('marketcap')['code'][34:])#大市值股票组合
# #--------------------将日期存入list
# # list = []
# # list = df2.index
#
# #--------------------按index(日期)截取
# #print(df2['2013-01-01':'2013-03-31'])
#
# #-------------------选取列表签数据 loc['行标签'，列标签]
# #print(df2.loc[:,'marketcap':'bm'])
#
# #-------------------计算日收益率
# df2['daily_return'] = df2[1:]['close']/df2[:-1]['close'].values-1
#
#
# #-------------------填充nan
# df3 = df2.fillna(0)
# #print(df3)
# #计算某一列的和
# #print(sum(df3['daily_return']))
# # 画图
# df5 = pd.DataFrame()
# df5['date'] = df2.index
# df5.index = df5['date']
# del df5['date']
# df5['600000'] = df3['close']
# df5['600015'] = df4['close']
# #print(df5)
# #一般图形
# #df5.plot(x=df5.index,y='600015')
# #-----------------------------------散点图
# df5.plot(kind='scatter',x='600000',y='600015').get_figure()
#
# #---------------------------------线性回归
# lm=ols('600000**600015',df5).fit()
# plt.plot(df5['600015'],lm.fittedvalues,'r',linewidth = 2)
# plt.show()

# ******************开始****************************
# ******************全局变量*************************
#-----------------------获取所有交易日期
engine = create_engine('mysql://root:@localhost/testdata?charset=utf8')

#由于股票存在停牌的不交易日，经过检测，概率最大的是971个交易日，所以我们选取此股票日期作为基准
date_df = pd.read_sql("SELECT  `code`, `date` FROM `stockdata` WHERE `code` = '600028'",engine)
date_list =[]
date_list = date_df['date'].values
#print(date_list[::60])

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


# -------------------从数据表获取Close，主要是为了计算投资组合的价值
def getCL(stocklist):
    frames_CL = []
    for i in range(0,len(stocklist)):
        code_CL = stocklist[i]
        i = pd.read_sql("SELECT  `code`, `date`, `close` FROM `stockdata` WHERE `code`= %(stockcode)s ",
                          engine,index_col='date',params={'stockcode':stocklist[i]})
        # 处理日收益率
        i[code_CL] = i['close']
        i = i.fillna(0)
        frames_CL.append(i[code_CL])

    result_CL = pd.concat(frames_CL,axis=1)

    # 返回日收益率的datafream
    return result_CL

# ------------------------------从数据表获取DailyReturn，并进行处理 测试ok
def getDR(stocklist):
    frames_DR = []
    for i in range(0,len(stocklist)):
        code_DR = stocklist[i]
        i = pd.read_sql("SELECT  `code`, `date`, `close` FROM `stockdata` WHERE `code`= %(stockcode)s ",
                          engine,index_col='date',params={'stockcode':stocklist[i]})
        # 处理日收益率
        i[code_DR] = i[1:]['close'] / i[:-1]['close'].values - 1
        i = i.fillna(0)
        frames_DR.append(i[code_DR])

    result_DR = pd.concat(frames_DR,axis=1)

    # 返回日收益率的datafream
    return result_DR

# --------------------------从数据表获取MarketCap，并进行处理 测试ok
def getMC(stocklist):
    frames_MC = []
    for i in range(0, len(stocklist)):
        code_MC = stocklist[i]
        i = pd.read_sql(
            "SELECT  `code`, `date`, `marketcap` FROM `stockdata` WHERE `code`= %(stockcode)s ",
            engine, index_col='date', params={'stockcode': stocklist[i]})
        #格式化市值
        i[code_MC] = i['marketcap']
        # print(i[code_MC]) ok
        frames_MC.append(i[code_MC])

    result_MC = pd.concat(frames_MC, axis=1)
    # 返回市值的datafraem
    return result_MC

# --------------------------从数据表获取BM，并进行处理 测试可用
def getBM(stocklist):
    frames_BM = []
    for i in range(0, len(stocklist)):
        code_MC = stocklist[i]
        i = pd.read_sql(
            "SELECT  `code`, `date`, `bm` FROM `stockdata` WHERE `code`= %(stockcode)s ",
            engine, index_col='date', params={'stockcode': stocklist[i]})
        #格式化市值
        i[code_MC] = i['bm']
        # print(i[code_MC]) ok
        frames_BM.append(i[code_MC])

    result_BM = pd.concat(frames_BM, axis=1)
    # 返回账面市值比的datafraem
    return result_BM

#-----------------------获取一段日期的市值股票组合
def  getStockMc(stocklist,t,datelist):
    MC = getMC(stocklist)
    x = len(datelist[::t])
    # 创建列表来存取分割好的df
    stock_df_list = []
    for i in range(0,x):
        if (i == x-1):
            # 最后日期处理
            date1 = datelist[::t][i]
            date2 = '2016-12-31'
        else:
            # 分割日期
            date1 = datelist[::t][i]
            date2 = datelist[::t][i + 1]
    #     根据获取的日期，利用MC来获取不停牌的股票代码
        stock_df = MC[date1:date2]
        # 去除这段时间内停牌的股票
        stock_df = stock_df.dropna(axis=1,how='any')
        stock_df_list.append(stock_df)
    return stock_df_list

#-----------------------获取一段日期的日收益率股票组合
def  getStockDr(stocklist,t,datelist):
    DR = getDR(stocklist)
    x = len(datelist[::t])
    stock_df_list = []
    for i in range(0,x):
        if (i == x-1):
            date1 = datelist[::t][i]
            date2 = '2016-12-31'
        else:
            date1 = datelist[::t][i]
            date2 = datelist[::t][i + 1]
        stock_df = DR[date1:date2]
        stock_df = stock_df.dropna(axis=1,how='any')
        stock_df_list.append(stock_df)
    return stock_df_list

#-----------------------获取一段日期的股票收盘价
def  getStockCl(stocklist,t,datelist):
    CL = getCL(stocklist)
    x = len(datelist[::t])
    stock_df_list = []
    for i in range(0,x):
        if (i == x-1):
            date1 = datelist[::t][i]
            date2 = '2016-12-31'
        else:
            date1 = datelist[::t][i]
            date2 = datelist[::t][i + 1]
        stock_df = CL[date1:date2]
        stock_df = stock_df.dropna(axis=1,how='any')
        stock_df_list.append(stock_df)
    return stock_df_list

#-----------------------获取一段日期的账面市值股票组合
def  getStockBm(stocklist,t,datelist):
    BM = getBM(stocklist)
    x = len(datelist[::t])
    stock_df_list = []
    for i in range(0,x):
        if (i == x-1):
            date1 = datelist[::t][i]
            date2 = '2016-12-31'
        else:
            date1 = datelist[::t][i]
            date2 = datelist[::t][i + 1]
        stock_df = BM[date1:date2]
        stock_df = stock_df.dropna(axis=1,how='any')
        stock_df_list.append(stock_df)
    return stock_df_list

# --------------获取上证50的日收益率
# 根据日期切成多块然后插入到一个列表中，
def getSZ50(t):
    sz50 = pd.read_sql("SELECT `date`,`close` FROM `sz50data` ", engine, index_col='date')
    datelist = sz50.index.values
    x = len(datelist[::t])
    sz50_df_list = []
    for i in range(0,x):
        if (i == x-1):
            date1 = datelist[::t][i]
            date2 = '20161231'
        else:
            date1 = datelist[::t][i]
            date2 = datelist[::t][i + 1]
        sz50_df = sz50[date1:date2]
        # print(sz50_df)
        sz50_df_list.append(sz50_df)
    # print(sz50_df_list)
    return sz50_df_list
    # sz50Dr = sz50[1:]/sz50[:-1].values-1


# --------------计算SMB HML RM
def getData(mcStockDf,drStockDf,bmStockDf,sz50Df):
    # 取某段时期所有股票
    stocks = mcStockDf.columns.values
    # 转置处理
    mcStockDf = mcStockDf.T
    bmStockDf = bmStockDf.T
    # 选取某一列作为基准
    mcStockDf = mcStockDf.iloc[:,0:1]
    bmStockDf = bmStockDf.iloc[:,0:1]
    # 取列名
    sortName = mcStockDf.columns
    # 排序
    mcStockDf = mcStockDf.sort_values(by=sortName[0])
    bmStockDf = bmStockDf.sort_values(by=sortName[0])
    # 取当前股票总数
    amount = len(mcStockDf)

    # 选取大市值股票组合
    B = mcStockDf[int(amount-amount/3):].index
    B = B.values
    # 选取小市值股票组合
    S = mcStockDf[:int(amount/3)].index
    S = S.values
    # print(S.values)

    # 选取高bm的股票组合
    H = bmStockDf[int(amount-amount/3):].index
    H = H.values
    # 选取低bm的股票组合
    L = bmStockDf[:int(amount/3)].index
    L = L.values
    # print(L)

      # 求因子的值
    SMB = drStockDf[S][1:].sum(axis=1) / len(S) - drStockDf[B][1:].sum(axis=1) / len(B)
    HML = drStockDf[H][1:].sum(axis=1) / len(H) - drStockDf[L][1:].sum(axis=1) / len(L)
    # print(SMB)

#     基准收益率  上证50指数
    # print(sz50Df)
    RM = np.diff(np.log(sz50Df['close']))-0.04/252
    # print(len(RM))

    X = pd.DataFrame({"RM": RM, "SMB": SMB, "HML": HML})
    # 取前g.NoF个因子为策略因子
    factor_flag = ["RM", "SMB", "HML"]
    X = X[factor_flag]

    # 对样本数据进行线性回归并计算ai
    t_scores = [0.0] * amount
    # 循环依次计算股票的分数
    for i in range(0,amount):
        t_stock = stocks[i]
        sample = pd.DataFrame()
        t_r = linreg(X, drStockDf[t_stock][1:] - 0.04 / 252, len(factor_flag))
        t_scores[i] = t_r[0]
    # 这个scores就是alpha
    scores=pd.DataFrame({'code':stocks,'score':t_scores})
    # 根据分数进行排序
    scores = scores.sort_values(by='score')
    # print (scores.sort_values(by='score'))
    return scores

# 辅助线性回归的函数
# 输入:X:回归自变量 Y:回归因变量 完美支持list,array,DataFrame等三种数据类型
#      columns:X有多少列，整数输入，不输入默认是3（）
# 输出:参数估计结果-list类型
def linreg(X,Y,columns=3):
    X=sm.add_constant(np.array(X))
    Y=np.array(Y)
    if len(Y)>1:
        results = regression.linear_model.OLS(Y, X).fit()
        return results.params
    else:
        return [float("nan")]*(columns+1)

#     计算投资组合价值
def withCapital(stocksScores,StockClDf,money):
    # 选取stocks中的前五只股票
    # print(stocksScores[-5:])
    stocks = stocksScores[23:28]['code'].values
    # 选取前五只股票的收盘价
    stocks = StockClDf[stocks]
    # 提取日期
    date = stocks.index[1:].values
    # 格式化 以每一天的价格除以第一天的价格
    normet = stocks[1:].values/stocks[0:1].values
    # print(type(normet)) np.ndarray

    #分配权重
    data = [0.2,0.2,0.2,0.2,0.2]
    allocs = np.array(data)
    alloced = normet*allocs
    # print(money)

    # 分配资金
    pos_vals = alloced*money

    # 计算投资组合收益
    port_val = pos_vals.sum(axis=1)

    port_val_df = pd.DataFrame(port_val,index=date)
    port_val_df.rename(columns={0:'port_val'},inplace=True)
    # print(port_val_df)
    return port_val_df
#
# 主函数
def main():
    # 调仓周期
    time=63
    # 这五个函数内容都一样，返回的是行为日期，列为股票代码的DataFrame
    # 获取所有股票市值
    StockMcDfList = getStockMc(stocklist,time,date_list)
    # 获取所有股票日收益率
    StockDrDfList = getStockDr(stocklist,time,date_list)
    # 获取所有股票账面市值比
    StockBmDfList = getStockBm(stocklist,time,date_list)
    # 获取所有股票收盘价
    StockClDfList = getStockCl(stocklist,time,date_list)
    # 获取上证50的收盘价
    Sz50DfList = getSZ50(time)

    # 持仓时间段
    chooseDate = len(StockDrDfList)
    # 创建一个列表，存放每段时间的投资组合收益
    frames_port = []
    for i in range(0,chooseDate):
        if (i==0):
            money = 100000
        else:
            money = port_val['port_val'][-1:].values
        # 选股
        stocksScores = getData(StockMcDfList[i],StockDrDfList[i],StockBmDfList[i],Sz50DfList[i])
        # 配资并计算投资组合每日的收益
        port_val = withCapital(stocksScores,StockClDfList[i],money)
        frames_port.append(port_val)

    Sz50Df = pd.read_sql("SELECT `date`,`close` FROM `sz50data` ", engine, index_col='date')
    # print(Sz50Df)
    # 初始化
    Sz50 = Sz50Df[1:].values/Sz50Df[0:1].values
    Sz50 = Sz50*100000
    Sz50Df = pd.DataFrame(Sz50)

    # 选择一个不停牌的股票作为参考
    SD601398df = pd.read_sql("SELECT `date`,`close` FROM `stockdata` where `code`=601398 ", engine, index_col='date')
    # 初始化
    SD601398 = SD601398df[1:].values / SD601398df[0:1].values
    SD601398 = SD601398 * 100000
    SD601398df = pd.DataFrame(SD601398)

    # 将获取到每段的投资组合收益再拼接起来
    result_port = pd.concat(frames_port)

    x=SD601398df[0].values
    y=result_port['port_val'].values
    z=Sz50Df[0].values
    x = x.tolist()
    y = y.tolist()
    z = z.tolist()
    x.insert(0,100000)
    y.insert(0,100000)
    z.insert(0,100000)

    # 将投资组合每日收益和SZ50每日收益合成一个Dataframe
    data = {'市场指数': z, '投资组合收益': y, '601398':x}
    result_df = pd.DataFrame(data=data, index=date_list)
    # 计算组合后的日收益率
    result_daily_return = np.diff(np.log(result_df),axis=0)+0*result_df[1:]
    # 绘制散点图
    result_daily_return.plot(kind='scatter',x='市场指数',y='投资组合收益')
    # 线性回归 通过散点图进行拟合
    beta_PVAL,alpha_PVAL = np.polyfit(result_daily_return['市场指数'],result_daily_return['投资组合收益'],1)

    # 计算策略收益
    P_end = result_port['port_val'][-1:].values
    P_start = result_port['port_val'][0:1].values
    TR = (P_end - P_start) / P_start * 100
    print('策略收益 ',TR[0])
    # 计算基准收益
    M_end = Sz50Df[0][-1:].values
    M_start = Sz50Df[0][0:1].values
    BR = (M_end - M_start) / M_start * 100
    print('基准收益 ',BR[0])
    #    计算策略年化收益
    P = sum(result_daily_return['投资组合收益'].values)
    TAR = ((1 + P) **(244 / 970) - 1) * 100
    print('策略年化收益 ',TAR)
    #     计算基准年化收益
    M = sum(result_daily_return['市场指数'].values)
    BAR = ((1 + M) ** (244 / 970) - 1) * 100
    print('基准年化收益 ',BAR)
    # 贝塔
    print('a',alpha_PVAL)
    print('beta_PVAL:', beta_PVAL)
    # 阿尔法
    alpha = (TAR-(4+beta_PVAL*(BAR-4)))
    print('alpha_PVAL:', alpha)
    # 夏普比率
    mean = np.mean(result_daily_return['投资组合收益'].values)
    std = np.std(result_daily_return['投资组合收益'].values)
    SR = np.sqrt(244)*((mean-0.04/244)/std)
    print('shape_PVAL:',SR)
    # 绘制拟合后的直线
    plt.plot(result_daily_return['市场指数'],beta_PVAL*result_daily_return['市场指数']+alpha_PVAL,'-',color = 'r')
    # 打印相关性
    print(result_daily_return.corr(method='pearson'))
    # 绘制收益图
    result_df.plot()
    plt.show()


if __name__ == '__main__':
    main()



