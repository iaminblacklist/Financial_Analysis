# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class MongoPipeline(object):
    collection_name = 'stock'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        #self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        # self.db_auth = self.client.admin
        # self.db_auth.authenticate("OAA", "1378215200zad")
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # collection_name = item.__class__.__name__
        #self.db[self.collection_name].insert(dict(item))
        self.db[self.collection_name].update({'title': item['title']}, {'$set': dict(item)}, True)
        #self.db[self.collection_name].update({'url_token': item['url_token']}, dict(item), True)
        return item








# class MongoPipeline(object):
#     def process_item(self, item, spider):
#         return item
