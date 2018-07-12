from pymongo import MongoClient
import chardet


client = MongoClient('localhost', 27017)
db = client.apple
collection = db.news
date = "2017-09"
cursor = collection.find({"datetime": {"$regex": date}})
# news = []


def ret_news():
    return cursor
    # news = ''
    # for i in cursor:
    #     # print(i)
    #     print(i['news'])
    #     return i['news']


if __name__=='__main__':
    for i in cursor:
        # print(i)
        print(i['news'])




