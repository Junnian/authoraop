# -*- coding: utf-8 -*-
import scrapy
from getauthor.items import GetauthorItem
from scrapy.http import Request
from scrapy.selector import Selector
import time
from random import random



Url = 'https://scholar.google.com'

class ScholarSpider(scrapy.Spider):
    name = 'othereauthor'
    allowed_domains = ['scholar.google.com']
    start_urls=[]
    #处理start_urls=[]
    # keys = ['aerospace']#之后可以添加
    keys = ['bigdata']
    # keys = ['biology']
    # keys = ['infornet']
    keys = ['newM']
    # keys = ['QC']
    # keys = ['shipB']
    
    for key in keys:
        file_ = 'new/'+key+'.txt'
        with open(file_,'r') as f:
            list_ = f.readlines()
            for i in list_:
                start_urls.append(i)
                if ' ' in i:
                    i=i.replace(' ','_')
                    start_urls.append(i)#也就是说有下划线，没下划线的都要
    scrawl_ID = set(start_urls)  # 记录待爬
    finish_ID = set()  # 记录已爬
    peopleUrl = set() #记录已经爬的人的主页url

    # keys = ['aerospace']#之后可以添加
    # keys = ['bigData']
    # keys = ['biology']
    # keys = ['informationNetworks']
    keys = ['newMaterials']
    # keys = ['QuantumCommunication']
    # keys = ['shipBuilding']
    
    for key in keys:
        file_ = 'key/'+key+'.txt'
        with open(file_,'r') as f:
            list_ = f.readlines()
            for i in list_:
                start_urls.append(i)
                if ' ' in i:
                    i=i.replace(' ','_') 
                    start_urls.append(i)#也就是说有下划线，没下划线的都

    def start_requests(self):
        #不知道为什么scrawl_ID叠加的起不到相关的作用,是不是并行请求的太多了，我现在把并行的设为16，之前是100，这次应该可以了吧
        while self.scrawl_ID.__len__():
            print self.scrawl_ID.__len__()
            field = self.scrawl_ID.pop()
            self.finish_ID.add(field)  # 加入已爬队列
            url = 'https://scholar.google.com/citations?view_op=search_authors&hl=zh-CN&mauthors=label:'+field
            yield Request(url=url, callback=self.parse1)
    def parse1 (self, response):
        #这个解析函数先处理每个领域第一页的人，用selector
        sel = Selector(response)
        authorurl = sel.xpath('//a[contains(@href,"/citations?user")]/@href').extract()
        t1 = response.url
        a = sel.xpath('//*[@id="gsc_authors_bottom_pag"]/div/button[2]/@onclick').extract()
        for url in authorurl:
            aurl = Url + url
            if aurl not in self.peopleUrl:
                self.peopleUrl.add(aurl)
                yield Request(url = aurl,callback = self.parse_info)
        if a!=[]:
            b = a[0].split('\\')
            c = b[-3]
            after_author = c[3:len(c)]
            L = t1.split('&')
            next2 = L[0] + '&' + L[1] + '&' + L[2] + '&after_author=' + after_author + '&astart=' + str(10)
            # print '-----------------1---------------------'
            yield Request(url = next2,callback = self.parse2)

    #主要处理某个领域第二页以后的情况
    def parse2(self, response):
        sel = Selector(response)
        authorurl = sel.xpath('//a[contains(@href,"/citations?user")]/@href').extract()

        # print authorurl
        for url in authorurl:
            aurl = Url + url
            if aurl not in self.peopleUrl:
                self.peopleUrl.add(aurl)
                yield Request(url = aurl,callback = self.parse_info)
        
        #获取下一页的动态
        t1 = response.url
        a = sel.xpath('//*[@id="gsc_authors_bottom_pag"]/div/button[2]/@onclick').extract()
        if a!=[]:
            b = a[0].split('\\')
            c = b[-3]
            after_author = c[3:len(c)]
            L = t1.split('&')
        # n = int(t1[-2:len(t1)])
        # L[-1]-7为当前页码的位数
            w = len(L[-1])-7
            n=L[-1][-w:]
            N = int(n) + 10
            # print N
            next = L[0] + '&' + L[1] + '&' + L[2] + '&after_author=' + after_author + '&astart=' + str(N)
            # print '-----------------3--------------------'
            yield  Request(url=next, callback=self.parse2)

   #处理作者详情页
    def parse_info(self,response):
        sel = Selector(response)
        i = GetauthorItem()
        url = response.url
        c = url.split('user=')
        i['ID'] = c[1].split('&')[0]
        i['authorurl'] = url
        i['Name'] = sel.xpath('//*[@id="gsc_prf_in"]/text()').extract()[0]
        Fields =sel.xpath('//*[contains(@href,"/citations?view_op=search_author")]/text()').extract()
        i['Fields'] = Fields
        Totalref = sel.xpath('//td[@class="gsc_rsb_std"]/text()').extract()
        if Totalref:
            i['Totalref'] = Totalref[0]
        Affi = sel.xpath('//*[@id="gsc_prf_i"]//text()').extract()
        i['Affi'] = Affi[1:len(Affi)-len(Fields)-1]
        coauthorurl = 'https://scholar.google.com/citations?view_op=list_colleagues&hl=zh-CN&user='+i['ID']
                      # https://scholar.google.com/citations?view_op=list_colleagues&hl=zh-CN&json=&user=wtMGHCQAAAAJ
        yield Request(url = coauthorurl,meta={'item':i},callback=self.parse_coauthorurl)

        
    def parse_coauthorurl(self,response):
        i = response.meta['item']
        sel = Selector(response)
        name = sel.xpath('//a[contains(@href,"/citations?user")]//text()').extract()
        Coauthorurl = sel.xpath('//a[contains(@href,"/citations?user")]/@href').extract()
        i['Coauthor'] = name[1:len(name)]
        
        yield i

        # 把合著作者的信息写在一个文件夹里。设置这个爬虫运行完之后，自动开始另一个爬虫
        # for courl in Coauthorurl:
        #     url = Url + courl
        #     with open("./copurlaa.txt", "a") as f:
        #         f.write(url + '\n')
        # 最后把补充领域
        for field in i['Fields']:
            if field not in self.finish_ID:
                if field not in self.scrawl_ID:
                    if ' ' in field:
                        field.replace(' ','_')
                        self.scrawl_ID.add(field)
        
                        print '----------add-----------'
                        print self.scrawl_ID.__len__()
                        # print self.scrawl_ID
                        with open("./field.txt", "a") as f:
                            f.write(field + '\n')