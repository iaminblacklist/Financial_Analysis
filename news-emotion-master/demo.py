# coding=utf8

import os
import pickle
import numpy as np
import operate_data as od
import ml_model as ml
from news import ret_news
# from supplier_news import supl_news
import supplier_news as sp

VECTOR_MODE = {'onehot': 0, 'wordfreq': 1, 'twovec': 2, 'tfidf': 3, 'outofdict': 4}

def save_model(best_vector,best_model):
    """
    存储效果最好的模型
    需要手动指明参数名字
    :param best_vector: 最好的文本->词向量的方法
    :param best_model: 最好的机器学习模型
    :return: info
    """
    od.loadStopwords()
    od.loadEmotionwords()
    od.loadWords(od.stopList)
    od.loadDocument(od.stopList)
    xpath = os.path.join('result', 'vector', 'resultX.npz')
    ypath = os.path.join('result', 'vector', 'resultY.npz')
    resultX = np.load(xpath)
    resultY = np.load(ypath)
    new_x, new_y = od.twoTag(resultX[best_vector], resultY[best_vector])
    model_saved = ml.linearLogistic(new_x, new_y)
    path = os.path.join('model','wordfreq_logistic.ml')
    with open(path,'wb') as f:
        pickle.dump(model_saved,f)
    print("Save over")

class Predictor(object):
    """
    更多的使用说明请去看README.md
    """
    def __init__(self):
        self._model = None
        self.news = None
        self.__tag = None
        self._vec = None
        self.mode = None

    def load_model(self,path=None):
        if not path:
            path = os.path.join('model','wordfreq_logistic.ml')

        with open(path,'rb') as f:
            self._model = pickle.load(f)

    def set_mode(self,mode):
        if isinstance(mode,int):
            assert mode in VECTOR_MODE.values(), "没有这种vector方式"
        if isinstance(mode,str):
            assert mode in VECTOR_MODE.keys(), "没有这种vector方式"
            mode = VECTOR_MODE[mode]
        self.mode = mode

    def set_news(self,news):
        if not len(news):
            print("请输入有效的新闻文本,谢谢")
            return
        self.news = news

    def trans_vec(self):
        vec_list = od.words2Vec(self.news,od.emotionList,od.stopList,od.posList,od.negList,mode=self.mode)
        self._vec = np.array(vec_list).reshape(1,-1)

    # 调用的时候计算函数
    def __call__(self, *args, **kwargs):
        self.__tag = self._model.predict(self._vec)
        return self.__tag

    def get_tag(self):
        return self.__tag


def test(reload=False):
    if reload:
        best_vector = "wordfreq"
        best_model = 1  # linearLogistic
        save_model(best_vector, best_model)
    else:
        od.loadStopwords()
        od.loadEmotionwords()
        od.loadWords(od.stopList)
        od.loadDocument(od.stopList)

    predictor = Predictor()
    predictor.load_model()
    predictor.set_mode(mode="wordfreq")

    news = "                                                    《经济通通讯社13日专讯》日股早市偏软,日经225指数报18312跌239点。  美元兑日圆疲软,新报108﹒78╱80。(tt)                                                                         "
    news = "                                                  周二,恒生指数收报20356.24点,跌236.76点,跌幅1.15%;国企指数收报10596.91点,跌148点,跌幅1.38%;大市成交492.76亿港元。美国3月非农就业数据表现疲弱,拖累隔夜欧美股市全线受压。中国3月份CPI同比增长3.6%,令货币政策在短期内放宽预期降低。港股早盘随外围低开两百多点,但是A股在汇金增持内银股刺激下探底回升,对港股起到支持,之后恒指于低位维持窄幅震荡整理,最终跌逾1%。银行股全线走软。四大内银股方面,工商银行跌0.4%,中国银行跌0.64%,建设银行跌0.67%,农业银行跌1.2%;国际金融股方面,汇丰控股跌1.75%,渣打集团跌1.89%。美国就业市场增长放缓及内地通胀反弹,投资者对经济信心下降。中国央行短期内下调存准机会大减,从而利淡大市气氛。预计港股本周将继续在20200至20700点之间震荡。                                                                         "  # 待转化的文本

    predictor.set_news(news=news)
    predictor.trans_vec()

    tag = predictor()
    print("算出来的和是",sum(predictor._vec[0]))
    print("打标的结果是：",tag)


def news_emotion(news_data):
    emotion = 0
    num = 0
    for i in news_data:
        # print(i['news'])
        news = i['news']
        try:
            predictor.set_news(news=news)
            predictor.trans_vec()

            tag = predictor()  # 分类结果
            emotion = tag + emotion
        except (TypeError, ValueError) as e:
            pass
        num = num + 1
    # emotion = emotion/num
    return emotion


