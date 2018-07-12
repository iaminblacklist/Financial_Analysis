from pymongo import MongoClient
import chardet

# sz300207
# sz000823
# sz002384
# sz300433
# sz002475
# sz300136
# sz002241
# sz002456
# sz000049

client = MongoClient('localhost', 27017)
db = client.sina
collection = db.stock

db = client.apple
appl_collection = db.news

date = "2016-01"
sunwoda = collection.find({"$and": [{"symbol": {"$regex": "sz300207"}}, {"datetime": {"$regex": date}}]})
goworld = collection.find({"$and": [{"symbol": {"$regex": "sz000823"}}, {"datetime": {"$regex": date}}]})
dsbj = collection.find({"$and": [{"symbol": {"$regex": "sz002384"}}, {"datetime": {"$regex": date}}]})
hnlens = collection.find({"$and": [{"symbol": {"$regex": "sz300433"}}, {"datetime": {"$regex": date}}]})
luxshare = collection.find({"$and": [{"symbol": {"$regex": "sz002475"}}, {"datetime": {"$regex": date}}]})
sunway = collection.find({"$and": [{"symbol": {"$regex": "sz300136"}}, {"datetime": {"$regex": date}}]})
goertek = collection.find({"$and": [{"symbol": {"$regex": "sz002241"}}, {"datetime": {"$regex": date}}]})
ofilm = collection.find({"$and": [{"symbol": {"$regex": "sz002456"}}, {"datetime": {"$regex": date}}]})
desay = collection.find({"$and": [{"symbol": {"$regex": "sz000049"}}, {"datetime": {"$regex": date}}]})

apple = appl_collection.find({"datetime": {"$regex": date}})


def apple_news():
    return apple


def sunwoda_news():
    return sunwoda


def goworld_news():
    return goworld


def dsbj_news():
    return dsbj


def hnlens_news():
    return hnlens


def luxshare_news():
    return luxshare


def sunway_news():
    return sunway


def goertek_news():
    return goertek


def ofilm_news():
    return ofilm


def desay_news():
    return desay
# news = ''
# x = 0
# for i in cursor:
#     print(i['news'])
#     print(i['datetime'])
#     x = x+1
# print(x)
