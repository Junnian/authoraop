# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class GetauthorPipeline(object):
    def open_spider(self,spider):
        host = '127.0.0.1'
        port = 27017
        dbname = 'authorinfo'  # 设置数据库,也就是这话怕论文的
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbname]
        # self.all = tdb['aerospace']
        # self.all = tdb['bigdata']
        # self.all = tdb['biology']
        # self.all = tdb['infornet']
        self.all = tdb['newM']
        # self.all = tdb['QC']
        # self.all = tdb['shipBuild']
        
        #存第一层合著作者
        # self.allc = tdb['aerospace_c']
        # self.allc = tdb['bigdata_c']
        # self.allc = tdb['biology_c']
        # self.allc = tdb['infornet_c']
        self.allc = tdb['newM_c']
        # self.allc = tdb['QC_c']
        # self.allc = tdb['shipBuild_c']

        #存第二层合著作者
        # self.allc2 = tdb['aerospace_c2']
        # self.allc2 = tdb['bigdata_c2']
        # self.allc2 = tdb['biology_c2']
        # self.allc2 = tdb['infornet_c2']
        self.allc2 = tdb['newM_c2']
        # self.allc2 = tdb['QC_c2']
        # self.allc2 = tdb['shipBuild_c2']

        #存无限扩展的作者
        # self.alla = tdb['aerospace_ca']
        # self.alla = tdb['bigdata_ca']
        # self.alla = tdb['biology_ca']
        # self.alla = tdb['infornet_ca']
        self.alla = tdb['newM_ca']
        # self.alla = tdb['QC_ca']
        # self.alla = tdb['shipBuild_ca']


    def process_item(self, item, spider):
        # items = dict(item)
        #不管重名不重名，主页的url肯定不一样，也一定都有，就以这个为标准插入
        # self.all.update({'ID': item['ID']}, {'$set': dict(item)}, True)
        # self.all.insert(items)
        if spider.name =="scholar":
            self.all.update({'ID': item['ID']}, {'$set': dict(item)}, True)
        if spider.name == "copinfo":
            self.allc.update({'ID': item['ID']}, {'$set': dict(item)}, True)
        if spider.name == "copinfo2":
            self.allc2.update({'ID': item['ID']}, {'$set': dict(item)}, True)
        if spider.name == "othereautho":
            self.allca.update({'ID': item['ID']}, {'$set': dict(item)}, True)

        return item

    ##存数据库的不同爬虫来源存不一样的数据库里


        # def process_item(self, item, spider):
        #     if spider.name == "reference":
        #         t = item['authorInfo']
        #     t1 = len(t) - len(t.replace(',', ''))
        #     t2 = len(item['author_url'])
        #
        #     if t1 == t2:
        #         item['authorInfo'] = item['authorInfo'][1:]  # 把字符串前边的逗号去掉
        #         items = dict(item)
        #         self.all.insert(items)
        #         return item
        #     else:
        #         raise DropItem("Duplicate item found: %s" % item)
        #
        # if spider.name == "geturl":
        #     url = item['refurl'] + '\n'
        #     self.f.write(url)
        #     return item
        #
        # def close_spider(self, spider):
        #     if spider.name == "geturl":
        #         self.f.close()