if __name__=='__main__':
    od.loadStopwords()
    od.loadEmotionwords()
    od.loadWords(od.stopList)
    od.loadDocument(od.stopList)
    ##### 单例模式 #####
    predictor = Predictor()
    predictor.load_model()
    predictor.set_mode(mode="wordfreq")  # 以上代码是初始化配置，只需要调用一次

    ##### 下面的代码可以循环调用 #####
    # news = "                                                    《经济通通讯社13日专讯》日股早市偏软,日经225指数报18312跌239点。  美元兑日圆疲软,新报108﹒78╱80。(tt)"  # 这是您的新闻样本

    txtnews = sp.apple_news()
    # print("apple:", news_emotion(txtnews))
    print(news_emotion(txtnews))

    txtnews = sp.sunway_news()
    # print("sunway:", news_emotion(txtnews))
    print(news_emotion(txtnews))

    txtnews = sp.goworld_news()
    # print("goworld:", news_emotion(txtnews))
    print(news_emotion(txtnews))

    txtnews = sp.sunwoda_news()
    # print("sunwoda:", news_emotion(txtnews))
    print(news_emotion(txtnews))

    txtnews = sp.dsbj_news()
    # print("dsbj:", news_emotion(txtnews))
    print(news_emotion(txtnews))

    txtnews = sp.hnlens_news()
    # print("hnlens:", news_emotion(txtnews))
    print(news_emotion(txtnews))

    txtnews = sp.luxshare_news()
    # print("luxshare:", news_emotion(txtnews))
    print(news_emotion(txtnews))

    txtnews = sp.goertek_news()
    # print("goertek:", news_emotion(txtnews))
    print(news_emotion(txtnews))

    txtnews = sp.ofilm_news()
    # print("ofilm:", news_emotion(txtnews))
    print(news_emotion(txtnews))

    txtnews = sp.desay_news()
    # print("desay:", news_emotion(txtnews))
    print(news_emotion(txtnews))


    #
    # # all_news = ret_news()
    # appl_news = ret_news()
    # emotion_1 = 0
    # for i in appl_news:
    #     # print(i['news'])
    #     news = i['news']
    #     try:
    #         predictor.set_news(news=news)
    #         predictor.trans_vec()
    #
    #         tag = predictor()  # 分类结果
    #         # print("算出来的和是", sum(predictor._vec[0]))
    #         # print("打标的结果是：", tag)
    #         emotion_1 = tag + emotion_1
    #     except (TypeError, ValueError) as e:
    #         pass
    # print("apple:", emotion_1)
    #
    # sunway_news = sp.sunway_news()
    # emotion_1 = 0
    # for i in sunway_news:
    #     # print(i['news'])
    #     news = i['news']
    #     predictor.set_news(news=news)
    #     predictor.trans_vec()
    #
    #     tag = predictor()  # 分类结果
    #     # print("算出来的和是", sum(predictor._vec[0]))
    #     # print("打标的结果是：", tag)
    #     emotion_1 = tag + emotion_1
    # print("sunway:", emotion_1)
    #
    # goworld_news = sp.goworld_news()
    # emotion_1 = 0
    # for i in goworld_news:
    #     # print(i['news'])
    #     news = i['news']
    #     predictor.set_news(news=news)
    #     predictor.trans_vec()
    #
    #     tag = predictor()  # 分类结果
    #     # print("算出来的和是", sum(predictor._vec[0]))
    #     # print("打标的结果是：", tag)
    #     emotion_1 = tag + emotion_1
    # print("goworld:", emotion_1)
    #
    # sunwoda_news = sp.sunwoda_news()
    # emotion_1 = 0
    # for i in sunwoda_news:
    #     # print(i['news'])
    #     news = i['news']
    #     predictor.set_news(news=news)
    #     predictor.trans_vec()
    #
    #     tag = predictor()  # 分类结果
    #     # print("算出来的和是", sum(predictor._vec[0]))
    #     # print("打标的结果是：", tag)
    #     emotion_1 = tag + emotion_1
    # print("sunword:", emotion_1)
    #
    # dsbj_news = sp.dsbj_news()
    # emotion_1 = 0
    # for i in dsbj_news:
    #     news = i['news']
    #     predictor.set_news(news=news)
    #     predictor.trans_vec()
    #     tag = predictor()  # 分类结果
    #     emotion_1 = tag + emotion_1
    # print("dsbj:", emotion_1)
    #
    # hnlens_news = sp.hnlens_news()
    # emotion_1 = 0
    # for i in hnlens_news:
    #     news = i['news']
    #     predictor.set_news(news=news)
    #     predictor.trans_vec()
    #     tag = predictor()  # 分类结果
    #     emotion_1 = tag + emotion_1
    # print("hnlens:", emotion_1)
    #
    # luxshare_news = sp.luxshare_news()
    # emotion_1 = 0
    # for i in luxshare_news:
    #     news = i['news']
    #     predictor.set_news(news=news)
    #     predictor.trans_vec()
    #     tag = predictor()  # 分类结果
    #     emotion_1 = tag + emotion_1
    # print("luxshare:", emotion_1)
    #
    # goertek_news = sp.goertek_news()
    # emotion_1 = 0
    # for i in goertek_news:
    #     news = i['news']
    #     predictor.set_news(news=news)
    #     predictor.trans_vec()
    #     tag = predictor()  # 分类结果
    #     emotion_1 = tag + emotion_1
    # print("goertek:", emotion_1)
    #
    # ofilm_news = sp.ofilm_news()
    # emotion_1 = 0
    # for i in ofilm_news:
    #     news = i['news']
    #     predictor.set_news(news=news)
    #     predictor.trans_vec()
    #     tag = predictor()  # 分类结果
    #     emotion_1 = tag + emotion_1
    # print("ofilm:", emotion_1)
    #
    # desay_news = sp.desay_news()
    # emotion_1 = 0
    # for i in desay_news:
    #     news = i['news']
    #     predictor.set_news(news=news)
    #     predictor.trans_vec()
    #     tag = predictor()  # 分类结果
    #     emotion_1 = tag + emotion_1
    # print("desay:", emotion_1)
    # predictor.set_news(news=news)
    # predictor.trans_vec()
    #
    # tag = predictor()  # 分类结果
    # print("算出来的和是", sum(predictor._vec[0]))
    # print("打标的结果是：", tag)

    pass


